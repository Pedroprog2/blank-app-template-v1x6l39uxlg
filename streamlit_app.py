import streamlit as st
import cv2
print(cv2.__version__)
import numpy as np
from PIL import Image

# Título do aplicativo
st.title('Upload de Imagens com OpenCV')

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
    
    # Converte de volta para o formato de imagem do PIL para exibição
    gray_image_pil = Image.fromarray(gray_image)
    
    # Exibe a imagem original e a imagem processada no aplicativo
    st.image(image, caption='Imagem carregada.', use_column_width=True)
    st.image(gray_image_pil, caption='Imagem em escala de cinza.', use_column_width=True)
    st.write("")
    st.write("Carregado e processado com sucesso!")
