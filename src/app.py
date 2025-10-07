import pandas as pd
import streamlit as st
from PIL import Image 
import os

# Funções de backend
from boa_scraper import extract_approved_courses, analyze_course_completion

# Componentes da interface
from components.sidebar import render_sidebar
from components.header import render_header
from components.file_upload import file_upload


def main():
    # --- Configuração de caminhos ---
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FAVICON_PATH = os.path.join(PROJECT_ROOT, "assets", "icon.png")
    LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "logo_ic.png")
    
    # --- Configuração da Página ---  
    st.set_page_config(
        page_title="Validador de Estágios",
        page_icon=FAVICON_PATH,
        layout="centered"
    )

    # --- Sidebar ---
    render_sidebar()

    # --- Cabeçalho com Logo ---
    render_header(LOGO_PATH)

    # --- Componentes da Interface ---
    uploaded_file = file_upload()

    # --- Lógica e Exibição dos Resultados ---
    if st.button("Analisar Equivalências", type="primary", use_container_width=True):
        if uploaded_file is not None:            
            with st.spinner('Analisando documento... Por favor, aguarde.'):
                # TODO: Passar o parametro certo (essa funcao nao aceita o arquivo diretamente, aceita o caminho)
                report = analyze_course_completion(uploaded_file)
                approved_courses = report['materias_aprovadas']
                # st.session_state['academic_data'] = academic_data

                st.write("### Resultado da Análise")
                st.write(approved_courses)
                
        else:
            st.error("Erro: Por favor, faça o upload de um arquivo PDF válido antes de processar.")
    
    # TODO: Comparar o academic_data com a tabela de empresas

    # TODO: Exibir as materias que podem ser cortadas

if __name__ == "__main__":
    main()
