# pip install streamlit pandas numpy
# python -m streamlit run app.py

import math
import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="Concessionária AutoVia — Vendas de Veículos",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)



# CATÁLOGO DE VEÍCULOS


CATALOGO = {
    "Chevrolet Onix Plus": {
        "marca": "Chevrolet", "categoria": "Hatch", "ano": 2025,
        "preco": 78990.00, "combustivel": "Flex", "cambio": "Manual",
        "estoque": 12,
        "cores": ["Branco", "Prata", "Preto", "Vermelho"],
    },
    "Toyota Corolla": {
        "marca": "Toyota", "categoria": "Sedan", "ano": 2025,
        "preco": 152900.00, "combustivel": "Híbrido", "cambio": "Automático",
        "estoque": 5,
        "cores": ["Prata", "Preto", "Branco", "Azul"],
    },
    "Hyundai Creta": {
        "marca": "Hyundai", "categoria": "SUV", "ano": 2025,
        "preco": 149900.00, "combustivel": "Flex", "cambio": "Automático",
        "estoque": 6,
        "cores": ["Branco", "Prata", "Azul", "Preto"],
    },
    "Chevrolet S10": {
        "marca": "Chevrolet", "categoria": "Picape", "ano": 2025,
        "preco": 219900.00, "combustivel": "Diesel", "cambio": "Automático",
        "estoque": 4,
        "cores": ["Branco", "Prata", "Preto"],
    },
    "BYD Dolphin": {
        "marca": "BYD", "categoria": "Elétrico", "ano": 2025,
        "preco": 149900.00, "combustivel": "Elétrico", "cambio": "Automático",
        "estoque": 2,
        "cores": ["Branco", "Azul", "Preto"],
    },
}

# Rótulos bonitinhos para o selectbox: "Onix Plus 2025  •  Hatch"
ROTULOS = {
    f"{nome} {veiculo['ano']}  •  {veiculo['categoria']}": nome
    for nome, veiculo in CATALOGO.items()
}


# ESTADO DA SESSÃO (session_state)


if "pedido" not in st.session_state:
    st.session_state.pedido = []          # itens do pedido de venda em andamento

if "vendas" not in st.session_state:
    st.session_state.vendas = []          # histórico de vendas já finalizadas

if "flash" not in st.session_state:
    st.session_state.flash = None         # aviso mostrado após um st.rerun()

if "estoque" not in st.session_state:
    # Cópia do estoque original para descontar as vendas já realizadas
    st.session_state.estoque = {
        nome: veiculo["estoque"] for nome, veiculo in CATALOGO.items()
    }



# FUNÇÕES AUXILIARES


def calcular_parcela(valor_financiado: float, taxa_juros: float, n_parcelas: int) -> float:
    """Calcula o valor da parcela (PMT) de um financiamento.

    Args:
        valor_financiado: valor a ser financiado (R$).
        taxa_juros: taxa de juros anual (%).
        n_parcelas: quantidade de parcelas mensais.

    Returns:
        O valor da parcela mensal (R$).
    """
    if valor_financiado <= 0 or n_parcelas <= 0:
        return 0.0

    i = taxa_juros / 100 / 12  # taxa mensal

    if i == 0:
        return valor_financiado / n_parcelas

    return valor_financiado * i / (1 - (1 + i) ** (-n_parcelas))


def total_pedido() -> float:
    """Soma o valor de todos os itens do pedido atual."""
    return sum(item["Total (R$)"] for item in st.session_state.pedido)


def registrar_aviso(tipo: str, mensagem: str) -> None:
    """Guarda uma mensagem para ser exibida no próximo re-run do app."""
    st.session_state.flash = (tipo, mensagem)


def dataframe_pedido() -> pd.DataFrame:
    """Monta o DataFrame do pedido atual com as colunas formatadas."""
    return pd.DataFrame(st.session_state.pedido)


def itens_vendidos() -> pd.DataFrame:
    """Achata os itens de todas as vendas já finalizadas em um DataFrame."""
    registros = []

    for venda in st.session_state.vendas:
        for item in venda.get("Itens", []):
            registro = dict(item)
            registro["Data"] = venda["Data"]
            registro["Cliente"] = venda["Cliente"]
            registros.append(registro)

    return pd.DataFrame(registros)



