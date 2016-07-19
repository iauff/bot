#coding:utf-8
import requests #sudo pip install requests
import json
from random import randint
import pdb

# configuração
# api key jonas: 0f15b34a3eff847e21197ed723e01d4046c9cf1b
# api key paulo: a96796bc93a6c0306c3ea81329ff15baa7c7840d

#obtem sentimento do texto no Alchemy (positive, negative ou neutral)
def obtemSentimento(texto):
    sentimento = "neutral"
    url_alchemy = "https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment"
    payload = {'text': texto,
                'apikey': '2afa3b869d4b307e2e3d3949a4ea1602719f9013',
                'outputMode': 'json'}
    r = requests.post(url_alchemy, payload)
    resultado = json.loads(r.text)
    if 'docSentiment' in resultado:
        sentimento = resultado['docSentiment']['type']
    return sentimento

#obtem o sentimento principal em um conjunto de posts relacionados a uma ideia
def sentimentoPrincipal(posts, ideia1, ideia2):
    #inicialização
    #pdb.set_trace()

    conta_sentimentos = {}
    for post in posts:
        texto = post['text'].lower()
        if (ideia1 in texto) or (ideia2 in texto):  #considera apenas os posts que tem a idéia.
            sentimento = obtemSentimento(texto)
            if sentimento not in conta_sentimentos.keys():
                conta_sentimentos[sentimento] = 1
            else:
                conta_sentimentos[sentimento] += 1


    #obtem sentimento_principal
    contador = 0
    sentimento_principal = ""
    for palavra in conta_sentimentos:
        if conta_sentimentos[palavra] > contador:
            sentimento_principal = palavra
            contador = conta_sentimentos[palavra]
            conta_sentimentos[palavra] = 0

    return sentimento_principal

#obtem o sentimento principal em um conjunto de comentários
def sentimentoComentarios(comments):
    #inicialização
    conta_sentimentos = {}
    for comment in comments:
        texto = comment['message']
        sentimento = obtemSentimento(texto)
        if sentimento not in conta_sentimentos.keys():
            conta_sentimentos[sentimento] = 1
        else:
            conta_sentimentos[sentimento] += 1
    #obtem sentimento_principal
    contador = 0
    sentimento_principal = ""
    for palavra in conta_sentimentos:
        if conta_sentimentos[palavra] > contador:
            sentimento_principal = palavra
            contador = conta_sentimentos[palavra]
            conta_sentimentos[palavra] = 0
    return sentimento_principal

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
    #teste1
    print (obtemSentimento("Que dia lindo!"))

    #teste2
    posts = [
                {'from':'me', 'texto':'Eu odeio o vasco', 'comentarios': [{'from':'amigo_01', 'texto':'comentario 1'}, {'from':'amigo_02', 'texto':'comentario 2'}]},
                {'from':'amigo_01', 'texto':'Eu odeio o fluminense', 'comentarios': [{'from':'amigo_01', 'texto':'comentario 3'}, {'from':'amigo_03', 'texto':'fluminense é muito bom!'}]},
                {'from':'amigo_01', 'texto':'Eu adoro o fluminense', 'comentarios': [{'from':'me', 'texto':'comentario 5'}, {'from':'amigo_02', 'texto':'comentario 6'}]},
                {'from':'amigo_01', 'texto':'Fluminense é muito bom!'},
                {'from':'amigo_01', 'texto':'Eu amo o vasco'}
            ]
    print  (sentimentoPrincipal(posts))
