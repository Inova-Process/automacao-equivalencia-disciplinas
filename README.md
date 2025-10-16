# Analisador de Equivalência de Disciplinas

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?style=for-the-badge&logo=pandas)

## 🚀 Acesse a Ferramenta Online!

**Link da Aplicação:** **[Clique aqui para acessar o Analisador de Equivalências](https://URL_DA_SUA_APLICACAO_AQUI)**

## 🎯 Sobre o Projeto

Bem-vindo ao Analisador de Equivalência de Disciplinas!

Esta ferramenta automatiza o processo de verificação de equivalência de matérias para estudantes universitários. Ela foi projetada para analisar o Boletim de Orientação Acadêmica (BOA) de um aluno, comparar as disciplinas já cursadas com as regras de equivalência do curso e, em segundos, gerar uma lista de todas as matérias que podem ser cortadas (solicitadas para isenção).

O objetivo é transformar um processo que é manual, demorado e sujeito a erros em uma solução automatizada, rápida e precisa, ajudando alunos e comissões de curso a economizar tempo e esforço.

## ✨ Funcionalidades Principais

-   **Análise Instantânea:** Faça o upload do seu BOA em PDF e receba o resultado em poucos segundos.
-   **Precisão:** Utiliza a base de regras de equivalência mais recente para garantir que a análise seja precisa.
-   **Interface Simples:** Construído com Streamlit para uma experiência de usuário limpa, direta e sem complicações.
-   **Seguro e Privado:** O documento enviado é processado em memória e não é armazenado no servidor.

## ⚙️ Como Usar a Ferramenta Online

Usar o analisador é muito simples. Siga os três passos abaixo:

1.  **Acesse o Site:**
    -   Clique no link da aplicação: **[Analisador de Equivalências](https://URL_DA_SUA_APLICACAO_AQUI)**

2.  **Faça o Upload do seu BOA:**
    -   Na página, encontre o botão de upload (geralmente "Browse files" ou "Carregar arquivo").
    -   Selecione o seu Boletim de Orientação Acadêmica (BOA) em formato `.pdf` no seu computador.

3.  **Analise e Veja o Resultado:**
    -   Após o upload, clique no botão **"Analisar Equivalências"**.
    -   Aguarde um instante enquanto o sistema processa seu documento. A lista de disciplinas que você pode solicitar o corte aparecerá na tela!

É simples assim!

## 🛠️ Para Desenvolvedores (Como Funciona)

Para aqueles interessados na parte técnica, o sistema opera em duas fases:

1.  **Preparação (Backend):**
    -   Um arquivo `Equações_de_Equivalência_do_Currículo.csv` contendo as regras brutas é processado por um script Python.
    -   Este script otimiza e agrupa as regras, salvando o resultado em um arquivo `regras_agrupadas.json`, que serve como a "base de conhecimento" para a aplicação.

2.  **Análise (Aplicação Web):**
    -   Quando um usuário faz o upload de um PDF, a aplicação extrai as disciplinas aprovadas.
    -   O motor de análise carrega as regras do `regras_agrupadas.json`.
    -   As disciplinas do aluno são comparadas com cada regra. Se os pré-requisitos (`requires`) de uma regra são satisfeitos, as disciplinas concedidas (`grants`) são adicionadas ao resultado final.
