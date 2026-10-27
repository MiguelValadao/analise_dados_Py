import streamlit as st
import pandas as pd

with st.sidebar:
    st.title("Sidebar")

    

st.title("Meu dash")

st.subheader("3A1")

st.write("Olá mundo")

materia1 = st.text_input("Digite sua materia 1")
materia2 = st.text_input("Digite sua materia 2")
materia3 = st.text_input("Digite sua materia 3")

st.divider()

notamateria1 = st.text_input("Digite sua nota materia 1")
notamateria2 = st.text_input("Digite sua nota materia 2")
notamateria3 = st.text_input("Digite sua nota materia 3")

if ((materia1 and materia2 and materia3) and (notamateria1 and notamateria2 and notamateria3)):
    df = pd.DataFrame({"disciplina": [f"{materia1}", f"{materia2}", f"{materia3}"], "nota": [notamateria1, notamateria2, notamateria3]})

    df

st.divider()

select = st.selectbox("Selecione o que estudar:", ["Portugues","Matematica","Python"])

st.write("Voce selecionou:", select)