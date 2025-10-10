import pandas as pd
import streamlit as st
from PIL import Image 
import os

# Funções de backend
from boa_scraper import extract_student_data_from_boa

# Componentes da interface
from components.sidebar import render_sidebar
from components.header import render_header
from components.file_upload import file_upload
from components.select_university import select_university

from equivalence_analyzer import run_equivalence_analysis


def main():
    # --- Configuração de caminhos ---
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FAVICON_PATH = os.path.join(PROJECT_ROOT, "assets", "icon.png")
    LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "logo_ic.png")
    
    # --- Configuração da Página ---  
    st.set_page_config(
        page_title="Equivalência de Disciplinas",
        page_icon=FAVICON_PATH,
        layout="centered"
    )

    # --- Sidebar ---
    # TODO: Modificar os textos da sidebar
    render_sidebar()

    # --- Cabeçalho com Logo ---
    render_header(LOGO_PATH)

    # --- Selecionar uma das Universidades Suportadas ---
    universities = [
        "UFRJ",
        "UFF",
        "UFRGS",
        "UNICARIOCA",
    ]

    university = select_university(universities)

    # TODO: Implementar logica condicional baseada na universidade escolhida
    # TODO: Implementar as classes referentes a cada universidade
    objects = {
        "UFRJ": "objeto_ufrj",
        "UFF": "objeto_uff",
        "UFRGS": "objeto_ufrgs",
        "UNICARIOCA": "objeto_unicarioca",
    }

    # --- Componentes da Interface ---
    uploaded_file = file_upload()

    # --- Lógica e Exibição dos Resultados ---
    if st.button("Analisar Equivalências", type="primary", use_container_width=True):
        if uploaded_file is not None:            
            with st.spinner('Analisando documento... Por favor, aguarde.'):
                student_data = extract_student_data_from_boa(uploaded_file)
                # st.write(student_data)
                st.session_state['student_data'] = student_data
        else:
            st.error("Erro: Por favor, faça o upload de um arquivo PDF válido antes de processar.")

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

            # Dados de teste
            approved_courses = {
                                    'ICP120',
                                    'MAB120',
                                    'MAB624',
                                    'ICP230'
                                }

            st.success("Análise concluída com sucesso!")

            # Exibe o nome do aluno de forma destacada
            st.subheader(f"Aluno: {student_name}")

            # Inserir logica de comparacao aqui
            equivalence_results = run_equivalence_analysis(approved_courses)
            
            if equivalence_results:
                st.markdown(f"##### Disciplinas que podem ser cortadas: {len(equivalence_results)}")
                with st.expander("Clique para ver as disciplinas que podem ser cortadas"):
                    for course in equivalence_results:
                        st.markdown(f"- `{course}`")
            

            # Usa um expander para não poluir a tela com a lista de matérias
            # with st.expander(f"Clique para ver as {len(approved_courses)} matérias aprovadas"):
            #     # Divide em colunas para melhor visualização
            #     num_columns = 3
            #     columns = st.columns(num_columns)
            #     for i, course in enumerate(approved_courses):
            #         with columns[i % num_columns]:
            #             st.markdown(f"- `{course}`")


if __name__ == "__main__":
    main()  