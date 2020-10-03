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
        readme_text.empty()
        run_the_app()

if __name__ == "__main__":
    main()