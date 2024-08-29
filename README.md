![CasseteImageMakerIcon](https://github.com/user-attachments/assets/7a44c8f2-7e8e-49fc-9a1e-d93b9b05a7e5)
# Easy Cassette Image Maker For ROBOBEAT
Application for the game [ROBOBEAT](https://store.steampowered.com/app/1456760/ROBOBEAT/) that makes creating custom cassette covers easy. <br> <br> <br>
### ATTENTION
This makes creating the COVER IMAGES for the cassettes easy, it does not make creating the actual mapped part of the cassettes easier.

## Planned Features
* Option to use image from clipboard as opposed to stored files.
* Button to flip image.
* button to use first image for second image and mirror it over to the other side of the cassette.
* Linux support.

## Build Instructions (Windows Only)
A few sources in VirusTotal incorrectly detect that the compiled version of the app found in releases as a trojan. If you don't trust that it's not actually a trojan or you are contributing to the project, you can build the app yourself directly from the source code. There is currently no support for Linux or Mac, but Linux support is planned in the future.

1. Make sure Python 3.12 is installed. (IMPORTANT: Make sure you are NOT using the microsoft store version of Python!):
```console
python3.12 -version
```
If the command returns an error because the command python3.12 is not recognized, you will need to install [Python](https://www.python.org/downloads/windows/)

2. Install the [Nuitka](https://pypi.org/project/Nuitka) library:
```console
python -m pip install nuitka
```

3. Install [Git](https://gitforwindows.org/) if you dont have it already and run this command:
```console
git clone https://github.com/roboltz/EasyCassetteImages.git
```
This will download the source code into your user directory which you can now find at C:\Users\(name)\EasyCassetteImages.
Now focus the working directory to the source code folder with this command:
```console
cd EasyCassetteImages
```

4. Install other required libraries:
```console
python -m pip install -r requirements.txt
```

5. Use Nuitka to compile source code:
```console
python -m nuitka --standalone --enable-plugin=tk-inter --windows-console-mode=attach --mingw64 --windows-icon-from-ico=CassetteImageMakerIcon.ico main.py
```

6. Open C:\Users\(name)\EasyCassetteImages and copy all image files, including the .ico file into main.dist. main.dist is the finished compiled folder that can run the app.

