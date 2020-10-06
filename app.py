import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os, urllib
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
from data_cleaner import data_cleaner_funtion
from regression import regression_function


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
        # mensagem aqui para mostrar que os dados estão sendo carregados era bom...
        url = 'https://bitbucket.org/SamuelHericlesBit/datasets/raw/f54dca5ffc162c58d66ff75c2df601e4f31c061c/acidentes2019_todas_causas_tipos.csv'
        df = pd.read_csv(url, sep = ';', encoding = 'latin-1')
        return data_cleaner_funtion(df)

df = load_data()

def explorantion_page():
    st.markdown('## Exploracao dos dados')




inputs = []
def modelagem_page():
    st.markdown('# Modelagem dos dados')

    
    
    br = st.sidebar.selectbox('Escolha uma BR', df['br'].unique())
    idade = st.sidebar.slider('Escolha a idade do condutor', 18, 100)
    
    
    fase_dia = st.sidebar.selectbox('Escolha uma fase do dia', df['fase_dia'].unique())
    fase_dia = list(df['fase_dia'].unique()).index(fase_dia) + 1
    
    estado = st.sidebar.selectbox('Escolha um estado', df['uf'].unique())
    
    municipio = st.sidebar.selectbox('Escolha um municipio', df.query('uf == "%s"' % estado)['municipio'].unique())
    municipio = list(df.query('uf == "%s"' % estado)['municipio'].unique()).index(municipio) + 1



    cond_meteorologica = st.sidebar.selectbox('Escolha uma fase do dia', df['condicao_metereologica'].unique())
    cond_meteorologica = list(df['condicao_metereologica'].unique()).index(cond_meteorologica) + 1
    
    dia_semana = st.sidebar.selectbox('Escolha uma fase do dia', df['dia_semana'].unique())
    dia_semana = list(df['dia_semana'].unique()).index(dia_semana) + 1

    inputs = [br, idade, fase_dia, cond_meteorologica, municipio, dia_semana] 

    

    st.markdown('### Categorias de periculosidade da predição')
    st.markdown("``Perigo muito elevado!``")
    st.markdown("``Perigo acima da média``")
    st.markdown("``Perigo baixo``")
    st.markdown("``Perigo abaixo da média``")
    st.markdown("``Perigo médio``")

    st.write('Array de inputs')
    st.write(inputs)

    if st.sidebar.button('Predict!'):
        with st.spinner('Carregando predição'):
            result = regression_function(df, inputs)
            st.markdown('### Predição da via:')
            st.write(result)



if __name__ == "__main__":
    main()