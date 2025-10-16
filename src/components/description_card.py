import streamlit as st

def description_card():
    """
    Exibe um card de descrição completo para o sistema de análise de equivalências,
    detalhando o funcionamento atual, a evolução da arquitetura e melhorias futuras.
    """
    with st.expander("ℹ️ Como funciona o sistema? (Clique para expandir)"):
        st.markdown("""
        Este sistema foi projetado para automatizar a verificação de equivalência de disciplinas de forma simples e rápida:
        
        - **1. Upload do Histórico:** O processo começa com o upload do seu histórico escolar em formato PDF.
        
        - **2. Seleção da Universidade:** Em seguida, você seleciona a sua universidade de origem em uma lista.
        
        - **3. Análise e Comparação:** Com um clique, o sistema lê as matérias cursadas no seu histórico e as compara com uma base de dados interna (um arquivo JSON) que define as regras de equivalência para gerar um relatório preliminar.
        """)

    with st.expander("🎯 Próximos Passos: Evolução da Arquitetura"):
        st.markdown("""
        Para aumentar a precisão e facilitar a inclusão de novas instituições, o próximo passo é refatorar a lógica de processamento. A estratégia é:
        
        - **1. Implementar Classes por Universidade:** Criar uma `classe` em Python específica para cada universidade parceira.
        
        - **2. Lógica Adaptada:** Cada classe conterá a lógica customizada para:
            - **Ler o layout único** do histórico escolar daquela instituição.
            - **Interpretar sistemas de notas** e créditos específicos.
            - **Tratar as particularidades** dos nomes das disciplinas.
            
        - **3. Benefícios:** Essa abordagem torna o sistema **mais robusto**, **preciso** e **escalável**, permitindo adicionar suporte a uma nova universidade de forma organizada, sem impactar as já existentes.
        """)

    with st.expander("🚀 Ideias de Melhorias Futuras"):
        st.markdown("""
        Além da evolução da arquitetura, planejamos outras funcionalidades para aprimorar a ferramenta a longo prazo:
        
        - **📄 Geração de Parecer em PDF:** Adicionar um botão para exportar o relatório final da análise para um arquivo PDF formatado, servindo como parecer oficial da comissão.
        
        - **⚙️ Banco de Dados de Decisões:** Criar um histórico de equivalências já analisadas. Se uma disciplina da Instituição X já foi deferida, o sistema pode aprovar automaticamente novos pedidos idênticos.
        
        - **📧 Notificações por E-mail:** Implementar o envio de um e-mail automático para o aluno e para os membros da comissão com o resultado da análise ou solicitando informações adicionais.
        """)
