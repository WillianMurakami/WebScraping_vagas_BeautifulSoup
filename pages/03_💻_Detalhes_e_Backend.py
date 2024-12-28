import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuração da barra lateral
st.sidebar.markdown(
    """
    Projeto desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
    Para mais projetos, [clique aqui](https://share.streamlit.io/user/willianmurakami).
    """
)

# Título e Introdução
st.title("🔧 Visão Técnica do Dashboard de Vagas")
st.markdown("""
Esta página fornece insights sobre o backend do projeto, mostrando como tecnologias modernas foram utilizadas para criar um dashboard eficiente e interativo.
""")

# Ferramentas e Tecnologias
st.header("🏗 Ferramentas e Tecnologias Utilizadas")
st.markdown("""
- **🐍 Python**: A linguagem principal utilizada para desenvolver todo o projeto, conhecida por sua simplicidade e facilidade de uso.
- **🔄 Streamlit**: Framework que permite transformar scripts Python em aplicativos web interativos rapidamente, perfeito para visualizações de dados.
- **📡 Requests**: Utilizada para realizar requisições HTTP e coletar dados de APIs, essencial para obter informações atualizadas de fontes externas.
- **🗃 pandas**: Biblioteca chave para a manipulação e análise de dados, fornece estruturas de dados poderosas como DataFrames.
- **📊 Plotly**: Ferramenta para criar gráficos interativos de alta qualidade, permitindo a exploração aprofundada dos dados.
""")

# Explicações de Código e Métodos
st.header("📜 Explicações de Código e Métodos")

st.subheader("Coleta de Dados")
st.markdown("""
Para coletar os dados das vagas, utilizamos a biblioteca `requests`. Esta biblioteca permite que façamos requisições HTTP para obter informações diretamente da API do Gupy.
Exemplo de implementação:
            python
            """)


def fetch_job_data(api_url):
    # Faz uma requisição GET para a API
    response = requests.get(api_url)
    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        return response.json()  # Retorna os dados em formato JSON
    else:
        raise Exception("Falha ao acessar os dados da API")