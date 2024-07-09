import streamlit as st
import cv2
print(cv2.__version__)
import numpy as np
from PIL import Image

# Título do aplicativo
st.title('Análise de Solo')
st.write("Bem-vindo! Prepare suas imagens!")

# Subtítulo para a seção de upload
st.subheader('Andamento da plataforma')
st.write("O botão para subir as imagens está pronto. Após subir a imagem, realiza-se a detecção de bordas")
st.write("Identifica-se a região de interesse (ROI),e realiza o recorte da imagem. Por fim, a imagem recortada é apresentada. ")

# Subtítulo para a seção de upload
st.subheader('Upload das imagens')
st.write("Este aplicativo usa OpenCV para processar imagens. Você pode carregar as imagens em formato .png.")

# Botão para upload de imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

# Verifica se o arquivo foi enviado
if uploaded_file is not None:
    # Abre a imagem
    image = Image.open(uploaded_file)
    
    # Converte a imagem para um array numpy
    img_array = np.array(image)
    
    # Converte a imagem para BGR (OpenCV usa BGR em vez de RGB)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Processa a imagem com OpenCV (exemplo: converte para escala de cinza)
    gray_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    #gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray_image, (3, 3)) 
  
# Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                                        param2 = 30, minRadius = 100, maxRadius = 1000) 
  
# Draw circles that are detected. 
    if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles))

    pt = np.round(detected_circles[0, 0]).astype("int")
    a, b, r = pt[0], pt[1], pt[2]
    imagem_recortada = img_array[a-r:a+ r, b - r:b + r]

    # Mostrar a imagem recortada
    #cv2.imshow('Imagem Recortada', imagem_recortada)
    
    # Converte de volta para o formato de imagem do PIL para exibição
    #gray_image_pil = Image.fromarray(gray_image)

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
    imagem_recortada= roi
    #print(roi.shape)

    
    # Exibe a imagem original e a imagem processada no aplicativo
    st.image(image, caption='Imagem carregada.', use_column_width=True)
    st.image(imagem_recortada, caption='Imagem recortada.', use_column_width=True)
    st.write("")
    st.write("Carregado e processado com sucesso!")
