import math
import ffmpy

#file=input(".osu file: ")
file=r"/home/ovo/Desktop/osudir/Songs/575330 Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo/osu.osu"
#file=r"/home/ovo/Desktop/osudir/Songs/302756 Nanahoshi Kangengakudan - Meikaruza/Nanahoshi Kangengakudan - Meikaruza (pkk) [Extra].osu"
f=open(file, 'r')
text=str(f.read())
#print(text)
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
    
curbpm=math.ceil(1/curbeat*60000)
print(f'bpm={curbpm}')

nextbpm=input('nextbpm=')
try:
    nextbpm=float(nextbpm)
except:
    print("nextbpm has to be a number")
    exit()

multiplier=nextbpm/curbpm

#get everything after the timing points and save it in a string
l=-1
for line in text.splitlines():
    l=l+1
    if(line=="[Colours]"):
        aftertiming=line+'\n'
        try:
            while(True):
                aftertiming=aftertiming+text.splitlines()[l+1]+'\n'
                l=l+1
        except:
            break
#print(aftertiming)

#get everything before the timing points and save it in a string
beforetiming=''
for line in text.splitlines():
    if(line=="[TimingPoints]"):
        break
    beforetiming=beforetiming+line+'\n'
#print(beforetiming)

final=open('temp.osu', 'w')
final.write(beforetiming+'\n')
final.close()

final=open('temp.osu', 'a')
timing=''
l=-1
for line in text.splitlines():
    l=l+1
    if(line=="[TimingPoints]"):
        l=l+1
        try:
            while(True):
                line=text.splitlines()[l]
                curbeat=float(line.split(',')[1])
                if(curbeat>=0):
                    beforebeat=line.split(',')[0]+','
                    afterbeat=','+line.split(',')[2]+','+line.split(',')[3]+','+line.split(',')[4]+','+line.split(',')[5]+','+line.split(',')[6]+','+line.split(',')[7]
                    curbeat=math.fabs(curbeat)
                    nextbeat=60000/(curbpm*multiplier)
                    final.write(beforebeat+nextbeat+afterbeat+'\n')
                else:
                    final.write(line+'\n')
                l=l+1
        except:
            break

final.write(aftertiming)