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
Bem-vindo à visão técnica do nosso Dashboard de Vagas. Aqui, exploramos as tecnologias que tornam este projeto possível, bem como o fluxo de trabalho implementado para coletar, processar e visualizar dados de maneira eficiente.
""")

# Ferramentas e Tecnologias
st.header("🏗 Ferramentas e Tecnologias Utilizadas")
st.markdown("""
- **🐍 Python**: A linguagem de programação base para nosso projeto, escolhida por sua versatilidade e rica gama de bibliotecas para ciência de dados.
- **🔄 Streamlit**: Utilizado para construir nossa interface de usuário interativa. Streamlit converte scripts Python em aplicativos web de forma simples e rápida, ideal para prototipagem e deploy de dashboards.
- **☁️ Streamlit Cloud**: Permite a implantação de nosso aplicativo Streamlit diretamente a partir do repositório GitHub, facilitando o compartilhamento e a colaboração online.
- **📡 Requests**: Biblioteca crucial para realizar requisições HTTP, permitindo-nos buscar dados em tempo real das APIs, como a do Gupy.
- **🗃 pandas**: A espinha dorsal do processamento de dados, pandas oferece estruturas de dados de alto desempenho e ferramentas analíticas robustas.
- **📊 Plotly**: Usado para criar gráficos interativos de alta qualidade, Plotly fornece uma experiência de visualização rica e envolvente para o usuário.
""")

# Explicações de Código e Métodos
st.header("📜 Explicações de Código e Métodos")

st.subheader("Coleta de Dados")
st.code("""
def fetch_job_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Falha ao acessar os dados da API")
""", language='python')
st.markdown("""
Este trecho de código ilustra como usamos a biblioteca `requests` para realizar chamadas HTTP e obter dados em tempo real de uma API. Verificamos a resposta para assegurar que os dados foram recebidos com sucesso antes de prosseguir com o processamento.
""")

st.subheader("Processamento de Dados")
st.code("""
def clean_data(json_data):
    df = pd.DataFrame(json_data)
    df['date'] = pd.to_datetime(df['date'])
    return df.dropna()
""", language='python')
st.markdown("""
Aqui, utilizamos `pandas` para converter os dados JSON em um DataFrame, que é uma estrutura de dados tabular. Convertimos strings de datas para objetos datetime e removemos entradas ausentes, preparando os dados para análise.
""")

st.subheader("Visualização de Dados")
st.code("""
def plot_vacancies_over_time(df):
    fig = px.line(df, x='date', y='vacancies', title='Número de Vagas ao Longo do Tempo')
    st.plotly_chart(fig)
""", language='python')
st.markdown("""
Este código mostra como criamos um gráfico de linhas usando `Plotly` para visualizar como o número de vagas varia ao longo do tempo. O gráfico é renderizado no Streamlit, permitindo que os usuários interajam com os dados de maneira dinâmica.
""")

# Telas complementares
st.header("📸 De modo visual:")

st.subheader("### Interface do Usuário")
st.image("link_para_imagem_da_interface.png", caption="Exemplo de como o layout do aplicativo aparece para o usuário.")
st.markdown("""
Esta imagem mostra o layout geral da interface do usuário, destacando como o Streamlit facilita a navegação e o uso interativo do dashboard.
""")

st.subheader("### Exemplo de Gráfico de Linhas")
st.image("link_para_imagem_do_grafico_de_linhas.png", caption="Gráfico ilustrando o número de vagas ao longo do tempo.")
st.markdown("""
Este print ilustra um gráfico de linhas interativo criado com Plotly, visualizando tendências de vagas ao longo do tempo. Ele permite que os usuários explorem os dados dinamicamente.
""")

st.subheader("### Código em Ação")
st.image("link_para_imagem_do_codigo.png", caption="Captura de tela do código em execução.")
st.markdown("""
Aqui está uma captura de tela do código Python em execução, mostrando a integração das bibliotecas e como elas são usadas para processar dados e gerar insights valiosos.
""")

st.markdown("Esperamos que esta visão técnica ofereça uma compreensão mais profunda dos processos e tecnologias que sustentam o dashboard. Para dúvidas ou mais informações, sinta-se à vontade para entrar em contato.")