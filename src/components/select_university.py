import streamlit as st


def select_university(universities: list) -> str:
    """
    Cria um componente de seleção em Streamlit para que o usuário
    possa escolher uma universidade de uma lista ou inserir um nome manualmente.

    Args:
        universities_df: DataFrame do Pandas que contém uma coluna "INSTITUIÇÃO"
                         com os nomes das universidades.

    Returns:
        O nome da universidade selecionada ou digitada pelo usuário.
    """
    # 2. Componente de Seleção (Selectbox)
    st.header("1. Selecione a Universidade")

    # Lista das universidades
    lista_universidades = universities

    # O widget selectbox retorna o nome que foi selecionado
    selected_university = st.selectbox(
        "Escolha uma universidade abaixo:",
        options=lista_universidades,
        index=None,
        placeholder="Selecione uma das universidades",
        help="O nome selecionado será associado ao documento enviado."
    )

    st.write("#### Não encontrou a universidade?")

    # Checkbox para ativar a entrada manual
    ativar_entrada_manual = st.checkbox("Digitar o nome de outra universidade")

    # Variável para armazenar o nome final da universidade
    nome_universidade_final = ""

    # Lógica condicional baseada no checkbox
    if ativar_entrada_manual:
        # Se o checkbox estiver MARCADO, mostra o campo de texto
        nome_digitado = st.text_input(
            "Digite o nome da nova universidade:",
            placeholder="Nome da universidade que não está na lista"
        )
        # O nome final será o que o usuário digitar
        if nome_digitado:
            nome_universidade_final = nome_digitado.strip()
    else:
        # Se o checkbox estiver DESMARCADO, o nome final é o do selectbox
        if selected_university:
            nome_universidade_final = selected_university

    return nome_universidade_final
