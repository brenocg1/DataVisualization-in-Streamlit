import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os, urllib

def main():
    # Render the readme as markdown using st.markdown.
    # readme_text = st.markdown(get_file_content_as_string("instructions.md"))

    # Lembrar de colocar aqui logo o load do dataframe

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("Selecione a pagina")
    app_mode = st.sidebar.selectbox("Navegaçao",
        ["Exploracao de dados", "Modelagem"])
    if app_mode == "Exploracao de dados":
        explorantion_page()
    elif app_mode == "Modelagem":
        modelagem_page()

@st.cache
def load_data():
    # mensagem aqui para mostrar que os dados estão sendo carregados era bom...
    url = 'https://bitbucket.org/SamuelHericlesBit/datasets/raw/f54dca5ffc162c58d66ff75c2df601e4f31c061c/acidentes2019_todas_causas_tipos.csv'
    df = pd.read_csv(url, sep = ';', encoding = 'latin-1')
    return df

df = load_data()

def explorantion_page():
    st.markdown('## Exploracao dos dados')

def modelagem_page():
    st.markdown('## Modelagem dos dados')
    st.markdown('### Regressão Linear')
    idade = st.sidebar.slider('Escolha a idade do condutor', 18, 100)
    municipios = st.sidebar.selectbox('Escolha um municipio', df['municipio'].unique())

if __name__ == "__main__":
    main()