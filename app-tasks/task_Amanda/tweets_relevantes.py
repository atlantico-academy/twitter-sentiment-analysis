import cv2
import json
import nltk
import requests
from datetime import timedelta
import streamlit as st
from streamlit_tags import st_tags
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from snscrape.modules.twitter import TwitterSearchScraper as tss

def get_tweets(tag, start_date, end_date, limit):
    query_str = f"{tag} lang:pt"# since:{start_date} {end_date}"
    tweets_list = []
    for i, tweet in enumerate(tss(query_str).get_items()):
        json_tweet = tweet.json()
        tweets_list.append(json.loads(json_tweet))
        if i >= limit:
            break
    return tweets_list


st.title('Ainda pensando ...')

tags = st_tags(
            label = f'Tags de busca',
            text = 'Adicione tags separadas por vírgula',
            maxtags = 3
        )
st.info('Adicione tags separadas por vírgula e pressione Enter para adicionar mais tags e comparar.')
col1, col2 = st.columns(2)
start_date = col1.date_input("Data inicial")
end_date = col2.date_input("Data final")
pesquisar = st.button("Pesquisar")

all_tweets = {}
if pesquisar:
    with st.spinner("Buscando tweets. Isso pode demorar..."):
        for tag in tags:
            all_tweets[tag] = get_tweets(tag, start_date, end_date, 100)

nltk.download('stopwords')
STOPWORDS = nltk.corpus.stopwords.words('portuguese')
# Lista de stopword
stopwords = set(STOPWORDS)
stopwords.update(["a","b","c","d","fato","ela","estou","nem","tudo","p","pq","quando","dele","RT","por","de",'dar','pois','em','um','da','ser','aqui','vou','dos','ter','não','ao','sou','seu','à','n','se','esse','uma','mais','ele','fazendo','você','pode','essa','é','mas','segue','pra','isso','vez','para','muito','pelo','pela','são', 'na','vamos','https','t','co','c','New','eu','seis','retweets','ano','pessoa','likes','vai','que','ou','anos','7dias','tirou','tem','q','0','O','e','os','assim','só','mesmo','tá','pro','votar','pessoas','vc'])

with st.expander('nuvens de palavras'):
    
    for tag, tweets in all_tweets.items():
        st.markdown(f"### {tag}")
        textos = []
        for tweet in tweets:
            textos.append(tweet['content'])
        texto = ' '.join(textos)
       
        wordcloud_md = WordCloud(stopwords=stopwords, background_color="black",
                      width=1600, height=800).generate(texto)

        # Mostra a imagem final
        fig, ax = plt.subplots(figsize=(10,6))
        ax.imshow(wordcloud_md, interpolation='bilinear')
        ax.set_axis_off()
        plt.title("", fontsize=18)
        st.pyplot(fig=fig)
    
            
with st.expander('tweets mais relevantes'):
    for tag, tweets in all_tweets.items():
        st.markdown(f"### {tag}")
        textos = []

        for tweet in tweets:
            textos.append(tweet['content'])
            
            if tweet['user']['verified'] == True:
                r = requests.get(f"https://publish.twitter.com/oembed?url={tweet['url']}")
                col1, col2 = st.columns([.1, .9])
                col1.image(tweet['user']['profileImageUrl'])
                col2.markdown(r.json()['html'], unsafe_allow_html=True)
                st.markdown('---')
    

