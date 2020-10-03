import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt

def regression_function(df):  
    df_aux = df.copy()

    df_aux.dia_semana.replace(
            {i:j+1 for i,j in zip(df['dia_semana'].unique(),range(df['dia_semana'].unique().shape[0]))},
            inplace=True)
    df_aux.municipio.replace(
        {i:j+1 for i,j in zip(df.municipio.unique(),range(df.municipio.unique().shape[0]))},
        inplace=True)
    df_aux.condicao_metereologica.replace(
        {i:j+1 for i,j in zip(df.condicao_metereologica.unique(),range(df.condicao_metereologica.unique().shape[0]))},
        inplace=True)
    df_aux['fase_dia'].replace(
        {i:j+1 for i,j in zip(df['fase_dia'].unique(),range(4))},
        inplace=True)
    df_remove = df_aux.loc[(df['br'] == 0) | (df['idade'] == 0) | (df['condicao_metereologica'] == "Ignorado")]
    # df_remove = df_remove.loc[(df['condicao_metereologica'] == "Ignorado")]
    df_novo = df_aux.drop(df_remove.index)
    X = df_novo[['br', 'idade','fase_dia','condicao_metereologica','municipio','dia_semana']]
    y = df_novo[['feridos_leves','feridos_graves','mortos']]

    model = LinearRegression()
    model.fit(X, y)
    Xnew = [[116, 20, 2, 4, 12, 2]]

    ynew = model.predict(Xnew)

    media_pesos = 0.10963494565279992

    caso = ynew[0] # Exemplo
    caso_pesos = (caso[0] + caso[1]*2.5 + caso[2]*6.5)/10
    perigo_do_caso = caso_pesos - media_pesos
    print(f'Media de perigo: {media_pesos}')
    print(f'Caso em questão: {caso_pesos}')
    print(f'Perigo do caso: {perigo_do_caso}')

    if perigo_do_caso >= 0.035:
        print("Perigo muito elevado!")
    elif perigo_do_caso >= 0.01:
        print("Perigo acima da média")
    elif perigo_do_caso <= -0.035:
        print("Perigo baixo")
    elif perigo_do_caso <= -0.01:
        print("Perigo abaixo da média")
    else:
        print("Perigo médio")
