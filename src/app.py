import pandas as pd
import streamlit as st
from PIL import Image 
import os

# Funções de backend
<<<<<<< HEAD
from boa_scraper import extract_approved_courses, analyze_course_completion
=======
from BOA_scraper import extract_student_data_from_boa
>>>>>>> e5c2d26352af53b105d852a45db579c7b86ec58a

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
<<<<<<< HEAD
                # TODO: Passar o parametro certo (essa funcao nao aceita o arquivo diretamente, aceita o caminho)
                report = analyze_course_completion(uploaded_file)
                approved_courses = report['materias_aprovadas']
                # st.session_state['academic_data'] = academic_data

                st.write("### Resultado da Análise")
                st.write(approved_courses)
                
=======
                # TODO: Passar o parametro certo (essa funcao nao aceita o arquivo diretamente)
                student_data = extract_student_data_from_boa(uploaded_file)
                st.session_state['student_data'] = student_data
>>>>>>> e5c2d26352af53b105d852a45db579c7b86ec58a
        else:
            st.error("Erro: Por favor, faça o upload de um arquivo PDF válido antes de processar.")
    
    # TODO: Comparar o academic_data com a tabela de empresas

    # TODO: Exibir as materias que podem ser cortadas

# --- 3. Exibição dos Resultados (após a análise) ---
    # Verifica se os dados do aluno já foram processados e estão na sessão.
    if 'student_data' in st.session_state:
        data = st.session_state['student_data']
        
        # Verifica se houve algum erro durante a extração
        if "error" in data:
            st.error(f"Ocorreu um erro ao processar o PDF: {data['error']}")
        else:
            student_name = data.get("student_name", "Nome não encontrado")
            approved_courses = data.get("approved_courses", [])
            
            st.success("Análise concluída com sucesso!")
            
            # Exibe o nome do aluno de forma destacada
            st.subheader(f"Análise para: {student_name}")

            # Usa um expander para não poluir a tela com a lista de matérias
            with st.expander(f"Clique para ver as {len(approved_courses)} matérias aprovadas"):
                # Divide em colunas para melhor visualização
                num_columns = 3
                columns = st.columns(num_columns)
                for i, course in enumerate(approved_courses):
                    with columns[i % num_columns]:
                        st.markdown(f"- `{course}`")

    # TODO: Comparar o student_data com a tabela de empresas
    # TODO: Exibir as materias que podem ser cortadas

if __name__ == "__main__":
    main()  