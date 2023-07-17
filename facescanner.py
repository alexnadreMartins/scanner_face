import sys
import os
import shutil
import face_recognition
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QMessageBox, QFileDialog, QMainWindow, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QDragEnterEvent, QDropEvent, QPainter
from PyQt5.QtCore import Qt, QMimeData, QRect






app = QApplication([])
window = QWidget()
window.setMinimumSize(1200, 900)
window.setWindowFlags(Qt.FramelessWindowHint)

layout = QGridLayout(window)
layout.setColumnStretch(0, 1)
layout.setColumnStretch(1, 2)
layout.setColumnStretch(2, 1)

title = QLabel("Search Face")
titleFont = QFont("Arial", 16, QFont.Bold)
title.setFont(titleFont)
layout.addWidget(title, 0, 0, 1, 3, alignment=Qt.AlignHCenter)

container = QWidget()  # Contêiner para os visualizadores
containerLayout = QVBoxLayout(container)
containerLayout.setContentsMargins(0, 0, 0, 0)
containerLayout.setSpacing(0)

leftViewer = QLabel()
rightViewer = QLabel()
leftViewer.setFixedSize(900, 500)
#rightViewer.setFixedSize(300, 500)
leftViewer.setStyleSheet("background-color: black; border: 5px solid black;")
#rightViewer.setStyleSheet("background-color: black; border: 5px solid black;")

visualizersLayout = QHBoxLayout()
visualizersLayout.addWidget(leftViewer)
#visualizersLayout.addWidget(rightViewer)

containerLayout.addLayout(visualizersLayout)

layout.addWidget(container, 1, 1)

progressBar = QProgressBar()
progressBar.setMinimum(0)
#progressBar.setMaximum()  # Altere esse valor de acordo com a quantidade de imagens
progressBar.setValue(0)  # Altere esse valor para o progresso atual

centralLayout = QVBoxLayout()
centralLayout.addWidget(leftViewer, 0, Qt.AlignHCenter)
#centralLayout.addWidget(rightViewer, 0, Qt.AlignRight)
centralLayout.addWidget(progressBar)

centralWidget = QWidget()
centralWidget.setLayout(centralLayout)
layout.addWidget(centralWidget, 1, 0, 1, 5)

# Coluna 3 (inferior) - Path browsers e botão "Iniciar"
sourcePath = QLineEdit()
destinationPath = QLineEdit()
startButton = QPushButton("Iniciar")
buscarSourceButton = QPushButton("Buscar Origem")
buscarDestButton = QPushButton("Buscar Destino")

bottomLayout = QVBoxLayout()
bottomLayout.addWidget(QLabel("Origem:"))
bottomLayout.addWidget(sourcePath)
bottomLayout.addWidget(buscarSourceButton)
bottomLayout.addWidget(QLabel("Destino:"))
bottomLayout.addWidget(destinationPath)
bottomLayout.addWidget(buscarDestButton)
bottomLayout.addWidget(startButton)

bottomWidget = QWidget()
bottomWidget.setLayout(bottomLayout)
layout.addWidget(bottomWidget, 2, 0, 1, 3)

# Botões personalizados para mover, minimizar e fechar a janela
#moveButton = QPushButton("Mover")
minimizeButton = QPushButton("Minimizar")
closeButton = QPushButton("Fechar")

def moveWindow():
    window.move(window.pos() + event.globalPos() - window.dragPos)
    window.dragPos = event.globalPos()
  
def minimizeWindow():
    window.showMinimized()

def closeWindow():
    sys.exit()

#layout.addWidget(moveButton, 0, 0)
#layout.addWidget(minimizeButton, 0, 1)
layout.addWidget(closeButton, 0, 2)

#moveButton.clicked.connect(moveWindow)
#minimizeButton.clicked.connect(minimizeWindow)
closeButton.clicked.connect(closeWindow)

