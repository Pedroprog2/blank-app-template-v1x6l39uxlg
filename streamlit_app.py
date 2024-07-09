import streamlit as st
from PIL import Image
import cv2

# Título do aplicativo
st.title('Upload de Imagens')

# Botão para upload de imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

# Verifica se o arquivo foi enviado
if uploaded_file is not None:
    # Abre a imagem
    image = cv2.imread(uploaded_file)
    
    # Exibe a imagem no aplicativo
    st.image(image, caption='Imagem carregada.', use_column_width=True)
    st.write("")
    st.write("Carregado com sucesso!")
