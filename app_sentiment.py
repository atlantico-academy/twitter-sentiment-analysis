import cv2
import nltk
import json
import joblib
import requests
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from snscrape.modules.twitter import TwitterSearchScraper as tss
import nltk
import numpy as np
import plotly.graph_objects as go
from scipy import stats


nltk.download('rslp')

model = joblib.load("models/model.joblib")


stemmer = nltk.stem.RSLPStemmer()

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

    st.title('Twitter Trending Topics')

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
    verificado = st.checkbox("Usuários verificados", help = "Retornar tweets apenas de usuários verificados?")
    
    nltk.download('stopwords')
    STOPWORDS = nltk.corpus.stopwords.words('portuguese')
    # Lista de stopword
    stopwords = set(STOPWORDS)
    stopwords.update(["a","b","c","d","fato","ela","estou","nem","tudo","p","pq","quando","dele","RT","por","de",'dar','pois','em','um','da','ser','aqui','vou','dos','ter','não','ao','sou','seu','à','n','se','esse','uma','mais','ele','fazendo','você','pode','essa','é','mas','segue','pra','isso','vez','para','muito','pelo','pela','são','na','vamos','https','t','co','c','New','eu','seis','retweets','ano','pessoa','likes','vai','que','ou','anos','7dias','tirou','tem','q','0','O','e','os','assim','só','mesmo','tá','pro','votar','pessoas','vc'])


    all_tweets = {}
    results = {}
    if pesquisar:
        with st.spinner("Buscando tweets. Isso pode demorar..."):
            limite = 100
            for tag in tags:
                textos = []
                st.markdown(f"### Resultados para a tag **{tag}**")
                tweets = get_tweets(tag, limite)
                all_tweets[tag] = tweets
                if tweets:
                    num_tweets = len(tweets)
                    st.markdown(f"Foram encontrados {num_tweets} tweets para a tag **{tag}**")
                    data = {
                        'username': [],
                        'original_text': [],
                        'tweet_text': [],
                        'verified': [],
                    }
                    for tweet in tweets:
                        preprocessed_tweet = [stemmer.stem(str(palavra)) for palavra in tweet['content'].split(' ') if palavra]
                        data['original_text'].append(tweet['content'])
                        data['tweet_text'].append(' '.join(preprocessed_tweet))
                        data['verified'].append(tweet['user']['verified'])
                        data['username'].append(tweet['user']['username'])
                    df = pd.DataFrame(data)
                    X = df[["tweet_text"]]
                    y_hat = model.predict(X)
                    probs = model.predict_proba(X)
                    media_probs = probs.mean(axis=0)
                    col1, col2, col3 = st.columns(3)
                    # gráfico negativo
                    gera_grafico("Negativo", media_probs[0]*100, col1)
                    gera_grafico("Neutro", media_probs[2]*100, col2)
                    gera_grafico("Positivo", media_probs[1]*100, col3)
                    if media_probs.argmax() == 0:
                        st.error("Mensagem negativa")
                    elif media_probs.argmax() == 1:
                        st.success("mensagem positiva")
                    else:
                        st.info("Mensagem neura.")
                    with st.expander(f"Tweets mais relevantes"):
                        if df.verified.sum() > 0:
                            for tweet in tweets:
                                if verificado:
                                    if tweet['user']['verified'] == True:
                                        textos.append(tweet['content'])
                                        r = requests.get(f"https://publish.twitter.com/oembed?url={tweet['url']}")
                                        col1, col2 = st.columns([.1, .9])
                                        col1.image(tweet['user']['profileImageUrl'])
                                        col2.markdown(r.json()['html'], unsafe_allow_html=True)
                                        st.markdown('---')
                                   
                                else:
                                    if tweet['user']['verified'] == False:
                                        textos.append(tweet['content'])
                                        r = requests.get(f"https://publish.twitter.com/oembed?url={tweet['url']}")
                                        col1, col2 = st.columns([.1, .9])
                                        col1.image(tweet['user']['profileImageUrl'])
                                        col2.markdown(r.json()['html'], unsafe_allow_html=True)
                                        st.markdown('---')
                        else:
                            st.info("Não foram encontrados tweets de pessoas verificadas.")
                            
                    with st.expander(f"Nuvem de palavras"):
                        if len(textos) > 0:
                            texto = ' '.join(textos)
                            imagem = cv2.imread("data/external/Twitter-Logo.png")
                            gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                            ret, mask = cv2.threshold(gray,250, 255, cv2.THRESH_BINARY)

                            wordcloud = WordCloud(stopwords=stopwords,
                                                  mask=mask,
                                                  colormap="winter",
                                                  background_color="white",    
                                                  contour_width = 0.5,
                                                  contour_color = "grey",
                                                  width=2000, height=800).generate(texto)

                            fig = plt.figure(figsize = (10, 10), facecolor = 'white') 
                            plt.title("Tweets mais relevantes", fontsize=14)
                            plt.imshow(wordcloud, interpolation = 'bilinear')
                            plt.axis('off') 
                            st.pyplot(fig=fig)
                        
                        else:
                            st.info("Impossível gerar a nuvem de palavras. Não foram encontrados tweets de pessoas verificadas.")
                            
                        
                else:
                    st.error(f"Não foram encontrados tweets suficientes para a tag **{tag}**")
                


if __name__ == '__main__':
    main()
