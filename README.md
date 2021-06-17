### Disclamer!!!
This script is specifically made for **linux** users!

It will not work on windows!

I only tested it on Manjaro KDE Plasma. If it doesn't work on your distro submit an issue and mabye I'll fix it. Provide the name of the distro and your window manager name aswell (Ex: i3, X11, etc.)


# BPM-changer

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ffmpy and pydub.

```bash
$ sudo pip install ffmpy pydub
```

Use your package manager to install ffpeg.

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

