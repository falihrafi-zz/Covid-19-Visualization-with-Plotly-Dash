import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import iplot,init_notebook_mode
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.MATERIA])

df = pd.read_csv('data/(3)covid_19_indonesia_time_series_all.csv')
new_result2_sul = pd.read_csv('data/newresult2sul.csv')
result = pd.read_csv('data/result.csv')
indonesia_province = json.load(open('data/indonesia-province.json','r'))
indonesia_province['features'][26]['properties']['kode'] = 1

state_id_map = {}
for feature in indonesia_province["features"]:
    feature["id"] = feature["properties"]["kode"]
    state_id_map[feature["properties"]["Propinsi"]] = feature["id"]

def show_province_table(x) :
        df1 = df[['Date','Location','New Cases','New Deaths','New Recovered']]
        df1.rename(columns={'Location':'Nama Provinsi',
                        'New Cases':'Jumlah Kasus',
                        'New Deaths':'Jumlah Kematian',
                        'New Recovered':'Jumlah Kesembuhan'},
                        inplace=True)
        tabel = df1[df1['Nama Provinsi'] == x]
        tabel['Date'] = pd.to_datetime(tabel['Date'])
        tabel['Hari'] = tabel['Date'].dt.day
        tabel['Bulan'] = tabel['Date'].dt.month
        tabel['Hari Terurut'] = np.arange(1,len(tabel)+1)
        tabel.index = np.arange(1,len(tabel)+1)
        return tabel

def show_line_plot(a,b,c):
        tabel = show_province_table(a)
        if b == 'Term 1' :
                fig = px.line(tabel, 
                        x=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Date']), 
                        y=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)][c]),
                        labels={'x':'Date','y':c},
                        template='none',
                        title='Grafik Perkembangan ' + c + ' pada Term 1'
                        )
                fig.update_layout(title={'font':{'size':15,'color':'#000000'}})
        elif b == 'Term 2' :
                fig = px.line(tabel,
                        x=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Date']),
                        y=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)][c]),
                        labels={'x':'Date','y':c},
                        template='none',
                        title='Grafik Perkembangan ' + c + ' pada Term 2'
                        )
                fig.update_layout(title={'font':{'size':15,'color':'#000000'}})
        elif b == 'Term 3' :
                fig = px.line(tabel,
                        x=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Date']),
                        y=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)][c]),
                        labels={'x':'Date','y':c},
                        template='none',
                        title='Grafik Perkembangan ' + c + ' pada Term 3'
                        )
                fig.update_layout(title={'font':{'size':15,'color':'#000000'}})
        elif b == 'Total' :
                fig = px.line(tabel,
                        x=tabel['Date'],
                        y=tabel[c],
                        template='none',
                        height=400,
                        title='Grafik Perkembangan ' + c + ' Keseluruhan'
                        )
                fig.update_layout(title={'font':{'size':15,'color':'#000000'}})

        return fig

def membuat_peta (x):
        fig = px.choropleth(
                new_result2_sul,
                locations='id',
                geojson = indonesia_province,
                color='Total Cases' + ' ' + x + ' ' + '(Logaritmik)',
                range_color = (1,5),
                hover_name='Nama Provinsi',
                hover_data=['Total Cases ' + '('+ x +')'],
                title='Persebaran Total Kasus Covid-19 di Indonesia pada' + ' ' + x,
        )
        fig.update_geos(fitbounds="locations", visible=False)

        return fig

