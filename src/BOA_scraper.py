import json
import re
from typing import Set, Dict, Any

import pdfplumber


def validate_boa(uploaded_file) -> bool:
    # Garante que o "cursor" de leitura do arquivo está no início
    uploaded_file.seek(0)
    with pdfplumber.open(uploaded_file) as pdf:
        first_page_text = pdf.pages[0].extract_text()
        
        if "BOLETIM DE ORIENTAÇÃO ACADÊMICA" in first_page_text:
            return True
        return False


def extract_student_data_from_boa(pdf_path: str) -> Dict[str, Any]:
    """
    Reads a BOA PDF file, extracts the student's full name, and lists all
    approved courses from all pages.

    Args:
        pdf_path: The file path to the BOA PDF document.

    Returns:
        A dictionary containing the student's name and a list of approved
        course codes.
        Example:
        {
            "student_name": "NOME COMPLETO DO ALUNO",
            "approved_courses": ["ICP131", "MAE111", ...]
        }
    """
    full_text = ""
    student_name = "Not found"
    approved_courses_set: Set[str] = set()

    # Codes to be ignored in the final list
    codes_to_exclude: Set[str] = {"ICPZ55", "ICPX06"}
    
    # Updated list of course prefixes to search for
    course_prefixes = ['CMT', 'FIM', 'FIT', 'FIW', 'ICP', 'MAB', 'MAC', 'MAE', 'MAW']
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from all pages
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

            
            name_match = re.search(r"Emissão\n\s*([A-Z\s]+)", full_text)
            if name_match:
                student_name = name_match.group(1).strip()

             
            prefixes_pattern = "|".join(course_prefixes)
            approved_pattern = re.compile(
                rf"^((?:{prefixes_pattern})\w+)\s+.*?\s+[\d\.]+\s*$", 
                re.MULTILINE
            )

            matches = approved_pattern.findall(full_text)
            for course_code in matches:
                if course_code.upper() not in codes_to_exclude:
                    approved_courses_set.add(course_code.upper())

        
        final_report = {
            "student_name": student_name.title(),
            "approved_courses": sorted(list(approved_courses_set))
        }

        return final_report

    except Exception as e:
        return {"error": f"An error occurred while processing the PDF: {e}"}


def extract_academic_data_from_boa(pdf_path: str) -> dict:
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() or ""

    # 2. Define os padrões de busca para cada campo de interesse
    # A chave do dicionário será a chave no nosso resultado final.
    # O valor é o texto exato que procuramos no documento.
    patterns = {
        "nome_aluno": r"Emissão\n\s*([A-Z\s]+)",
        "periodos_integralizados": r"Períodos Integralizados \(RES 10/2004 - CEG\):",
        "prazo_maximo": r"Prazo máximo de integralização:",
        "carga_horaria_obtida": r"Carga horária obtida acumulada:",
        "creditos_obtidos": r"Créditos obtidos acumulados:",
        "cr_acumulado": r"CR acumulado:",
        "carga_horaria_extensao": r"Carga horária acumulada extensão:"
    }

    extracted_data = {}

    # 3. Itera sobre cada padrão para encontrar o valor correspondente
    for key, label in patterns.items():
        # Constrói a expressão regular:
        # - texto_label: O texto que estamos procurando.
        # - \s*: Procura por zero ou mais espaços, quebras de linha ou tabs.
        # - ([\d.]+): Captura um grupo de um ou mais dígitos (\d) ou pontos (.).
        #   Este grupo é o nosso valor!
        regex = rf"{label}\s*([\d.]+)"

        # Procura pelo padrão no texto completo
        match = re.search(regex, full_text)

        if match:
            if key == "nome_aluno":
                extracted_data[key] = match.group(1).strip().title()
            else:
                extracted_data[key] = float(match.group(1))
        else:
            extracted_data[key] = "Not found"

    return extracted_data




def extract_approved_courses(page_text: str) -> Set[str]:
    """
    Extracts all approved course codes from the text.

    :param page_text: The full text extracted from the first page of the BOA PDF.
    :return: A set of course codes for all approved courses.
    """
    codes_to_exclude = {"ICPZ55", "ICPX06"}

    # Pattern to find approved courses (lines ending with a grade).
    approved_pattern = r"^((?:ICP|MAE|MAD|ICPX|ICPZ)\w+)\s+.*?\s+\d+\.\d\s+\d+\s+([\d\.]{1,4})$"
    
    approved_set = set()
    
    matches = re.findall(approved_pattern, page_text, re.MULTILINE)
    for match in matches:
        course_code = match[0].upper()
        if course_code not in codes_to_exclude:
            approved_set.add(course_code)
            
    return approved_set


 
def analyze_course_completion(file_path: str) -> Dict[str, Any]:
    """
    Orchestrates the full process of extracting and comparing course data from a BOA PDF.

    :param file_path: The path to the BOA PDF file.
    :return: A dictionary with the complete analysis.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            page_1_text = pdf.pages[0].extract_text()

            # Step 1: Extract required courses
            required = extract_required_courses(page_1_text)
            
            # Step 2: Extract approved courses
            approved = extract_approved_courses(page_1_text)

            # TODO: implement extraction for other pages
            
            # Step 3: Compare and get the status
            completion_status = check_course_completion_status(required, approved)

            # Combine all information into a final report
            final_report = {
                "materias_necessarias_periodo4": sorted(list(required)),
                "materias_aprovadas": sorted(list(approved)),
                "status": completion_status
            }

            return final_report

    except Exception as e:
        return {"error": f"An error occurred while processing the PDF: {e}"}


if __name__ == "__main__":
    # file_path = r"data/boa - giovanna.pdf"
    file_path = r"data/boa.pdf"

    # academic_data = extract_academic_data_from_boa(file_path)
    # print(academic_data)
    
    full_analysis = analyze_course_completion(file_path)

    print("\n--- Course Completion Analysis ---")
    print(json.dumps(full_analysis, indent=2, ensure_ascii=False))
