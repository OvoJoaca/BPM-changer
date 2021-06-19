import math
import ffmpy
from pydub import AudioSegment
import os
from shutil import move
from zipfile import ZipFile
from time import sleep
import subprocess

def get_bpm(text : str): #for refference, in game you will see: "BPM: lowestBPM-highestBPM(*it gets this*)" (I hope) 
    beatLength=0                                                                            #^
    l=-1                                                                                    #|
    x=1                                                                                     #|
    lineDifference=0                                                                        #|
    l1=0                                                                                    #|
    for line in text.splitlines():                                                          #|
        l=l+1                                                                               #|
        i=1                                                                                 #|
        if line == "[TimingPoints]":                                                        #|
            while True:                                                                     #|
                try:                                                                        #|
                    splitlinesText=float(text.splitlines()[l+i].split(",")[1])              #|
                except:                                                                     #|
                    break                                                                   #|
                if(splitlinesText>0 and x%2==1):                                            #|
                    l1=l+i                                                                  #|
                    x=x+1                                                                   #|
                elif(splitlinesText>0 and x%2==0):                                          #|
                    l2=l+i                                                                  #|
                    if l2-l1>lineDifference:                                                #|
                        lineDifference=l2-l1                                                #|
                        linePog=l1 #this is the line where this is located--------------------
                    l1=l2
                elif(text.splitlines()[l+i]=="[Colours]"):
                    break
                i=i+1
            break
        
    #print(lineDifference)
    #print(linePog)
    
    l=-1
    for line in text.splitlines():
        l=l+1
        if l==linePog:
            beatLength=float(line.split(',')[1])
    
    #convert beatLength to BPM
    curbpm=round(60000/beatLength)
    print(f'BPM: {curbpm}')
    return curbpm


