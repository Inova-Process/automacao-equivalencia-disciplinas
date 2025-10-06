import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Optional
import re
import os

def get_page_content(url: str) -> Optional[BeautifulSoup]:
    """
    Busca o conteúdo de uma URL, tratando a codificação de caracteres corretamente.
    """
    print(f"Acessando a URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser', from_encoding='iso-8859-1')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return None


def extract_tables_data(soup: BeautifulSoup) -> Optional[Dict[str, List[List[str]]]]:
    """
    Extrai dados de múltiplas tabelas para um dicionário, usando a lógica do usuário.
    A chave do dicionário é o título da tabela.
    """
    tabelas = soup.find_all('table', class_='cellspacingTable')
    if not tabelas:
        return None
    
    dados_por_tabela = {}
    
    for tabela in tabelas:
        titulo_tr = tabela.find("tr", class_="tableTitleBlue")
        
        if titulo_tr:
            titulo_texto = titulo_tr.get_text(strip=True)
            if not titulo_texto:
                titulo_texto = f"Tabela Encontrada (sem título)"

            linhas_de_dados = titulo_tr.find_next_siblings('tr')
            dados_da_tabela_atual = []
            
            for linha in linhas_de_dados:
                celulas_header = [celula.get_text(strip=True) for celula in linha.find_all('th')]
                celulas_data = [celula.get_text(strip=True) for celula in linha.find_all('td')]
                
                celulas = celulas_header + celulas_data
                if celulas:
                    dados_da_tabela_atual.append(celulas)
            
            if dados_da_tabela_atual:
                dados_por_tabela[titulo_texto] = dados_da_tabela_atual
                
    if not dados_por_tabela:
        print("Lógica do usuário: Nenhuma tabela com a estrutura de título 'tableTitleBlue' foi processada com sucesso.")
        return None

    return dados_por_tabela


def create_dataframes(data: Dict[str, List[List[str]]]) -> Dict[str, pd.DataFrame]:
    """
    Cria um dicionário de DataFrames, garantindo que todas as linhas de dados
    tenham o mesmo número de colunas que o cabeçalho.
    """
    dataframes_dict = {}
    for table_name, table_data in data.items():
        if not table_data:
            print(f"Aviso: Tabela '{table_name}' está vazia. Pulando.")
            continue
        
        header = table_data[0]
        body_data = table_data[1:]
        
        num_cols_header = len(header)
        
        dados_corretos = []
        for i, row in enumerate(body_data):
            if len(row) == num_cols_header:
                dados_corretos.append(row)
            else:
                print(f"Aviso na tabela '{table_name}': Linha {i+1} tem {len(row)} colunas (esperado: {num_cols_header}). Será ignorada.")
        
        df = pd.DataFrame(dados_corretos, columns=header)
        dataframes_dict[table_name] = df
        
    return dataframes_dict


def main():
    """
    Orquestra todo o fluxo de scraping: buscar, extrair, transformar e salvar
    cada tabela em um arquivo Excel separado na pasta 'data'.
    """
    URL_ALVO = "https://www.siga.ufrj.br/sira/repositorio-curriculo/distribuicoes/402FED54-92A4-F79C-3ACF-54A4EA89ED35.html"
    PASTA_SAIDA = "data"
    
    soup = get_page_content(URL_ALVO)
    if not soup:
        print("Encerrando o script, pois não foi possível obter o conteúdo da página.")
        return

    dados_brutos = extract_tables_data(soup)
    if not dados_brutos:
        print("Nenhuma tabela foi encontrada na página com os critérios definidos. Encerrando.")
        return

    dataframes = create_dataframes(dados_brutos)
    if not dataframes:
        print("Não foi possível criar os DataFrames a partir dos dados extraídos. Encerrando.")
        return

    # --- ETAPA 4: SALVAR RESULTADOS EM ARQUIVOS EXCEL SEPARADOS ---
    print("\n--- Iniciando a gravação dos arquivos Excel ---")
    
    # Cria a pasta 'data' se ela não existir
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    
    # Itera sobre o dicionário de DataFrames para salvar cada um
    for table_name, df in dataframes.items():
        try:
            # Cria um nome de arquivo seguro a partir do título da tabela
            safe_filename = re.sub(r'[^\w\s-]', '', table_name).strip().replace(' ', '_')
            output_filename = f"{safe_filename}.xlsx"
            
            # Define o caminho completo do arquivo, dentro da pasta 'data'
            caminho_completo = os.path.join(PASTA_SAIDA, output_filename)
            
            # Salva o DataFrame em seu próprio arquivo Excel
            df.to_excel(caminho_completo, index=False, engine='openpyxl')
            print(f"[SUCESSO] Tabela '{table_name}' salva como '{caminho_completo}'")

        except Exception as e:
            print(f"[ERRO] Falha ao salvar a tabela '{table_name}': {e}")


if __name__ == "__main__":
    main()