def membuat_plot_chart (x):
# Membuat plot chart 
        Nama_Provinsi = result['Nama Provinsi'].unique()

        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=['Perbandingan Kematian', 'Perbandingan Kesembuhan'])

        fig.add_trace(go.Pie(labels =Nama_Provinsi, values = result['Total Deaths' + " " + '('+ x + ')'], name="Kematian"),
                1, 1)
        fig.add_trace(go.Pie(labels =Nama_Provinsi, values = result['Total Recovered' + " " + '('+ x + ')' ], name="Kesembuhan"),
                1, 2)

        fig.update_layout(title_text='Perbandingan Tingkat Kematian dan Tingkat Kesembuhan di Indonesia pada' + ' ' + x, uniformtext_minsize=12, uniformtext_mode='hide')   
        fig.update_layout(title={'font':{'size':15}})
        fig.update_traces(hole=.5, hoverinfo="label+percent+name",textposition='inside')

        annotations=[dict(text='Tingkat Kematian', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Tingkat Kesembuhan',x=0.82, y=0.5, font_size=20, showarrow=False)]

        return (fig)

def show_pie_chart(a,b) :
        tabel = show_province_table(a)
        if b == 'Term 1' :
                fig = px.pie(
                        values = [(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Jumlah Kematian']).sum(),
                                (tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Jumlah Kesembuhan']).sum(),
                                ((tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Jumlah Kasus']).sum() - 
                                ((tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Jumlah Kematian']).sum() + 
                                (tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Jumlah Kesembuhan']).sum()))],
                        names = ['Jumlah Kematian','Jumlah Kesembuhan','Jumlah Kasus Aktif'],
                        hole=0.6,
                        template='simple_white',
                        title='Perbandingan Kasus Aktif, Kematian, dan Kesembuhan pada Term 1'
                        )
                fig.update_layout(title={'font':{'size':12,'color':'#000000'}})
        elif b == 'Term 2' :
                fig = px.pie(
                        values = [(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Jumlah Kematian']).sum(),
                                (tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Jumlah Kesembuhan']).sum(),
                                ((tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Jumlah Kasus']).sum() - 
                                ((tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Jumlah Kematian']).sum() + 
                                (tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Jumlah Kesembuhan']).sum()))],
                        names = ['Jumlah Kematian','Jumlah Kesembuhan','Jumlah Kasus Aktif'],
                        hole=0.6,
                        template='simple_white',
                        title='Perbandingan Kasus Aktif, Kematian, dan Kesembuhan pada Term 2'
                        )
                fig.update_layout(title={'font':{'size':12,'color':'#000000'}})
        elif b == 'Term 3' :
                fig = px.pie(
                        values = [(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Jumlah Kematian']).sum(),
                                (tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Jumlah Kesembuhan']).sum(),
                                ((tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Jumlah Kasus']).sum() - 
                                ((tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Jumlah Kematian']).sum() + 
                                (tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Jumlah Kesembuhan']).sum()))],
                        names = ['Jumlah Kematian','Jumlah Kesembuhan','Jumlah Kasus Aktif'],
                        hole=0.6,
                        template='simple_white',
                        title='Perbandingan Kasus Aktif, Kematian, dan Kesembuhan pada Term 3'
                        )
                fig.update_layout(title={'font':{'size':12,'color':'#000000'}})
        elif b == 'Total' :
                fig = px.pie(
                        values = [(tabel['Jumlah Kematian']).sum(),
                                (tabel['Jumlah Kesembuhan']).sum(),
                                ((tabel['Jumlah Kasus']).sum() - (tabel['Jumlah Kematian'].sum() + tabel['Jumlah Kesembuhan'].sum()))],
                        names = ['Jumlah Kematian','Jumlah Kesembuhan','Jumlah Kasus Aktif'],
                        hole=0.6,
                        template='simple_white',
                        height=400,
                        title='Perbandingan Kasus Aktif, Kematian, dan Kesembuhan Keseluruhan'
                        )
                fig.update_layout(title={'font':{'size':12,'color':'#000000'}})

        return fig

def get_options(nama_provinsi):
        dict_list = []
        for i in nama_provinsi:
                dict_list.append({'label': i, 'value': i})

        return dict_list

def total_sum (x):
        total_active = result['Total Cases ' + '(' + x + ')'].sum() - (result['Total Deaths ' + '(' + x + ')'].sum() + result['Total Recovered '+ '(' + x + ')'].sum())
        total_deaths = result['Total Deaths ' + '(' + x + ')'].sum()
        total_recovered = result['Total Recovered '+ '(' + x + ')'].sum()
        return (total_active, total_deaths,total_recovered)
    
def pie_total (x) :
        total = ['Jumlah Kasus Aktif ' + '(' + x + ')','Jumlah Kematian ' + '(' + x + ')', 'Jumlah Kesembuhan ' + '(' + x + ')' ]
        labels = total
        values = total_sum (x)
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.2, 0])])
        fig.update_layout(title_text='Perbandingan Jumlah Kasus Aktif, Kematian, dan Kesembuhan di Indonesia pada ' + x)
        return fig

def hitung_rata2(x,y):
        if y == 'Term 1' :
                rata2 = (result['Total ' + x + ' (' + y + ')'].sum())/92
        if y == 'Term 2' :
                rata2 = (result['Total ' + x + ' (' + y + ')'].sum())/61
        if y == 'Term 3' :
                rata2 = (result['Total ' + x + ' (' + y + ')'].sum())/56
        if y == 'Keseluruhan' :
                rata2 = (result['Total ' + x + ' (' + y + ')'].sum())/209
    
        return str(int(rata2)) + ' Orang'

def hitung_rata2_jumlah_kasus_aktif (y):
        jumlah_kasus = result['Total Cases' + ' (' + y + ')'].sum()
        jumlah_kematian = result['Total Deaths' + ' (' + y + ')'].sum()
        jumlah_kesembuhan = result['Total Recovered' + ' (' + y + ')'].sum()
        jumlah_kasus_aktif = jumlah_kasus - (jumlah_kematian + jumlah_kesembuhan)

        if y == 'Term 1' :
                rata2 = jumlah_kasus_aktif/92
        if y == 'Term 2' :
                rata2 = jumlah_kasus_aktif/61
        if y == 'Term 3' :
                rata2 = jumlah_kasus_aktif/56
        if y == 'Keseluruhan' :
                rata2 = jumlah_kasus_aktif/209

        return str(int(rata2)) + ' Orang'

def show_bar_chart(x,y) :
        tabel = result.copy()
        tabel['Rasio Kesembuhan'] = tabel['Total Recovered ' + '(' + y + ')']/tabel['Total Cases ' + '(' + y + ')']
        tabel['Rasio Kematian'] = tabel['Total Deaths ' + '(' + y + ')']/tabel['Total Cases ' + '(' + y + ')']
        tabel = tabel.sort_values(by='Rasio ' + x, ascending=False).head()
        fig = px.bar(tabel, 
                x=tabel['Nama Provinsi'], 
                y=tabel['Rasio ' + x],
                template='none',
                color=tabel['Rasio ' + x],
                title='5 Provinsi dengan Rasio ' + x + ' Tertinggi'
        )
        fig.update(layout_coloraxis_showscale=False)

        return fig


#-----------------------------------------(Penginisiasian Aplikasi Dash serta Judul Tulisan)

app.layout = html.Div([

        dbc.Row([
                dbc.Col(
                        html.H1('Visualisasi Kasus Pandemi Covid-19 di Indonesia'),
                        width={'size': 8,'offset':3}
                )
        ]),

#-----------------------------------------(Dropdown 1 dan Grafik 1 : Peta Pesebaran)

        dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dcc.Dropdown(id='my-range-slider1',
                                options=[
                                {'label': 'Term 1 (Maret - Mei)', 'value': 'Term 1'},
                                {'label': 'Term 2 (Juni - Juli)', 'value': 'Term 2'},
                                {'label': 'Term 3 (Agustus - September)', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Keseluruhan'}
                                ],
                                multi=False, 
                                value='Keseluruhan',
                                clearable=False
                                ),
                        width={'size': 4, "offset": 4}
                )
        ]),

        dbc.Row([
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='our_graph1',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 8,'offset':2}
                )
        ]),

#-----------------------------------------(Dropdown 2, Box angka, dan Grafik 2 : Perbandingan Jumlah Kasus Aktif, Kematian, dan Kesembuhan)

        dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dcc.Dropdown(id='my-range-slider2',
                                options=[
                                {'label': 'Term 1 (Maret - Mei)', 'value': 'Term 1'},
                                {'label': 'Term 2 (Juni - Juli)', 'value': 'Term 2'},
                                {'label': 'Term 3 (Agustus - September)', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Keseluruhan'}
                                ],
                                multi=False, 
                                value='Term 1',
                                clearable=False
                                ),
                        width={'size': 4, "offset": 4}
                )
        ]),

        dbc.Row([
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card([
                                html.H1(id='rata2_kasus',style={'text-align':'center'}),
                                html.Br(),html.Br(),
                                html.H5('Rata-Rata Jumlah Kasus per Hari',style={'text-align':'center'})
                        ],body=True,color='secondary'),
                width={'size': 3,'offset':0}),
                dbc.Col(
                        dbc.Card([
                                html.H1(id='rata2_kasus_aktif',style={'text-align':'center'}),
                                html.Br(),html.Br(),
                                html.H5('Rata-Rata Jumlah Kasus Aktif per Hari',style={'text-align':'center'})
                        ],body=True,color='secondary'),
                width={'size': 3,'offset':0}),
                dbc.Col(
                        dbc.Card([
                                html.H1(id='rata2_kematian',style={'text-align':'center'}),
                                html.Br(),html.Br(),
                                html.H5('Rata-Rata Jumlah Kematian per Hari',style={'text-align':'center'})
                        ],body=True,color='secondary'),
                width={'size': 3,'offset':0}),
                dbc.Col(
                        dbc.Card([
                                html.H1(id='rata2_kesembuhan',style={'text-align':'center'}),
                                html.Br(),html.Br(),
                                html.H5('Rata-Rata Jumlah Kesembuhan/Hari',style={'text-align':'center'}),
                        ],body=True,color='secondary'),
                width={'size': 3,'offset':0}),
        ]),

        dbc.Row([
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='our_graph2',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 8,'offset':2}
                )
        ]),

#-----------------------------------------(Dropdown 3 dan Grafik 3 : Perbandingan Tingkat Kematian dan Kesembuhan pada 34 Provinsi)
        dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col(
                        dcc.Dropdown(id='my-range-slider3',
                                options=[
                                {'label': 'Term 1 (Maret - Mei)', 'value': 'Term 1'},
                                {'label': 'Term 2 (Juni - Juli)', 'value': 'Term 2'},
                                {'label': 'Term 3 (Agustus - September)', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Keseluruhan'}
                                ],
                                multi=False, 
                                value='Keseluruhan',
                                clearable=False
                                ),
                        width={'size': 3, "offset": 2}
                ),
                dbc.Col(
                        dcc.Dropdown(id='my-range-slider4',
                                options=[
                                {'label': 'Tingkat Kesembuhan', 'value': 'Kesembuhan'},
                                {'label': 'Tingkat Kematian', 'value': 'Kematian'}
                                ],
                                multi=False, 
                                value='Kesembuhan',
                                clearable=False
                                ),
                        width={'size': 3, "offset": 3}
                ),
        ]),

        dbc.Row([
                html.Br(),
                html.Br(),
        ]),
        
        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='our_graph3',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 7,'offset':0}
                ),
                dbc.Col(
                        dbc.Card(dcc.Graph(id='our_graph4',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5,'offset':0}
                ),
        ]),


#-----------------------------------------(Dropdown 4 dan Grafik Detail Kasus Covid-19 tiap Provinsi)

        dbc.Row([
                html.Br(),
                html.Br(),
                html.Br(),
        ]),

        dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id='pilihan1',
                                options=get_options(df['Location'].unique()),
                                multi=False, 
                                value='DKI Jakarta',
                                clearable=False
                                ),
                        html.Br(),
                        dcc.Dropdown(id='pilihan2',
                                options=[
                                {'label': 'Term 1 (Maret - Mei)', 'value': 'Term 1'},
                                {'label': 'Term 2 (Juni - Juli)', 'value': 'Term 2'},
                                {'label': 'Term 3 (Agustus - Spetember)', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Total'}
                                ],
                                multi=False, 
                                value='Total',
                                clearable=False
                                ),
                ],width={'size': 3, "offset": 2}),

                dbc.Col([
                        dcc.Dropdown(id='pilihan3',
                                options=get_options(df['Location'].unique()),
                                multi=False, 
                                value='Jawa Timur',
                                clearable=False
                                ),
                        html.Br(),
                        dcc.Dropdown(id='pilihan4',
                                options=[
                                {'label': 'Term 1 (Maret - Mei)', 'value': 'Term 1'},
                                {'label': 'Term 2 (Juni - Juli)', 'value': 'Term 2'},
                                {'label': 'Term 3 (Agustus - Spetember)', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Total'}
                                ],
                                multi=False, 
                                value='Total',
                                clearable=False
                                ),
                ],width={'size': 3, "offset": 2}),
        ]),

        dbc.Row([
                html.Br(),
                html.Br()
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph1-1',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5,'offset':1}
                ),
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph2-1',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5}
                ),
        ]),

        dbc.Row([
                html.Br()
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph1-2',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5,'offset':1}
                ),
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph2-2',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5}
                ),
        ]),

        dbc.Row([
                html.Br()
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph1-3',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5,'offset':1}
                ),
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph2-3',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5}
                ),
        ]),

        dbc.Row([
                html.Br()
        ]),

        dbc.Row([
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph1-4',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5,'offset':1}
                ),
                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph2-4',config={'scrollZoom':False}),body=True,color='secondary'),width={'size': 5}
                ),
        ]),

        dbc.Row([
                html.Br()
        ]),
])

