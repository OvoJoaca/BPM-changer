### Disclamer!!!
This script is specifically made for **linux** users!

It will not work on windows!

I only tested it on Manjaro KDE Plasma. If it doesn't work on your distro submit an issue and mabye I'll fix it. Provide the name of the distro and your window manager name aswell (Ex: i3, X11, etc.)


# BPM-changer

## Description
This is basically a scuffed version of [osutrainer](https://github.com/FunOrange/osu-trainer), but specifically made to run on linux.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ffmpy and pydub.

```bash
$ sudo pip install ffmpy pydub
```

Use your package manager to install ffmpeg.

Examples:
```bash
$ sudo pacman -S ffmpeg

$ sudo apt install ffmpeg
```

## Usage

1. Open *osu!*.

2. Start the script using python3.

```bash
$ python3 bpmchanger.py
```

3. If it's the first time using the script, it will ask you for the path to your osu folder. It should look like this:

   ![example](https://cdn.discordapp.com/attachments/551757053564157952/854807799035854918/unknown.png)

The script will save it in $HOME/.config/bpmchanger/osupath.txt

4. Next, enter the map of which you want to change the bpm of and pause it. The script should recognize it. 
   If it doesn't, the script will give you an error: 
   ![error](https://cdn.discordapp.com/attachments/551757053564157952/854981451559600128/unknown.png)
   If you want to continue you will have to specify the **beatmapset id or path to beatmap folder** yourself:
   ![id](https://cdn.discordapp.com/attachments/551757053564157952/854981068451872778/unknown.png)
   
   **Example:**
   /home/ovo/Desktop/osudir/OSU/Songs/830964 Aika - Sakura Trip/
   or
   830964

5. Go back to the script and specify the changed bpm.

6. Wait a bit until the process finishes, go back to osu and it should detect a new beatmap automatically.

## How it works

1. It gets the name of the map from the title of the osu window using xdotool.

2. It searches for the map path in osu!.db using [osu-db-tools](https://github.com/jaasonw/osu-db-tools).

3. It changes the speed of the audio to the wanted bpm.

4. It starts rewriting the .osu file and calculating the AR and OD.

5. After that, it creates an .osz archive so osu can notice the change.

6. That's it!




