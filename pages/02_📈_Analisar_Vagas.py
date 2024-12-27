import streamlit as st
import pandas as pd
import spacy
from collections import Counter
import plotly.express as px
from datetime import datetime
import numpy as np

# Carregar o modelo de idioma português do spaCy
nlp = spacy.load("pt_core_news_sm")

# Stopwords específicas para cada categoria
COMMON_STOPWORDS = {
    "domínio", "experiência", "conhecimento", "sólido", "avançado", "familiaridade", "técnico", "desejável",
    "analítico", "proficiente", "proficiência", "detalhado", "essencial", "importante", "capacidade", "nível",
    "habilidade", "excelente", "fundamental", "competência", "área", "áreas", "vida", "saúde", "trabalho", "empresa",
    "vale", "completo", "superior", "ambiente", "colaboradores", "colaborador", "atividades", "anos", "dia", "garantindo",
    "será", "notas", "auxílio", "refeição", "busca", "vaga", "alimentação", "gente", "creche", "benefícios", "trabalhar",
    "dias", "visando", "uso", "utilização", "solução", "implementação", "integração", "desenvolvimento", "serviço",
    "sistema", "tecnologia", "plataforma", "software", "aplicativo", "programa", "cresol", "time", "ciências", "estamos", "garantir", "garantindo",
    "profissional", "ações", "ação", "oportunidades", "oportunidade", "responsável",
}

def normalize_terms(text, stopwords_set):
    """Normaliza os termos extraindo tokens sem stopwords."""
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop and token.text not in stopwords_set]
    return Counter(tokens)

def categorize_terms(df):
    """Extrai hard skills, soft skills e ferramentas dos anúncios de vagas."""
    hard_skills = Counter()
    soft_skills = Counter()
    tools = Counter()

    if 'description' in df.columns:
        description_text = " ".join(df['description'].dropna())
    else:
        description_text = ""

    # Processamento distinto para cada categoria
    hard_skills.update(normalize_terms(description_text, COMMON_STOPWORDS))
    soft_skills.update(normalize_terms(description_text, COMMON_STOPWORDS))
    tools.update(normalize_terms(description_text, COMMON_STOPWORDS))

    # Limitar a exibição a 45 palavras mais frequentes
    hard_skills = dict(hard_skills.most_common(45))
    soft_skills = dict(soft_skills.most_common(45))
    tools = dict(tools.most_common(45))

    return hard_skills, soft_skills, tools

def calculate_days_between(dates1, dates2):
    """Calcula o número de dias entre duas listas de datas, preservando o comprimento original."""
    days = [(d2 - d1).days if pd.notnull(d1) and pd.notnull(d2) else np.nan for d1, d2 in zip(dates1, dates2)]
    return days

# Verificar se os dados do scraping estão presentes
if 'job_data' not in st.session_state or st.session_state.job_data.empty:
    st.warning("Nenhum dado de vaga encontrado. Por favor, faça a busca de vagas antes de acessar a análise.")
