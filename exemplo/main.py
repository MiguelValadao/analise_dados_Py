import streamlit as st
import pandas as pd 
import plotly.express as px

# Configuração de página
st.set_page_config(page_title="Cuidados", layout="wide", page_icon="👀")

@st.cache_data
def carregar_dados(caminho_arquivo):
    xls = pd.ExcelFile(caminho_arquivo)
    
    abas_anos = [sheet for sheet in xls.sheet_names if "(CV)" not in sheet]

    dados_totais = []
    
    for ano in abas_anos: 
        df_raw = pd.read_excel(xls, sheet_name=ano)
        
        # Localizar onde começam os dados de localização (Brasil, Regiões, UFs)
        col_0_clean = df_raw.iloc[:, 0].astype(str).str.strip()
        matches = df_raw[col_0_clean == "Brasil"].index
        
        if matches.empty:
            continue
            
        start_idx = matches[0]
        
        # Selecionar as colunas relevantes: Localidade, Total, Homem, Mulher
        df_ano = df_raw.iloc[start_idx:, [0, 1, 2, 3]].copy()
        df_ano.columns = ["Localidade", "Total", "Homem", "Mulher"]

        df_ano = df_ano.dropna(subset=["Localidade"])
        df_ano["Localidade"] = df_ano["Localidade"].astype(str).str.strip()
        df_ano = df_ano[df_ano["Localidade"] != ""]

        # Criar a coluna identificadora do Ano
        df_ano["Ano"] = str(ano).strip()

        # Converter colunas numéricas
        for col in ["Total", "Homem", "Mulher"]:
            df_ano[col] = pd.to_numeric(df_ano[col], errors="coerce")

        dados_totais.append(df_ano)

    # Consolida os dados de todos os anos após percorrer todas as abas
    if dados_totais:
        df_completo = pd.concat(dados_totais, ignore_index=True)
        return df_completo
    else:
        return pd.DataFrame(columns=["Localidade", "Total", "Homem", "Mulher", "Ano"])

# Carregar arquivo
caminho_arquivo = r"H:\Python\Terceira Etapa\Jupyter\exemplo\Tabela 1.1.2.xls"

try: 
    df = carregar_dados(caminho_arquivo)

    # --- Sidebar --- #
    st.sidebar.header("🔍 Filtros")
    
    # Seleção de Ano
    anos_disponiveis = sorted(df["Ano"].unique(), reverse=True)
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano: ", anos_disponiveis)

    # Seleção de Localidades
    localidades_disponiveis = df["Localidade"].unique().tolist()
    
    # Filtrar os padrões para garantir que existam no DataFrame lido
    padrao_localidades = [loc for loc in ["Brasil", "Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"] if loc in localidades_disponiveis]
    if not padrao_localidades:
        padrao_localidades = localidades_disponiveis[:5]

    localidades_selecionadas = st.sidebar.multiselect(
        "Selecione as Regiões/UFs: ",
        options=localidades_disponiveis,
        default=padrao_localidades
    )
    
    # --- Body --- #
    st.title("Horas Dedicadas a Cuidados e Afazeres Domésticos")
    st.markdown("Análise da média de horas semanais dedicadas por pessoas ocupadas de 14 anos ou mais, por sexo")

    # Filtrar DataFrame com base nas seleções 
    df_filtrado = df[(df["Ano"] == ano_selecionado) & (df["Localidade"].isin(localidades_selecionadas))]

    if not df_filtrado.empty:
        # Visualização em Tabela
        st.subheader(f"Dados em Tabela ({ano_selecionado})")
        st.dataframe(df_filtrado[["Localidade", "Total", "Homem", "Mulher"]].reset_index(drop=True), use_container_width=True)

        st.markdown("---")
        st.subheader("Gráficos Comparativos")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Barras: Comparativo Homem x Mulher
            df_melted = df_filtrado.melt(
                id_vars=["Localidade"],
                value_vars=["Homem", "Mulher"],
                var_name="Gênero",
                value_name="Horas Semanais"
            )
            
            fig_bar = px.bar(
                df_melted,
                x="Localidade",
                y="Horas Semanais",
                color="Gênero",
                barmode="group",
                title=f"Média de Horas por Gênero ({ano_selecionado})",
                color_discrete_sequence=['#1f77b4', '#e377c2'],
                labels={"Horas Semanais": "Horas/Semana", "Localidade": "Região/UF"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Gráfico de Evolução Temporal (para as localidades selecionadas)
            df_historico = df[df["Localidade"].isin(localidades_selecionadas)]

            fig_line = px.line(
                df_historico,
                x="Ano",
                y="Total",
                color="Localidade",
                markers=True,
                title="Evolução Temporal do Total de Horas Dedicadas",
                labels={"Total": "Horas/Semana", "Ano": "Ano"}
            )
            st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Nenhuma localidade selecionada nos filtros da barra lateral.")

except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.info("Certifique-se de que o arquivo 'Tabela 1.1.2.xls' está no diretório correto.")