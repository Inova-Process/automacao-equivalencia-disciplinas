import streamlit as st
import pdfplumber


def validate_boa(uploaded_file) -> bool:
    # Garante que o "cursor" de leitura do arquivo está no início
    uploaded_file.seek(0)
    with pdfplumber.open(uploaded_file) as pdf:
        first_page_text = pdf.pages[0].extract_text()
        
        if "BOLETIM DE ORIENTAÇÃO ACADÊMICA" in first_page_text:
            return True
        return False


def file_upload():
    """
    Renderiza a seção de upload de arquivo dentro de um container
    e realiza a validação inicial do arquivo BOA.

    Retorna:
        O objeto do arquivo carregado (UploadedFile) se for válido, senão None.
    """
    # O container agora faz parte do componente
    with st.container(border=True):
        st.header("2. Faça o upload do Histórico Acadêmico em PDF")
        uploaded_file = st.file_uploader(
            "Anexe o Boletim de Orientação Acadêmica do aluno",
            type="pdf",
            help="Apenas arquivos no formato .pdf são aceitos.",
            label_visibility="collapsed" 
        )

        # Validação do arquivo 
        if uploaded_file:
            if validate_boa(uploaded_file):
                st.success(f"Arquivo '{uploaded_file.name}' validado e pronto para análise!")
                return uploaded_file
            else:
                st.error("O arquivo carregado não parece ser um BOA válido. Por favor, verifique e tente novamente.")
                return None
    return None