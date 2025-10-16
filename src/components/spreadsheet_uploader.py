import streamlit as st
import pandas as pd
from src.data_loader import load_spreadsheet 

REQUIRED_COLUMNS = {
    "Códigos Origem",
    "Nomes Origem",
    "Equivalente?",
    "Códigos UFRJ Destino",
    "Nomes UFRJ Destino",
    "Justificativa Parecer"
}

def validate_spreadsheet(uploaded_file) -> tuple[bool, str]:
    """
    Valida a planilha carregada, verificando se todas as abas contêm as colunas necessárias.

    Args:
        uploaded_file: O objeto de arquivo carregado pelo Streamlit.

    Returns:
        tuple[bool, str]: Uma tupla contendo (True/False para validade, mensagem de status).
    """
    if uploaded_file is None:
        return False, "Nenhum arquivo carregado."

    spreadsheet_data = load_spreadsheet(uploaded_file)
    
    if spreadsheet_data is None:
        return False, "O arquivo não pôde ser lido. Verifique se é um arquivo .xlsx válido."
    
    for sheet_name, df in spreadsheet_data.items():
        sheet_columns = set(df.columns)
        
        if not REQUIRED_COLUMNS.issubset(sheet_columns):
            missing_cols = REQUIRED_COLUMNS - sheet_columns
            error_message = (
                f"Validação falhou! A aba '{sheet_name}' não contém as seguintes colunas obrigatórias: "
                f"{', '.join(missing_cols)}"
            )
            return False, error_message
            
    return True, "Planilha validada com sucesso! Todas as abas contêm as colunas necessárias."


def render_spreadsheet_uploader():
    """
    Renderiza o componente de upload de arquivo e realiza a validação da planilha.

    Returns:
        O objeto do arquivo carregado (UploadedFile) se for válido, senão None.
    """
    st.subheader("1. Carregue a Planilha de Equivalências")
    uploaded_file = st.file_uploader(
        "Selecione o arquivo .xlsx com os dados de equivalência",
        type="xlsx",
        label_visibility="collapsed"
    )

    if uploaded_file:
        is_valid, message = validate_spreadsheet(uploaded_file)
        if is_valid:
            st.success(message)
            return uploaded_file
        else:
            st.error(message)
            return None
            
    return None