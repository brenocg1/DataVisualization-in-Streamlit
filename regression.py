    print(df)
   
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
    Xnew = []
    for i in range(165832):
        Xnew.append([np.random.choice(df_aux['br'].unique()),
                    np.random.choice(df_aux['idade'].unique()),
                    np.random.choice(df_aux['fase_dia'].unique()),
                    np.random.choice(df_aux['condicao_metereologica'].unique()),
                    np.random.choice(df_aux['municipio'].unique()),
                    np.random.choice(df_aux['dia_semana'].unique())])
    Xnew

    ynew = model.predict(Xnew)

    plt.figure(figsize=(20,10))
    plt.plot(ynew,'*-')

    #'feridos_leves','feridos_graves','mortos'
    medias = np.mean(ynew,axis=0)
    print(medias)
    media_pesos = (medias[0] + medias[1]*2.5 + medias[2]*6.5)/10
    print(media_pesos)
    # Tratar isso com uma média geral
    # Os pesos dão mais importância aos casos mais raros
    tabela_perigos = []
    for i in range(ynew.shape[0]):
        caso = ynew[i]
        caso_pesos = (caso[0] + caso[1]*2.5 + caso[2]*6.5)/10
        tabela_perigos.append(caso_pesos - media_pesos)
    tabela_perigos = pd.DataFrame(tabela_perigos)
    print(f'Máximo valor de perigo encontrado: {tabela_perigos.max()}')
    print(f'Mínimo valor de perigo encontrado: {tabela_perigos.min()}')
    caso = ynew[101] # Exemplo
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