else:
    df_vagas = st.session_state.job_data

    # Ajustar os dados de data
    df_vagas['Data de Publicação'] = pd.to_datetime(df_vagas['publishedDate'].str.split('T').str[0], errors='coerce')
    if 'applicationDeadline' in df_vagas.columns:
        df_vagas['Data de Candidatura'] = pd.to_datetime(df_vagas['applicationDeadline'].str.split('T').str[0], errors='coerce')

    st.title("Análise de Vagas 📈")
    st.markdown("""Aqui temos as principais informações das vagas. 
Neste painel você encontrará informações para facilitar sua análise e compreensão sobre a área pesquisada!""")

    # Linha 1: Cartões de Métricas com nova ordem e proporção
    col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.2, 0.4])

    with col1:
        total_vagas = len(df_vagas)
        st.metric(label="Total de Vagas", value=total_vagas)

    with col2:
        data_min = df_vagas['Data de Publicação'].min().date() if not df_vagas['Data de Publicação'].isnull().all() else None
        data_max = df_vagas['Data de Publicação'].max().date() if not df_vagas['Data de Publicação'].isnull().all() else None
        total_dias = (data_max - data_min).days if data_max and data_min else 1
        st.metric(label="Total de Dias Observados", value=total_dias)

    with col3:
        # Tempo médio de fechamento das vagas
        if 'Data de Candidatura' in df_vagas.columns:
            df_vagas['Tempo Fechamento'] = calculate_days_between(
                df_vagas['Data de Publicação'], df_vagas['Data de Candidatura']
            )
            tempo_medio_fechamento = df_vagas['Tempo Fechamento'].mean() if not df_vagas['Tempo Fechamento'].empty else 0
            st.metric(label="Tempo Médio de Fechamento", value=f"{tempo_medio_fechamento:.2f} dias")

    with col4:
        if data_min and data_min != data_max:
            selected_date = st.slider("Controle de Tempo", min_value=data_min, max_value=data_max, value=(data_min, data_max))
        else:
            st.write(f"A única data disponível é {data_min}.")
            selected_date = (data_min, data_max)

    # Converter datas selecionadas para datetime64[ns] para compatibilidade com pandas
    selected_start = pd.to_datetime(selected_date[0])
    selected_end = pd.to_datetime(selected_date[1])

    df_filtered = df_vagas[(df_vagas['Data de Publicação'] >= selected_start) & (df_vagas['Data de Publicação'] <= selected_end)]

    # Gráfico de Linhas - Vagas por Data
    if not df_filtered['Data de Publicação'].isnull().all():
        publicacao_counts = df_filtered['Data de Publicação'].value_counts().sort_index().reset_index()
        publicacao_counts.columns = ['Data', 'Número de Vagas']
        fig_publicacao = px.line(publicacao_counts, x='Data', y='Número de Vagas', labels={'Data': 'Data', 'Número de Vagas': 'Número de Vagas'}, title='Vagas por Data de Publicação')
        st.plotly_chart(fig_publicacao)

    # Linha 2: Gráficos de Modalidade de Contratação e Sunburst
    col5, col6 = st.columns([0.5, 0.5])

    with col5:
        if 'type' in df_filtered.columns:
            df_filtered['Modalidade Traduzida'] = df_filtered['type'].apply(lambda x: x.split('_')[-1]).map({
                'effective': 'Efetivo',
                'legal': 'Pessoa Jurídica',
                'temporary': 'Temporário'
            })
            modalidade_counts = df_filtered['Modalidade Traduzida'].value_counts()
            pie_fig = px.pie(modalidade_counts, values=modalidade_counts, names=modalidade_counts.index, title='Modalidade de Contratação')
            st.plotly_chart(pie_fig)

    with col6:
        sunburst_data = df_filtered.copy()
        sunburst_data['Estado'] = sunburst_data.apply(lambda row: 'Remoto' if row['isRemoteWork'] else row['state'], axis=1)
        sunburst_data['Cidade'] = sunburst_data.apply(lambda row: 'Remoto' if row['isRemoteWork'] else row['city'], axis=1)
        
        # Conte o número de vagas por Estado e Cidade
        sunburst_count = sunburst_data.groupby(['Estado', 'Cidade']).size().reset_index(name='Número de Vagas')

        sunburst_fig = px.sunburst(
            sunburst_count,
            path=['Estado', 'Cidade'],
            values='Número de Vagas',
            title="Distribuição de Vagas por Estado e Cidade"
        )
        st.plotly_chart(sunburst_fig)

    # Linha 3: Gráfico de Vagas por Empresa
    empresa_counts = df_filtered['careerPageName'].value_counts().nlargest(15)
    demais_empresas = df_filtered['careerPageName'].value_counts().iloc[15:].sum()
    top_empresas = pd.concat([empresa_counts, pd.Series({'Demais': demais_empresas})])

    empresa_fig = px.bar(top_empresas.sort_values(ascending=False), y=top_empresas.index, x=top_empresas.values, orientation='h', 
                         title='Top 15 Empresas por Número de Vagas')
    empresa_fig.update_layout(yaxis_title='Empresas', xaxis_title='Número de Vagas', 
                              plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(showgrid=True), xaxis=dict(showgrid=True))
    st.plotly_chart(empresa_fig)

    # Modalidade do Trabalho como Gráfico de Pizza
    if 'Modalidade de Trabalho' in df_filtered.columns:
        work_type_counts = df_filtered['Modalidade de Trabalho'].value_counts()
        pie_fig = px.pie(work_type_counts, values=work_type_counts, names=work_type_counts.index, title='Modalidade de Trabalho')
        st.plotly_chart(pie_fig)

    # Análise de Texto: Extração e Visualização de Habilidades e Ferramentas
    st.header("Análise de Habilidades e Ferramentas")
    st.markdown("""
    A análise feita pela IA, utilizando a biblioteca spaCy, aponta que as principais características necessárias para essas vagas são:
    \n\n*(Esse gráfico pode levar mais tempo para ser gerado devido à análise detalhada realizada pela IA.)*
    """)

    hard_skills, soft_skills, tools = categorize_terms(df_filtered)

    # Treemap para Ferramentas e Habilidades
    combined_skills_tools = Counter(hard_skills) + Counter(soft_skills) + Counter(tools)
    if combined_skills_tools:
        treemap_data = pd.DataFrame(combined_skills_tools.items(), columns=['Característica', 'Frequência'])
        treemap_data = treemap_data.sort_values(by='Frequência', ascending=False).head(45)
        fig_treemap = px.treemap(treemap_data, path=['Característica'], values='Frequência', title="Principais Características Requeridas")
        fig_treemap.update_traces(tiling=dict(pad=1))
        st.plotly_chart(fig_treemap)

# Configuração da barra lateral
st.sidebar.markdown(
    """
    Projeto desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
    Para mais projetos, [clique aqui](https://github.com/WillianMurakami).
    """
)