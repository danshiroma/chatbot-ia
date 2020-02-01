#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# inicio leitura dataset intencao frase
# array dataset frase
array_frase = []
# array dataset intencao
array_intencao = []

filepath = 'dataset_intencao_frase.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       #print("Line {}: {}".format(cnt, line.strip()))
       line = line.replace("\n","").replace("\ufeff","")
       line_array = line.split("|")
       #print(line_array)
       array_intencao.append(line_array[0])
       array_frase.append(line_array[1])
       line = fp.readline()
       cnt += 1
# fim leitura dataset intencao frase

# inicio leitura dataset etiquetas entidades
# dic etiquetas
dic_etiquetas = {}
filepath = 'etiquetadores.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       #print("Line {}: {}".format(cnt, line.strip()))
       line = line.replace("\n","").replace("\ufeff","")
       line_array = line.split(":")
       #print(line_array)
       dic_etiquetas[line_array[0]] = line_array[1].split(",")
       line = fp.readline()
       cnt += 1
# fim leitura dataset entidades

print("Intencoes: ", len(array_intencao), " - ", array_intencao)
print("Frases: ", len(array_frase), " - ", array_frase)
print("Dic etiquetas: ", len(dic_etiquetas), " - ", dic_etiquetas)

# inicio treinamento modelo
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,strip_accents='unicode')

corpus = np.array(array_frase)
#corpus = np.array(['Boa noite gostaria de saber valor do aluguel do espaço de festa', 'Seria para o dia 07/12', 'e o valor', 'qual o aluguel'])
x = vectorizer.fit_transform(corpus)
#print(x)
y = np.array(array_intencao)
#y = np.array(['sobre_espaco', 'data_possibilidade', 'valor', 'valor'])

# treinamento do modelo com KNN - usando n_neighbors = 1
model = KNeighborsClassifier(n_neighbors=1)
model.fit(x,y)

# fim treinamento modelo

#dicionario para intencoes
intencoes = {
    "saudacao": "Olá {fulano} em que podemos ajudar?",
    "horario": "O nosso horário da locação para o espaço é das 8h às 21h.",
    "sobre_espaco": "O nosso espaço possui:\n - Cozinha \n - Freezer \n - Fogão industrial \n - Churrasqueira com espetos e grelha. \n - 10 mesas e 40 cadeiras \n - Bancos de madeira (namoradeira) \n - WIFI \n - Pergolado com redário \n - Limpeza \n - Piscina 8x4 + Prainha (ideal para crianças) \n - Aparelho de Som\n\n Endereço: Rua 60, nº64, Bairro Nova Campo Grande (próximo ao aeroporto). ",
    "valor": "De segunda a quinta é R$ 600 e entre sexta e domingo é R$800.",
    "forma_pagamento": "O pagamento pode ser feito tanto em dinheiro como em cartão. Pedimos que metade do valor seja pago quando o contrato é assinado e a outra metade depois do evento.",
    "data_possibilidade": "As seguintes datas estão ocupadas: {datas}. Para combinarmos melhor, me passe seu número de contato e entraremos em contato com você",
    "visita": "Sim claro, iremos adorar te receber aqui! Me passe seu número de contato e entraremos em contato com você =D.",
}

datas_indisponiveis = ['12/12/2019', '16/12/2019', '24/12/2019', '04/01/2020']

# funcao que customiza saudacao colocando nome no usuario
def msg_saudacao(msg_chat, frase_intencao):
    return frase_intencao.replace("{fulano}", msg_chat.first_name + " " + msg_chat.last_name)

# funcao que inseri nas resposta as datas disponiveis
def msg_data_possibilidade(msg_chat, frase_intencao):
    dias = ""
    for n in range(len(datas_indisponiveis)): dias += datas_indisponiveis[n] + ", "
    frase = frase_intencao.replace("{datas}", dias)
    return frase

# funcao reconhece_entidade descrita no trabalho para ser implementada
def reconhece_entidades(dic_etiquetas_param, msg):
    rec_dic = {}
    msg_array = msg.split()
    for s in msg_array:
        for d in dic_etiquetas_param:
            if(s.lower() in dic_etiquetas_param[d]):
                #print("Achou Etiqueta entidade: ", s)
                #print(d not in rec_dic)
                if (d not in rec_dic):
                    array_str = []
                    array_str.append(s)
                    #print(array_str)
                    rec_dic[d] = array_str
                    #print(rec_dic[d])
                else:
                    array_str = rec_dic[d]
                    array_str.append(s)
                    rec_dic[d] = array_str

    return rec_dic

# palavras com respostas padroes que nao possuem intencao definida
#palavras_sem_intencao = ["ok", "blz", "entendi", "certo"]
#print(palavras_sem_intencao)
#print("teste".lower() not in palavras_sem_intencao)

# integracao telegram
# No telegram procure pelo usuario EspacoShiromaBot
bot = telebot.TeleBot("1063681683:AAECsaZW2GsRVOZbeCa_QWemBIM9XucRhJg")

# funcao handler chamada ao usuario iniciar uma conversa com o bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Olá, tudo bem? Somos do Espaço Shiroma, aqui você poderá tirar dúvidas e solicitar informações sobre o nosso Espaço. Em que posso ser útil?")

# funcao handler executada a cada mensagem enviada pelo usuario
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print(message.chat)
    #bot.reply_to(message, message.text)
    msg = message.text
    inst = vectorizer.transform([msg])
    intencao = model.predict(inst)
    print(intencao[0])
    resposta_intencao = ""
    #print(msg.split())
    if (intencao[0] == 'saudacao'):
        resposta_intencao = msg_saudacao(message.chat, intencoes[intencao[0]])
    elif (intencao[0] == 'data_possibilidade'):
        resposta_intencao = msg_data_possibilidade(message.chat, intencoes[intencao[0]])
        print(reconhece_entidades(dic_etiquetas_param= dic_etiquetas, msg= msg))
    else:
        resposta_intencao = intencoes[intencao[0]]
    
    bot.send_message(message.chat.id, resposta_intencao)

print("---------- Aguardando mensagens ----------")
# funcao que mantem o programa em execucao aguardando mensagens dos usuarios
bot.polling()

