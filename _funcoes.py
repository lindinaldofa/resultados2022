from dash import dash_table


#gerador de tabela
def tabela_pag(dataframe):
    return dash_table.DataTable(
        columns=[
            {"name": i, "id": i, "selectable": True} for i in dataframe.columns
        ],
        data=dataframe.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current= 0,
        page_size= 15,
    )

#Calculando Escala
def escala(d):
    med = d.mean()[0]
    max = d.max()[1]
    esc = (med+max/4).round(0)
    return esc