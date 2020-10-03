import streamlit as st
import pandas as pd
import numpy as np

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    # Render the readme as markdown using st.markdown.
    # readme_text = st.markdown(get_file_content_as_string("instructions.md"))

	# Lembrar de colocar aqui logo o load do dataframe

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("Selecione a pagina")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["exploracao de dados", "Modelagem"])
    if app_mode == "exploracao de dados":
        st.sidebar.success('To continue select "Run the app".')
        st.code(get_file_content_as_string("app.py"))
    elif app_mode == "Modelagem":
        run_the_app()

@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://bitbucket.org/SamuelHericlesBit/datasets/raw/f54dca5ffc162c58d66ff75c2df601e4f31c061c/acidentes2019_todas_causas_tipos.csv'
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")



if __name__ == "__main__":
    main()