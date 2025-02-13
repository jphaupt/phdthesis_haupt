def print_hello():
    print("hello")

display_csv = lambda f: display(Markdown(pd.read_csv(f,comment="#").to_markdown(index=False)))
display_md = lambda f: display(Markdown(open(f).read()))
