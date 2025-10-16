import pandas as pd
from pandas import DataFrame

def find_equivalencies(
    all_data: dict[str, DataFrame], 
    selected_university: str, 
    course_codes_str: str
) -> list[dict]:
    """
    Busca por equivalências de disciplinas em um DataFrame de uma universidade específica.

    Args:
        all_data (dict[str, DataFrame]): Dicionário com todos os dados da planilha.
        selected_university (str): O nome da universidade (aba da planilha) selecionada.
        course_codes_str (str): Uma string contendo os códigos das disciplinas,
                                separados por vírgulas, espaços ou quebras de linha.

    Returns:
        list[dict]: Uma lista de dicionários, onde cada dicionário representa o
                    resultado de uma busca para um código de disciplina.
    """
    results = []
    
    university_df = all_data.get(selected_university)
    if university_df is None:
        return [{"error": f"Dados para a universidade '{selected_university}' não encontrados."}]

    # 1. Prepara os códigos de entrada do usuário em um CONJUNTO (set) para facilitar a remoção.
    cleaned_str = course_codes_str.replace(",", " ").replace("\n", " ")
    # Usamos um set para que a remoção de itens seja mais eficiente
    input_codes_set = {code.strip().upper() for code in cleaned_str.split() if code.strip()}

    # 2. Itera primeiro sobre as REGRAS da planilha (cada linha do DataFrame)
    for index, rule in university_df.iterrows():
        origin_codes_str = str(rule['Códigos Origem'])
        # Pega a lista de códigos necessários para ESTA regra
        required_codes = {c.strip().upper() for c in origin_codes_str.split('+')}
        
        # 3. Verifica se a regra PODE ser aplicada:
        # A regra só é válida se TODOS os seus códigos requeridos estiverem no input do usuário
        if required_codes.issubset(input_codes_set):
            # A regra foi acionada!
            result_details = {
                "status": "Encontrado",
                "origin_codes": rule['Códigos Origem'],
                "origin_names": rule['Nomes Origem'],
                "is_equivalent": rule['Equivalente?'],
                "dest_codes": rule['Códigos UFRJ Destino'],
                "dest_names": rule['Nomes UFRJ Destino'],
                "justification": rule['Justificativa Parecer']
            }
            results.append(result_details)
            
            # 4. CRUCIAL: Se a regra foi aplicada, remove os códigos usados do conjunto de input.
            # Isso impede que eles sejam usados para acionar outra regra.
            input_codes_set -= required_codes

    # 5. Adiciona os códigos que sobraram no conjunto como 'Não Encontrado na Planilha'
    # O que sobrou aqui são os códigos que o usuário digitou mas que não se encaixaram em nenhuma regra.
    for remaining_code in sorted(list(input_codes_set)): # sorted para ordem consistente
        results.append({
            "input_code": remaining_code,
            "status": "Não Encontrado na Planilha"
        })

    return results
