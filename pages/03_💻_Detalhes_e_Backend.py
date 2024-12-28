import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuração da barra lateral
st.sidebar.markdown(
    """
    Projeto desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/).
    Para mais projetos, [clique aqui](https://share.streamlit.io/user/willianmurakami).
    """
)

# Título e Introdução
st.title("🔧 Visão Técnica do Dashboard de Vagas")
st.markdown("""
Bem-vindo à visão técnica desse projeto de Webscraping e análise visual das vagas! Nesta página, a ideia é explicar melhor sobre as ferramentas utilizadas, os métodos desenvolvidos e o fluxo de trabalho aplicado para tornar o projeto funcional e eficiente. 
Se você deseja entender como as diferentes partes do projeto se integram, está no lugar certo!
""")

# Ferramentas e Tecnologias
st.header("🏗 Ferramentas e Tecnologias Utilizadas")
st.markdown("""
O projeto faz uso de uma stack tecnológica moderna e robusta, que inclui:
- **🐍 Python**: Linguagem base devido à sua versatilidade e ecossistema rico em bibliotecas de análise e visualização de dados.
- **📡 Requests**: Biblioteca para realizar requisições HTTP, usada para consumir dados da API Gupy.
- **🗃 pandas**: Biblioteca essencial para manipulação e análise dos dados.
- **📊 Plotly**: Ferramenta de visualização interativa para gráficos de alta qualidade.
- **🔄 Streamlit**: Framework para criação de dashboards e aplicativos web interativos para o usuário final de forma ágil e intuitiva.
- **☁️ Streamlit Cloud**: Para deploy direto e compartilhamento da aplicação de forma online e colaborativa.
""")

# Fluxo Geral do Projeto
st.header("📋 Fluxo Geral do Projeto")
st.markdown("""
O fluxo de trabalho do projeto pode ser resumido em 3 etapas principais:

1. **Coleta de Dados**:
    - Os dados de vagas de emprego são raspados (coletados) a partir da API do portal Gupy usando a biblioteca `requests`.
    - São realizadas requisições paginadas para garantir que grandes volumes de dados sejam coletados.

2. **Processamento de Dados**:
    - Os dados brutos retornados pela API são processados com o `pandas` para limpeza, padronização e organização.
    - Métodos são aplicados para lidar com informações como datas, palavras-chave e cálculo de métricas.

3. **Visualização Interativa**:
    - Utilizamos `Streamlit` e `Plotly` para criar gráficos interativos que permitem ao usuário explorar as informações.
    - O dashboard facilita a análise de tendências, comparação de empresas e visualização de características chave.
""")

# Explicações de Código e Métodos
st.header("📜 Explicações de Código e Métodos")

st.subheader("1️⃣ Coleta de Dados")
st.code("""
def fetch_jobs_from_api(job_name, max_results=1000):
    jobs = []
    offset = 0
    limit = 10

    while len(jobs) < max_results:
        formatted_job_name = job_name.replace(' ', '%20')
        api_url = f"https://portal.api.gupy.io/api/v1/jobs?jobName={formatted_job_name}&offset={offset}&limit={limit}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            batch_jobs = data.get('data', [])
            
            if not batch_jobs:
                break

            jobs.extend(batch_jobs)
            offset += limit
        else:
            st.error(f"Erro ao acessar API: {response.status_code}")
            break

    return pd.DataFrame(jobs[:max_results])
""", language='python')
st.markdown("""
Esse método utiliza a biblioteca `requests` para realizar chamadas à API do Gupy e obter dados de vagas em lotes (paginados). Os principais pontos aqui são:
- **Parâmetros de controle**: `offset` e `limit` são usados para obter dados em pequenos blocos e evitar sobrecarga.
- **Tratamento de erros**: Verificamos o código de resposta da API (`status_code`) e paramos a execução caso algo dê errado.
- **Transformação em DataFrame**: No final, os dados são estruturados com o `pandas` para fácil manipulação.
""")

st.subheader("2️⃣ Processamento e Limpeza de Dados")
st.code("""
def process_job_data(df):
    df['Data de Publicação'] = pd.to_datetime(df['publishedDate'].str.split('T').str[0], errors='coerce')
    if 'applicationDeadline' in df.columns:
        df['Data de Candidatura'] = pd.to_datetime(df['applicationDeadline'].str.split('T').str[0], errors='coerce')
    if 'Data de Candidatura' in df.columns:
        df['Tempo de Fechamento'] = (df['Data de Candidatura'] - df['Data de Publicação']).dt.days

    return df.dropna(subset=['Data de Publicação'])
""", language='python')
st.markdown("""
Este método ilustra como os dados brutos retornados pela API são organizados e limpos:
- **Conversão de Datas**: Os campos de data são convertidos para o formato `datetime` para cálculos e filtragem.
- **Cálculo de Métricas**: Calculamos o tempo médio de fechamento de vagas subtraindo a data de publicação da data limite.
- **Remoção de Nulos**: Garantimos que apenas registros válidos sejam mantidos no DataFrame.
""")

st.subheader("3️⃣ Visualização de Dados")
st.code("""
fig_publicacao = px.line(publicacao_counts, x='Data', y='Número de Vagas', title='Vagas por Data de Publicação')
st.plotly_chart(fig_publicacao)
""", language='python')
st.markdown("""
Este é um exemplo de visualização criada com o Plotly para exibir o número de vagas publicadas por dia:
- **Gráfico de Linhas**: Escolhemos este formato para mostrar tendências ao longo do tempo.
- **Interatividade**: Com o Plotly, o gráfico permite zoom e visualização dinâmica dos dados.
""")

st.subheader("4️⃣ Extração de Palavras Relevantes")
st.code("""
def extract_relevant_terms(text, stopwords):
    words = text.lower().split()
    keywords = [word.strip(",.") for word in words if word not in stopwords and len(word) > 3]
    return Counter(keywords)
""", language='python')
st.markdown("""
Esta função analisa as descrições das vagas e extrai palavras-chave relevantes:
- **Remoção de Stopwords**: Stopwords comuns como "vaga", "empresa", "trabalho" são ignoradas.
- **Contagem de Frequência**: Usamos `collections.Counter` para contar a ocorrência de termos significativos.
""")

# Conclusão
st.header("📌 Conclusão")
st.markdown("""
O dashboard desenvolvido demonstra como unir Python, APIs e ferramentas de visualização pode simplificar a análise de dados complexos. 
Com abordagens modulares e bibliotecas poderosas como `pandas` e `Plotly`, é possível criar soluções interativas e eficazes para explorar informações em tempo real.
""")