# SIDEBAR — CONFIGURAÇÕES E FILTROS


with st.sidebar:
    st.markdown("## 🚗 AutoVia")
    st.caption("Concessionária • Painel de vendas")

    st.divider()

    st.markdown("### ⚙️ Financiamento")

    taxa_juros = st.slider(
        "Taxa de juros anual (%)",
        min_value=0.0,
        max_value=5.0,
        value=1.49,
        step=0.01,
        help="Taxa anual aplicada sobre o valor financiado.",
    )

    parcelas_padrao = st.select_slider(
        "Parcelas padrão",
        options=list(range(12, 85, 12)),
        value=48,
        help="Quantidade de parcelas mensais oferecidas.",
    )

    st.divider()

    st.markdown("### 🔄 Ações rápidas")

    if st.button("🧹 Limpar pedido atual", width="stretch"):
        st.session_state.pedido = []
        registrar_aviso("info", "Pedido atual limpo. Pronto para um novo atendimento.")
        st.rerun()

    if st.button("🗑️ Apagar histórico de vendas", width="stretch"):
        st.session_state.vendas = []
        st.session_state.estoque = {
            nome: veiculo["estoque"] for nome, veiculo in CATALOGO.items()
        }
        registrar_aviso("info", "Histórico de vendas apagado e estoque restaurado.")
        st.rerun()

    st.divider()

    st.caption(
        f"Usuário: **Vendedor de balcão**  \n"
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )


# CABEÇALHO


st.title("Concessionária AutoVia")
st.caption(
    "Ponto de venda de veículos • montagem de pedido, "
    "financiamento, estoque e relatórios"
)
st.divider()

# Aviso que sobrevive ao st.rerun() (ex.: venda finalizada / pedido limpo)
if st.session_state.flash:
    tipo, mensagem = st.session_state.flash
    getattr(st, tipo)(mensagem)
    st.session_state.flash = None


# ABAS DO DASHBOARD


aba_venda, aba_estoque, aba_relatorios = st.tabs(
    ["🛒 Ponto de Venda", "🚘 Estoque", "📊 Relatórios"]
)


# ABA 1 — PONTO DE VENDA


