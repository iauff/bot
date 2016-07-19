#coding:utf-8
from datetime import date, timedelta
import requests #sudo pip install requests
import json     #sudo pip install json
from random import randint
import sentimentos
import pdb

def obtemNoticia(assunto1, assunto2, humor_posts):

    #url de busca do twitter
    url = "https://e4cf4d83-2d9d-4e00-a157-2fb27959e81e:cEJVoOJKmQ@cdeservice.mybluemix.net:443/api/v1/messages/search"

    #define data de 7 dias atrás
    data = (date.today() - timedelta(days=7))
    posted_from = data.strftime("%Y-%m-%d")

    #define query
    payload = {'q': (assunto1 + ' ' + assunto2  + ' lang:pt ' +
                    'posted:' + posted_from + ''),
                    'from': '0',
                    'size': '10'} # consulta até 20 tweets
    r = requests.get(url, payload)


    #trata resposta
    resultado = json.loads(r.text)
    mensagem = ""
    link = ""
    sentimento = ""
    noticias = []
    noticia = {'texto': 'Sem novidades...', 'link': 'nenhum', 'sentimento': 'nenhum'}

    if (resultado['search']['results'] > 0):
        tweets = resultado['tweets']
        #analisa sentimento do tweet para tentar pegar o mesmo humor do bot,
        #para isso teste se cada um dos tweets encontrados está no mesmo humor
        #e utiliza o primeiro que coincidir para fazer a postagem, caso nenhum
        #coincida, retorna uma qualquer da lista.
        for tweet in tweets:
            mensagem =  tweet['message']['body']
            link = tweet['message']['link']
            tweetid = tweet['message']['id']
            sentimento = sentimentos.obtemSentimento(mensagem)

            if (sentimento == humor_posts):
                noticia = {'texto': mensagem, 'link': link, 'sentimento': sentimento}
                noticias.insert(0,noticia)

        if (noticias == []): #pega qq noticia
            ultimo_humor='talvez' #inicializei
            if (humor_posts=='positive'):
                ultimo_humor = 'bom'
            elif (humor_posts=='negative'):
                ultimo_humor = 'ruim'
            payload = {'q': (ultimo_humor + ' is:verified lang:pt'),
                            'from': '0',
                            'size': '10'} # consulta até 20 tweets
            r2 = requests.get(url, payload)
            #trata resposta
            resultado2 = json.loads(r2.text)
            tweets2 = resultado2['tweets']
            for tweet2 in tweets2:
                mensagem = tweet2['message']['body']
                link = tweet2['message']['link']
                noticia = {'texto': mensagem, 'link': link, 'sentimento': 'nenhum'}
            noticias.insert(0,noticia)
    i = randint(0,len(noticias)-1) # sorteia uma das notícias selecionadas para evitar repeticao
    return noticias[i]

#obtem uma mansagem em função do sentimento
def obtemMensagem(sentimento):
    mensagens = []
    if sentimento == 'positive':
        mensagens = [
                    "Legal, olha só isso.",
                    "Show de bola!",
                    "Fantástico! Veja isso também.",
                    "Que maravilha, você já viu isso?"
                    ]
    elif sentimento == 'neutral':
        mensagens = [
                    "Certo, olha só.",
                    "Hum, já viu isso?",
                    "Olha isso.",
                    "Olha esse post."
                    ]
    elif sentimento == 'negative':
        mensagens = [
                    "Que desagradável.",
                    "É complicado. Olha isso.",
                    "Estou desanimando.",
                    "Isso é um problema."
                    ]
    i = randint(0,len(mensagens)-1) # sorteia uma das mensagens evitando repeticao
    return mensagens[i]

if __name__ == '__main__':
    #teste
    print (obtemNoticia("futebol", "positive"))
