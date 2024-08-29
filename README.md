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
A few sources in VirusTotal detect the compiled version of the app found in releases as a trojan. If you don't trust that it's not actually a trojan or you are contributing to the project, you can build directly from the source code. There is currently no support for Linux or Mac, but Linux support is planned in the future.

1. Make sure Python 3.12 is installed:
```console
python3.12 -version
```
If the command returns an error because the command python3.12 is not recognized, you will need to install python 3.12 with this command in Powershell:
```console
winget install --id=Python.Python.3.12  -e
```

2. Install the [PyInstaller](https://pypi.org/project/pyinstaller/) library:
```console
python3 -m pip install pyinstaller
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

4. Use PyInstaller to package the source code into a useable .exe. This step is most likely why some antiviruses in VirusTotal detect this application as a virus. Windows Defender will most likely show up when running saying it's a potentially unwanted app. This does not mean it's a virus, Windows is just saying that there is a possibility of it being dangerous. Do your research on PyInstaller and different commands used in this process if you are skeptical.
![image](https://github.com/user-attachments/assets/f1b5ba98-1a8f-4c80-b6bd-7253b91b97d7)
```console
python3 -m PyInstaller main.py --onefile --noconsole
```

5. Open C:\Users\(name)\EasyCassetteImages and move all image files including the .ico into the dist folder. rename main.exe to whatever you want and you should be able to run it as long as the image files are in the same folder as the .exe.

