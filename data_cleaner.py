import pandas as pd

def data_cleaner_funtion(df):
    df["pesid"].fillna(0, inplace=True)
    df["br"].fillna(0, inplace=True)
    df["km"].fillna(0, inplace=True)
    df["id_veiculo"].fillna(0, inplace=True)
    df["marca"].fillna('Vazio', inplace=True)
    df["ano_fabricacao_veiculo"].fillna(0, inplace=True)
    df["idade"].fillna(0, inplace=True)
    df["uop"].fillna('Vazio', inplace=True)
    df["tipo_acidente"].fillna('Vazio', inplace=True)
    df["ordem_tipo_acidente"].fillna('Vazio', inplace=True)    

    df["pesid"] = df["pesid"].astype(int)
    df["ano_fabricacao_veiculo"] = df["ano_fabricacao_veiculo"].astype(int)
    df["idade"] = df["idade"].astype(int)
    df["data_inversa"] = pd.to_datetime(df["data_inversa"])
    df["horario"] = pd.to_datetime(df["horario"])   

    df.loc[df.idade >= 120, "idade"] = 0
    df.loc[df.idade <= 0, "idade"]   = 0

    return df