#----------------------------------------------------------------------------------------

#---------------------------------(app callback 1)
@app.callback(
        Output('our_graph1','figure'),
        Input('my-range-slider1','value')
)

def show_plot1(a):
        fig1 = membuat_peta(a)

        return fig1

#---------------------------------(app callback 2)

@app.callback([
        Output('rata2_kasus','children'),
        Output('rata2_kasus_aktif','children'),
        Output('rata2_kematian','children'),
        Output('rata2_kesembuhan','children'),
        Output('our_graph2','figure')],
        Input('my-range-slider2','value')
)

def show_plot2(a):
        fig2 = hitung_rata2('Cases',a)
        fig3 = hitung_rata2_jumlah_kasus_aktif(a)
        fig4 = hitung_rata2('Deaths',a)
        fig5 = hitung_rata2('Recovered',a)
        fig6 = pie_total(a)

        return fig2,fig3,fig4,fig5,fig6

#---------------------------------(app callback 3)

@app.callback([
        Output('our_graph3','figure'),
        Output('our_graph4','figure')],
        [Input('my-range-slider3','value'),
        Input('my-range-slider4','value')]
)

def show_plot3(a,b):
        fig7 = membuat_plot_chart(a)
        fig8 = show_bar_chart(b,a)

        return fig7,fig8

