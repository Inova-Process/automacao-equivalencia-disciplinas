import streamlit as st

def description_card():
    """
    Exibe um card de descrição completo para o sistema, alinhado com a
    funcionalidade atual do MVP.
    """
    with st.expander("ℹ️ Como funciona o sistema? (Clique para expandir)", expanded=True):
        st.markdown("""
        Este sistema foi projetado para automatizar e padronizar a verificação de equivalência de disciplinas para a comissão. O fluxo atual é:
        
        - **1. Upload da Base de Dados:** O processo começa com o upload da planilha oficial `.xlsx` que contém todas as regras de equivalência já estabelecidas, com cada universidade em uma aba separada.
        
        - **2. Análise da Solicitação:** Em seguida, o membro da comissão seleciona a universidade de origem do aluno e insere os códigos das disciplinas que o aluno deseja verificar.
        
        - **3. Relatório Imediato:** O sistema compara os códigos inseridos com as regras da planilha e exibe um relatório instantâneo, classificando cada disciplina como "Equivalente", "Não Equivalente" ou "Não Encontrada".
        
        - **4. Geração de PDF:** Caso todas as disciplinas inseridas sejam encontradas na base de dados, um botão é habilitado para gerar e baixar um relatório em PDF com o resultado da análise.
        """)

    with st.expander("🎯 Próximos Passos: Evolução da Arquitetura"):
        st.markdown("""
        A arquitetura atual é **data-driven**, ou seja, toda a lógica de equivalência está na planilha e não no código, o que a torna flexível. O próximo passo é evoluir a fonte de dados:
        
        - **1. Centralizar a Planilha:** Substituir o upload manual de um arquivo `.xlsx` por uma conexão direta com uma planilha no **Google Sheets via API**.
        
        - **2. Colaboração em Tempo Real:** Permitir que múltiplos membros da comissão usem a ferramenta com a certeza de que estão sempre acessando a versão mais atualizada das regras de equivalência.
        
        - **3. Benefícios:** Essa evolução elimina a necessidade de gerenciar versões de arquivos, previne erros e transforma a ferramenta em uma plataforma colaborativa e centralizada, mantendo a arquitetura data-driven.
        """)

    with st.expander("🚀 Ideias de Melhorias Futuras"):
        st.markdown("""
        Com uma base de dados centralizada, podemos planejar novas funcionalidades para aprimorar a ferramenta:
        
        - **✍️ Interface de Edição:** Criar uma área no próprio sistema para que membros autorizados da comissão possam **adicionar ou editar regras de equivalência** diretamente, sem precisar abrir a planilha.
        
        - **📧 Notificações por E-mail:** Implementar o envio de um e-mail automático para o aluno ou secretaria com o relatório em PDF gerado pela análise.
        """)


def render_sidebar():
    """
    Renderiza a barra lateral com as seções de informação.
    """
    with st.sidebar:
        st.header("ℹ️ Sobre o Sistema")
        description_card()
        st.markdown("---")
        # --- Contato Atualizado ---
        st.info(
            "Esta ferramenta está em desenvolvimento. Para qualquer dúvida, entre em contato com um dos membros do Inova Process: ryanbl@dcc.ufrj.br.",
            icon="📧"
        )