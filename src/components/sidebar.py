import streamlit as st
from .description_card import description_card

def render_sidebar():
    """
    Renderiza a barra lateral com as seções de informação
    e aplica o CSS para ajustar sua largura.
    """
   

    # Conteúdo da sidebar
    with st.sidebar:
        st.header("ℹ️ Sobre o Sistema")
        description_card()   
        st.info("Esta ferramenta está em desenvolvimento. Em caso de dúvidas, contate a secretaria secgrad@ic.ufrj.br.")
