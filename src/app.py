import streamlit as st
import os

# Funções de backend
from data_loader import load_spreadsheet, get_university_list
from core import find_equivalencies

# Componentes da interface
from components.sidebar import render_sidebar
from components.header import render_header
from components.spreadsheet_uploader import render_spreadsheet_uploader
from components.report_card import report_card_compact

# TODO: Futuramente, importar a função de gerar PDF
from pdf_generator import create_pdf_bytes



def main():
    # --- Configuração de caminhos ---
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FAVICON_PATH = os.path.join(PROJECT_ROOT, "assets", "icon.png")
    LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "logo_ic.png")
    
    # --- Configuração da Página ---  
    st.set_page_config(
        page_title="Analisador de Equivalências",
        page_icon=FAVICON_PATH,
        layout="centered"
    )

    # --- Inicialização do Estado da Aplicação ---
    if 'spreadsheet_data' not in st.session_state:
        st.session_state.spreadsheet_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []

    # --- Renderização dos Componentes Visuais Estáticos ---
    render_sidebar()
    # TODO: Modificar os textos da sidebar
    render_header(LOGO_PATH)
    st.title("Analisador de Equivalência de Disciplinas")
    st.markdown("---")

    # --- ETAPA 1: UPLOAD E VALIDAÇÃO DA PLANILHA ---
    uploaded_file = render_spreadsheet_uploader()
    #TODO subheader 1

    if uploaded_file and st.session_state.spreadsheet_data is None:
        st.session_state.spreadsheet_data = load_spreadsheet(uploaded_file)
        st.session_state.analysis_results = []
   
    # --- ETAPA 2 e 3: SELEÇÃO DA UNIVERSIDADE E ENTRADA DOS CÓDIGOS ---

    #TODO botar nome aluno

    if st.session_state.spreadsheet_data:
        st.subheader("2. Selecione a Universidade e Insira os Códigos")
        
        col1, col2 = st.columns([1, 2])
        
        #TODO testar visualização em colunas
        with col1:
            st.markdown("**Universidade de Origem**")
            university_list = get_university_list(st.session_state.spreadsheet_data)
            selected_university = st.selectbox(
                "Universidade de Origem",
                options=university_list,
                label_visibility="collapsed" 
            )

        with col2:
            st.markdown("**Códigos das Disciplinas de Origem**")
            course_codes_input = st.text_area(
                "Códigos das Disciplinas de Origem",
                height=150,
                label_visibility="collapsed"  
            )
            st.caption("Separe os códigos por espaço, vírgula ou quebra de linha.")

    # --- ETAPA 4: BOTÃO DE ANÁLISE ---
        if st.button("Analisar Equivalências", type="primary", use_container_width=True):
            if course_codes_input.strip(): # Verifica se o usuário digitou algo
                with st.spinner("Buscando equivalências..."):
                    st.session_state.analysis_results = find_equivalencies(
                        st.session_state.spreadsheet_data,
                        selected_university,
                        course_codes_input
                    )
            else:
                st.warning("Por favor, insira pelo menos um código de disciplina para analisar.")

    # --- ETAPA 5: EXIBIÇÃO DOS RESULTADOS ---
    if st.session_state.analysis_results:
        st.markdown("---")
        st.header("Resultado da Análise")
        
        # --- ALTERAÇÃO 1: Substituindo o loop pelo componente ---
        # A lógica de exibição agora está encapsulada no componente report_card,
        # que retorna a flag 'has_not_found' para nós.
        has_not_found = report_card_compact(st.session_state.analysis_results)

        st.markdown("---")

        # --- ETAPA 6: GERAÇÃO DO PDF (CONDICIONAL) ---

        

        # A lógica abaixo agora funciona com a flag retornada pelo componente.
        if not has_not_found:
            st.subheader("3. Gerar Relatório")
            st.success("Todas as disciplinas foram encontradas! Você já pode gerar o relatório.")

            pdf_bytes = create_pdf_bytes(st.session_state.analysis_results)
            st.download_button(
                label="Baixar Relatório em PDF",
                data=pdf_bytes,
                file_name="relatorio_equivalencia.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        else:
            st.error("⚠️ **Atenção:** Algumas disciplinas não foram encontradas na planilha. O relatório final não pode ser gerado até que todas as disciplinas sejam verificadas manualmente ou os códigos corrigidos.")

if __name__ == "__main__":
    main()