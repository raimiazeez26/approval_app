
import pandas as pd
import base64
from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

test_png = 'Xavier_Mcallister.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

#columns = ["symbol", "Position", "Confluence"]

columns = ["symbol", "Lots", "Position", "Confluence", "Candlestick", "Zone In/Out", 
                    "P/A Pattern", "Analyst", "Approval", "SL", "TP","Comment" ]
buy_sell_list = ["Buy", "Sell"]

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) #dbc.themes.ZEPHYR]
server = app.server

def layout_function():
    url = 'https://raw.githubusercontent.com/raimiazeez26/approval_app/main/approval.csv'
    try:
        data = pd.read_csv(url).to_dict('records')
    except:
        data=[
                {}
            ]
    
    return html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(test_base64),
                    style={'height':'25%', 'width':'25%'}),

            html.H1(children = 'Trades Approval Table',
            style={'margin-left': '25%', 
                   'margin-right': '25%', 
                   'margin-top': '20px',
                   'text_align' : 'center',
                   #'color' : '#ff0000',
                   #'border': '1px solid red'
                  }),

        ],style={'margin-left': '15%', 
                   'margin-right': '15%', 
                   'margin-top': '20px',
                   'text_align' : 'center',
                   #'color' : '#ff0000',
                   #'border': '1px solid red',
                 'diplay' : 'inline'
                  }),

        html.Hr(),


        html.Div([

            dash_table.DataTable(
            id='adding-rows-table',
            css=[{"selector":".dropdown", "rule": "position: static"}],
            #css=( {"selector": ".Select-menu-outer", "rule": 'display : block !important'}),
            
            columns = [{'id': 'Symbol', 'name': 'Symbol'},
            {'id': 'Lots', 'name': 'Lots'},
            {'id': 'Position', 'name': 'Position', 'presentation': 'dropdown'},
            {'id': 'Confluence', 'name': 'Confluence', 'presentation': 'dropdown'},
            {'id': 'Candlestick', 'name': 'Candlestick', 'presentation': 'dropdown'},
            {'id': 'Zone In/Out', 'name': 'Zone In/Out', 'presentation': 'dropdown'},
            {'id': 'P/A Pattern', 'name': 'P/A Pattern', 'presentation': 'dropdown'},
            {'id': 'Analyst', 'name': 'Analyst', 'presentation': 'dropdown'},
            {'id': 'Approval', 'name': 'Approval', 'presentation': 'dropdown'},
            {'id': 'SL', 'name': 'SL'},
            {'id': 'TP', 'name': 'TP'},
            {'id': 'Comment', 'name': 'Comment'},
                       ],

            data=data,
            editable=True,
            row_deletable=True,
                
            dropdown={
            'Position': {
                'options': [
                    {'label': i, 'value': i}
                    for i in buy_sell_list
                ]
            },
            'Confluence': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["Both", "One", "None"]
                ]
            },
            'Candlestick': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["Both TF", "One TF", "None"]
                ]
            },
            'Zone In/Out': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["In", "Out"]
                ]
            },
            'P/A Pattern': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["Yes", "No"]
                ]
            },
            'Analyst': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["Trader F.A.", "Trader I.J.", "Trader G.O.",
                             "Trader B.E.","Trader M.O.","Trader R.A."]
                ]
            },
            'Approval': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in ["Approved", "Not Approved" ]
                ]
            },
        },

            style_cell={'textAlign': 'center',
                       #'backgroundColor': '#36454F',
                        'color': 'white'},

            style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white','fontWeight': 'bold'}, 

            style_data={
                    'backgroundColor': '#000000',
                    'color': 'white'
                        },
        ),

        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        html.Button('Request/Send Approval', id='approval-button', n_clicks=0),
        html.Div(id="send_request",children="Press button to send Request"),
        dcc.Interval(id='update', interval=1000, n_intervals=0)

        ],style={'margin-left': '10%', 
                       'margin-right': '10%', 
                       'margin-top': '20px',
                       'text_align' : 'center',
                       #'color' : '#ff0000',
                       #'border': '1px solid red',
                        "height": "90vh", "maxHeight": "900vh"
                      }),
        
        
        ])

app.layout = layout_function

@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'),
    )
    
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    Output('send_request', 'children'),
    Input('approval-button', 'n_clicks'),
    State('adding-rows-table', 'data'))

def update_table(nclicks,table1):
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv(url, index=False)
        return "Request/Approval Sent"
    
    
if __name__ == '__main__':
    # starts the server
    app.run_server("192.168.0.101" ,port = 8080)
