import os
import shutil
import face_recognition
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    plt.show()


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

        # Imprime o progresso no terminal
        print(f"Processando arquivo {i+1}/{len(arquivos)}")

    print("Processo concluído.")

# Exemplo de uso:
pasta_origem = '/run/media/ale/DADOSBT/GIT/rosto/fotos/'
pasta_destino = '/run/media/ale/DADOSBT/GIT/rosto/teste/'
imagem_referencia = '/run/media/ale/DADOSBT/GIT/rosto/referencia/DSCF4461.jpg'

# Marca o rosto de referência na imagem
marcar_rosto_referencia(imagem_referencia)

# Copia as fotos com rostos similares ao rosto de referência para a pasta de destino
copiar_fotos_com_rosto_referencia(pasta_origem, pasta_destino, imagem_referencia)
