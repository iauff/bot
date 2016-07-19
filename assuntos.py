 # -*- coding: iso-8859-1 -*-
import nltk #sudo pip install nltk
import pdb #sudo pip install pdb
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

#obtem a idéia principal
def assuntosPrincipaisDosPosts(posts):
    #inicialização
    contapalavras = {}
    for post in posts:
        substantivos = inferenomes(nltk.word_tokenize(post['text']))
        for subst in substantivos:
            if subst not in contapalavras.keys():
                contapalavras[subst] = 1
            else:
                contapalavras[subst] += 1

    #obtem ideia_principal
    contador = 0
    ideia_principal = ""
    for palavra in contapalavras:
        if contapalavras[palavra] > contador:
            ideia_principal = palavra
            contador = contapalavras[palavra]
            contapalavras[palavra] = 0

    #obtem ideia_secundaria
    contador = 0
    ideia_secundaria = ""
    for palavra in contapalavras:
        if contapalavras[palavra] > contador:
            ideia_secundaria = palavra
            contador = contapalavras[palavra]
            contapalavras[palavra] = 0
    return [{'descricao': ideia_principal}, {'descricao': ideia_secundaria}]

#obtem a idéia principal
def assuntoPrincipal(texto):
    #inicialização
    contapalavras = {}
    substantivos = inferenomes(nltk.word_tokenize(texto))
    for subst in substantivos:
        if subst not in contapalavras.keys():
            contapalavras[subst] = 1
        else:
            contapalavras[subst] += 1

    #obtem ideia_principal
    contador = 0
    ideia_principal = ""
    for palavra in contapalavras:
        if contapalavras[palavra] > contador:
            ideia_principal = palavra
            contador = contapalavras[palavra]
            contapalavras[palavra] = 0

    #obtem ideia_secundaria
    contador = 0
    ideia_secundaria = ""
    for palavra in contapalavras:
        if contapalavras[palavra] > contador:
            ideia_secundaria = palavra
            contador = contapalavras[palavra]
            contapalavras[palavra] = 0
    return [{'descricao': ideia_principal}, {'descricao': ideia_secundaria}]


#função para filtrar os tokens.
#TODO(Paulo): na próxima versão treinar um tagger PoS para pegar só nomes.
def inferenomes(tokens):
    #inicialização
    newtokens = []
    for token in tokens:
        #padroniza todos os tokens em minúsculas
        token = token.lower()
        # remove tokens pequenos e terminados em r, ndo (verbos) e algumas palavras predefinidas
        if  (len(token) > 4) and (token[-1:] != "r") and (token[-3:] != "ndo") and (token not in getPalavrasReservadas()):
            newtokens.insert(0,token)
    return newtokens

def getPalavrasReservadas():
    palavras = ['gosto', 'faço']
    return palavras

if __name__ == "__main__":
    #teste
    posts = [
                {'from':'me', 'texto':'Eu odeio o vasco', 'comentarios': [{'from':'amigo_01', 'texto':'comentario 1'}, {'from':'amigo_02', 'texto':'comentario 2'}]},
                {'from':'amigo_01', 'texto':'Eu odeio o fluminense', 'comentarios': [{'from':'amigo_01', 'texto':'comentario 3'}, {'from':'amigo_03', 'texto':'fluminense é muito bom!'}]},
                {'from':'amigo_01', 'texto':'Eu adoro o fluminense', 'comentarios': [{'from':'me', 'texto':'comentario 5'}, {'from':'amigo_02', 'texto':'comentario 6'}]},
                {'from':'amigo_01', 'texto':'Fluminense é muito bom!'},
                {'from':'amigo_01', 'texto':'Eu amo o vasco'}
            ]
    #print   assuntosPrincipais(posts)
    print (getBigrams('Eu adoro o fluminense'))
