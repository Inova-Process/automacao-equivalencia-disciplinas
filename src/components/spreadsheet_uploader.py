import streamlit as st
import pandas as pd
from data_loader import load_spreadsheet 


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
    Valida a planilha carregada, verificando se PELO MENOS UMA aba 
    contém as colunas necessárias (definidas em REQUIRED_COLUMNS).

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
    
    # Se o dict de planilhas estiver vazio (arquivo sem abas)
    if not spreadsheet_data:
         return False, "O arquivo .xlsx está vazio (não contém abas)."

    # Itera pelas abas procurando por PELO MENOS UMA válida
    for sheet_name, df in spreadsheet_data.items():
        sheet_columns = set(df.columns)
        
        # Se as colunas obrigatórias SÃO um subconjunto das colunas da aba
        if REQUIRED_COLUMNS.issubset(sheet_columns):
            # Encontrou uma aba válida, a planilha inteira é considerada válida
            return True, "Planilha validada: Pelo menos uma aba de faculdade válida foi encontrada."
            
    # Se o loop terminar, significa que NENHUMA aba válida foi encontrada
    error_message = (
        "Validação falhou! Nenhuma aba na planilha contém o conjunto completo de colunas obrigatórias. "
        f"Verifique se pelo menos uma aba possui: {', '.join(list(REQUIRED_COLUMNS))}"
    )
    return False, error_message


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
