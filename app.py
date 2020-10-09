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
from bokeh.plotting import figure


def main():
    st.sidebar.title("Selecione a página")
    app_mode = st.sidebar.selectbox("",
        ["Exploração de dados", "Modelagem"])
    if app_mode == "Exploração de dados":
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


def freq_without_percent(x: pd.Series):
    contagem = x.value_counts()
    # percentual = round((x.value_counts() / x.shape[0]) * 100, 3)
    res = pd.DataFrame({'Qtd.': contagem})
    return res


def freq(x: pd.Series, plot=False):
    contagem = x.value_counts()
    percentual = round((x.value_counts() / x.shape[0]) * 100, 3)
    res = pd.DataFrame({'Qtd.': contagem, 'Percentual': percentual})
    if plot:
      plt.show()
    return res.sort_values('Percentual',ascending=False)



# Exploracao
def explorantion_page():
    st.markdown('## Exploracao dos dados')
    
    st.markdown("### Ranking de mortos por município")
    table_temp = df.groupby("municipio")["mortos"].sum().sort_values(ascending=False).head(10)
    st.dataframe(table_temp)

    st.markdown("### Ranking de mortos por rodovia")
    table_temp = df.groupby("br")["mortos"].sum().sort_values(ascending=False).head(10)
    st.dataframe(table_temp)

    # grafico
    # st.markdown("### Gráfico da quantidade de mortes por ocorrência no período de 04/2019 à 06/2019")
    # df_prov = df.loc[df['data_inversa'] >= '2019-04']
    # df_prov = df_prov.loc[df_prov['data_inversa'] <= '2019-06']
    # st.line_chart(df_prov)
    
    st.markdown("### Quantidade de mortes em ocorrências por estado")
    df_prov = df.groupby("uf")["mortos"].sum().sort_values(ascending=True)
    st.bar_chart(df_prov)

    st.markdown("### Agrupamento de tipos de acidentes por mortos") 
    df_prov = df.groupby("tipo_acidente")["mortos"].sum().sort_values(ascending=True)
    st.bar_chart(df_prov)
    
    st.markdown("### Agrupamento de tipos de acidentes por traçado da via")
    df_prov = df.loc[df['tipo_acidente'] == 'Colisão frontal']
    df_prov = df_prov.groupby("tracado_via")["mortos"].sum().sort_values(ascending=True)
    st.bar_chart(df_prov)

    st.markdown("### Agrupamento de causas de acidente por mortos no total")
    df_prov = df.groupby("causa_acidente")["mortos"].sum().sort_values(ascending=True)
    st.bar_chart(df_prov)

    st.markdown("### Agrupamento de dias da semana por mortos no total")
    df_prov = df.groupby("dia_semana")["mortos"].sum().sort_values(ascending=False)
    st.bar_chart(df_prov)

    st.markdown("### Quantidade de mortes por condição metereológica")
    df_prov = df.groupby("condicao_metereologica")["mortos"].sum().sort_values(ascending=False)
    st.bar_chart(df_prov)

    st.markdown("### Quantidade de mortes pela fase do dia")
    df_prov = df.groupby("fase_dia")["mortos"].sum().sort_values(ascending=False)
    st.bar_chart(df_prov)

    # copy df
    df_copy = df

    st.markdown("### Quantidade de mortes em relação a idade dos envolvidos")
    df_remove = df_copy.loc[(df['idade'] == 0)]
    df_novo = df_copy.drop(df_remove.index)
    df_prov = df_novo
    df_prov = df_prov.groupby("idade")["mortos"].sum().sort_values(ascending=False).head(25)
    st.bar_chart(df_prov)

    st.markdown("### Quantidade de ocorrências por fase do dia")
    df_prov = freq_without_percent(df.fase_dia.sort_values(ascending=False))
    st.bar_chart(df_prov)

    # Ranking
    st.markdown("## Ranking's")

    st.markdown("### Ranking do percentual de ocorrências por estado")
    st.write(freq(df.uf, plot=True).head(10))

    st.markdown("### Ranking do percentual de ocorrências por condição metereologica")
    st.write(freq(df.condicao_metereologica, plot=True).head(10))

    st.markdown("### Ranking do percentual de causa de acidentes")
    st.write(freq(df.causa_acidente, plot=True).head(10))

    st.markdown("### Ranking do percentual de tipo de acidente")
    st.write(freq(df.tipo_acidente, plot=True).head(10))

    st.markdown("### Ranking de ocorrência por tipo de via")
    st.write(freq(df.tipo_pista, plot=True))
    
    st.markdown("### Ranking de ocorrência por tipo de traçado da via")
    st.write(freq(df.tracado_via, plot=True))
    





# Modelagem
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



    cond_meteorologica = st.sidebar.selectbox('Escolha uma condição meteorológica', df['condicao_metereologica'].unique())
    cond_meteorologica = list(df['condicao_metereologica'].unique()).index(cond_meteorologica) + 1
    
    dia_semana = st.sidebar.selectbox('Escolha um dia da semana', df['dia_semana'].unique())
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