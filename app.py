from flask import Flask, request, render_template
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

API_ENDPOINT = 'https://zenquotes.io/api/random'  # API de frases motivacionais

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    nome = request.form.get('nome', None)

    if not nome:
        return render_template('index.html', erro="Você precisa informar um nome!")

    response = requests.get(API_ENDPOINT)

    if response.status_code == 200:
        dados = response.json()
        frase_original = dados[0]['q']  # Obtém a frase em inglês
        autor = dados[0]['a']  # Obtém o autor da frase

        # Traduzindo a frase para o português
        frase_traduzida = GoogleTranslator(source='auto', target='pt').translate(frase_original)

        return render_template('index.html', nome=nome, frase=frase_traduzida, autor=autor)
    else:
        return render_template('index.html', erro="Erro ao buscar a frase motivacional!")

if __name__ == '__main__':
    app.run()