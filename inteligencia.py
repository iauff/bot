# -*- coding: iso-8859-1 -*-
from multiprocessing import Process
import sys
import time
import signal
import sentimentos
import twitterutil
import json
import pdb
import pln
import noticias
import tweepy
import assuntos

#Este programa tem como função analisar os posts dos amigos e gera novos posts
#
# Observação:
# A inteligência do programa está em analizar o que os amigos estão
# postanto e comentando, identificar a idéia principal e baseado na idéia
# principal fazer uma publicação. Na sequência ele monitora os posts e
# responde ao comentário com um humor correspondente a reação dos amigos.

num_execucoes = 0

def inteligencia():

    # controle informativo do número de execuções
    global num_execucoes
    num_execucoes += 1
    print ("[" + str(num_execucoes) + "]")

    #######################################################################
    # Obtem os tweets
    #######################################################################
    postsUser = twitterutil.getPostsUser()
    postsAmigos = twitterutil.getPostsAmigos()
    print ("[tweets]\n    tweets user: " + str(len(postsUser)) + "\n    tweets amigos: " + str(len(postsAmigos)))

    #######################################################################
    # Definir os assuntos
    #######################################################################
    #pares_palavras = pln.obtemBigramas(postsAmigos)
    assuntosPrincipais = []
    assuntosPrincipais = assuntos.assuntosPrincipaisDosPosts(postsAmigos)
    print ("[assuntos] " )
    print (assuntosPrincipais)
    print ("    assunto escolhido: " + assuntosPrincipais[0]['descricao'] + " e " + assuntosPrincipais[1]['descricao'])


    if len(postsAmigos) > 0:
        #######################################################################
        # Definir personalidade
        #######################################################################
        sentimento = 'neutral' #incializa humor como neutro
        retweeta = 0 #inicializa retweeta como 0 (não)
        sentimento_amigos = sentimentos.sentimentoPrincipal(postsAmigos, assuntosPrincipais[0]['descricao'], assuntosPrincipais[1]['descricao'])

        maioria = 1 #define quanto é a maioria dos posts (dos amigos)
        if (len(postsAmigos)>1):
            maioria = (len(postsAmigos)//2)+1

        ## positive se:
        tweets_com_like = 0
        retweets = 0
        #sentimento = 'positive'
        # maioria dos seus tweets tem like ou  (favorite_count > 0)
        # maioria dos seus tweets from retweetados ou (retweet_count > 0)
        # maioria dos sentimentos dos posts dos amigos são positivos (sentimento = 'positive')
        for post in postsUser:
            if post['favorite_count'] > 0:
                tweets_com_like += 1
            if post['retweet_count'] > 0:
                retweets += 1

        print ("[personalidade] definindo...")
        print ("    retweets: " + str(retweets))
        print ("    tweets com like: " + str(tweets_com_like))
        print ("    sentimento dos amigos: " + str(sentimento_amigos))

        if (tweets_com_like >= maioria) or (retweets >= maioria) or (sentimento_amigos == 'positive'):
            sentimento = 'positive'

        ## negativo se:
        # maioria dos comentários são negativos ou (sentimento = 'negative')
        # nenhum tweet tem like (favorite_count == 0)
        elif (tweets_com_like < 1) or (sentimento_amigos == 'negative'):
            sentimento = 'negative'

        ## neutro se:
        # não se enquadra em nenhum dos sentimentos anterior

        print ("[personalidade]\n    humor: " + sentimento)

        #######################################################################
        # Obter notícia
        #######################################################################
        print ("[noticia]")
        noticia = noticias.obtemNoticia(assuntosPrincipais[0]['descricao'], assuntosPrincipais[1]['descricao'], sentimento)
        print ("    texto: "     + (str(noticia['texto'])[:100] + '...') if len(str(noticia['texto'])) > 100 else str(noticia['texto']))
        print ("    sentimento: " + str(noticia['sentimento']))
        print ("    url: "     + str(noticia['link']))

        #######################################################################
        # Prepara o tweet (refraseando a notícia)
        #######################################################################
        mensagem = noticias.obtemMensagem(sentimento)
        mensagem = mensagem + " " + noticia['texto']

        #######################################################################
        # Realiza o tweet
        #######################################################################
        print ("[publicando]")
        print ("    texto: "  + (mensagem[:100] + '...') if len(str(mensagem)) > 100 else str(mensagem))
        try:
            twitterutil.api.update_status(mensagem[:139])
        except tweepy.error.TweepError as e:
            print( "    erro: %s" % e )


if __name__ == '__main__':
    comando = 'p'
    while True:
        if (comando =='p'):
            inteligencia()
        elif (comando =='s'):
            break
        comando=input('> p=processar, s=sair:')
