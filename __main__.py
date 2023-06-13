#!/usr/bin/env python
# Archivo principal del programa
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

isLinux = (sys.platform == "linux")
if isLinux:
    import mpv # Windows tiene problemas con la libreria de mpv...

import os
 
import scraper
import scraper_config as config
import widget_classes as widgetClasses
import styles
import paths

# Clase para la ventana principal
class mainActivityWindow(QtWidgets.QMainWindow):
    """Función inicial"""
    def __init__(self):
        super().__init__()
        self.resize(1500, 800)
        self.setWindowTitle("PyQT youtube scraper")
        self.setWindowIcon(QtGui.QIcon(os.path.join(paths.resFolder, "logo0.png")))

        # Widget principal de la ventana
        self.mainWidget = widgetClasses.gridLayoutWidget("mainWidget")
        self.mainWidget.setStyleSheet(styles.mainWidget)

        # Widgets de los elementos del stack
        self.mainMenu = widgetClasses.gridLayoutWidget()
        self.videoList = widgetClasses.vLayoutWidget()
        self.videoPlayer = widgetClasses.vLayoutWidget()
        self.loadingScreen = widgetClasses.gridLayoutWidget()
        self.configMenu = widgetClasses.gridLayoutWidget()

        # Inicializar menú principal
        self.setupMainMenuUI()

        # Añadir elementos al stack
        self.Stack = QtWidgets.QStackedWidget()
        self.Stack.addWidget(self.mainMenu)         # stack 0
        self.Stack.addWidget(self.videoList)        # stack 1
        self.Stack.addWidget(self.videoPlayer)      # stack 2
        self.Stack.addWidget(self.loadingScreen)    # stack 3
        self.Stack.addWidget(self.configMenu)       # stack 4

        # Añadir stack al widget principal y mostrar ventana
        self.mainWidget.layout.addWidget(self.Stack)
        self.setCentralWidget(self.mainWidget)
        self.show()

    """Funciones compartidas"""
    def changeStack(self, index): # Cambiar de stack...
        self.Stack.setCurrentIndex(index)

    """Funciones de setup"""
    def setupMainMenuUI(self):
        def startLoadingBar(self, action, query=""):
            if ((action == "subs") or (action == "search" and query != "")):
                # Crear objeto de barra de carga y cambiar stack
                self.queryPrompt.setText("")
                loadingObjects = widgetClasses.setupLoadingObjects()
                self.loadingScreen.layout.addWidget(loadingObjects,0,0,1,0,QtCore.Qt.AlignCenter)
                win.changeStack(3)

                # Adquirir datos del scraper
                loadingObjects.loadingLabel.setText("Adquiriendo información de los videos...")
                if action == "subs":
                    videoData = scraper.getSubsData()
                else:
                    videoData = scraper.getSearchData(query)
                
                loadingObjects.loadingBar.setValue(100)

                # Descargar miniaturas (si están activadas)
                if config.getConfig("enable-thumbs", "bool"):  
                    jsonLen = len(videoData)
                    configLen = config.getConfig("max-results", "int")

                    # Limitar las miniaturas descargadas a lo que configuró el usuario
                    if jsonLen <= configLen:
                        vidCant = jsonLen
                    else:
                        vidCant = configLen
                    
                    # Barra de progreso
                    barMax = 100 // vidCant
                    progress = 0
                    loadingObjects.loadingBar.setValue(0)
                    loadingObjects.loadingLabel.setText("Descargando miniaturas...")

                    # Descargar una por una las miniaturas...
                    for i in range(vidCant):
                        loadingObjects.loadingLabelCurrent.setText(videoData[i]['title'])
                        scraper.downloadThumbnail(videoData[i]['videoID'])
                        progress += barMax
                        loadingObjects.loadingBar.setValue(progress)

                    if progress < vidCant: # Llenar la barra de carga si no se terminó de llenar
                        loadingObjects.loadingBar.setValue(100)
                else:
                    loadingObjects.loadingBar.setValue(100)

                # Cargar lista de videos
                self.setupVideoListUI(videoData)
                self.changeStack(1)

        def showConfig(self):
            # Mostrar stack de confiración
            self.setupConfigUI()
            self.changeStack(4)

        # Spacers
        verticalSpacer1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        verticalSpacer2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)

        # Widget para centrar el menú
        self.mainMenuContainer = widgetClasses.vLayoutWidget()
        self.mainMenu.layout.addWidget(self.mainMenuContainer,0,0,1,0,QtCore.Qt.AlignCenter)

        # Título del menú
        titleLabel = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        titleLabel.setFont(font)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setText("PyQT youtube scraper")
        titleLabel.setMaximumSize(10000, 100)
        self.mainMenuContainer.layout.addWidget(titleLabel)

        # Spacer
        self.mainMenuContainer.layout.addItem(verticalSpacer1)

        # Label del botón de subs
        subsTitleLabel = QtWidgets.QLabel()
        subsTitleLabel.setText("Suscripciones")
        subsTitleLabel.setMaximumSize(10000, 100)
        subsTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainMenuContainer.layout.addWidget(subsTitleLabel)

        # Botón de subs
        subsButton = QtWidgets.QPushButton()
        subsButton.setText("Cargar suscripciones")
        subsButton.setMinimumSize(100, 40)
        font = QtGui.QFont()
        font.setBold(True)
        subsButton.setFont(font)
        if not paths.hasCookies:
            subsButton.setEnabled(False)
            subsButton.setText("No se encontro el archivo cookies.txt")
        subsButton.clicked.connect(lambda: startLoadingBar(self, "subs"))
        subsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        subsButton.setStyleSheet(styles.genericPushButton)
        self.mainMenuContainer.layout.addWidget(subsButton)

        # Spacer
        self.mainMenuContainer.layout.addItem(verticalSpacer2)

        # Label del query
        queryLabel = QtWidgets.QLabel()
        queryLabel.setText("Buscar videos")
        queryLabel.setMaximumSize(10000, 100)
        queryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainMenuContainer.layout.addWidget(queryLabel)

        # Contenedor del input y botón del query
        queryContainer = widgetClasses.hLayoutWidget("queryContainer")
        queryContainer.setStyleSheet(styles.queryContainer)
        self.mainMenuContainer.layout.addWidget(queryContainer)

        # Input del query
        self.queryPrompt = QtWidgets.QLineEdit()
        self.queryPrompt.returnPressed.connect(lambda: startLoadingBar(self, "search", self.queryPrompt.text()))
        self.queryPrompt.setPlaceholderText("Ingresa tu busqueda...")
        self.queryPrompt.setMaximumSize(325, 38)
        self.queryPrompt.setStyleSheet(styles.genericLineEdit)
        queryContainer.layout.addWidget(self.queryPrompt)

        # Botón del query
        sendQueryButton = QtWidgets.QPushButton()
        sendQueryButton.setText(">")
        sendQueryButton.setMinimumSize(30,30)
        font = QtGui.QFont()
        font.setBold(True)
        sendQueryButton.setFont(font)
        sendQueryButton.clicked.connect(lambda: startLoadingBar(self, "search", self.queryPrompt.text()))
        sendQueryButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sendQueryButton.setStyleSheet(styles.genericPushButton)
        queryContainer.layout.addWidget(sendQueryButton)

        # Spacer
        self.mainMenuContainer.layout.addItem(verticalSpacer2)
        
        # Contenedor de botones
        miscButtonsContainer = widgetClasses.hLayoutWidget()
        self.mainMenuContainer.layout.addWidget(miscButtonsContainer)

        # Botón de config
        configButton = QtWidgets.QPushButton()
        configButton.setText("Configuración")
        configButton.setMinimumSize(100, 40)
        font = QtGui.QFont()
        font.setBold(True)
        configButton.setFont(font)
        configButton.clicked.connect(lambda: showConfig(self))
        configButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        configButton.setStyleSheet(styles.genericPushButton)
        miscButtonsContainer.layout.addWidget(configButton)
        
        # Botón de salida
        exitButton = QtWidgets.QPushButton()
        exitButton.setText("Salir")
        exitButton.setMinimumSize(100, 40)
        font = QtGui.QFont()
        font.setBold(True)
        exitButton.setFont(font)
        exitButton.clicked.connect(lambda: QtCore.QCoreApplication.quit())
        exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        exitButton.setStyleSheet(styles.genericPushButton)
        miscButtonsContainer.layout.addWidget(exitButton)

    def setupVideoListUI(self, videosJSON):
        def createVideo(index, videoInfo):
            def loadVideo(self):
                # Cargar el video...
                win.setupVideoPlayerUI(videoInfo)
                win.changeStack(2)
            
            # Widget para cada video
            vidContainer = widgetClasses.hLayoutWidget("vidContainer")
            vidContainer.setStyleSheet(styles.vidListContanier)
            vidContainer.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            vidContainer.mousePressEvent = loadVideo
            
            # Miniatura del video
            vidThumb = QtWidgets.QLabel(vidContainer)
            
            # Verificar si el usuario activó las miniaturas...
            if config.getConfig("enable-thumbs", "bool"):
                thumbPath = os.path.join(paths.thumbFolder, videoInfo['videoID'])
                if os.path.isfile(thumbPath+'.jpg'):
                    pixmap = QtGui.QPixmap(thumbPath+'.jpg')
                else:
                    pixmap = QtGui.QPixmap(thumbPath+'_bad.jpg')
            else:
                pixmap = QtGui.QPixmap(os.path.join(paths.resFolder, "defaultThumb.png"))
            
            vidThumb.setPixmap(pixmap.scaledToHeight(270))
            vidThumb.setAlignment(QtCore.Qt.AlignCenter)
            vidThumb.setMaximumSize(480, 270) # Asumir aspect ratio de 16:9 para las miniaturas
            vidThumb.setStyleSheet(styles.vidListThumbnail)
            vidContainer.layout.addWidget(vidThumb)

            # Widget de info del video
            vidInfoWidget = widgetClasses.vLayoutWidget()
            vidInfoWidget.setMaximumSize(700, 400)
            vidContainer.layout.addWidget(vidInfoWidget)

            # Título del video
            vidTitle = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setPointSize(15)
            font.setBold(True)
            font.setWeight(60)
            vidTitle.setFont(font)
            vidTitle.setAlignment(QtCore.Qt.AlignLeft)
            vidTitle.setText(videoInfo['title'])
            vidTitle.setWordWrap(True)
            vidTitle.setMaximumSize(1000, 100)
            vidInfoWidget.layout.addWidget(vidTitle)

            # Información del video
            vidInfo = QtWidgets.QLabel(vidContainer)
            infoString = 'Canal: '+videoInfo['channel']+'\n'
            infoString += 'Duración: '+str(videoInfo['duration'])+'\n'
            infoString += 'Vistas: '+str(videoInfo['views'])+'\n'
            infoString += 'Fecha de subida: '+str(videoInfo['date'])
            vidInfo.setText(infoString)
            vidInfoWidget.layout.addWidget(vidInfo)

            # Añadir widget del video al scroll
            videoListScroll.layout.addWidget(vidContainer)

        def onBackClick(self):
            # Al volver limpiar todo
            win.videoList.clearLayout()
            win.loadingScreen.clearLayout()
            win.changeStack(0)

        # Botón de volver
        backToMenu = QtWidgets.QPushButton()
        backToMenu.clicked.connect(onBackClick)
        backToMenu.setText("< Volver")
        backToMenu.setMinimumSize(100, 30)
        font = QtGui.QFont()
        font.setBold(True)
        backToMenu.setFont(font)
        backToMenu.setStyleSheet(styles.genericPushButton)
        backToMenu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.videoList.layout.addWidget(backToMenu, alignment=QtCore.Qt.AlignLeft)

        # Area con scrolling
        dummyVideoList = widgetClasses.gridLayoutWidget("dummyVideoList")
        dummyVideoList.setStyleSheet(styles.vidListScrollingArea)

        videoListScroll = widgetClasses.vLayoutWidget()
        dummyVideoList.layout.addWidget(videoListScroll,0,0,1,0,QtCore.Qt.AlignCenter)

        scrollAnchor = QtWidgets.QScrollArea()
        scrollAnchor.setObjectName("listScrollAnchor")
        scrollAnchor.setWidgetResizable(True)
        scrollAnchor.setWidget(dummyVideoList)
        scrollAnchor.setStyleSheet(styles.vidListScrollingAnchor)
        self.videoList.layout.addWidget(scrollAnchor)

        # Crear e insertar los widgets de video
        jsonLen = len(videosJSON)
        configLen = config.getConfig("max-results", "int") # Verificar la cantidad maxima de videos
        if jsonLen <= configLen:
            vidLen = jsonLen
        else:
            vidLen = configLen

        for i in range(vidLen):
            createVideo(i, videosJSON[i])

    def setupVideoPlayerUI(self, videoInfo):
        def onThumbnailClick(self):
            # Widget al que se bindea el reproductor
            playerContainer = QtWidgets.QWidget()
            playerContainer.setMinimumSize(1280, 720)

            # Locales para MPV
            import locale
            locale.setlocale(locale.LC_NUMERIC, 'C')

            # Cargar configuraciones del usuario
            if config.getConfig("hwaccel", "bool"):
                hwaccel = "auto"
            else:
                hwaccel = "no"

            if config.getConfig("enable-format-edition", "bool"):
                ydl_options = config.getConfig("ydl-format")
            elif config.getConfig("prefer-vp9", "bool"):
                ydl_options = config.getConfig("ydl-default-vp9")
            else:
                ydl_options = config.getConfig("ydl-default-h264")

            if isLinux:
                # Crear objeto del reproductor
                win.player = mpv.MPV(player_operation_mode='pseudo-gui',
                                osd_font_size=20,
                                input_default_bindings=True,
                                input_vo_keyboard=True,
                                #input_conf=str(paths.mpvInputFile),
                                osc=True,
                                wid=str(int(playerContainer.winId())), # Bindear reproductor a un widget
                                #log_handler=print,
                                #loglevel='debug',
                                ytdl=True,
                                ytdl_format=str(ydl_options),
                                hwdec=str(hwaccel))
                win.player.play('https://youtu.be/'+videoInfo['videoID'])

                """
                win.player.wait_until_playing()
                for i in config.mpvInput['mpv-keybindings']:
                    print(i)
                    print(config.mpvInput['mpv-keybindings'][i])
                    win.player.keybind(str(i), str(config.mpvInput['mpv-keybindings'][i]))
                """

                win.player.keybind("WHEEL_UP", "")
                win.player.keybind("WHEEL_DOWN", "")

                # Eliminar miniatura grande y reemplazarla por el reproductor
                #win.player.wait_until_playing()
                playerDummyArea.layout.removeWidget(playerBigThumb)
                playerBigThumb.close()
                playerDummyArea.layout.addWidget(playerContainer)
            else:
                # Como windows tiene problemas cuando se trabaja con libmpv, un workaround es usar un ejecutable de mpv
                command = paths.mpvExe+" --hwdec="+str(hwaccel)+" --ytdl-format=\""+str(ydl_options)+"\" --osd-font-size=20 --script-opts=ytdl_hook-ytdl_path=\""+str(paths.winYtDl)+"\" \"https://youtu.be/"+str(videoInfo['videoID'])+"\""
                print(command)
                os.system(command)
                
        def onBackClick(self):
            # Eliminar el reproductor sin crashear el programa antes de volver
            try:
                win.player.terminate()
            except:
                print(" ¯\_(ツ)_/¯")
            win.videoPlayer.clearLayout()
            win.changeStack(1)

        # Boton de volver
        backButton = QtWidgets.QPushButton()
        backButton.clicked.connect(onBackClick)
        backButton.setText("< Volver")
        backButton.setMinimumSize(100, 30)
        font = QtGui.QFont()
        font.setBold(True)
        backButton.setFont(font)
        backButton.setStyleSheet(styles.genericPushButton)
        backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.videoPlayer.layout.addWidget(backButton, alignment=QtCore.Qt.AlignLeft)

        # Zona de scrolling del reproductor
        playerScrollArea = widgetClasses.vLayoutWidget("playerScrollArea")
        playerScrollArea.setStyleSheet(styles.playerScrollingArea)

        scrollAnchor = QtWidgets.QScrollArea()
        scrollAnchor.setObjectName("playerScrollAnchor")
        scrollAnchor.setWidgetResizable(True)
        scrollAnchor.setWidget(playerScrollArea)
        scrollAnchor.setStyleSheet(styles.playerScrollingAnchor)
        self.videoPlayer.layout.addWidget(scrollAnchor)

        # Contenedor para el Video/Miniatura
        playerDummyArea = widgetClasses.gridLayoutWidget("playerDummyArea")
        playerScrollArea.layout.addWidget(playerDummyArea)
        playerDummyArea.setStyleSheet(styles.playerDummyArea)

        # Miniatura grande para mostrar antes del reproductor
        playerBigThumb = QtWidgets.QLabel("playerBigThumb")
        playerBigThumb.mousePressEvent = onThumbnailClick
        playerBigThumb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Verificar si el usuario activó las miniaturas
        if config.getConfig("enable-thumbs", "bool"):  
            thumbPath = os.path.join(paths.thumbFolder, videoInfo['videoID'])
            if os.path.isfile(thumbPath+'.jpg'):
                playerBigThumb.setPixmap(QtGui.QPixmap(thumbPath+'.jpg'))
                playerBigThumb.setMinimumSize(1200, 675)
            else:
                pixmap = QtGui.QPixmap(thumbPath+'_bad.jpg')
                playerBigThumb.setPixmap(pixmap.scaledToHeight(720))
                playerBigThumb.setMinimumSize(960, 720)
        else:
            playerBigThumb.setPixmap(QtGui.QPixmap(os.path.join(paths.resFolder, "defaultThumb.png")))
            playerBigThumb.setMinimumSize(1200, 675)

        playerDummyArea.layout.addWidget(playerBigThumb,0,0,1,0,QtCore.Qt.AlignCenter)

        # Contenedor de info. del video
        infoWidget = widgetClasses.vLayoutWidget("infoWidget")
        playerScrollArea.layout.addWidget(infoWidget)
        infoWidget.setStyleSheet(styles.playerInfoWidget)

        # Titulo del video
        videoTitleLabel = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        videoTitleLabel.setFont(font)
        videoTitleLabel.setAlignment(QtCore.Qt.AlignLeft)
        videoTitleLabel.setText(videoInfo['title'])
        videoTitleLabel.setMaximumSize(10000, 50)
        infoWidget.layout.addWidget(videoTitleLabel)

        # Información del video
        vidInfo = QtWidgets.QLabel()
        vidInfo.setMinimumSize(700, 100)
        infoString = 'Canal: '+videoInfo['channel']+'\n'
        infoString += 'Duración: '+str(videoInfo['duration'])+'\n'
        infoString += 'Vistas: '+str(videoInfo['views'])+'\n'
        infoString += 'Fecha de subida: '+str(videoInfo['date'])
        vidInfo.setText(infoString)
        infoWidget.layout.addWidget(vidInfo)

    def setupConfigUI(self):
            def onBackClick(writeConfig):
                # Escribir configuraciones (o no) al salir
                if writeConfig:
                    config.setConfig("hwaccel", int(checkboxHW.isChecked()))
                    config.setConfig("ydl-format", formatSelector.toPlainText())
                    config.setConfig("enable-format-edition", int(checkboxFormats.isChecked()))
                    config.setConfig("prefer-vp9", int(checkboxVP9.isChecked()))
                    config.setConfig("max-results", int(vidCantSlider.value()))
                    config.setConfig("del-thumb-cache", int(cacheCheckbox.isChecked()))
                    config.setConfig("enable-thumbs", int(thumbCheckbox.isChecked()))
                win.changeStack(0)
                win.configMenu.clearLayout()

            def onFormatClick(isEnabled):
                # Click checkbox de modificación de formatos
                checkboxVP9.setEnabled(not isEnabled)
                formatSelector.setEnabled(isEnabled)
                if isEnabled:
                    checkboxVP9.setChecked(False)
            
            def onSliderChange(value):
                # Cambio del slider
                vidCantLabel.setText(str(value))

            def onCacheClearClick():
                # Botón de limpieza de miniaturas
                scraper.delThumbnails()
                cacheButton.setText("Miniaturas Limpiadas!")
                cacheButton.setEnabled(False)

            def onThumbCheck(isEnabled):
                # Click checkbox de activar miniaturas
                cacheCheckbox.setEnabled(isEnabled)
                cacheButton.setEnabled(isEnabled)

            # Contendor para centrar el menú
            configContainer = widgetClasses.vLayoutWidget()
            self.configMenu.layout.addWidget(configContainer,0,0,1,0,QtCore.Qt.AlignCenter)

            # Titulo del menú
            configTitleLabel = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setPointSize(25)
            font.setBold(True)
            font.setWeight(75)
            configTitleLabel.setFont(font)
            configTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
            configTitleLabel.setText("Configuración")
            configTitleLabel.setMaximumSize(10000, 100)
            configContainer.layout.addWidget(configTitleLabel)

            # Config. de MPV
            mpvConfContainer = widgetClasses.vLayoutWidget()
            configContainer.layout.addWidget(mpvConfContainer)

            # Label
            vidSetLabel = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setUnderline(True)
            vidSetLabel.setFont(font)
            vidSetLabel.setText("Configuración de MPV")
            mpvConfContainer.layout.addWidget(vidSetLabel)

            # HW. Accel. checkbox
            checkboxHW = QtWidgets.QCheckBox()
            checkboxHW.setChecked(config.getConfig("hwaccel", "bool"))
            checkboxHW.setText("Activar aceleración de video por hardware")
            checkboxHW.setStyleSheet(styles.genericCheckBox)
            mpvConfContainer.layout.addWidget(checkboxHW)

            # VP9 checkbox
            checkboxVP9 = QtWidgets.QCheckBox()
            checkboxVP9.setChecked(config.getConfig("prefer-vp9", "bool"))
            checkboxVP9.setEnabled(not config.getConfig("enable-format-edition", "bool"))
            checkboxVP9.setText("Preferir codec VP9")
            checkboxVP9.setStyleSheet(styles.genericCheckBox)
            mpvConfContainer.layout.addWidget(checkboxVP9)

            # Format checkbox
            checkboxFormats = QtWidgets.QCheckBox()
            checkboxFormats.setChecked(config.getConfig("enable-format-edition", "bool"))
            checkboxFormats.setText("Modificar manualmente los formatos de video")
            checkboxFormats.setStyleSheet(styles.genericCheckBox)
            checkboxFormats.clicked.connect(lambda: onFormatClick(checkboxFormats.isChecked()))
            mpvConfContainer.layout.addWidget(checkboxFormats)

            # Label de formatos
            formatLabel = QtWidgets.QLabel()
            formatLabel.setText("Formatos que mpv buscará en youtube:")
            font = QtGui.QFont()
            font.setItalic(True)
            formatLabel.setFont(font)
            mpvConfContainer.layout.addWidget(formatLabel)
            formatSelector = QtWidgets.QTextEdit()
            formatSelector.setStyleSheet(styles.genericTextEdit)
            formatSelector.setText(config.getConfig("ydl-format"))
            formatSelector.setEnabled(config.getConfig("enable-format-edition", "bool"))
            mpvConfContainer.layout.addWidget(formatSelector)

            # Spacer
            configContainer.layout.addItem(QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum))

            # Conf. Misc.
            miscConfContainer = widgetClasses.vLayoutWidget()
            configContainer.layout.addWidget(miscConfContainer)

            # Label conf. misc.
            miscLabel = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setUnderline(True)
            miscLabel.setFont(font)
            miscLabel.setText("Configuración miscelánea")
            miscConfContainer.layout.addWidget(miscLabel)

            # Slider + label de valores
            sliderLabel = QtWidgets.QLabel()
            sliderLabel.setText("Cantidad maxima de videos mostrados")
            font = QtGui.QFont()
            font.setItalic(True)
            sliderLabel.setFont(font)
            miscConfContainer.layout.addWidget(sliderLabel)
            sliderWidget = widgetClasses.hLayoutWidget()
            miscConfContainer.layout.addWidget(sliderWidget)
            vidCantSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            vidCantSlider.setMinimum(10)
            vidCantSlider.setMaximum(100)
            vidCantSlider.setTickInterval(10)
            vidCantSlider.setSingleStep(10)
            vidCantSlider.setValue(config.getConfig("max-results", "int"))
            vidCantSlider.valueChanged.connect(lambda: onSliderChange(vidCantSlider.value()))
            sliderWidget.layout.addWidget(vidCantSlider)
            vidCantLabel = QtWidgets.QLabel()
            vidCantLabel.setText(str(vidCantSlider.value()))
            sliderWidget.layout.addWidget(vidCantLabel)

            # Thumb. checkbox
            thumbCheckbox = QtWidgets.QCheckBox()
            thumbCheckbox.setText("Activar miniaturas")
            thumbCheckbox.setStyleSheet(styles.genericCheckBox)
            thumbCheckbox.setChecked(config.getConfig("enable-thumbs", "bool"))
            thumbCheckbox.clicked.connect(lambda: onThumbCheck(thumbCheckbox.isChecked()))
            miscConfContainer.layout.addWidget(thumbCheckbox)
            
            # Cache checkbox
            cacheCheckbox = QtWidgets.QCheckBox()
            cacheCheckbox.setChecked(config.getConfig("del-thumb-cache", "bool"))
            cacheCheckbox.setText("Limpiar miniaturas al iniciar el programa")
            cacheCheckbox.setStyleSheet(styles.genericCheckBox)
            cacheCheckbox.setEnabled(config.getConfig("enable-thumbs", "bool"))
            miscConfContainer.layout.addWidget(cacheCheckbox)
            cacheButton = QtWidgets.QPushButton()
            cacheButton.setText("Limpiar miniaturas ahora")
            cacheButton.setStyleSheet(styles.genericPushButton)
            cacheButton.setEnabled(config.getConfig("enable-thumbs", "bool"))
            cacheButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            cacheButton.clicked.connect(lambda: onCacheClearClick())
            miscConfContainer.layout.addWidget(cacheButton)

            # Aceptar/Cancelar
            buttonContainer = widgetClasses.hLayoutWidget()
            configContainer.layout.addWidget(buttonContainer)
            acceptButton = QtWidgets.QPushButton()
            acceptButton.setText("Aceptar")
            acceptButton.setStyleSheet(styles.genericPushButton)
            acceptButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            acceptButton.clicked.connect(lambda: onBackClick(True))
            buttonContainer.layout.addWidget(acceptButton)
            cancelButton = QtWidgets.QPushButton()
            cancelButton.setText("Cancelar")
            cancelButton.setStyleSheet(styles.genericPushButton)
            cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            cancelButton.clicked.connect(lambda: onBackClick(False))
            buttonContainer.layout.addWidget(cancelButton)

def main():
    # Inicializar QT, crear ventana, ejecutar, etc...
    app = QtWidgets.QApplication(sys.argv)
    global win # El objeto de ventana es global para evitar problemas algunas funciones
    win = mainActivityWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
