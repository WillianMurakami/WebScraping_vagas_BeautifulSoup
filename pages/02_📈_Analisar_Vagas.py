import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

# Stopwords simples
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

    # Métricas gerais
    total_vagas = len(df_vagas)
    st.metric("Total de Vagas", total_vagas)

    # Gráfico: Vagas por Empresa
    top_empresas = df_vagas['careerPageName'].value_counts().head(10)
    fig_empresas = px.bar(top_empresas, x=top_empresas.values, y=top_empresas.index, orientation="h",
                          title="Top 10 Empresas por Número de Vagas")
    st.plotly_chart(fig_empresas)

    # Análise de palavras-chave (extração simples)
    if 'description' in df_vagas.columns:
        all_descriptions = " ".join(df_vagas['description'].dropna())
        terms = extract_terms(all_descriptions, STOPWORDS)

        # Exibir nuvem de palavras (ou lista)
        top_terms = dict(terms.most_common(20))
        fig_terms = px.bar(x=list(top_terms.keys()), y=list(top_terms.values()), title="Principais Termos nas Descrições")
        st.plotly_chart(fig_terms)
