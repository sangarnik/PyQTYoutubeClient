# Directorios que el programa utiliza
import tempfile
import os
import sys

programName = "pyqt_yt_scraper"
tmpDir = os.path.join(tempfile.gettempdir(), programName) # Carpeta temporal
try:
    os.mkdir(tmpDir)
except:
    print(str(tmpDir)+" ya existe")

thumbFolder = os.path.join(tmpDir, "thumbs") # Carpeta de miniaturas
try:
    os.mkdir(thumbFolder)
except:
    print(str(thumbFolder)+" ya existe")

workingDir = os.path.dirname(os.path.realpath(__file__)) # Carpeta del programa
try:
    os.mkdir(workingDir)
except:
    print(str(workingDir)+" ya existe")

resFolder = os.path.join(workingDir, "resources") # Carpeta con los recursos del programa
try:
    os.mkdir(resFolder)
except:
    print(str(resFolder)+" ya existe")

confFolder = os.path.join(workingDir, "config") # Carpeta de configración
try:
    os.mkdir(confFolder)
except:
    print(str(resFolder)+" ya existe")

cookiesFile = os.path.join(confFolder, "cookies.txt") # Archivo de cookies (ver leeme)
hasCookies = os.path.isfile(cookiesFile)
configFile = os.path.join(confFolder, "config.ini") # Archivo de configración
#mpvInputFile = os.path.join(resFolder, "mpvKeybindings.ini") # Keybindings de MPV

if sys.platform != "linux":
    mpvExe = os.path.join(resFolder, "mpv", "mpv.exe")
    if not os.path.isfile(mpvExe):
        print("Ejecutable de mpv no encontrado en: "+str(mpvExe))
        print("Asegurate de haber colocado el ejecutable correctamente")
        exit(1)
    winYtDl = os.path.join(resFolder, "mpv", "yt-dlp.exe")
    if not os.path.isfile(winYtDl):
        print("Ejecutable de youtube-dl/yt-dlp no encontrado en: "+str(winYtDl))
        print("Asegurate de haber colocado el ejecutable correctamente")
        exit(1)