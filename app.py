import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os, urllib

from regression import regression_function
from data_cleaner import data_cleaner_funtion

def main():

    st.sidebar.title("Selecione a pagina")
    app_mode = st.sidebar.selectbox("Navegaçao",
        ["Exploracao de dados", "Modelagem"])
    if app_mode == "Exploracao de dados":
        explorantion_page()
    elif app_mode == "Modelagem":
        modelagem_page()

@st.cache(show_spinner=False)
def load_data():
    with st.spinner("Carregando dataset"):
        df = data_cleaner_funtion(pd.read_csv('data.csv', sep = ';', encoding = 'latin-1'))
    return df

df = load_data()

def explorantion_page():
    st.markdown('## Exploracao dos dados')

def modelagem_page():
    st.markdown('## Modelagem dos dados')
    st.markdown('### Regressão Linear')
    
    idade = st.sidebar.slider('Escolha a idade do condutor', 18, 100)
    fase_dia = st.sidebar.selectbox('Escolha uma fase do dia', df['fase_dia'].unique())
    
    estado = st.sidebar.selectbox('Escolha um estado', df['uf'].unique())
    municipios = st.sidebar.selectbox('Escolha um municipio', df.query('uf == "%s"' % estado)['municipio'].unique())
    
    cond_meteorologica = st.sidebar.selectbox('Escolha uma fase do dia', df['condicao_metereologica'].unique())
    dia_semana = st.sidebar.selectbox('Escolha uma fase do dia', df['dia_semana'].unique())

    regression_function(df)
    
    st.markdown('## Modelagem dos dados')

if __name__ == "__main__":
    main()