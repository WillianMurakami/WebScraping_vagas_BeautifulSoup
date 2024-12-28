import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

# Stopwords customizadas
STOPWORDS = {"vaga", "trabalho", "empresa", "projeto", "experiência", "responsável", 
             "atividades", "requisitos", "realizar", "desejável", "mínimo", "área", 
             "anos", "nível", "pessoa", "profissional", "processo", "relacionados", 
             "informações", "outros", "possuir", "candidato", "atuar", "conhecimento"}

# Função para extrair palavras-chave relevantes
def extract_relevant_terms(text, stopwords):
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

    # Linha 1: Métricas e Controle de Tempo
    col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.2, 0.4])
    with col1:
        st.metric(label="Total de Vagas", value=total_vagas)
    with col2:
        st.metric(label="Dias Observados", value=total_dias)
    with col3:
        st.metric(label="Tempo Médio de Fechamento", value=f"{tempo_medio_fechamento:.2f} dias" if tempo_medio_fechamento else "N/A")
    with col4:
        if data_min and data_min != data_max:
            selected_date = st.slider("Controle de Tempo", min_value=data_min, max_value=data_max, value=(data_min, data_max))
        else:
            st.write(f"A única data disponível é {data_min}.")
            selected_date = (data_min, data_max)

    # Filtra os dados com base no controle de tempo
    selected_start = pd.to_datetime(selected_date[0])
    selected_end = pd.to_datetime(selected_date[1])
    df_filtered = df_vagas[(df_vagas['Data de Publicação'] >= selected_start) & (df_vagas['Data de Publicação'] <= selected_end)]

    # Gráfico de Linhas: Vagas por Data
    if not df_filtered['Data de Publicação'].isnull().all():
        publicacao_counts = df_filtered['Data de Publicação'].value_counts().sort_index().reset_index()
        publicacao_counts.columns = ['Data', 'Número de Vagas']
        fig_publicacao = px.line(publicacao_counts, x='Data', y='Número de Vagas', title='Vagas por Data de Publicação')
        st.plotly_chart(fig_publicacao)

    # Gráfico de Barras: Vagas por Empresas
    empresa_counts = df_filtered['careerPageName'].value_counts()
    demais_empresas = empresa_counts.iloc[15:].sum()  # Soma das empresas restantes
    top_empresas = pd.concat([empresa_counts.nlargest(15), pd.Series({"Demais": demais_empresas})])
    empresa_fig = px.bar(
        top_empresas.sort_values(ascending=False), y=top_empresas.index, x=top_empresas.values,
        orientation='h', title="Vagas por Empresas"
    )
    st.plotly_chart(empresa_fig)

    # Linha 3: Gráficos de Contratação e Localização
    col5, col6 = st.columns(2)

    # Gráfico de Pizza: Tipos de Contratação
    with col5:
        df_filtered['Modalidade Traduzida'] = df_filtered['type'].apply(lambda x: x.split('_')[-1]).map({
            'effective': 'Efetivo',
            'legal': 'Pessoa Jurídica',
            'temporary': 'Temporário'
        })
        modalidade_counts = df_filtered['Modalidade Traduzida'].value_counts()
        pie_fig = px.pie(modalidade_counts, values=modalidade_counts, names=modalidade_counts.index, title='Modalidade de Contratação')
        st.plotly_chart(pie_fig)

    # Gráfico de Sunburst: Estado e Cidade
    with col6:
        df_filtered['Estado'] = df_filtered.apply(
            lambda row: 'Remoto' if row.get('isRemoteWork') else row.get('state', 'Desconhecido'), axis=1
        )
        df_filtered['Cidade'] = df_filtered.apply(
            lambda row: 'Remoto' if row.get('isRemoteWork') else row.get('city', 'Desconhecida'), axis=1
        )
        sunburst_count = df_filtered.groupby(['Estado', 'Cidade']).size().reset_index(name='Número de Vagas')
        sunburst_fig = px.sunburst(sunburst_count, path=['Estado', 'Cidade'], values='Número de Vagas', 
                                   title="Distribuição de Vagas por Estado e Cidade")
        st.plotly_chart(sunburst_fig)

    # Treemap de Palavras Relevantes
    if 'description' in df_filtered.columns:
        all_descriptions = " ".join(df_filtered['description'].dropna())
        terms = extract_relevant_terms(all_descriptions, STOPWORDS)
        top_terms = dict(terms.most_common(75))
        treemap_data = pd.DataFrame(top_terms.items(), columns=['Característica', 'Frequência'])
        fig_treemap = px.treemap(
            treemap_data, path=['Característica'], values='Frequência',
            title="Principais Características Requeridas"
        )
        st.plotly_chart(fig_treemap)