#---------------------------------(app callback 4 kiri)

@app.callback([
        Output('graph1-1','figure'),
        Output('graph1-2','figure'),
        Output('graph1-3','figure'),
        Output('graph1-4','figure')],
        [Input('pilihan1','value'),
        Input('pilihan2','value')]
)

def show_plot4(a,b):
        fig9 = show_line_plot(a,b,'Jumlah Kasus')
        fig10 = show_line_plot(a,b,'Jumlah Kematian')
        fig11 = show_line_plot(a,b,'Jumlah Kesembuhan')
        fig12 = show_pie_chart(a,b)

        return fig9,fig10,fig11,fig12

#---------------------------------(app callback 4 kanan)

@app.callback([
        Output('graph2-1','figure'),
        Output('graph2-2','figure'),
        Output('graph2-3','figure'),
        Output('graph2-4','figure')],
        [Input('pilihan3','value'),
        Input('pilihan4','value')]
)

def show_plot5(a,b):
        fig13 = show_line_plot(a,b,'Jumlah Kasus')
        fig14 = show_line_plot(a,b,'Jumlah Kematian')
        fig15 = show_line_plot(a,b,'Jumlah Kesembuhan')
        fig16 = show_pie_chart(a,b)

        return fig13,fig14,fig15,fig16

#----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