with aba_venda:

    col1, col2 = st.columns([1.25, 1], gap="large")

    
    # COLUNA 1 — SELEÇÃO DE VEÍCULOS E PEDIDO
    
    with col1:

        st.subheader("Seleção de Veículos")

        # Formulário: a página só recarrega ao clicar em "Adicionar ao Pedido"
        with st.form("form_veiculo", clear_on_submit=False):

            rotulo_selecionado = st.selectbox(
                "Escolha o Veículo",
                options=list(ROTULOS.keys()),
            )

            veiculo_nome = ROTULOS[rotulo_selecionado]
            veiculo = CATALOGO[veiculo_nome]

            preco_unit = veiculo["preco"]
            estoque_atual = st.session_state.estoque.get(veiculo_nome, 0)

            st.caption(
                f"**{veiculo_nome} {veiculo['ano']}** — "
                f"{veiculo['categoria']} • {veiculo['combustivel']} • "
                f"câmbio {veiculo['cambio']}  \n"
                f"Preço de tabela: **R\$ {preco_unit:,.2f}** • "
                f"Disponível em estoque: **{estoque_atual}**"
            )

            cor = st.selectbox("Cor", veiculo["cores"])

            quantidade = st.number_input(
                "Quantidade",
                min_value=1,
                max_value=max(estoque_atual, 1),
                value=1,
                step=1,
            )

            desconto = st.number_input(
                "Desconto do vendedor (%)",
                min_value=0.0,
                max_value=30.0,
                value=0.0,
                step=0.5,
                format="%.1f",
            )

            btn_adicionar = st.form_submit_button(
                "Adicionar ao Pedido",
                type="primary",
                width="stretch",
            )

            if btn_adicionar:
                if quantidade > estoque_atual:
                    st.error(
                        f"Estoque insuficiente para **{veiculo_nome}**. "
                        f"Disponível: {estoque_atual} unidade(s)."
                    )
                else:
                    valor_bruto = preco_unit * quantidade
                    valor_desconto = valor_bruto * (desconto / 100)
                    total_item = valor_bruto - valor_desconto

                    st.session_state.pedido.append(
                        {
                            "Veículo": veiculo_nome,
                            "Marca": veiculo["marca"],
                            "Ano": veiculo["ano"],
                            "Cor": cor,
                            "Qtd": quantidade,
                            "Preço Unit. (R$)": preco_unit,
                            "Desconto (%)": desconto,
                            "Total (R$)": total_item,
                        }
                    )

                    st.session_state.estoque[veiculo_nome] = (
                        estoque_atual - quantidade
                    )

                    st.success(
                        f"**{quantidade}x {veiculo_nome} ({cor})** adicionado "
                        f"ao pedido — **R\$ {total_item:,.2f}**."
                    )

        st.divider()

        st.subheader("Pedido de Venda")

        if st.session_state.pedido:

            df_pedido = dataframe_pedido()

            st.dataframe(
                df_pedido,
                hide_index=True,
                width="stretch",
                column_config={
                    "Preço Unit. (R$)": st.column_config.NumberColumn(
                        "Preço Unit.", format="R$ %,.2f"
                    ),
                    "Desconto (%)": st.column_config.NumberColumn(
                        "Desconto", format="%.1f%%"
                    ),
                    "Total (R$)": st.column_config.NumberColumn(
                        "Total", format="R$ %,.2f"
                    ),
                },
            )

            # Remover um item específico do pedido
            opcoes_remover = [
                f"{i + 1}. {item['Veículo']} ({item['Cor']}) x{item['Qtd']}"
                for i, item in enumerate(st.session_state.pedido)
            ]

            col_remover, col_limpar = st.columns([2, 1])

            with col_remover:
                item_para_remover = st.selectbox(
                    "Selecione o item para remover", opcoes_remover
                )

            with col_limpar:
                st.write("")
                st.write("")
                if st.button("Remover item", width="stretch"):
                    indice = opcoes_remover.index(item_para_remover)
                    item_removido = st.session_state.pedido.pop(indice)
                    st.session_state.estoque[item_removido["Veículo"]] = (
                        st.session_state.estoque.get(item_removido["Veículo"], 0)
                        + item_removido["Qtd"]
                    )
                    registrar_aviso(
                        "info",
                        f"Item **{item_removido['Veículo']}** removido do pedido.",
                    )
                    st.rerun()

            if st.button("🧹 Limpar Pedido", width="stretch"):
                for item in st.session_state.pedido:
                    st.session_state.estoque[item["Veículo"]] = (
                        st.session_state.estoque.get(item["Veículo"], 0) + item["Qtd"]
                    )
                st.session_state.pedido = []
                registrar_aviso("info", "Pedido limpo. Estoque restaurado.")
                st.rerun()

        else:
            st.info(
                "O pedido está vazio. Escolha um veículo acima e clique em "
                "**Adicionar ao Pedido**."
            )

    
    # COLUNA 2 — FINANCIAMENTO E FECHAMENTO
    
    with col2:

        st.subheader("Financiamento e Fechamento")

        total_compra = total_pedido()
        total_itens = sum(item["Qtd"] for item in st.session_state.pedido)

        st.metric(label="TOTAL DA VENDA", value=f"R$ {total_compra:,.2f}")
        st.caption(
            f"{len(st.session_state.pedido)} item(ns) • {total_itens} veículo(s) no pedido"
        )

        st.divider()

        with st.form("form_pagamento"):
            cliente = st.text_input(
                "Nome do cliente",
                placeholder="Ex.: Maria Souza",
            )

            entrada = st.number_input(
                "Entrada / pagamento à vista (R$)",
                min_value=0.0,
                value=0.0,
                step=500.0,
                format="%.2f",
            )

            n_parcelas = st.select_slider(
                "Quantidade de parcelas",
                options=list(range(12, 85, 12)),
                value=parcelas_padrao,
            )

            st.caption(f"Taxa de juros anual aplicada: **{taxa_juros:.2f}%**")
            st.caption(
                "Os campos do formulário só são atualizados após o envio — "
                "clique em **Calcular Financiamento** para refazer a simulação."
            )

            b_calcular = st.form_submit_button(
                "🧮 Calcular Financiamento", width="stretch"
            )
            b_finalizar = st.form_submit_button(
                "✅ Finalizar Venda e Novo Cliente",
                type="primary",
                width="stretch",
            )

        # ---- Cálculos do pagamento ----
        valor_financiado = max(total_compra - entrada, 0.0)
        valor_parcela = calcular_parcela(valor_financiado, taxa_juros, n_parcelas)
        total_pago = entrada + valor_parcela * n_parcelas
        custo_credito = total_pago - total_compra

        if total_compra == 0:
            st.warning("Adicione veículos ao pedido antes de prosseguir com o pagamento.")
        elif entrada > total_compra:
            st.error(
                f"**Entrada acima do valor da venda!** A entrada de "
                f"R\$ {entrada:,.2f} ultrapassa o total de R\$ {total_compra:,.2f}."
            )
        else:
            st.success("**Pagamento estruturado com sucesso!**")
            st.metric(
                label="VALOR DA PARCELA MENSAL",
                value=f"R$ {valor_parcela:,.2f}",
                delta=f"{n_parcelas}x de R$ {valor_parcela:,.2f}",
                delta_color="off",
            )
            st.caption(
                f"Valor financiado: **R\$ {valor_financiado:,.2f}** • "
                f"Total pago: **R\$ {total_pago:,.2f}** • "
                f"Custo do crédito: **R\$ {custo_credito:,.2f}**"
            )

        if b_calcular and total_compra > 0 and entrada <= total_compra:
            st.info(
                f"Simulação: **{n_parcelas} parcelas** de "
                f"**R\$ {valor_parcela:,.2f}** com juros de **{taxa_juros:.2f}% a.a.**"
            )

        st.divider()

        with st.expander("🧾 Ver comprovante da venda"):
            st.write(f"**Cliente:** {cliente or 'Cliente Balcão'}")
            st.write(f"**Veículos no pedido:** {total_itens}")
            st.write(f"**Total da venda:** R\$ {total_compra:,.2f}")
            st.write(f"**Entrada:** R\$ {entrada:,.2f}")
            st.write(f"**Valor financiado:** R\$ {valor_financiado:,.2f}")
            st.write(f"**Parcelas:** {n_parcelas} x R\$ {valor_parcela:,.2f}")
            st.write(f"**Taxa de juros:** {taxa_juros:.2f}% a.a.")
            st.write(f"**Total pago:** R\$ {total_pago:,.2f}")
            st.write(f"**Custo do crédito:** R\$ {custo_credito:,.2f}")

        # ---- Fechamento da venda ----
        if b_finalizar:
            if total_compra == 0:
                st.error("Adicione veículos ao pedido antes de finalizar a venda.")
            elif entrada > total_compra:
                st.error(
                    "Não é possível finalizar: a entrada é maior que o total da venda."
                )
            else:
                modelos = ", ".join(
                    f"{item['Veículo']} x{item['Qtd']}"
                    for item in st.session_state.pedido
                )

                marcas = ", ".join(
                    sorted({item["Marca"] for item in st.session_state.pedido})
                )

                itens = [
                    {
                        "Veículo": item["Veículo"],
                        "Marca": item["Marca"],
                        "Categoria": CATALOGO[item["Veículo"]]["categoria"],
                        "Qtd": item["Qtd"],
                        "Total (R$)": item["Total (R$)"],
                    }
                    for item in st.session_state.pedido
                ]

                st.session_state.vendas.append(
                    {
                        "Data": datetime.now(),
                        "Cliente": cliente or "Cliente Balcão",
                        "Veículos": total_itens,
                        "Modelos": modelos,
                        "Marcas": marcas,
                        "Total (R$)": total_compra,
                        "Entrada (R$)": entrada,
                        "Financiado (R$)": valor_financiado,
                        "Parcelas": n_parcelas,
                        "Parcela (R$)": valor_parcela,
                        "Total Pago (R$)": total_pago,
                        "Itens": itens,
                    }
                )

                st.session_state.pedido = []
                registrar_aviso(
                    "success",
                    f"**Venda finalizada com sucesso!** Total de "
                    f"R\$ {total_compra:,.2f} registrado no histórico.",
                )
                st.rerun()