def get_beatmap(sid):
    while True:
        output = subprocess.Popen([f"xdotool getwindowname {sid}"], shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[0:-1]
        try:
            beatmap = output.split('  - ')[1]
            #print(beatmap)
            break
        except:
            pass
        sleep(0.1)
    return beatmap #example: Kano - Stella-rium (Asterisk MAKINA Remix) [Starlight]


def osupathDOTtxt(): #check for osupath.txt
    HOME=os.getenv("HOME")
    try:
        f = open(f"{HOME}/.config/bpmchanger/osupath.txt", 'r')
        osupath=f.read()
        f.close()
    except:
        os.mkdir(f"{HOME}/.config/bpmchanger/")
        osupath=input("Path to osu! folder (you won't be asked for it again): ")
        print('')
        f = open(f"{HOME}/.config/bpmchanger/osupath.txt", 'w')
        f.write(osupath)
        f.close()
        print(f"osupath.txt written at {HOME}/.config/bpmchanger/osupath.txt")
    return osupath

#this is taken from here https://github.com/FunOrange/osu-trainer/blob/master/osu-trainer/DifficultyCalculator.cs and translated into python
def ApproachRateToMs(approachRate):
    if(approachRate <= 5):
        return 1800 - approachRate * 120
    else:
        remainder = approachRate - 5
        return 1200 - remainder * 150
def MsToApproachRate(ms):
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

osupath=osupathDOTtxt()

try: #automatically get the beatmap
    pid = subprocess.Popen(["pidof 'osu!.exe'"], shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[0:-1] #osu pid
    #print(pid)
    search = subprocess.Popen(["xdotool", "search", "--pid", f"{pid}"], stdout=subprocess.PIPE).stdout.read().decode('utf-8')[0:-1] #osu window id list
    #print(search)
    for ok in search.split('\n'): #osu window id
        if subprocess.Popen([f"xdotool getwindowname {ok}"], shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[0:-1].split('  - ')[0] == 'osu!':
            sid=ok
            break
    #print(sid)
    print("Checking for beatmap")
    beatmap = get_beatmap(sid) #start checking for beatmap
    beatmapdiff = f"[{beatmap.split(' [', )[-1]}"
    beatmapname = beatmap.split(beatmapdiff)[0][0:-1]
    print(f"Beatmap found: {beatmap}")

    for btmp in os.listdir(f"{osupath}/Songs/"): #check for beatmaps and see if they match
        #print(btmp)
        if btmp.split(' [')[-1]=="no video]":
            btmpnovid = btmp.split(' [')[0]
        else:
            btmpnovid = btmp
        #print(btmp.split(' ', 1)[1])
        if btmpnovid.split(' ', 1)[1] == beatmapname:
            for diff in os.listdir(f"{osupath}/Songs/{btmp}"): #this is a mess
                #print(diff)
                if(diff[(len(diff)-5):]=="].osu"):
                    if(diff.split(' [')[-1][:-4]==beatmapdiff[1:]):
                        #print("pass")
                        file=f"{osupath}/Songs/{btmp}/{diff}"
                        break
except KeyboardInterrupt:
    print("\nScript closed (KeyboardInterrupt)")
    exit()
except: #if it doesn't work, ask the user for the id or path to beatmap
    z=input("\nHmm... Something went wrong with beatmap detection. Do you want to specify the beatmapset id or path to beatmap folder instead?(Y/n):")
    if(z=='' or z=='y' or z=='Y' or z=='yes' or z=='Yes' or z=='YES'): #lmao
        path=input("Beatmap id or path to beatmap folder: ")
        try:
            id=int(path)
            osupath=osupathDOTtxt()
            for btmp in os.listdir(f"{osupath}/Songs/"):
                #print(btmp)
                if(btmp.split(" ")[0]==str(id)):
                    print(f"Selected beatmapset: {btmp}")
                    print("Diffs:")
                    diffs=[]
                    i=1
                    for diff in os.listdir(f"{osupath}/Songs/{btmp}/"):
                        if(diff[(len(diff)-5):]=="].osu"):
                            print(f"{i}. [{diff.split('[')[-1][0:-5]}]")
                            diffs.append(f"{osupath}/Songs/{btmp}/{diff}")
                            i=i+1
                    diff=int(input("Select difficulty: "))
                    file=diffs[diff-1]
                    #print(path)
        except ValueError:
            osupath=osupathDOTtxt()
            print(f"Selected beatmapset: {os.path.split(path)[1]}")
            print("Diffs:")
            diffs=[]
            i=1
            for diff in os.listdir(path):
                if(diff[(len(diff)-5):]=="].osu"):
                    print(f"{i}. [{diff.split('[')[-1][0:-5]}]")
                    diffs.append(f"{path}/{diff}")
                    i=i+1
            diff=int(input("Select difficulty: "))
            file=diffs[diff-1]
            #print(path)
    else:
        exit()


print(file)


prefix=os.path.split(file)[0]
suffix=os.path.split(file)[1]


#open the .osu file and save it's contents into a varible
f=open(file, 'r')
text=str(f.read())
f.close()

#:(((
if(text.splitlines()[0]=="osu file format v14"):
    pass
else:
    print(f"(unfortunately) the script can only edit osu file format v14(this map file is: {text.splitlines()[0]})")
    print("I've done my best job at fixing the issue, but if it doesn't work open an issue at https://github.com/OvoJoaca/BPM-changer/issues")
    x = input("Do you wish to continue?(Y,n):")
    if(x=='n' or x=='N'):
        exit()
    else:
        pass


curbpm=get_bpm(text)
nextbpm=input('NextBPM: ')
try:
    nextbpm=float(nextbpm)
except:
    print("nextbpm has to be a number")
    exit()

multiplier=nextbpm/curbpm
formatted_multiplier="{:.3f}".format(round(multiplier, 3)) #only show 3 decimals of the multiplier for good looks


#to do: When AR or OD > 10 play with DT
""" 
for line in text.splitlines():
    if(line.split(":")[0]=="ApproachRate"): #AR
        oldAR=float(line.split(":")[1])
        newAR=CalculateMultipliedAR(oldAR, multiplier)
        if(newAR>10):
            
            newAR=10
    elif(line.split(":")[0]=="OverallDifficulty"): #OD
        oldOD=float(line.split(":")[1])
        newOD=CalculateMultipliedOD(oldOD, multiplier)
        if(newOD>10):
            newOD=10
"""


#get the path to the audio file
for line in text.splitlines():
    if(line.split(': ')[0]=="AudioFilename"):
        OGaudio=f"{prefix}/{line.split(': ')[1]}"
        break
print(OGaudio)

#convert to wav
audio=f"{OGaudio[0:-4]} {formatted_multiplier}x ({nextbpm}bpm).wav"
NEWaudio=AudioSegment.from_file(OGaudio).export(audio, format='wav')

#get the length of the original audio file
OGlength=len(AudioSegment.from_wav(audio))

#speed up/down the audio file
audioTemp=f"{prefix}/temp.wav"
ff = ffmpy.FFmpeg(inputs={audio: None}, outputs={audioTemp: ["-filter:a", f"atempo={multiplier}"]})
ff.run()

move(audioTemp, audio)

#convert back to mp3
NEWaudio=AudioSegment.from_wav(audio)
NEWaudio.export(f"{audio[0:-4]}.mp3", format='mp3')
NEWlength=len(NEWaudio) #get the length of the new audio file
audio=f"{audio[0:-4]}.mp3"



#start rewriting .osu file
temp=f"{osupath}/temp.osu"
f = open(temp, 'w')
f.write('')
f.close()

f = open(temp, 'a')

y=0
i=0
l=-1
for line in text.splitlines():
    l=l+1
    if(i>1): #skip loop for however many times it went through the while True statements
        i=i-1
        continue
    elif(line.split(' ')[0]=="osu"):
        fformat = int(line.split('v')[-1])
        f.write("osu file format v14")
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
        f.write(f'Version:{line.split(":")[1]} {formatted_multiplier}x ({nextbpm}bpm)\r\n')
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
            #print(f"ln={ln}")
            if(ln[0:-(len(ln)-2)]=="//"):
                break
            f.write(f'{ln.split(",")[0]},{int(int(ln.split(",")[1])*NEWlength/OGlength)},{int(int(ln.split(",")[2])*NEWlength/OGlength)}\r\n')
            i=i+1
        continue
    elif(line=="[TimingPoints]"): #timing points
        y=1
        f.write("[TimingPoints]\r\n")
        i=1
        while True:
            ln=text.splitlines()[l+i]
            #print(f"{ln}")
            if(ln[0:-(len(ln)-1)]=="[" or ln==""):
                break
            idk=ln.split(",")[1]
            #bpm
            if(float(ln.split(",")[1])>0):
                timingBpm=60000/float(ln.split(",")[1])*multiplier #beat length -> bpm then mutiplies it
                newBeatLength=60000/timingBpm #bpm -> new beat length
                idk=newBeatLength 
            #timing
            f.write(f'{int(int(round(float(ln.split(",")[0])))*NEWlength/OGlength)},{idk},{ln.split(",")[2]},{ln.split(",")[3]},{ln.split(",")[4]},{ln.split(",")[5]},{ln.split(",")[6]},{ln.split(",")[7]}\r\n')
            i=i+1         # MY GOD ^
    elif(line=="[HitObjects]"): #hit objects
        y=1
        f.write("[HitObjects]\r\n")
        i=1
        while True:
            try:
                ln=text.splitlines()[l+i]
            except:
                break
            #print(f"{ln}")
            if(ln[0:-(len(ln)-1)]=="[" or ln==""):
                break
            if(ln.split(',')[3]=="12"): #spinners
                if(fformat<10):
                    f.write(f'{ln.split(",")[0]},{ln.split(",")[1]},{int(int(ln.split(",")[2])*NEWlength/OGlength)},{ln.split(",")[3]},{ln.split(",")[4]},{int(int(ln.split(",")[5])*NEWlength/OGlength)},0:0:0:0:')
                else:
                    f.write(f'{ln.split(",")[0]},{ln.split(",")[1]},{int(int(ln.split(",")[2])*NEWlength/OGlength)},{ln.split(",")[3]},{ln.split(",")[4]},{int(int(ln.split(",")[5])*NEWlength/OGlength)},')
                    j=6
                    while True:
                        f.write(f"{ln.split(',')[j]}")
                        if(ln.split(",")[j]==ln.split(",")[-1]): #check if it's the last thing so it won't add a comma at the end of the line
                            f.write('\r\n')
                            break
                        else:
                            f.write(',')
                        j=j+1
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

move(temp, f"{prefix}/{suffix[0:-5]} {formatted_multiplier}x ({nextbpm}bpm)].osu")

#print(f"p: {prefix}")
#print(f"s: {suffix}")
#print(f"o: {osupath}")
osz = ZipFile(f"{osupath}/Songs/{prefix.split('/')[-1]}.osz", 'w')
for file in os.listdir(f"{prefix}"):
    osz.write(f"{prefix}/{file}")
osz.close()

