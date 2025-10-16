from data_loader import load_spreadsheet, get_university_list

TEST_FILE_PATH = 'data/planilha_teste.xlsx'

def run_tests():
    print("--- Iniciando teste do data_loader ---")
    
    # Testa o carregamento da planilha
    all_data = load_spreadsheet(TEST_FILE_PATH)

    # Verifica se os dados foram carregados antes de prosseguir
    if all_data:
        print("\n--- Testando extração da lista de universidades ---")
        universities = get_university_list(all_data)
        print(f"Lista de universidades extraída: {universities}")
        
        # Validações básicas (asserts) para garantir que tudo está certo
        assert len(universities) == 3  # Esperamos 3 abas
        assert "UFRGS" in universities
        assert "PUC-Rio" in universities
        assert "UFF" in universities
        print("Validação da lista de universidades: OK")

        print("\n--- Teste de leitura de uma aba específica (UFRGS) ---")
        ufrgs_data = all_data.get('UFRGS')
        if ufrgs_data is not None:
            print("Cabeçalho dos dados da UFRGS:")
            print(ufrgs_data.head()) # Mostra as 5 primeiras linhas
            
            # Valida se as colunas esperadas estão presentes
            expected_columns = ["Códigos Origem", "Equivalente?", "Códigos UFRJ Destino"]
            for col in expected_columns:
                assert col in ufrgs_data.columns
            print("Validação das colunas da UFRGS: OK")
        
        print("\n✅ Todos os testes do data_loader passaram com sucesso!")

if __name__ == "__main__":
    run_tests()