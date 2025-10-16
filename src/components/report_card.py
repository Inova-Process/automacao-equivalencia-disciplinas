import streamlit as st

def report_card_compact(results: list) -> bool:
    """
    Exibe um relatório de equivalência de matérias de forma compacta,
    agrupando os resultados por status em expanders.
    Todo o relatório é encapsulado em um container com borda.

    Args:
        results (list): Uma lista de dicionários com os detalhes da análise.
    
    Returns:
        bool: True se todas as matérias foram encontradas, False caso contrário.
    """
    # Container principal que engloba todo o relatório
    with st.container(border=True):
        st.subheader("Resultado da Análise de Equivalência")

        if not results:
            st.info("Nenhuma matéria foi processada para exibir o resultado.")
            return True # Retorna True se a lista de entrada estiver vazia

        # 1. Separar os resultados em listas por categoria
        equivalentes = []
        nao_equivalentes = []
        nao_encontrados = []

        for result in results:
            status = result.get("status")
            if status == "Encontrado":
                is_equivalent_str = str(result.get("is_equivalent", "Não")).lower()
                if is_equivalent_str in ['sim', 's', 'true', '1', 'verdadeiro']:
                    equivalentes.append(result)
                else:
                    nao_equivalentes.append(result)
            elif status == "Não Encontrado na Planilha":
                nao_encontrados.append(result)

        # 2. Criar um expander para cada categoria, se não estiver vazia

        # Expander para Matérias Equivalentes
        if equivalentes:
            with st.expander(f"✅ Matérias Equivalentes ({len(equivalentes)})", expanded=True):
                for item in equivalentes:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Origem:** {item.get('origin_names', 'N/A')}")
                        st.caption(f"Código: `{item.get('origin_codes', 'N/A')}`")
                    with col2:
                        st.markdown(f"**Destino (UFRJ):** {item.get('dest_names', 'N/A')}")
                        st.caption(f"Código: `{item.get('dest_codes', 'N/A')}`")
                    
                    if item.get('justification'):
                        st.info(f"**Justificativa:** {item.get('justification')}", icon="ℹ️")
                    st.divider()

        # Expander para Matérias Não Equivalentes
        if nao_equivalentes:
            with st.expander(f"❌ Matérias Não Equivalentes ({len(nao_equivalentes)})", expanded=False):
                for item in nao_equivalentes:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Origem:** {item.get('origin_names', 'N/A')}")
                        st.caption(f"Código: `{item.get('origin_codes', 'N/A')}`")
                    with col2:
                        st.markdown(f"**Destino (UFRJ):** {item.get('dest_names', 'N/A')}")
                        st.caption(f"Código: `{item.get('dest_codes', 'N/A')}`")

                    if item.get('justification'):
                        st.warning(f"**Justificativa:** {item.get('justification')}", icon="⚠️")
                    st.divider()

        # Expander para Matérias Não Encontradas
        if nao_encontrados:
            with st.expander(f"❓ Matérias Não Encontradas ({len(nao_encontrados)})", expanded=False):
                codes = [f"`{item.get('input_code')}`" for item in nao_encontrados]
                st.write("Os seguintes códigos não foram localizados na base de dados de equivalência:")
                st.warning(", ".join(codes))

        # 3. Retornar o booleano com base na lista de 'nao_encontrados'
        return len(nao_encontrados) > 0


if __name__ == "__main__":
    # Título do seu App
    st.title("Analisador de Equivalência de Matérias")

    # --- CENÁRIO 1: Todas as matérias são encontradas ---
    st.header("Cenário 1: Todas Encontradas")
    sample_results_all_found = [
        {
            "input_code": "CEX001", "status": "Encontrado", "origin_codes": "CEX001",
            "origin_names": "Cálculo I", "is_equivalent": "Sim", "dest_codes": "MAC118",
            "dest_names": "Cálculo Diferencial e Integral I", "justification": "Ementa e carga horária totalmente compatíveis."
        },
        {
            "input_code": "FIS002", "status": "Encontrado", "origin_codes": "FIS002",
            "origin_names": "Física Experimental I", "is_equivalent": "Não", "dest_codes": "FIS121",
            "dest_names": "Física Experimental I", "justification": "Carga horária da matéria de origem é inferior à da matéria de destino."
        }
    ]

    todas_encontradas = report_card_compact(sample_results_all_found)
    st.write(f"**Resultado da verificação:** `todas_encontradas` é `{todas_encontradas}`")
    st.write("---")


    # --- CENÁRIO 2: Algumas matérias NÃO são encontradas ---
    st.header("Cenário 2: Algumas Não Encontradas")
    sample_results_some_not_found = [
        {
            "input_code": "CEX001", "status": "Encontrado", "origin_codes": "CEX001",
            "origin_names": "Cálculo I", "is_equivalent": "Sim", "dest_codes": "MAC118",
            "dest_names": "Cálculo Diferencial e Integral I", "justification": "Ementa compatível."
        },
        {"input_code": "COMP123", "status": "Não Encontrado na Planilha"}
    ]

    todas_encontradas_2 = report_card_compact(sample_results_some_not_found)
    st.write(f"**Resultado da verificação:** `todas_encontradas_2` é `{todas_encontradas_2}`")

    # Exemplo de como você pode usar o booleano em outra lógica
    if todas_encontradas_2:
        st.success("Tudo certo! Todas as matérias foram processadas e você pode prosseguir.")
    else:
        st.error("Atenção: Uma ou mais matérias não foram encontradas. Verifique os códigos e tente novamente.")
