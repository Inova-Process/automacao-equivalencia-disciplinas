import pandas as pd
from pandas import DataFrame


def load_spreadsheet(file_path: str) -> dict[str, DataFrame] | None:
    """
    Carrega todas as abas de uma planilha Excel em um dicionário de DataFrames.

    Args:
        file_path (str): O caminho para o arquivo .xlsx.

    Returns:
        dict[str, DataFrame] | None: Um dicionário onde cada chave é o nome de uma aba
                                     e o valor é o DataFrame correspondente.
                                     Retorna None se o arquivo não for encontrado ou ocorrer um erro.
    """
    try:
        spreadsheet_data = pd.read_excel(file_path, sheet_name=None)
        print(f"Planilha '{file_path}' carregada com sucesso.")
        return spreadsheet_data
    except FileNotFoundError:
        print(f"ERRO: O arquivo não foi encontrado no caminho: {file_path}")
        return None
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao ler a planilha: {e}")
        return None


def get_university_list(spreadsheet_data: dict[str, DataFrame]) -> list[str]:
    """
    Extrai a lista de nomes das universidades (abas) do dicionário de dados.

    Args:
        spreadsheet_data (dict[str, DataFrame]): O dicionário de DataFrames
                                                  carregado pela função load_spreadsheet.

    Returns:
        list[str]: Uma lista com os nomes das universidades (as chaves do dicionário).
    """
    if not spreadsheet_data:
        return []
    
    return list(spreadsheet_data.keys())