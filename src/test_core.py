
from data_loader import load_spreadsheet
from core import find_equivalencies
import json  
# Carrega os dados uma vez para usar nos testes
TEST_FILE_PATH = 'data/planilha_teste.xlsx'
spreadsheet_data = load_spreadsheet(TEST_FILE_PATH)

def run_core_tests():
    print("--- Iniciando teste do core.py ---")
    
    # Cenário 1: Testar com a UFRGS
    print("\n--- Testando busca na UFRGS ---")
    selected_uni = "UFRGS"
    # Inclui um código simples, um código de uma combinação e um código que não existe
    codes_to_test = "INF01202, INF01107, ABC123"
    
    if spreadsheet_data:
        results = find_equivalencies(spreadsheet_data, selected_uni, codes_to_test)
        
        # Imprime os resultados de forma organizada
        print("Resultados da busca:")
        for res in results:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        
        # Validações
        assert len(results) == 3
        assert results[0]['status'] == 'Encontrado'
        assert results[1]['status'] == 'Encontrado'
        assert results[2]['status'] == 'Não Encontrado na Planilha'
        assert results[1]['origin_codes'] == 'INF01108+INF01107'
        print("Validações do teste da UFRGS: OK")

    print("\n✅ Todos os testes do core passaram com sucesso!")


if __name__ == "__main__":
    run_core_tests()