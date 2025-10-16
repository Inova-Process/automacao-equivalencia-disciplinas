from fpdf import FPDF


def create_pdf_bytes(results: list) -> bytes:
    """
    Gera o conteúdo de um relatório em PDF como um objeto de bytes.

    Args:
        results (list): A lista de dicionários com os resultados da análise.
    
    Returns:
        bytes: O conteúdo do arquivo PDF gerado.
    """
    found_results = [r for r in results if r.get("status") == "Encontrado"]

    if not found_results:
        return b""

    # --- Configuração do PDF ---
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Parecer de Análise de Equivalência de Disciplinas", 0, 1, "C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(230, 230, 230)

    col_widths = {
        "dest_code": 25, "dest_name": 65, "origin_code": 25,
        "origin_name": 65, "year": 20, "parecer": 35
    }
    
    pdf.cell(col_widths["dest_code"] + col_widths["dest_name"], 8, "Disciplinas a Serem Dispensadas no IC/UFRJ", 1, 0, "C", fill=True)
    pdf.cell(col_widths["origin_code"] + col_widths["origin_name"] + col_widths["year"] + col_widths["parecer"], 8, "Disciplinas Cursadas na IES de Origem", 1, 1, "C", fill=True)

    pdf.cell(col_widths["dest_code"], 8, "Código", 1, 0, "C", fill=True)
    pdf.cell(col_widths["dest_name"], 8, "Nome", 1, 0, "C", fill=True)
    pdf.cell(col_widths["origin_code"], 8, "Código", 1, 0, "C", fill=True)
    pdf.cell(col_widths["origin_name"], 8, "Nome", 1, 0, "C", fill=True)
    pdf.cell(col_widths["year"], 8, "Ano", 1, 0, "C", fill=True)
    pdf.cell(col_widths["parecer"], 8, "Parecer", 1, 1, "C", fill=True)

    pdf.set_font("Arial", "", 9)
    for item in found_results:
        is_equivalent_str = str(item.get("is_equivalent", "Não")).lower()
        is_equivalent = is_equivalent_str in ['sim', 's', 'true', '1', 'verdadeiro']

        if is_equivalent:
            parecer_text = "Favorável"
            pdf.set_text_color(34, 139, 34)
        else:
            parecer_text = "Desfavorável"
            pdf.set_text_color(220, 20, 60)

        pdf.cell(col_widths["dest_code"], 8, item.get("dest_codes", ""), 1, 0, "L")
        pdf.cell(col_widths["dest_name"], 8, item.get("dest_names", ""), 1, 0, "L")
        pdf.cell(col_widths["origin_code"], 8, item.get("origin_codes", ""), 1, 0, "L")
        pdf.cell(col_widths["origin_name"], 8, item.get("origin_names", ""), 1, 0, "L")
        pdf.cell(col_widths["year"], 8, "20XX.X", 1, 0, "C")
        
        current_x = pdf.get_x()
        current_y = pdf.get_y()
        pdf.multi_cell(col_widths["parecer"], 8, parecer_text, 1, "C")
        pdf.set_xy(current_x + col_widths["parecer"], current_y)

        pdf.ln()
        pdf.set_text_color(0, 0, 0)

    return bytes(pdf.output())


if __name__ == "__main__":
    print("Iniciando teste de geração de PDF...")

    sample_results_for_test = [
        {"input_code": "CEX001", "status": "Encontrado", "origin_codes": "CEX001", "origin_names": "Cálculo I", "is_equivalent": "Sim", "dest_codes": "MAC118", "dest_names": "Cálculo Diferencial e Integral I", "justification": "Ementa compatível."},
        {"input_code": "FIS002", "status": "Encontrado", "origin_codes": "FIS002", "origin_names": "Física Experimental I", "is_equivalent": "Não", "dest_codes": "FIS121", "dest_names": "Física Experimental I", "justification": "Carga horária insuficiente."},
        {"input_code": "COMP123", "status": "Não Encontrado na Planilha"},
        {"input_code": "QUI003", "status": "Encontrado", "origin_codes": "QUI003, QUI004", "origin_names": "Química Geral e Inorgânica", "is_equivalent": True, "dest_codes": "QUIG11", "dest_names": "Química Geral", "justification": "Conteúdo coberto."}
    ]

    pdf_bytes = create_pdf_bytes(sample_results_for_test)

    if pdf_bytes:
        file_path = "teste_relatorio.pdf"
        # O modo "wb" (write bytes) é o correto para o que a função retorna
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ PDF de teste gerado com sucesso!")
        print(f"Abra o arquivo '{file_path}' para verificar o resultado.")
    else:
        print("❌ Nenhum dado encontrado para gerar o PDF.")
