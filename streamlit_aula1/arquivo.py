# python -m pip install pandas streamlit

import streamlit as st
import pandas as pd

itens = [
"Pão Francês (kg)",
"Pão de Queijo (un)",
"Leite Integral (L)",
"Queijo Mussarela (g)",
"Presunto (g)",
"Café Espesso (un)",
"Bolo de Cenoura (fatia)"
] 
 
# Lista com os respectivos valores em Reais (R$) 
precos = [
14.90,
2.50,
5.80,
12.50,
9.80,
6.00,
8.50
]  

st.title("Minha lista de compras")

st.subheader("Abaixo tem a lista de itens com seus preços")

select = st.selectbox("Selecione:", ["Portugues","Matematica","Python"])

st.write("Voce selecionou:", select)

df = pd.DataFrame({"item": itens, "preço": precos})

df