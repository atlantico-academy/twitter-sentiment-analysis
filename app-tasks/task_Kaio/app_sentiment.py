import json
import joblib
import requests
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
from streamlit_tags import st_tags
from snscrape.modules.twitter import TwitterSearchScraper as tss
import nltk
import numpy as np
import plotly.graph_objects as go
from wordcloud import WordCloud, ImageColorGenerator
from scipy import stats
from PIL import Image
import cv2


nltk.download('rslp')
#carregando modelo
model = joblib.load("models/model.joblib")
#carregando lista de stopwords
nltk.download('stopwords')
stopnltk = nltk.corpus.stopwords.words('portuguese')
stopwords = set(stopnltk)
stopwords.update(json.load(open('stopwords.json', 'r')))
stemmer = nltk.stem.RSLPStemmer()

#função para importar os tweets
def get_tweets(tag, limit=10):
    search = tss(query=f"{tag} lang:pt")
    results = []
    for i, result in enumerate(search.get_items(), start=1):
        if i > limit:
            return results
        results.append(json.loads(result.json()))
#função para gerar os gráficos
def gera_grafico(titulo, valor, coluna, cor):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': titulo},
        gauge = {'axis': {'range': [0, 100]},
                'bar': {'color': cor}}
    ))
    if coluna:
        coluna.plotly_chart(fig)
    else:
        st.plotly_chart(fig)        
#função para gerar as nuvens de palavras
def nuvem_palavras(cor, texto, sentimento, coluna, query, stopwords):
    stopwords.update([query, query.lower(), query.upper(), query.capitalize()])
    place = coluna if coluna else st
    texto = texto.lower()
    if sentimento == 0:
        place.markdown("Tweets negativos")
        # importando imagem
        imagem = cv2.imread("data/external/deslike.jpg")
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray,250, 255, cv2.THRESH_BINARY)
              
        wordcloud = WordCloud(stopwords=stopwords,
                              colormap = "copper",
                          background_color= cor,contour_color = "black",
                          contour_width = 0.5,
                          width=500, height=500, max_words=2000,
                          max_font_size=200, mask=mask,
                          min_font_size=1).generate(texto)
        # Mostra a imagem final
        fig, ax = plt.subplots(figsize=(10,10))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        place.pyplot(fig=fig)
    elif sentimento == 1:
        place.markdown("Tweets positivos")        
        # importando imagem
        #imagem = cv2.imread("like.jpg")
        imagem = cv2.imread("data/external/like.jpg")
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray,250, 255, cv2.THRESH_BINARY)
        wordcloud = WordCloud(stopwords=stopwords,
                              colormap = "copper",
                          background_color=cor,contour_color = "black",
                          contour_width = 0.5,
                          width=500, height=500, max_words=2000,
                          max_font_size=200, mask=mask,
                          min_font_size=1).generate(texto)
        # Mostra a imagem final
        fig, ax = plt.subplots(figsize=(10,10))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        place.pyplot(fig=fig)

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
    
    #verificado = st.checkbox("Usuários verificados", help = "Retornar tweets apenas de usuários verificados?")
    pesquisar = st.button("Pesquisar")
    all_tweets = {}
    results = {}
    all_df = {}
    if pesquisar:
        with st.spinner("Buscando tweets. Isso pode demorar..."):            
            limite = 100
            for tag in tags:
                textos = []
                texts = []
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
                    df['classe'] = y_hat
                    all_df[tag] = df
                    probs = model.predict_proba(X)
                    media_probs = probs.mean(axis=0)
                    result = media_probs/(media_probs[0]+media_probs[1])                    
                    col1, col2, col3 = st.columns(3)
                    # gráfico negativo
                    gera_grafico("Sentimento", result[1]*100, None, "green")
                    #gera_grafico("Neutro", media_probs[2]*100, col2, "white")
                    #gera_grafico("Positivo", media_probs[1]*100, col3, "green")
                    if media_probs.argmax() == 0:
                        st.error("A tag pesquisada possui mais tweets negativos")
                    elif media_probs.argmax() == 1:
                        st.success("A tag pesquisada possui mais tweets positivos")
                    else:
                        st.info("A tag pesquisada possui mais tweets neutros")
                with st.expander('Nuvens de palavras'):
                    
                    for tag, df in all_df.items():
                        col1, col2 = st.columns(2)
                        #st.markdown(f"### {tag}")
                        for sentimento, coluna in zip([0,1],st.columns(2)):
                            
                            tt = df.query("classe == @sentimento").original_text.to_list()                                                   
                            texto = ' '.join(tt)                            
                            nuvem_palavras("white", texto, sentimento, coluna, tag, stopwords)
                        
                        for tweet in tweets:                                    
                            texts.append(tweet['content'])
                        text = ' '.join(texts)
                        imagem = cv2.imread("data/external/twitter.jpg")
                        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                        ret, mask = cv2.threshold(gray,250, 255, cv2.THRESH_BINARY)

                        wordcloud = WordCloud(stopwords=stopwords,
                                              mask=mask,
                                              colormap="copper",
                                              background_color="white",    
                                              contour_width = 0.5,
                                              contour_color = "grey",
                                              width=2000, height=800).generate(text)

                        fig = plt.figure(figsize = (8, 8), facecolor = 'white') 
                        plt.title("Tweets mais relevantes", fontsize=12)
                        plt.imshow(wordcloud, interpolation = 'bilinear')
                        plt.axis('off') 
                        st.pyplot(fig=fig)
                        
                with st.expander(f"Tweets sobre o assunto:"):                        
                    if df.verified.sum() > 0:
                        for tweet in tweets:                                        
                            r = requests.get(f"https://publish.twitter.com/oembed?url={tweet['url']}")
                            col1, col2 = st.columns([.1, .9])
                            col1.image(tweet['user']['profileImageUrl'])
                            col2.markdown(r.json()['html'], unsafe_allow_html=True)
                            st.markdown('---')
                    else:
                        st.info("Não foram encontrados tweets.")


                     
                       

if __name__ == '__main__':
    main()