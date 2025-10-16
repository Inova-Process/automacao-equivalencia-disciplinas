import streamlit as st

def render_header(logo_path):
    """
    Renderiza o cabeçalho centralizado da aplicação com a logo,
    título e subtítulo.
    """
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, width=200)

    st.title("Equivalência de Disciplinas")
    st.caption("Uma ferramenta para auxiliar e automatizar a comissão de equivalência de disciplinas.")

    st.divider()
