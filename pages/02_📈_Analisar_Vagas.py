import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

# Stopwords básicas
STOPWORDS = {"vaga", "trabalho", "empresa", "projeto", "experiência", "responsável"}

def extract_terms(text, stopwords):
    """
    Extrai palavras-chave de um texto, removendo stopwords.
    """
    words = text.lower().split()
    keywords = [word.strip(",.") for word in words if word not in stopwords and len(word) > 3]
    return Counter(keywords)

# Verifica se há dados de vagas
if 'job_data' not in st.session_state or st.session_state.job_data.empty:
    st.warning("Nenhum dado encontrado. Retorne à página 1 e faça a busca de vagas.")
else:
    df_vagas = st.session_state.job_data

    st.title("📈 Análise de Vagas")

    # Ajusta os campos de data
    df_vagas['Data de Publicação'] = pd.to_datetime(df_vagas['publishedDate'].str.split('T').str[0], errors='coerce')
    if 'applicationDeadline' in df_vagas.columns:
        df_vagas['Data de Candidatura'] = pd.to_datetime(df_vagas['applicationDeadline'].str.split('T').str[0], errors='coerce')

    # Adiciona dias de fechamento, se possível
    if 'Data de Candidatura' in df_vagas.columns:
        df_vagas['Tempo de Fechamento'] = (df_vagas['Data de Candidatura'] - df_vagas['Data de Publicação']).dt.days

    # Calcula métricas gerais
    total_vagas = len(df_vagas)
    data_min = df_vagas['Data de Publicação'].min().date() if not df_vagas['Data de Publicação'].isnull().all() else None
    data_max = df_vagas['Data de Publicação'].max().date() if not df_vagas['Data de Publicação'].isnull().all() else None
    total_dias = (data_max - data_min).days if data_max and data_min and data_max != data_min else 1
    tempo_medio_fechamento = df_vagas['Tempo de Fechamento'].mean() if 'Tempo de Fechamento' in df_vagas.columns else None

    # Controle de slider para intervalo de datas
    if data_min and data_min != data_max:
        selected_date = st.slider("Controle de Tempo", min_value=data_min, max_value=data_max, value=(data_min, data_max))
    else:
        st.write(f"A única data disponível é {data_min}.")
        selected_date = (data_min, data_max)

    # Filtra os dados com base no controle de tempo
    selected_start = pd.to_datetime(selected_date[0])
    selected_end = pd.to_datetime(selected_date[1])
    df_filtered = df_vagas[(df_vagas['Data de Publicação'] >= selected_start) & (df_vagas['Data de Publicação'] <= selected_end)]

    # Linha 1: Cartões de Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Vagas", value=total_vagas)
    with col2:
        st.metric(label="Dias Observados", value=total_dias)
    with col3:
        st.metric(label="Tempo Médio de Fechamento", value=f"{tempo_medio_fechamento:.2f} dias" if tempo_medio_fechamento else "N/A")

    # Gráfico de Linhas: Vagas por Data
    if not df_filtered['Data de Publicação'].isnull().all():
        publicacao_counts = df_filtered['Data de Publicação'].value_counts().sort_index().reset_index()
        publicacao_counts.columns = ['Data', 'Número de Vagas']
        fig_publicacao = px.line(publicacao_counts, x='Data', y='Número de Vagas', title='Vagas por Data de Publicação')
        st.plotly_chart(fig_publicacao)

    # Gráfico de Barras: Vagas por Empresa
    empresa_counts = df_filtered['careerPageName'].value_counts().nlargest(15)
    empresa_fig = px.bar(
        empresa_counts.sort_values(ascending=False), y=empresa_counts.index, x=empresa_counts.values,
        orientation='h', title="Top 15 Empresas por Número de Vagas"
    )
    st.plotly_chart(empresa_fig)

    # Treemap das Palavras Mais Frequentes
    if 'description' in df_filtered.columns:
        all_descriptions = " ".join(df_filtered['description'].dropna())
        terms = extract_terms(all_descriptions, STOPWORDS)

        # Treemap das Palavras Mais Frequentes
        top_terms = dict(terms.most_common(75))
        treemap_data = pd.DataFrame(top_terms.items(), columns=['Característica', 'Frequência'])
        fig_treemap = px.treemap(
            treemap_data, path=['Característica'], values='Frequência',
            title="Principais Características Requeridas"
        )
        st.plotly_chart(fig_treemap)
