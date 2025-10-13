import json
from typing import List, Set, Dict

# A função load_rules_from_json continua a mesma...
def load_rules_from_json(file_path: str) -> List[Dict]:
    """Carrega a lista de regras de um arquivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)
        return rules
    except FileNotFoundError:
        print(f"Erro: Arquivo de regras não encontrado em '{file_path}'.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: O arquivo em '{file_path}' não é um JSON válido.")
        return []

# A nova função com o modo debug
def find_possible_equivalences(
    approved_courses: Set[str],
    rules: List[Dict[str, List[str]]],
    debug: bool = False
) -> List[str]:
    """
    Compara as disciplinas aprovadas de um aluno com a lista de regras de equivalência.
    """
    waivable_courses = set()
    if debug:
        print("\n--- MODO DE DIAGNÓSTICO ATIVADO ---")
    for i, rule in enumerate(rules):
        required_courses = set(rule['requires'])
        is_satisfied = required_courses.issubset(approved_courses)
        if debug:
            print(f"\nVerificando Regra #{i+1}:")
            print(f"--> Requer: {sorted(list(required_courses))}")
            if is_satisfied:
                print(f"--> Status: OK! (Aluno possui todos os pré-requisitos)")
                print(f"--> Concede: {rule['grants']}")
            else:
                missing = required_courses.difference(approved_courses)
                print(f"--> Status: FALHOU. Faltam as seguintes matérias: {sorted(list(missing))}")
        if is_satisfied:
            waivable_courses.update(rule['grants'])
    if debug:
        print("\n--- FIM DO DIAGNÓSTICO ---")
    return sorted(list(waivable_courses))


# run_equivalence_analysis ajustada para aceitar o parâmetro 'debug'
def run_equivalence_analysis(
    approved_courses: Set[str],
    rules_file_path: str,
    debug: bool = False
) -> List[str]:
    """
    Orquestra todo o fluxo de análise de equivalência.
    """
    equivalence_rules = load_rules_from_json(rules_file_path)
    if not equivalence_rules:
        return []
    result = find_possible_equivalences(approved_courses, equivalence_rules, debug=debug)
    return result


if __name__ == "__main__":
    
    student_approved_courses = {
        'ICP120',
        'MAB120',
        'MAB624',
        'ICP230'
    }

    print("--- Análise de Equivalência ---")
    print(f"Disciplinas Aprovadas do Aluno: {sorted(list(student_approved_courses))}\n")

    # Executa a análise, agora passando debug=True para ver o passo a passo
    waivable_courses = run_equivalence_analysis(student_approved_courses, debug=True)

    print("\n--- RESULTADO FINAL ---")
    if waivable_courses:
        print("O aluno pode solicitar o corte das seguintes disciplinas:")
        for course in waivable_courses:
            print(f"- {course}")
    else:
        print("Nenhuma equivalência possível foi encontrada para as disciplinas aprovadas.")