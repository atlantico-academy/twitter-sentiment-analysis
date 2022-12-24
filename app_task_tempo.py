# bibliotecas da aplicação
import json
import joblib
import requests
import pandas as pd
import streamlit as st
import nltk
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from streamlit_tags import st_tags
from snscrape.modules.twitter import TwitterSearchScraper as tss
from scipy import stats
from bokeh.plotting import figure

# paraâmetros iniciais 
nltk.download('rslp')

model = joblib.load("models/model.joblib")

stemmer = nltk.stem.RSLPStemmer()

# funções
def get_tweets(tag, limit=100):
    search = tss(query=f"{tag} lang:pt")
    results = []
    for i, result in enumerate(search.get_items(), start=1):
        if i > limit:
            return results
        results.append(json.loads(result.json()))

def gera_grafico(titulo, valor, coluna):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': titulo},
        gauge = {'axis': {'range': [0, 100]}}
    ))
    coluna.plotly_chart(fig)
    
def main():

    st.title('Nome da aplicação')

    tags = st_tags(
                label = f'Tags de busca',
                text = 'Adicione tags separadas por vírgula',
                maxtags = 2
            )
    # st.info('Adicione tags separadas por vírgula e pressione Enter para adicionar mais tags e comparar.')
    # col1, col2 = st.columns(2)
    # start_date = col1.date_input("Data inicial")
    # end_date = col2.date_input("Data final")
    pesquisar = st.button("Pesquisar")

    all_tweets = {}
    results = {}
    if pesquisar:
        with st.spinner("Buscando tweets. Isso pode demorar..."):
            limite = 100
            for tag in tags:
                st.markdown(f"### Resultados para a tag **{tag}**")
                tweets = get_tweets(tag, limite)
                all_tweets[tag] = tweets
                if tweets:
                    num_tweets = len(tweets)
                    st.markdown(f"Foram encontrados {num_tweets} tweets para a tag **{tag}**")
                    
                    # dicionário com dados utilizados para análise
                    data = {
                        'username': [],
                        'original_text': [],
                        'tweet_text': [],
                        'verified': [],
                        'tweet_date' : [],
                    }
                    
                    # preenchendo dicionário
                    for tweet in tweets:
                        preprocessed_tweet = [stemmer.stem(str(palavra)) for palavra in tweet['content'].split(' ') if palavra]
                        data['original_text'].append(tweet['content'])
                        data['tweet_text'].append(' '.join(preprocessed_tweet))
                        data['verified'].append(tweet['user']['verified'])
                        data['username'].append(tweet['user']['username'])
                        data['tweet_date'].append(tweet['date'])
                    
                    # leitura dataframe
                    df = pd.DataFrame(data)
                    X = df[["tweet_text"]]
                    y_hat = model.predict(X)
                    probs = model.predict_proba(X)
                    media_probs = probs.mean(axis=0)
                    col1, col2, col3 = st.columns(3)
                    
                    
                    # aba tweets horarios
                    with st.expander(f"Horários dos tweets encontrados"):
                        df['tweet_date'] = pd.to_datetime(df['tweet_date'])
                        df['tweet_date'] = df.tweet_date.dt.tz_convert('Brazil/East')
                        df['tweet_hour'] = df['tweet_date'].dt.hour
                        df['tweet_min'] = df['tweet_date'].dt.minute
                        df['tweet_sec'] = df['tweet_date'].dt.second
                        
                        df['sentimento'] = model.predict(X)

                        lista_positivo:[]
                        lista_negativo:[]
                        lista_neutro:[]
                        
                        dict_tempo = {"positivo": lista_positivo, "negativo": lista_negativo, "neutro": lista_neutro}
                        
                        for i in df['tweet_sec']:
                            p = 0
                            n = 0
                            o = 0
                            for j in df['sentimento']:
                                if j == 1:
                                    p+=1
                                elif j == 0:
                                    n+=1
                                else:
                                    o+=0
                                    
                            if p>n and p>o:
                                lista_positivo.append(i)
                            if n>p and n>o:
                                lista_negativo.append(i)
                            else:
                                lista_neutro.append(i)

                        chart_data = pd.DataFrame.from_dict(dict_tempo, orient = "index")

                        st.line_chart( data = chart_data)
                    
                else:
                    st.error(f"Não foram encontrados tweets suficientes para a tag **{tag}**")
        

# instanciação
if __name__ == '__main__':
    main()