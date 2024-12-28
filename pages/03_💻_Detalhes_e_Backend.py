import streamlit as st

# Título e Introdução
st.title("🔧 Visão Técnica do Dashboard de Vagas")
st.markdown("""
Esta página fornece insights sobre o backend do projeto para aqueles interessados nos aspectos técnicos do desenvolvimento.
""")

# Ferramentas e Tecnologias
st.header("Ferramentas e Tecnologias Utilizadas")
st.markdown("""
- **Python**: Linguagem principal para desenvolvimento do projeto.
- **Streamlit**: Para criar interfaces interativas e intuitivas.
- **Requests**: Utilizado para efetuar requisições HTTP e coletar dados web.
- **pandas**: Para manipulação e análise de dados.
- **Plotly**: Para visualização de dados interativos.
""")

# Explicações de Código
st.header("Explicações de Código e Métodos")
st.markdown("""
### Coleta de Dados
Utilizamos a biblioteca `requests` para acessar dados da API do Gupy de forma eficiente e segura.

### Processamento de Dados
`pandas` foi instrumental no tratamento e organização dos dados para análise.

### Visualização de Dados
Com `Plotly`, criamos gráficos interativos que tornam os insights facilmente compreensíveis.

""")

# Prints e Explicações
st.header("Componentes Visuais e Prints")
st.image("path_to_image.png", caption="Exemplo de Gráfico de Vagas por Data")
st.markdown("""
- **Gráficos de Linhas e Barras**: Indicam tendências temporais e distribuições por setor.
- **Palavras-Chave**: Identificação das habilidades mais requisitadas.
""")

# Conclusão
st.markdown("""
Espero que esta visão técnica ofereça uma compreensão mais profunda dos processos e tecnologias que sustentam o dashboard. Para dúvidas ou mais informações, sinta-se à vontade para entrar em contato.
""")