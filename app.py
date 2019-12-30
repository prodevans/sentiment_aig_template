import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import openpyxl as xl
import matplotlib.pyplot as plt


import dash_auth
from dash.dependencies import Input, Output
from os import listdir
from os.path import isfile, join
import numpy as np
import plotly_express as px
import pickle

from tqdm import tqdm

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


infile2 = open("/app/senti_predi_textblob.pickle","rb")
df = pickle.load(infile2)
print(df.columns)
infile2.close()


infile3 = open("/app/pos_text.pickle","rb")
df1 = pickle.load(infile3)
infile3.close()
print("################")
#print(df1)
print("################")

 
from textblob import TextBlob
# Get the polarity score using below function
def get_textBlob_score(sent):
    # This polarity score is between -1 to 1
    polarity = TextBlob(sent).sentiment.polarity
    return polarity


def senti_text(sent):
    sentiment_textblob=[]
    polarity=get_textBlob_score(sent)
    #print(polarity)
    if polarity > 0:
        
        sentiment_textblob.append('positive')
    elif polarity < 0:
        sentiment_textblob.append('negative')
    else:
        sentiment_textblob.append('neutral')
    return sentiment_textblob[0]
    

print('###################################')
#sent='i am antrony and i dont like firm'
#print(senti_text(sent))
#print(sentiment_textblob)
#print(df)

print('###################################')

x1 = df[df['senti_textblob']=='negative']
neg_count = x1.shape[0]
print("the negative count ", neg_count)

x2 = df[df['senti_textblob']=='positive']
pos_count = x2.shape[0]
print("the positive count ", pos_count)

x3 = df[df['senti_textblob']=='neutral']
neutral_count = x3.shape[0]
print("the nagative count ", neutral_count)


x_labels=['Negative', 'Neutral', 'Positive']
colors = ['#FF7F0E','#1F77B4', '#2CA02C']
Back_colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}

charts_type = ['bar graph', 'pie chart','word cloud']

app.layout = html.Div([
    html.Div([
        html.H1(children='Welcome to Iventura Platform',
                style={'textAlign': 'center','color':'#7FDBFF'}),
        html.H2(children='Sentiment for Insurance Provider',style={'textAlign': 'center','color':'orange'}),
        html.H6(children='Enter text and submit',style={'color':'black'}),
        html.Div([dcc.Input(id='input-box', type='text')],
                 style={'padding': '20px 0px'}),
        html.Button('Submit', id='button'),
        html.Div(id='container-button-basic',children='Enter text')

    
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '50px 5px'
    }),
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='graph-type',
                options=[{'label': i, 'value': i} for i in charts_type],
                value='Select the chart type'
            ),
            
        ],
        style={'width': '49%', 'display': 'inline-block'}),

    
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='graphDiv',
            
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    
    ])


from wordcloud import WordCloud, STOPWORDS 

def word_cloud_form(text_value):
    comment_words = ' '
    stopwords = set(STOPWORDS) 
    for words in text_value.split(): 
        comment_words =comment_words + words + ' '



    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='black', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 

    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor='y', edgecolor='w') 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 

    plt.show()
   

@app.callback(
    dash.dependencies.Output('graphDiv', 'figure'),
    [
     dash.dependencies.Input('graph-type', 'value'),
    ])
def graphType( xaxis_column_name):
    if xaxis_column_name in ['bar graph']:
        return bargraph()
    elif xaxis_column_name in ['word cloud']:
        return word11()
    else:
        return piechart()


def bargraph():
    return {
       
        'data': [
                 go.Bar(x=x_labels, y=[neg_count, neutral_count, pos_count], marker_color=colors),
        ],
    }

def piechart():
   return {
       'data': [
               go.Pie(labels=x_labels, values=[neg_count, neutral_count, pos_count]),
            ],

   }
def word11():
    return word_cloud_form(df1)

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    insertIntoExcel(value)
    print(value)
    values_text=senti_text(str(value))
    print(values_text)
    return "The sentiment for input text is {0}".format(values_text)



def insertIntoExcel(test_value):
    book = xl.load_workbook('/app/text.xlsx')
    sheet = book.active
    rows = test_value
    values_text=senti_text(str(test_value))

    # for row in rows:
    sheet.append([rows])
    sheet.append([values_text])

    book.save('/app/text.xlsx')

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')

