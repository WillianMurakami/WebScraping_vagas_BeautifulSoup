import requests
import pandas as pd
import streamlit as st

def fetch_jobs_from_api(job_name, max_results=1000):
    """Função para buscar vagas de emprego a partir da API, com base no nome da vaga e limite de resultados."""
    jobs = []  # Lista para armazenar todas as vagas
    offset = 0
    limit = 10  # Limite de vagas por requisição, para otimizar a busca

    while len(jobs) < max_results:
        formatted_job_name = job_name.replace(' ', '%20')
        api_url = f"https://portal.api.gupy.io/api/v1/jobs?jobName={formatted_job_name}&offset={offset}&limit={limit}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            batch_jobs = data.get('data', [])
            
            if not batch_jobs:
                break  # Se não há mais vagas, interrompe o loop

            jobs.extend(batch_jobs)
            offset += limit  # Incrementa o offset para a próxima requisição
        else:
            st.error(f"Erro ao acessar API: {response.status_code}")
            break

    return pd.DataFrame(jobs[:max_results])  # Retorna um DataFrame com as vagas

# Configuração do Streamlit
st.set_page_config(page_title="Busca de Vagas", layout="wide")

# Cabeçalho e introdução ao dashboard
st.title("📊 Dashboard de Vagas de Emprego")
st.markdown("""
    Esse projeto visa auxilar na pesquisa de vagas utilziando o portal Gupy e posterior análise dessas vagas, use essa página para pesquisar e extração dos dados do poral (utilizando webscraping) a vaga de interesse (*também é possível visualizar os resultados e fazer download da tabela em formato CSV*). 
    Utilize a barra lateral para acessar os resultados e ver mais detalhes.
""")

# Configuração do estado da sessão para armazenar dados de vagas
if 'job_data' not in st.session_state:
    st.session_state.job_data = pd.DataFrame()

# Inputs para busca de vagas
col1, col2 = st.columns([0.7, 0.3])  # Coloca as inputs na mesma linha

with col1:
    job_name = st.text_input("Digite o nome da vaga:", value="")

with col2:
    max_results = st.number_input("Número máximo de vagas a buscar:", min_value=1, max_value=1000, value=100)

# Botão para iniciar a busca de vagas
if st.button("Buscar Vagas"):
    with st.spinner("Buscando vagas..."):
        st.session_state.job_data = fetch_jobs_from_api(job_name, max_results)

# Exibição dos resultados da busca
if not st.session_state.job_data.empty:
    st.success(f"Foram encontradas {len(st.session_state.job_data)} vagas!")
    st.dataframe(st.session_state.job_data.style.set_properties(**{'white-space': 'nowrap', 'overflow-x': 'auto'}))
else:
    st.warning("Faça a busca das vagas pela barra de pesquisa.")

# Configuração da barra lateral
st.sidebar.markdown(
    """
    Projeto desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
    Para mais projetos, [clique aqui](https://share.streamlit.io/user/willianmurakami).
    """
)