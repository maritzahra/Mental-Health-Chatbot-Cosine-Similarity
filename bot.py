from flask import Flask, request, jsonify, render_template
import random
from newspaper import Article
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import warnings
import re

from gtts import gTTS
import IPython.display as ipd
import time
from io import BytesIO

nltk.download('punkt', quiet=True)

app = Flask(__name__)

article = Article('https://www.kompasiana.com/nainnahalisha1704/617e8c5979b2394961324782/mental-illness-salah-siapa')
article.download()
article.parse()
article.nlp()

article2 = Article('https://www.kompasiana.com/bryanitazizah/6062b6db8ede48269735bb73/stress-yuk-kenali-mental-illness-ini')
article2.download()
article2.parse()
article2.nlp()

article3 = Article('https://www.qubisa.com/article/penyakit-mental-dan-mengatasinya#showContent')
article3.download()
article3.parse()
article3.nlp()

article4 = Article('https://www.halodoc.com/artikel/ini-pentingnya-menjaga-kesehatan-mental-remaja')
article4.download()
article4.parse()
article4.nlp()

corpus = article.text + article2.text + article3.text + article4.text 
print(corpus)

# Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #A list of sentences

# Print the list of sentences
print(sentence_list)


def greeting_response(text):
    text = text.lower()

    #List sapaan dari bot kepada user
    bot_greetings = ['hi','hello','hola', 'halo', 'hai', 'yuhuu', 'selamat pagi juga', 'selamat siang juga', 'selamat sore juga', 'selamat malam juga']

    #List sapaan dari user kepada bot
    user_greetings = ['hi', 'hey', 'hello', 'Halo','Hai','wassup', 'permisi', 'punten', 'selamat pagi', 'selamat siang', 'selamat sore', 'selamat malam']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

    #Random response to greeting
    def gratitude_response(text):
        text=text.lower()

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index

def bot_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response= ''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break

        if response_flag==0:
            bot_response=bot_response+" "+"Mohon maaf, perkataan Anda tidak dimengerti. Tanyakan hal lain!" #Memberikan respon ini apabila sistem tidak mengenal kata yang user input

        sentence_list.remove(user_input)

        return bot_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_input = data.get('user_input', '')
    response = greeting_response(user_input) or bot_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False)