# Função para marcar o rosto de referência na imagem
def marcar_rosto_referencia(imagem):
    # Carrega a imagem
    img = face_recognition.load_image_file(imagem)

    # Detecta os rostos na imagem
    rostos = face_recognition.face_locations(img)

    # Exibe a imagem com os rostos marcados
    fig, ax = plt.subplots()
    ax.imshow(img)

    for (top, right, bottom, left) in rostos:
        # Desenha um retângulo ao redor do rosto
        rect = patches.Rectangle((left, top), right - left, bottom - top, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')
    #plt.show()

# Função para copiar fotos com rosto de referência
def copiar_fotos_com_rosto_referencia(pasta_origem, pasta_destino, imagem_referencia):
    # Verifica se a pasta de destino existe, caso contrário, a cria
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Lista todos os arquivos na pasta de origem
    arquivos = os.listdir(pasta_origem)

    # Carrega a imagem de referência
    imagem_referencia = face_recognition.load_image_file(imagem_referencia)
    rosto_referencia = face_recognition.face_encodings(imagem_referencia)[0]

    # Percorre cada arquivo e verifica se contém rostos similares ao rosto de referência
    for i, arquivo in enumerate(arquivos):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)

        # Carrega a imagem
        imagem = face_recognition.load_image_file(caminho_arquivo)

        # Detecta os rostos na imagem
        rostos = face_recognition.face_encodings(imagem)

        # Compara os rostos encontrados com o rosto de referência
        for rosto in rostos:
            # Compara os rostos usando a distância euclidiana
            distancia = face_recognition.face_distance([rosto_referencia], rosto)

            # Se a distância for menor que um limite, copia a foto para a pasta de destino
            if distancia < 0.6:
                caminho_destino = os.path.join(pasta_destino, arquivo)
                shutil.copy2(caminho_arquivo, caminho_destino)

        # Atualiza o valor da barra de progresso
        progressBar.setValue(i+1)

    # Exibe uma mensagem de conclusão
    QMessageBox.information(window, "Concluído", "Processo concluído.")

# Função para iniciar o processo ao clicar no botão "Iniciar"
def iniciarProcesso():
    pasta_origem = sourcePath.text()
    pasta_destino = destinationPath.text()
    imagem_referencia = leftViewer.property("imagem_referencia")

    try:
        # Marca o rosto de referência na imagem
        marcar_rosto_referencia(imagem_referencia)

        # Copia as fotos com rostos similares ao rosto de referência para a pasta de destino
        copiar_fotos_com_rosto_referencia(pasta_origem, pasta_destino, imagem_referencia)
    except Exception as e:
        # Exibe uma mensagem de erro, caso ocorra uma exceção
        QMessageBox.critical(window, "Erro", str(e))

# Conectar o sinal clicked do botão "Iniciar" à função iniciarProcesso
startButton.clicked.connect(iniciarProcesso)

# Função para lidar com eventos de arrastar e soltar na visualização esquerda
def dragEnterEvent(event: QDragEnterEvent):
    if event.mimeData().hasUrls():
        event.acceptProposedAction()

def dropEvent(event: QDropEvent):
    if event.mimeData().hasUrls():
        urls = event.mimeData().urls()
        image_path = urls[0].toLocalFile()
        pixmap = QPixmap(image_path)
        leftViewer.setPixmap(pixmap.scaled(leftViewer.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        leftViewer.setProperty("imagem_referencia", image_path)

leftViewer.setAcceptDrops(True)
leftViewer.dragEnterEvent = dragEnterEvent
leftViewer.dropEvent = dropEvent

# Função para lidar com o botão "Buscar Imagem"
def buscarImagem():
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(window, "Selecionar Imagem", "", "Imagens (*.jpg *.jpeg *.png)")
    if file_path:
        pixmap = QPixmap(file_path)
        leftViewer.setPixmap(pixmap.scaled(leftViewer.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        leftViewer.setProperty("imagem_referencia", file_path)

# Conectar o sinal clicked do botão "Buscar Imagem" à função buscarImagem
#buscarSourceButton.clicked.connect(buscarImagem)

# Função para lidar com o botão "Buscar Origem"
def buscarOrigem():
    file_dialog = QFileDialog()
    directory = file_dialog.getExistingDirectory(window, "Selecionar Pasta de Origem")
    if directory:
        sourcePath.setText(directory)

# Conectar o sinal clicked do botão "Buscar Origem" à função buscarOrigem
buscarSourceButton.clicked.connect(buscarOrigem)

# Função para lidar com o botão "Buscar Destino"
def buscarDestino():
    file_dialog = QFileDialog()
    directory = file_dialog.getExistingDirectory(window, "Selecionar Pasta de Destino")
    if directory:
        destinationPath.setText(directory)

# Conectar o sinal clicked do botão "Buscar Destino" à função buscarDestino
buscarDestButton.clicked.connect(buscarDestino)

window.show()

sys.exit(app.exec_())
