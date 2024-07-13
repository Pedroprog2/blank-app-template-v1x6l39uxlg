import streamlit as st
import cv2
print(cv2.__version__)
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Título do aplicativo
st.title('Análise de Solo')
st.write("Bem-vindo! Prepare suas imagens!")

# Subtítulo para a seção de upload
st.subheader('Andamento da plataforma')
st.markdown('<p style="color:red;">O botão para subir as imagens está pronto.</p>', unsafe_allow_html=True)

st.write("Após subir a imagem, realiza-se a detecção de bordas.")
st.write("Identifica-se a região de interesse (ROI) e realiza o recorte da imagem.")
st.write("Por fim, a imagem recortada é apresentada.")

# Subtítulo para a seção de upload
st.subheader('Próximos passos')
st.write("Realizar a extração dos histogramas dos canais de cores: R, G e B.")

st.write("Salvar o modelo SVM (kernel?) (tunelamento).")
st.write("Podemos salvar o modelo no google cloud e acessá-lo via API, o gpt recomendou uma estratégia")

# Subtítulo para a seção de upload
st.subheader('Upload das imagens')
st.write("Este aplicativo usa OpenCV para processar imagens. Você pode carregar as imagens em formato .png.")

# Botão para upload de imagem
uploaded_files = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Verifica se o arquivo foi enviado
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption=uploaded_file.name)
        
        # Converte a imagem para um array numpy
        img_array = np.array(uploaded_file)
        
        # Converte a imagem para BGR (OpenCV usa BGR em vez de RGB)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Processa a imagem com OpenCV (exemplo: converte para escala de cinza)
        gray_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Aplica blur usando um kernel 3x3
        gray_blurred = cv2.blur(gray_image, (3, 3)) 

        # Aplica a transformada de Hough na imagem borrada
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=30, minRadius=100, maxRadius=1000) 

        # Desenha os círculos detectados
        if detected_circles is not None: 
            # Converte os parâmetros dos círculos (a, b e r) para inteiros
            detected_circles = np.uint16(np.around(detected_circles))
            pt = np.round(detected_circles[0, 0]).astype("int")
            a, b, r = pt[0], pt[1], pt[2]
            imagem_recortada = img_array[a-r:a+ r, b - r:b + r]

            # Obter as dimensões da imagem
            altura, largura, _ = imagem_recortada.shape

            # Calcular as coordenadas do retângulo central
            tamanho_lado_quadrado = min(altura, largura) * 3//5
            centro_x, centro_y = largura // 2, altura // 2
            x1 = centro_x - tamanho_lado_quadrado // 2
            y1 = centro_y - tamanho_lado_quadrado // 2
            x2 = centro_x + tamanho_lado_quadrado // 2
            y2 = centro_y + tamanho_lado_quadrado // 2

            # Recortar a região quadrada central
            roi = imagem_recortada[y1:y2, x1:x2]
            imagem_recortada = roi

            # Calcular o tamanho da imagem
            total_pixels = np.prod(roi.shape[:2])

            # Exibe a imagem original e a imagem processada no aplicativo
            st.image(img_array, caption='Imagem carregada.', use_column_width=True)
            st.image(imagem_recortada, caption='Imagem recortada.', use_column_width=True)
            st.write("Carregado e processado com sucesso!")

            # Exibe o tamanho da imagem
            st.subheader('Informações da imagem')
            st.write("Tamanho da imagem em pixels:", total_pixels)

            # Extrai histogramas
            st.subheader('Extraindo histogramas')

            # Converter a imagem para formato HSV
            imagem_hsv = cv2.cvtColor(imagem_recortada, cv2.COLOR_BGR2HSV)

            # Separar os canais HSV
            hue = imagem_hsv[:, :, 0]
            saturation = imagem_hsv[:, :, 1]
            value = imagem_hsv[:, :, 2]
                
            # Calcular os histogramas
            hist_hue = cv2.calcHist([hue], [0], None, [256], [0, 256]) / total_pixels
            hist_saturation = cv2.calcHist([saturation], [0], None, [256], [0, 256]) / total_pixels
            hist_value = cv2.calcHist([value], [0], None, [256], [0, 256]) / total_pixels

            # Converter a imagem para escala de cinza
            imagem_cinza = cv2.cvtColor(imagem_recortada, cv2.COLOR_BGR2GRAY)
            hist_cinza = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256]) / total_pixels

            # Separar os canais de cores (B, G, R)
            canal_azul = imagem_recortada[:, :, 0]
            canal_verde = imagem_recortada[:, :, 1]
            canal_vermelho = imagem_recortada[:, :, 2]

            # Calcular os histogramas
            hist_azul = cv2.calcHist([canal_azul], [0], None, [256], [0, 256]) / total_pixels
            hist_verde = cv2.calcHist([canal_verde], [0], None, [256], [0, 256]) / total_pixels
            hist_vermelho = cv2.calcHist([canal_vermelho], [0], None, [256], [0, 256]) / total_pixels

            # Concatenar os histogramas em um único vetor
            vetor_concatenado = np.concatenate((hist_azul, hist_verde, hist_vermelho, hist_hue, hist_saturation, hist_value, hist_cinza), axis=None)

            # Criar um gráfico
            plt.figure()
            plt.plot(vetor_concatenado)
            plt.title('Histograma da Imagem')
            plt.xlabel('Bins')
            plt.ylabel('Frequência')
            
            # Exibir o gráfico
            st.pyplot(plt)
            
            st.write("Histograma da Imagem:", vetor_concatenado.T)
            st.write("Tamanho do vetor da imagem:", vetor_concatenado.shape)
