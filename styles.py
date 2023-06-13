# CSS que se utiliza en los widgets
"""Estilos genéricos"""
genericPushButton = """
    QPushButton {
        background: rgb(35, 35, 35);
        color: white;
        border: 3px solid rgb(40, 40, 40);
        border-radius: 3px;
    }
    QPushButton:disabled {
        color: grey
    }
"""

genericTextEdit = """
    QTextEdit {
        background-color: rgb(35, 35, 35);
        border: 2px solid rgb(40, 40, 40);
        color: white;
    }
    QTextEdit:disabled {
        color: grey
    }
"""

genericLineEdit = """
    QLineEdit {
        background-color: rgb(35, 35, 35);
        border: 2px solid rgb(40, 40, 40);
        color: white;
    }
    QLineEdit:disabled {
        color: grey
    }
"""

genericCheckBox = """
    QCheckBox {
        border: none;
        color: white;
    }
    QCheckBox:disabled {
        color: grey
    }
"""

"""Estilos de widgets específicos"""
mainWidget = """
    QFrame#mainWidget {
        background-color: rgb(25, 25, 25);
        border-width: 0.5;
        border-radius: 1;
        border-style: solid;
        border-color: rgb(64, 64, 64)
    }
    QLabel {
        color: white;
    }
"""

queryContainer = """
    QFrame#queryContainer{
        border: 1px solid rgb(40, 40, 40);
        border-radius: 10px;
    }
"""

vidListContanier = """
    QFrame#vidContainer {
        border-width: 2;
        border-radius: 10;
        border-style: solid;
        border-color: rgb(128, 128, 128);
    }
    QFrame#vidContainer::hover {
        background: rgb(40, 40, 40);
    }
"""

vidListThumbnail = """
    QFrame {
        border-width: 2;
        border-radius: 1;
        border-style: solid;
        border-color: rgb(128, 128, 128)
    }
"""

vidListScrollingArea = """
    QFrame#dummyVideoList{
        background-color: rgb(15, 15, 15);
    }
"""

vidListScrollingAnchor = """
    QFrame#listScrollAnchor {
        border: 1px solid rgb(40, 40, 40);
    }
"""

playerScrollingArea = """
    QFrame#playerScrollArea{
        background-color: rgb(15, 15, 15);
    }
"""

playerScrollingAnchor = """
    QFrame#playerScrollAnchor {
        border: 1px solid rgb(40, 40, 40);
    }
"""

playerDummyArea = """
    QFrame#playerDummyArea {
        border-width: 2;
        background-color: black;
        border-radius: 10;
        border-style: solid;
        border-color: rgb(40, 40, 40)
    }
"""

playerInfoWidget = """
    QFrame#infoWidget {
        border-width: 2;
        border-radius: 10;
        border-style: solid;
        border-color: rgb(40, 40, 40)
    }                            
"""

loadingBarStyle = """
    QProgressBar {
        color: black;
        border: 2px solid rgb(40, 40, 40);
        border-radius: 7px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #063970;
        width: 10px;
    }
"""