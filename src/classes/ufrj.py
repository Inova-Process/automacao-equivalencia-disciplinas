import json
import re
from typing import Set, Dict, Any, List

import pdfplumber

# TODO: Implementar funcao de validacao do pdf (verificar se eh BOA)
class UFRJ:
    """
    Classe para processar e extrair dados de documentos acadêmicos da UFRJ.

    Atributos:
        equivalences (dict): Um dicionário carregado de um arquivo JSON
                             contendo as regras de equivalência de disciplinas.
    """

    def __init__(self, equivalences_json_path: str):
        """
        Inicializa o processador da UFRJ.

        Args:
            equivalences_json_path (str): O caminho para o arquivo JSON
                                          contendo as regras de equivalência.
        """
        self.equivalences = self._load_equivalences(equivalences_json_path)

    def _load_equivalences(self, json_path: str) -> Dict[str, Any]:
        """
        Carrega as regras de equivalência de um arquivo JSON.

        Args:
            json_path (str): Caminho para o arquivo JSON.

        Returns:
            Um dicionário com os dados de equivalência ou um dicionário vazio
            se o arquivo não for encontrado ou for inválido.
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                print(f"✅ Arquivo de equivalências '{json_path}' carregado com sucesso.")
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Erro: Arquivo de equivalências não encontrado em '{json_path}'.")
            return {}
        except json.JSONDecodeError:
            print(f"⚠️ Erro: O arquivo '{json_path}' não é um JSON válido.")
            return {}

    def extract_student_data(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extrai todos os dados relevantes do aluno de um arquivo BOA (PDF).

        Esta função combina a extração de dados gerais (nome, CR, etc.) com a
        lista de todas as disciplinas aprovadas.

        Args:
            pdf_path (str): O caminho para o arquivo PDF do BOA.

        Returns:
            Um dicionário contendo os dados do aluno e a lista de matérias
            aprovadas. Retorna um dicionário de erro se o processamento falhar.
        """
        try:
            full_text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"

            # 1. Extrair dados acadêmicos (CR, Períodos, etc.)
            patterns = {
                "nome_aluno": r"Emissão\n\s*([A-Z\s]+)",
                "periodos_integralizados": r"Períodos Integralizados \(RES 10/2004 - CEG\):\s*([\d.]+)",
                "prazo_maximo": r"Prazo máximo de integralização:\s*([\d.]+)",
                "carga_horaria_obtida": r"Carga horária obtida acumulada:\s*([\d.]+)",
                "creditos_obtidos": r"Créditos obtidos acumulados:\s*([\d.]+)",
                "cr_acumulado": r"CR acumulado:\s*([\d.]+)",
                "carga_horaria_extensao": r"Carga horária acumulada extensão:\s*([\d.]+)"
            }

            extracted_data = {}
            for key, regex in patterns.items():
                match = re.search(regex, full_text)
                if match:
                    value = match.group(1).strip()
                    if key == "nome_aluno":
                        extracted_data[key] = value.title()
                    else:
                        extracted_data[key] = float(value)
                else:
                    extracted_data[key] = None # Usa None para indicar que não foi encontrado

            # 2. Extrair todas as matérias aprovadas
            approved_courses_set: Set[str] = set()
            codes_to_exclude: Set[str] = {"ICPZ55", "ICPX06"}
            
            # Padrão para encontrar linhas que representam matérias aprovadas
            # Procura por um código, seguido de qualquer texto, e terminando com uma nota numérica.
            approved_pattern = re.compile(
                r"^([A-Z]{3}\d{3,})\s+.*?\s+[\d\.]+\s*$",
                re.MULTILINE
            )

            matches = approved_pattern.findall(full_text)
            for course_code in matches:
                if course_code.upper() not in codes_to_exclude:
                    approved_courses_set.add(course_code.upper())
            
            # 3. Combinar todos os dados em um relatório final
            extracted_data["approved_courses"] = sorted(list(approved_courses_set))

            return extracted_data

        except Exception as e:
            return {"error": f"Ocorreu um erro ao processar o PDF: {e}"}

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # 1. Crie um arquivo chamado 'equivalencias_ufrj.json' com este conteúdo:
    # {
    #   "MAC118": ["Cálculo I", "Cálculo A"],
    #   "FIM120": ["Física I", "Física Experimental I"],
    #   "ICP100": ["Introdução à Programação", "Algoritmos e Estruturas de Dados I"]
    # }
    
    equivalencias_file = "equivalencias_ufrj.json"
    
    # Adicionei um bloco para criar o arquivo JSON de exemplo, caso ele não exista
    try:
        with open(equivalencias_file, 'x', encoding='utf-8') as f:
            example_json = {
              "MAC118": ["Cálculo I", "Cálculo A"],
              "FIM120": ["Física I", "Física Experimental I"],
              "ICP100": ["Introdução à Programação", "Algoritmos e Estruturas de Dados I"]
            }
            json.dump(example_json, f, indent=2, ensure_ascii=False)
            print(f"📄 Arquivo de exemplo '{equivalencias_file}' criado.")
    except FileExistsError:
        pass # O arquivo já existe, não faz nada

    # 2. Instancia a classe, carregando as regras de equivalência
    ufrj_processor = UFRJ(equivalences_json_path=equivalencias_file)

    # 3. Exibe as regras carregadas
    print("\n--- Regras de Equivalência Carregadas ---")
    print(json.dumps(ufrj_processor.equivalences, indent=2, ensure_ascii=False))

    # 4. Processa um arquivo BOA
    #    (substitua 'data/boa.pdf' pelo caminho do seu arquivo)
    file_path = r"data/boa.pdf" 
    print(f"\n--- Analisando o arquivo: {file_path} ---")
    student_data = ufrj_processor.extract_student_data_from_boa(file_path)

    # 5. Exibe o resultado da extração
    print("\n--- Dados Extraídos do Aluno ---")
    if "error" in student_data:
        print(f"Erro: {student_data['error']}")
    else:
        print(json.dumps(student_data, indent=2, ensure_ascii=False))