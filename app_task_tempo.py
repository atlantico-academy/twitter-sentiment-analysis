# bibliotecas da aplicação
import json
import joblib
import requests
import pandas as pd
import streamlit as st
import nltk
import numpy as np
import plotly.graph_objects as go

from streamlit_tags import st_tags
from snscrape.modules.twitter import TwitterSearchScraper as tss
from scipy import stats
from bokeh.plotting import figure

# paraâmetros iniciais 
nltk.download('rslp')

model = joblib.load("models/model.joblib")

stemmer = nltk.stem.RSLPStemmer()

# funções
def get_tweets(tag, limit=10):
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
                    
                    # gráfico negativo
                    gera_grafico("Negativo", media_probs[0]*100, col1)
                    # gráfico neutro
                    gera_grafico("Neutro", media_probs[2]*100, col2)
                    # gráfico positivo
                    gera_grafico("Positivo", media_probs[1]*100, col3)
                    
                    if media_probs.argmax() == 0:
                        st.error("Mensagem negativa")
                    elif media_probs.argmax() == 1:
                        st.success("Mensagem positiva")
                    else:
                        st.info("Mensagem neutra.")
                    
                    # aba tweets mais relevantes
                    with st.expander(f"Tweets mais relevantes"):
                        if df.verified.sum() > 0:
                            for tweet in tweets:
                                if tweet['user']['verified']:
                                    r = requests.get(f"https://publish.twitter.com/oembed?url={tweet['url']}")
                                    col1, col2 = st.columns([.1, .9])
                                    col1.image(tweet['user']['profileImageUrl'])
                                    col2.markdown(r.json()['html'], unsafe_allow_html=True)
                                    st.markdown('---')
                        else:
                            st.info("Não foram encontrados tweets de pessoas verificadas.")

                    # aba tweets horarios
                    df['tweet_date'] = pd.to_datetime(df['tweet_date'])
                    df['tweet_date'] = df.tweet_date.dt.tz_convert('Brazil/East')
                    df['tweet_hour'] = df['tweet_date'].dt.hour
                    df['tweet_day'] = df['tweet_date'].dt.date
                    
                    with st.expander(f"Horários dos tweets encontrados"):
                        #st.line_chart(x = df['tweet_day'], y = media_probs[0])
                        x = df['tweet_day']
                        y = df['tweet_hour']
                        p = figure(
                            title='simple line example',
                            x_axis_label='x',
                            y_axis_label='y')
                        p.line(x, y, legend_label='Trend', line_width=2)
                        st.bokeh_chart(p, use_container_width=True)
                            
                else:
                    st.error(f"Não foram encontrados tweets suficientes para a tag **{tag}**")
        

# instanciação
if __name__ == '__main__':
    main()