# ABA 2 — ESTOQUE


with aba_estoque:

    st.subheader("Controle de Estoque")

    marcas = sorted({v["marca"] for v in CATALOGO.values()})
    categorias = sorted({v["categoria"] for v in CATALOGO.values()})
    combustiveis = sorted({v["combustivel"] for v in CATALOGO.values()})
    preco_maximo_mil = math.ceil(max(v["preco"] for v in CATALOGO.values()) / 1000)

    f_marca, f_categoria, f_combustivel, f_preco = st.columns(4)

    with f_marca:
        marcas_sel = st.multiselect("Marca", marcas, default=marcas)

    with f_categoria:
        categorias_sel = st.multiselect("Categoria", categorias, default=categorias)

    with f_combustivel:
        combustiveis_sel = st.multiselect(
            "Combustível", combustiveis, default=combustiveis
        )

    with f_preco:
        limite_preco = st.slider(
            "Preço máximo (R$ mil)",
            min_value=50,
            max_value=preco_maximo_mil,
            value=preco_maximo_mil,
            step=5,
        )

    linhas = []
    for nome, veiculo in CATALOGO.items():
        if veiculo["marca"] not in marcas_sel:
            continue
        if veiculo["categoria"] not in categorias_sel:
            continue
        if veiculo["combustivel"] not in combustiveis_sel:
            continue
        if veiculo["preco"] > limite_preco * 1000:
            continue

        disponivel = st.session_state.estoque.get(nome, 0)

        if disponivel == 0:
            status = "🔴 Esgotado"
        elif disponivel <= 2:
            status = "🟡 Últimas unidades"
        else:
            status = "🟢 Disponível"

        linhas.append(
            {
                "Veículo": nome,
                "Marca": veiculo["marca"],
                "Categoria": veiculo["categoria"],
                "Ano": veiculo["ano"],
                "Combustível": veiculo["combustivel"],
                "Câmbio": veiculo["cambio"],
                "Preço (R$)": veiculo["preco"],
                "Estoque": disponivel,
                "Status": status,
            }
        )

    df_estoque = pd.DataFrame(linhas)

    if df_estoque.empty:
        st.warning("Nenhum veículo encontrado com os filtros selecionados.")
    else:
        unidades = df_estoque["Estoque"].sum()
        valor_estoque = (df_estoque["Preço (R$)"] * df_estoque["Estoque"]).sum()
        criticos = df_estoque[df_estoque["Estoque"] <= 2]
        esgotados = df_estoque[df_estoque["Estoque"] == 0]

        e1, e2, e3, e4 = st.columns(4)

        with e1:
            st.metric("SKUs listados", f"{len(df_estoque)}")
        with e2:
            st.metric("Unidades disponíveis", f"{unidades}")
        with e3:
            st.metric("Valor em estoque", f"R$ {valor_estoque:,.0f}")
        with e4:
            st.metric(
                "Itens críticos",
                f"{len(criticos)}",
                delta="atenção" if len(criticos) else "ok",
                delta_color="inverse" if len(criticos) else "normal",
            )

        st.dataframe(
            df_estoque,
            hide_index=True,
            width="stretch",
            column_config={
                "Preço (R$)": st.column_config.NumberColumn(
                    "Preço", format="R$ %,.2f"
                ),
                "Estoque": st.column_config.NumberColumn("Estoque", format="%d"),
            },
        )

        if not criticos.empty:
            lista = ", ".join(
                f"{row['Veículo']} ({row['Estoque']} un.)"
                for _, row in criticos.iterrows()
            )
            st.warning(f"**Estoque baixo:** {lista}")

        if not esgotados.empty:
            lista = ", ".join(esgotados["Veículo"].tolist())
            st.error(f"**Sem unidades disponíveis:** {lista}")


