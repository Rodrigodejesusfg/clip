import streamlit as st
import pandas as pd
from datetime import datetime


# Configuração da página
st.set_page_config(page_title="Barbosa.Ai", page_icon=":newspaper:")
st.title("📰 Clip.Ai")

# Cor personalizada
COR_PERSONALIZADA = "#518CB7"

# Carregar DataFrame com as notícias
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Google_alerts2.xlsx")
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%Y-%m-%d') # Formatando data durante o carregamento
    return df

df = carregar_dados()

# Carregar dados da planilha 'analise_empresas'
@st.cache_data
def carregar_dados_empresas():
    df_empresas = pd.read_excel("analise_empresas.xlsx")
    return df_empresas

df_empresas = carregar_dados_empresas()

# Paleta de cores
COR_FUNDO = "#FFFFFF"  # Branco
COR_PRIMARIA = "#2C5794"
COR_SECUNDARIA = "#518CB7"
COR_TEXTO = "#3F3F3F"
COR_ACENTO = "#D1D1D1"

# Configurar cores do tema do Streamlit
st.markdown(f"""
<style>
    body {{
        background-color: {COR_FUNDO};
        color: {COR_TEXTO};
    }}
    .stApp {{
        background-color: {COR_FUNDO};
    }}
    .stTextInput > div > div > input {{
        background-color: {COR_ACENTO};
        color: {COR_TEXTO};
    }}
    /* ... outros estilos ... */
</style>
""", unsafe_allow_html=True)

# Interface do usuário
opcao_selecionada = st.sidebar.radio(
    "Escolha uma opção:",
    ("Comentar Notícias", "Resumir por Tema e Data", "Analisar Empresas", "📊 Estatísticas")
)

# Número de notícias por página
noticias_por_pagina = 8

# Filtro de busca
filtro_busca = st.text_input("Pesquisar notícias (por palavras-chave):")

