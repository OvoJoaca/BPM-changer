import math
import ffmpy
from pydub import AudioSegment
import os
from shutil import move
#file=input(".osu file: ")
#file=r"/home/ovo/.local/share/osu-wine/OSU/Songs/575330 Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo/Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo. (PoNo) [Reverberation].osu"
#file=r"/home/ovo/.local/share/osu-wine/OSU/Songs/1081431 Imperial Circus Dead Decadence - Songs Compilation/Imperial Circus Dead Decadence - Songs Compilation (Val) [Gyakusatsu].osu"
file=r"/home/ovo/.local/share/osu-wine/OSU/Songs/382400 DragonForce - Through the Fire and Flames/DragonForce - Through the Fire and Flames (Ponoyoshi) [Myth].osu"
#file=input("path to .osu file: ")
prefix=os.path.split(file)[0]
suffix=os.path.split(file)[1]
print(prefix)


#this is liteally taken from here https://github.com/FunOrange/osu-trainer/blob/master/osu-trainer/DifficultyCalculator.cs and translated into python
#I have no idea how it works but I hope this works
def ApproachRateToMs(approachRate):
    if(approachRate <= 5):
        return 1800 - approachRate * 120
    else:
        remainder = approachRate - 5
        return 1200 - remainder * 150
def MsToApproachRate(ms): #this makes no sense
    smallestDiff = 100000 #initial value
    AR=0
    while(AR<=110):
        newDiff = abs(ApproachRateToMs(AR/10) - ms)
        if(newDiff<smallestDiff):
            smallestDiff=newDiff
        else:
            return (AR - 1) / 10
        AR=AR+1
def CalculateMultipliedAR(AR, multiplier):
    newbpmMS=ApproachRateToMs(AR) / multiplier
    newbpmAR=MsToApproachRate(newbpmMS)
    return newbpmAR
#same here
def OverallDifficultyToMs(OD):
    return -6 * OD + 79.5
def MsToOverallDifficulty(ms):
    return (79.5 - ms) / 6
def CalculateMultipliedOD(OD, multiplier):
    newbpmMS = OverallDifficultyToMs(OD) / multiplier
    newbpmOD = MsToOverallDifficulty(newbpmMS)
    newbpmOD = round(newbpmOD*10)/10
    return newbpmOD




#get the bpm
f=open(file, 'r')
text=str(f.read())
#print(text.splitlines()[3])
f.close()

l=-1
for line in text.splitlines():
    l=l+1
    try:
        if(line=="[TimingPoints]"):
            curbeat=float(text.splitlines()[l+1].split(',')[1])
            print(curbeat)
            break
    except:
        print("can't find timing points")
    
curbpm=math.ceil(60000/curbeat)
print(f'bpm={curbpm}')

nextbpm=input('nextbpm=')
try:
    nextbpm=float(nextbpm)
except:
    print("nextbpm has to be a number")
    exit()


multiplier=nextbpm/curbpm
formatted_multiplier="{:.3f}".format(round(nextbpm/curbpm, 3))



#░█████╗░██╗░░░██╗██████╗░██╗░█████╗░
#██╔══██╗██║░░░██║██╔══██╗██║██╔══██╗
#███████║██║░░░██║██║░░██║██║██║░░██║
#██╔══██║██║░░░██║██║░░██║██║██║░░██║
#██║░░██║╚██████╔╝██████╔╝██║╚█████╔╝
#╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═╝░╚════╝░
#this text is dumb

#get the name of the audio file
for line in text.splitlines():
    if(line.split(': ')[0]=="AudioFilename"):
        OGaudio=r"{}/{}".format(prefix,line.split(': ')[1])
        break
print(OGaudio)

#convert to wav
NEWaudio=AudioSegment.from_mp3(OGaudio)
NEWaudio.export(r"{}/audio(x{}, {}BPM).wav".format(prefix, formatted_multiplier, nextbpm), format='wav')
audio=r"{}/audio(x{}, {}BPM).wav".format(prefix, formatted_multiplier, nextbpm)
NEWaudio=AudioSegment.from_wav(audio)

#get the length of the original audio file
OGlength=len(NEWaudio)

#speed up/down the audio file
ff = ffmpy.FFmpeg(inputs={f"{audio}": None}, outputs={r"{}/temp.wav".format(prefix): ["-filter:a", f"atempo={multiplier}"]})
ff.run()

move(r"{}/temp.wav".format(prefix), audio)

#convert back to mp3
NEWaudio=AudioSegment.from_wav(audio)
NEWaudio.export(f"{audio[0:-4]}.mp3", format='mp3')

#get the length of the new audio file
NEWaudio=AudioSegment.from_mp3(f"{audio[0:-4]}.mp3")
NEWlength=len(NEWaudio)

#print(f'NEWlenght {NEWlength}')
#print(f'OGlenght {OGlength}')

#x=input(' ')



#░░░░█████╗░░██████╗██╗░░░██╗    ███████╗██╗██╗░░░░░███████╗
#░░░██╔══██╗██╔════╝██║░░░██║    ██╔════╝██║██║░░░░░██╔════╝
#░░░██║░░██║╚█████╗░██║░░░██║    █████╗░░██║██║░░░░░█████╗░░
#░░░██║░░██║░╚═══██╗██║░░░██║    ██╔══╝░░██║██║░░░░░██╔══╝░░
#██╗╚█████╔╝██████╔╝╚██████╔╝    ██║░░░░░██║███████╗███████╗
#╚═╝░╚════╝░╚═════╝░░╚═════╝░    ╚═╝░░░░░╚═╝╚══════╝╚══════╝
#CBT
#██████╗░███████╗░██╗░░░░░░░██╗██████╗░██╗████████╗███████╗
#██╔══██╗██╔════╝░██║░░██╗░░██║██╔══██╗██║╚══██╔══╝██╔════╝
#██████╔╝█████╗░░░╚██╗████╗██╔╝██████╔╝██║░░░██║░░░█████╗░░
#██╔══██╗██╔══╝░░░░████╔═████║░██╔══██╗██║░░░██║░░░██╔══╝░░
#██║░░██║███████╗░░╚██╔╝░╚██╔╝░██║░░██║██║░░░██║░░░███████╗
#╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚══════╝

f = open(f'{prefix}/temp.osu', 'w')
f.write('')
f.close()

f = open(f'{prefix}/temp.osu', 'a')

y=0
i=0
l=-1
for line in text.splitlines():
    l=l+1
    if(i>1): #skip however many lines it went through the while True statements
        i=i-1
        continue
    elif(line.split(": ")[0]=="AudioFilename"): #mou ii kai dt moment
        f.write(f'AudioFilename: {os.path.split(audio)[1]}\r\n')
        continue
        #break
    elif(line.split(': ')[0]=="PreviewTime"): #idk what's this
        f.write(f'PreviewTime: {int(int(line.split(": ")[1])*NEWlength/OGlength)}\r\n')
        continue
    elif(line.split(': ')[0]=="Bookmarks"): #bookmarks
        f.write('Bookmarks: ')
        bookmarks=line.split(': ')[1]
        for time in bookmarks.split(','):
            NEWtime=int(int(time)*NEWlength/OGlength)
            f.write(f"{NEWtime}")
            if(time==bookmarks.split(',')[-1]):
                pass
            else:
                f.write(',')
        f.write('\r\n')
        continue
    elif(line.split(':')[0]=="Version"): #difficulty name
        diff=line.split(":")[1]
        f.write(f'Version:{line.split(":")[1]} x{formatted_multiplier} ({nextbpm}bpm)\r\n')
        continue
    elif(line.split(":")[0]=="ApproachRate"): #AR
        oldAR=float(line.split(":")[1])
        newAR=CalculateMultipliedAR(oldAR, multiplier)
        if(newAR>10):
            newAR=10
        f.write(f"ApproachRate:{newAR}\r\n")
        continue
    elif(line.split(":")[0]=="OverallDifficulty"): #OD
        oldOD=float(line.split(":")[1])
        newOD=CalculateMultipliedOD(oldOD, multiplier)
        if(newOD>10):
            newOD=10
        f.write(f"OverallDifficulty:{newOD}\r\n")
        continue
    elif(line=="//Break Periods"): #break periods
        f.write('//Break Periods\r\n')
        i=1
        while True:
            ln=text.splitlines()[l+i]
            print(f"ln={ln}")
            if(ln[0:-(len(ln)-2)]=="//"):
                break
            f.write(f'{ln.split(",")[0]},{int(int(ln.split(",")[1])*NEWlength/OGlength)},{int(int(ln.split(",")[2])*NEWlength/OGlength)}\r\n')
            i=i+1
        continue
    elif(line=="[TimingPoints]"): #timing points look something like this: time(ms), idk something about the bpm, some more bullshit
        y=1
        f.write("[TimingPoints]\r\n")
        i=1
        while True:
            ln=text.splitlines()[l+i]
            print(f"{ln}")
            if(ln[0:-(len(ln)-1)]=="[" or ln==""):
                break
            idk=ln.split(",")[1]
            #bpm
            if(float(ln.split(",")[1])>0):
                timingbpm=60000/float(ln.split(",")[1])*multiplier #tempo -> bpm then mutiplies it
                newtimingtempo=60000/timingbpm #bpm -> new tempo
                idk=newtimingtempo #idk discovered this by reverse engeneering so it might not be correct
            #timing
            f.write(f'{int(int(ln.split(",")[0])*NEWlength/OGlength)},{idk},{ln.split(",")[2]},{ln.split(",")[3]},{ln.split(",")[4]},{ln.split(",")[5]},{ln.split(",")[6]},{ln.split(",")[7]}\r\n')
            i=i+1
    elif(line=="[HitObjects]"):
        y=1
        f.write("[HitObjects]\r\n")
        i=1
        while True:
            try:
                ln=text.splitlines()[l+i]
            except:
                break
            print(f"{ln}")
            if(ln[0:-(len(ln)-1)]=="[" or ln==""):
                break
            #timing
            if(ln.split(',')[3]=="12"):
                f.write(f'{ln.split(",")[0]},{ln.split(",")[1]},{int(int(ln.split(",")[2])*NEWlength/OGlength)},{ln.split(",")[3]},{ln.split(",")[4]},{int(int(ln.split(",")[5])*NEWlength/OGlength)},')
                j=6
            else:
                f.write(f'{ln.split(",")[0]},{ln.split(",")[1]},{int(int(ln.split(",")[2])*NEWlength/OGlength)},')
                j=3
            while True:
                f.write(f"{ln.split(',')[j]}")
                if(ln.split(",")[j]==ln.split(",")[-1]): #check if it's the last thing so it won't add a comma at the end of the line
                    f.write('\r\n')
                    break
                else:
                    f.write(',')
                j=j+1
            i=i+1
    if(y==1):
        y=0
    else:
        f.write(f'{line}\r\n')


move(f"{prefix}/temp.osu", f"{prefix}/{suffix[0:-5]} x{formatted_multiplier} ({nextbpm}bpm)].osu")