# ABA 3 — RELATÓRIOS


with aba_relatorios:

    st.subheader("Relatórios de Vendas")

    if not st.session_state.vendas:

        st.info(
            "Nenhuma venda foi finalizada ainda. Registre uma venda na aba "
            "**Ponto de Venda** para visualizar os relatórios."
        )

    else:

        df_vendas = pd.DataFrame(st.session_state.vendas)

        receita_total = df_vendas["Total (R$)"].sum()
        ticket_medio = df_vendas["Total (R$)"].mean()
        veiculos_vendidos = int(df_vendas["Veículos"].sum())
        total_financiado = df_vendas["Financiado (R$)"].sum()
        total_entradas = df_vendas["Entrada (R$)"].sum()
        custo_credito = df_vendas["Total Pago (R$)"].sum() - receita_total

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric("Vendas concluídas", f"{len(df_vendas)}")
        with r2:
            st.metric("Receita total", f"R$ {receita_total:,.2f}")
        with r3:
            st.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")
        with r4:
            st.metric("Veículos vendidos", f"{veiculos_vendidos}")

        r5, r6, r7, r8 = st.columns(4)

        with r5:
            st.metric("Entradas recebidas", f"R$ {total_entradas:,.2f}")
        with r6:
            st.metric("Valor financiado", f"R$ {total_financiado:,.2f}")
        with r7:
            st.metric("Custo do crédito", f"R$ {custo_credito:,.2f}")
        with r8:
            st.metric(
                "Participação no financiamento",
                f"{(total_financiado / receita_total * 100) if receita_total else 0:.1f}%",
            )

        st.divider()

        g1, g2 = st.columns([1.4, 1])

        with g1:
            st.markdown("#### Evolução da receita por mês")

            df_mes = (
                df_vendas.assign(
                    Mês=df_vendas["Data"].dt.to_period("M").dt.to_timestamp()
                )
                .groupby("Mês", as_index=False)["Total (R$)"]
                .sum()
                .rename(columns={"Mês": "Mês", "Total (R$)": "Receita"})
            )

            st.line_chart(
                df_mes,
                x="Mês",
                y="Receita",
                height=320,
            )

        with g2:
            st.markdown("#### Receita por marca")

            df_itens = itens_vendidos()

            if df_itens.empty:
                st.info("Sem itens vendidos para gerar o gráfico.")
            else:
                df_marca = (
                    df_itens.groupby("Marca", as_index=False)["Total (R$)"]
                    .sum()
                    .rename(columns={"Total (R$)": "Receita"})
                    .sort_values("Receita", ascending=False)
                )

                st.bar_chart(
                    df_marca,
                    x="Marca",
                    y="Receita",
                    horizontal=True,
                    height=320,
                )

        st.markdown("#### Receita por categoria")

        df_itens = itens_vendidos()

        if df_itens.empty:
            st.info("Sem itens vendidos para gerar o gráfico.")
        else:
            df_categoria = (
                df_itens.groupby("Categoria", as_index=False)["Total (R$)"]
                .sum()
                .rename(columns={"Total (R$)": "Receita"})
                .sort_values("Receita", ascending=False)
            )

            st.bar_chart(
                df_categoria,
                x="Categoria",
                y="Receita",
                height=320,
            )

        st.divider()

        st.markdown("#### Histórico de vendas")

        df_exibicao = df_vendas.drop(columns=["Itens"]).copy()
        df_exibicao["Data"] = df_exibicao["Data"].dt.strftime("%d/%m/%Y %H:%M")

        st.dataframe(
            df_exibicao,
            hide_index=True,
            width="stretch",
            column_config={
                "Total (R$)": st.column_config.NumberColumn(
                    "Total", format="R$ %,.2f"
                ),
                "Entrada (R$)": st.column_config.NumberColumn(
                    "Entrada", format="R$ %,.2f"
                ),
                "Financiado (R$)": st.column_config.NumberColumn(
                    "Financiado", format="R$ %,.2f"
                ),
                "Parcela (R$)": st.column_config.NumberColumn(
                    "Parcela", format="R$ %,.2f"
                ),
                "Total Pago (R$)": st.column_config.NumberColumn(
                    "Total Pago", format="R$ %,.2f"
                ),
                "Parcelas": st.column_config.NumberColumn("Parcelas", format="%d"),
                "Veículos": st.column_config.NumberColumn("Veículos", format="%d"),
            },
        )

        st.download_button(
            "⬇️ Baixar histórico de vendas (CSV)",
            data=df_vendas.to_csv(index=False).encode("utf-8-sig"),
            file_name="vendas_concessionaria.csv",
            mime="text/csv",
            width="stretch",
        )


# RODAPÉ


st.divider()
st.caption(
    "Concessionária AutoVia • Painel de vendas • "
    f"{len(st.session_state.pedido)} item(ns) no pedido atual • "
    f"{len(st.session_state.vendas)} venda(s) no histórico"
)
