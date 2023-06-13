# Funciones/Procedimientos relacionados con el archivo de configuración
import configparser
import paths
import os

# Configuración predeterminada
# ydl-default-vp9 y ydl-default-h264 son los formatos de video que yt-dlp busca (303 es vp9_1080p60, 299 es h264_1080p60, etc...)
# Conseguidos ingresando en la terminal: "yt-dlp -F <url de un video>"
if not os.path.isfile(paths.configFile):
    defaultConfig = configparser.ConfigParser()
    defaultConfig['Config'] = { 'ydl-default-vp9': '303+bestaudio/299+bestaudio/bestvideo[height<=?1080][vcodec=vp9][fps<=?60]+bestaudio/best',
                                'ydl-default-h264': '299+bestaudio/298+bestaudio/bestvideo[height<=?1080][vcodec!=?vp9][fps<=?60]+bestaudio/22+bestaudio/best',
                                'ydl-format': 'bestvideo+bestaudio',
                                'hwaccel': '1',
                                'enable-format-edition': '0',
                                'prefer-vp9': '0',
                                'max-results': '100',
                                'del-thumb-cache': '0',
                                'enable-thumbs': '1'}
    defaultConfig.write(open(paths.configFile, 'w'))

# Función que devuelve el valor de un parámetro del archivo de configuración
def getConfig(configName, returnType=None):
    configHandler = configparser.ConfigParser()
    configHandler.read(paths.configFile)
    if returnType == "bool":
        return bool(int(configHandler['Config'][configName]))
    elif returnType == "int":
        return int(configHandler['Config'][configName])
    else:
        return configHandler['Config'][configName]

# Guardar un valor en uno de los parámetros del archivo de configuración
def setConfig(configName, value):
    configHandler = configparser.ConfigParser()
    configHandler.read(paths.configFile)
    configHandler['Config'][configName] = str(value)
    configHandler.write(open(paths.configFile, 'w'))

#mpvInput = configparser.ConfigParser()
#mpvInput.read(paths.mpvInputFile)