# --- Seção para Comentar Notícias ---
if opcao_selecionada == "Comentar Notícias":
    # Filtrar notícias com base na busca
    if filtro_busca:
        df_filtrado = df[df['Título'].str.contains(filtro_busca, case=False) |
                         df['Conteúdo'].str.contains(filtro_busca, case=False)]
    else:
        df_filtrado = df

    # Paginação
    pagina = st.number_input("Página:", min_value=1, max_value=(len(df_filtrado) // noticias_por_pagina) + 1)
    inicio = (pagina - 1) * noticias_por_pagina
    fim = inicio + noticias_por_pagina

    # Exibir notícias da página atual
    for i in range(inicio, fim):
        if i < len(df_filtrado):
            noticia = df_filtrado.iloc[i]

            # Formatando data (já formatada durante o carregamento)
            data_noticia = noticia['Data']

            # Definindo a cor do sentimento
            cor_sentimento = {
                'Neutro': 'yellow',
                'Positivo': 'green',
                'Negativo': 'red'
            }.get(noticia['Sentimento'], 'gray')  # 'gray' para casos não encontrados

            # Exibindo a notícia
            st.markdown(
                f"""
                <div style='background-color: {COR_PERSONALIZADA}; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <div style='display: flex; align-items: center;'>
                        <p style='color: white; margin-right: 10px;'>{data_noticia}</p>
                        <p style='color: white; margin-right: 10px;'>Relevância: {noticia['Relevância']}</p>
                        <div style='background-color: {cor_sentimento}; width: 15px; height: 15px; border-radius: 50%; margin-right: 10px;'></div>
                    </div>
                    <div style='background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                        <h3 style='color: black;'>{i + 1}. {noticia['Título']}</h3>
                        <p style='color: black;'>{noticia['Conteúdo']}</p>
                        <p style='color: black;'><strong>Palavras-chave:</strong> {noticia['Palavras-chave']}</p>
                        <a href="{noticia['Link']}" target="_blank" style="color: black;">Abrir link da notícia</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- Seção para Resumir por Tema e Data ---
elif opcao_selecionada == "Resumir por Tema e Data":
    # Obter lista de clusters únicos
    clusters_unicos = df['cluster'].unique()

    # Selecionar cluster
    cluster_selecionado = st.selectbox("Selecione um Tema e Data para resumir:", clusters_unicos)

    # Filtrar notícias do cluster selecionado
    noticias_cluster = df[df["cluster"] == cluster_selecionado]

    # Paginação
    pagina = st.number_input("Página:", min_value=1,
                             max_value=(len(noticias_cluster) // noticias_por_pagina) + 1)
    inicio = (pagina - 1) * noticias_por_pagina
    fim = inicio + noticias_por_pagina

    # Exibir notícias da página atual
    for i in range(inicio, fim):
        if i < len(noticias_cluster):
            noticia = noticias_cluster.iloc[i]

            # Formatando data (já formatada durante o carregamento)
            data_noticia = noticia['Data']

            # Definindo a cor do sentimento
            cor_sentimento = {
                'Neutro': 'gray',
                'Positivo': 'green',
                'Negativo': 'red'
            }.get(noticia['Sentimento'], 'yellow')  # para casos não encontrados

            # Exibindo a notícia
            st.markdown(
                f"""
                <div style='background-color: {COR_PERSONALIZADA}; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <div style='display: flex; align-items: center;'>
                        <p style='color: white; margin-right: 10px;'>{data_noticia}</p>
                        <p style='color: white; margin-right: 10px;'>Relevância: {noticia['Relevância']}</p>
                        <div style='background-color: {cor_sentimento}; width: 15px; height: 15px; border-radius: 50%; margin-right: 10px;'></div>
                    </div>
                    <div style='background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                        <h3 style='color: black;'>{i + 1}. {noticia['Título']}</h3>
                        <p style='color: black;'>{noticia['Conteúdo']}</p>
                        <p style='color: black;'><strong>Palavras-chave:</strong> {noticia['Palavras-chave']}</p>
                        <a href="{noticia['Link']}" target="_blank" style="color: black;">Abrir link da notícia</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Instrução para o resumo do cluster
    instrucao_resumo = st.text_input("Instrução para o resumo do dia:")

    if st.button("Gerar Resumo do dia"):
        with st.spinner("Gerando resumo..."):
            textos_cluster = noticias_cluster['Conteúdo'].tolist()
            texto_resumo = " ".join(textos_cluster)
            resumo = gerar_comentário(texto_resumo, instrucao_resumo)
            st.success("**Resumo:**")
            st.write(resumo)

# --- Seção para Analisar Empresas ---
elif opcao_selecionada == "Analisar Empresas":
    st.subheader("Análise de Empresas e Projetos")

    # Lista suspensa para seleção da empresa
    todas_empresas = df_empresas['Empresa'].unique()
    empresa_selecionada = st.selectbox("Selecione uma empresa:", ["Todas"] + list(todas_empresas))

    if empresa_selecionada == "Todas":
        empresas_filtradas = df_empresas
        noticias_empresa = df  # Todas as notícias
    else:
        empresas_filtradas = df_empresas[df_empresas['Empresa'] == empresa_selecionada]
        noticias_empresa = df[df['Título'].str.contains(empresa_selecionada, case=False)]




    
    # Exibir informações das empresas selecionadas
    for i, empresa in empresas_filtradas.iterrows():
        if empresa_selecionada == "Todas":
            st.markdown(f"**Comentário sobre {empresa['Empresa']}:**")
            st.write(empresa['Comentário'])

            st.markdown(f"**Notícias sobre {empresa['Empresa']}:**")
            noticias_filtradas = noticias_empresa[noticias_empresa['Título'].str.contains(empresa['Empresa'], case=False)]
        else:
            st.markdown(f"**Comentário sobre {empresa_selecionada}:**")
            st.write(empresas_filtradas['Comentário'].iloc[0])

            st.markdown(f"**Notícias sobre {empresa_selecionada}:**")
            noticias_filtradas = noticias_empresa

        if not noticias_filtradas.empty:
            for _, noticia in noticias_filtradas.iterrows():
                st.markdown(
                    f"- **{noticia['Título']}**  ({noticia['Data']})\n   {noticia['Conteúdo']}\n   [Abrir link da notícia]({noticia['Link']})")
        else:
            st.write("Nenhuma notícia encontrada para a empresa selecionada.")

       

            
# In[ ]:

            
# In[ ]:





