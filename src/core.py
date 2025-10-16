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
    
    # 1. Pega o DataFrame da universidade correta
    university_df = all_data.get(selected_university)
    if university_df is None:
        return [{"error": f"Dados para a universidade '{selected_university}' não encontrados."}]

    # 2. Limpa e separa os códigos de entrada
    cleaned_str = course_codes_str.replace(",", " ").replace("\n", " ")
    input_codes = [code.strip().upper() for code in cleaned_str.split() if code.strip()]

    # 3. Itera sobre cada código que o usuário inseriu
    for code in input_codes:
        found = False
        for index, row in university_df.iterrows():
            origin_codes = str(row['Códigos Origem'])
                
            if code in [c.strip().upper() for c in origin_codes.split('+')]:
                # 4. Se encontrou, monta um dicionário com os resultados
                result_details = {
                    "input_code": code,
                    "status": "Encontrado", 
                    "origin_codes": row['Códigos Origem'],
                    "origin_names": row['Nomes Origem'],
                    "is_equivalent": row['Equivalente?'],
                    "dest_codes": row['Códigos UFRJ Destino'],
                    "dest_names": row['Nomes UFRJ Destino'],
                    "justification": row['Justificativa Parecer']
                }
                results.append(result_details)
                found = True
                break 
        
        # 5. Se o loop terminou e não encontrou, registra como "Não Encontrado"
        if not found:
            results.append({
                "input_code": code,
                "status": "Não Encontrado na Planilha"  
            })

    return results