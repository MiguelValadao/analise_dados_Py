import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Executive Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
    /* Fundo geral */
    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #080d19;
        border-right: 1px solid #1f2937;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(145deg, #111827, #0f172a);
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 20px;
        min-height: 145px;
        box-shadow: 0 8px 30px rgba(0,0,0,.18);
    }

    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 31px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-change-up {
        color: #34d399;
        font-size: 13px;
        margin-top: 7px;
    }

    .metric-change-down {
        color: #fb7185;
        font-size: 13px;
        margin-top: 7px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 750;
        color: #f8fafc;
        margin: 20px 0 8px 0;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 14px;
    }

    .status-ok {
        background: rgba(16,185,129,.12);
        color: #34d399;
        border: 1px solid rgba(52,211,153,.2);
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .status-warning {
        background: rgba(245,158,11,.12);
        color: #fbbf24;
        border: 1px solid rgba(251,191,36,.2);
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .status-danger {
        background: rgba(244,63,94,.12);
        color: #fb7185;
        border: 1px solid rgba(251,113,133,.2);
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .info-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 16px;
    }

    .small-label {
        color: #64748b;
        font-size: 12px;
    }

    .big-number {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 750;
    }

    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 12px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    hr {
        border-color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS
# ============================================================

@st.cache_data
def generate_data():

    np.random.seed(42)

    dates = pd.date_range(
        end=datetime.today().date(),
        periods=180,
        freq="D"
    )

    regions = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    channels = ["Online", "Loja física", "Parceiros", "Marketplace"]
    categories = ["Tecnologia", "Casa", "Moda", "Esportes", "Beleza"]

    rows = []

    for date in dates:
        for region in regions:

            sales = np.random.randint(8000, 30000)
            orders = np.random.randint(40, 180)
            customers = np.random.randint(30, 140)
            returns = np.random.randint(1, max(2, int(orders * .08)))

            rows.append({
                "Data": date,
                "Região": region,
                "Canal": np.random.choice(channels),
                "Categoria": np.random.choice(categories),
                "Vendas": sales,
                "Pedidos": orders,
                "Clientes": customers,
                "Devoluções": returns,
                "Ticket": sales / max(orders, 1),
                "Margem": np.random.uniform(.18, .42),
            })

    return pd.DataFrame(rows)


df = generate_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📊 Executive")
    st.caption("Analytics Platform v2.4")

    st.divider()

    st.markdown("### Navegação")

    page = st.radio(
        "",
        [
            "📊 Overview",
            "💰 Financeiro",
            "👥 Clientes",
            "📦 Operações",
            "🎯 Performance"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Filtros")

    min_date = df["Data"].min().date()
    max_date = df["Data"].max().date()

    date_range = st.date_input(
        "Período",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date
    )

    selected_regions = st.multiselect(
        "Região",
        sorted(df["Região"].unique()),
        default=list(df["Região"].unique())
    )

    selected_channels = st.multiselect(
        "Canal",
        sorted(df["Canal"].unique()),
        default=list(df["Canal"].unique())
    )

    selected_categories = st.multiselect(
        "Categoria",
        sorted(df["Categoria"].unique()),
        default=list(df["Categoria"].unique())
    )

    st.divider()

    st.markdown("### Sistema")

    st.success("● Todos os serviços operacionais")

    st.caption(
        f"Última atualização: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

# ============================================================
# FILTROS
# ============================================================

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

filtered = df[
    (df["Data"].dt.date >= start_date) &
    (df["Data"].dt.date <= end_date) &
    (df["Região"].isin(selected_regions)) &
    (df["Canal"].isin(selected_channels)) &
    (df["Categoria"].isin(selected_categories))
].copy()

# ============================================================
# HEADER
# ============================================================

col_title, col_actions = st.columns([3, 1])

with col_title:

    st.markdown(
        "# Dashboard Executivo"
    )

    st.markdown(
        "Visão consolidada de vendas, clientes, operações e performance."
    )

with col_actions:

    st.write("")

    if st.button("🔄 Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.divider()

# ============================================================
# KPIs
# ============================================================

total_sales = filtered["Vendas"].sum()
total_orders = filtered["Pedidos"].sum()
total_customers = filtered["Clientes"].sum()
avg_ticket = total_sales / max(total_orders, 1)
margin = np.average(
    filtered["Margem"],
    weights=filtered["Vendas"]
) * 100

return_rate = (
    filtered["Devoluções"].sum() /
    max(total_orders, 1)
) * 100

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Receita</div>
        <div class="metric-value">R$ {total_sales/1e6:.2f}M</div>
        <div class="metric-change-up">▲ 14,8% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Pedidos</div>
        <div class="metric-value">{total_orders:,}</div>
        <div class="metric-change-up">▲ 8,2% crescimento</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Clientes</div>
        <div class="metric-value">{total_customers:,}</div>
        <div class="metric-change-up">▲ 11,4% ativos</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Ticket médio</div>
        <div class="metric-value">R$ {avg_ticket:,.0f}</div>
        <div class="metric-change-up">▲ 5,7% evolução</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Margem</div>
        <div class="metric-value">{margin:.1f}%</div>
        <div class="metric-change-up">▲ 2,1 p.p.</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GRÁFICO PRINCIPAL
# ============================================================

st.markdown('<div class="section-title">Evolução de receita</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="section-subtitle">Performance diária no período selecionado</div>',
    unsafe_allow_html=True
)

daily = (
    filtered
    .groupby("Data", as_index=False)
    .agg({
        "Vendas": "sum",
        "Pedidos": "sum"
    })
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=daily["Data"],
        y=daily["Vendas"],
        mode="lines",
        name="Receita",
        line=dict(
            color="#6366f1",
            width=3
        ),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,.08)"
    )
)

fig.update_layout(
    height=350,
    margin=dict(l=0, r=0, t=10, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    hovermode="x unified",
    xaxis=dict(
        showgrid=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#1f2937",
        tickprefix="R$ "
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# ============================================================
# SEGUNDA LINHA
# ============================================================

col1, col2 = st.columns([1.4, 1])

# ------------------------------------------------------------
# REGIÕES
# ------------------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-title">Performance por região</div>',
        unsafe_allow_html=True
    )

    region_data = (
        filtered
        .groupby("Região", as_index=False)
        .agg({
            "Vendas": "sum",
            "Pedidos": "sum",
            "Clientes": "sum"
        })
        .sort_values("Vendas", ascending=False)
    )

    fig_region = px.bar(
        region_data,
        x="Vendas",
        y="Região",
        orientation="h",
        color="Vendas",
        color_continuous_scale=[
            "#312e81",
            "#4f46e5",
            "#818cf8"
        ],
        text_auto=".2s"
    )

    fig_region.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickprefix="R$ "
        ),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ------------------------------------------------------------
# CANAIS
# ------------------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-title">Distribuição por canal</div>',
        unsafe_allow_html=True
    )

    channel_data = (
        filtered
        .groupby("Canal", as_index=False)["Vendas"]
        .sum()
    )

    fig_channel = px.pie(
        channel_data,
        values="Vendas",
        names="Canal",
        hole=.65,
        color_discrete_sequence=[
            "#6366f1",
            "#22c55e",
            "#f59e0b",
            "#ec4899"
        ]
    )

    fig_channel.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        legend=dict(
            orientation="h",
            y=-0.05
        )
    )

    st.plotly_chart(
        fig_channel,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ============================================================
# TERCEIRA LINHA
# ============================================================

col3, col4 = st.columns(2)

# ------------------------------------------------------------
# CATEGORIAS
# ------------------------------------------------------------

with col3:

    st.markdown(
        '<div class="section-title">Categorias</div>',
        unsafe_allow_html=True
    )

    category_data = (
        filtered
        .groupby("Categoria", as_index=False)
        .agg({
            "Vendas": "sum",
            "Pedidos": "sum",
            "Margem": "mean"
        })
        .sort_values("Vendas", ascending=False)
    )

    fig_category = px.bar(
        category_data,
        x="Categoria",
        y="Vendas",
        color="Margem",
        color_continuous_scale="Viridis"
    )

    fig_category.update_layout(
        height=330,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1f2937",
            tickprefix="R$ "
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ------------------------------------------------------------
# MARGEM
# ------------------------------------------------------------

with col4:

    st.markdown(
        '<div class="section-title">Receita × Margem</div>',
        unsafe_allow_html=True
    )

    scatter_data = (
        filtered
        .groupby(["Categoria", "Região"], as_index=False)
        .agg({
            "Vendas": "sum",
            "Margem": "mean",
            "Pedidos": "sum"
        })
    )

    fig_scatter = px.scatter(
        scatter_data,
        x="Vendas",
        y="Margem",
        size="Pedidos",
        color="Categoria",
        hover_name="Região",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig_scatter.update_layout(
        height=330,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#1f2937"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1f2937",
            tickformat=".0%"
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ============================================================
# ALERTAS
# ============================================================

st.markdown(
    '<div class="section-title">Alertas operacionais</div>',
    unsafe_allow_html=True
)

alert1, alert2, alert3 = st.columns(3)

with alert1:
    st.markdown("""
    <div class="info-box">
        <span class="status-warning">ATENÇÃO</span>
        <br><br>
        <strong>Taxa de devolução elevada</strong>
        <br>
        <span class="small-label">
        A taxa atual está acima da meta estabelecida.
        </span>
    </div>
    """, unsafe_allow_html=True)

with alert2:
    st.markdown("""
    <div class="info-box">
        <span class="status-ok">NORMAL</span>
        <br><br>
        <strong>Processamento de pedidos</strong>
        <br>
        <span class="small-label">
        Operação funcionando dentro do SLA.
        </span>
    </div>
    """, unsafe_allow_html=True)

with alert3:
    st.markdown("""
    <div class="info-box">
        <span class="status-danger">CRÍTICO</span>
        <br><br>
        <strong>Estoque de produtos</strong>
        <br>
        <span class="small-label">
        8 produtos estão próximos do estoque mínimo.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RANKING
# ============================================================

st.markdown(
    '<div class="section-title">Ranking de performance</div>',
    unsafe_allow_html=True
)

ranking = (
    filtered
    .groupby(["Região", "Canal"], as_index=False)
    .agg(
        Receita=("Vendas", "sum"),
        Pedidos=("Pedidos", "sum"),
        Clientes=("Clientes", "sum"),
        Margem=("Margem", "mean")
    )
)

ranking["Ticket médio"] = (
    ranking["Receita"] /
    ranking["Pedidos"].replace(0, 1)
)

ranking = ranking.sort_values(
    "Receita",
    ascending=False
).reset_index(drop=True)

ranking.insert(
    0,
    "Posição",
    ranking.index + 1
)

ranking["Receita"] = ranking["Receita"].map(
    lambda x: f"R$ {x:,.0f}"
)

ranking["Margem"] = ranking["Margem"].map(
    lambda x: f"{x*100:.1f}%"
)

ranking["Ticket médio"] = ranking["Ticket médio"].map(
    lambda x: f"R$ {x:,.0f}"
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Posição": st.column_config.NumberColumn(
            "🏆",
            width="small"
        ),
        "Receita": st.column_config.TextColumn(
            "Receita"
        ),
        "Pedidos": st.column_config.NumberColumn(
            "Pedidos",
            format="%d"
        ),
        "Clientes": st.column_config.NumberColumn(
            "Clientes",
            format="%d"
        ),
    }
)

# ============================================================
# DETALHES
# ============================================================

st.markdown(
    '<div class="section-title">Análise detalhada</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs([
    "📈 Tendência",
    "🧮 Indicadores",
    "📋 Dados brutos"
])

with tab1:

    trend = (
        filtered
        .groupby("Data", as_index=False)
        .agg(
            Receita=("Vendas", "sum"),
            Pedidos=("Pedidos", "sum"),
            Clientes=("Clientes", "sum")
        )
    )

    trend["Média móvel"] = (
        trend["Receita"]
        .rolling(7)
        .mean()
    )

    fig_trend = go.Figure()

    fig_trend.add_trace(
        go.Scatter(
            x=trend["Data"],
            y=trend["Receita"],
            name="Receita",
            line=dict(
                color="#6366f1",
                width=2
            )
        )
    )

    fig_trend.add_trace(
        go.Scatter(
            x=trend["Data"],
            y=trend["Média móvel"],
            name="Média móvel 7 dias",
            line=dict(
                color="#22c55e",
                width=3,
                dash="dot"
            )
        )
    )

    fig_trend.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1f2937",
            tickprefix="R$ "
        )
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

with tab2:

    i1, i2, i3, i4 = st.columns(4)

    with i1:
        st.metric(
            "Receita diária",
            f"R$ {filtered['Vendas'].mean():,.0f}"
        )

    with i2:
        st.metric(
            "Pedidos/dia",
            f"{filtered['Pedidos'].mean():,.0f}"
        )

    with i3:
        st.metric(
            "Margem média",
            f"{filtered['Margem'].mean()*100:.1f}%"
        )

    with i4:
        st.metric(
            "Devoluções",
            f"{return_rate:.2f}%"
        )

    st.divider()

    metric_data = pd.DataFrame({
        "Indicador": [
            "Receita total",
            "Pedidos",
            "Clientes",
            "Ticket médio",
            "Margem média",
            "Taxa de devolução"
        ],
        "Valor": [
            f"R$ {total_sales:,.2f}",
            f"{total_orders:,}",
            f"{total_customers:,}",
            f"R$ {avg_ticket:,.2f}",
            f"{margin:.2f}%",
            f"{return_rate:.2f}%"
        ],
        "Status": [
            "🟢 Saudável",
            "🟢 Saudável",
            "🟢 Saudável",
            "🟢 Saudável",
            "🟢 Saudável",
            "🟡 Monitorar"
        ]
    })

    st.dataframe(
        metric_data,
        use_container_width=True,
        hide_index=True
    )

with tab3:

    display_df = filtered.copy()

    display_df["Data"] = display_df["Data"].dt.strftime(
        "%d/%m/%Y"
    )

    st.dataframe(
        display_df.sort_values(
            "Data",
            ascending=False
        ),
        use_container_width=True,
        height=450,
        hide_index=True
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

footer1, footer2 = st.columns([3, 1])

with footer1:
    st.caption(
        "Executive Analytics Dashboard • Streamlit • "
        "Dados demonstrativos"
    )

with footer2:
    st.caption(
        f"{len(filtered):,} registros analisados"
    )
