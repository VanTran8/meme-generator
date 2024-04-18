import random
import os
import requests
from itertools import chain
from flask import Flask, render_template, abort, request
from PIL import Image

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeGenerator

app = Flask(__name__)

meme = MemeGenerator('./_data/photos/dog')


def setup():
    """ Load all resources """

    quote_files = ['/workspace/home/_data/DogQuotes/DogQuotesTXT.txt',
                   '/workspace/home/_data/DogQuotes/DogQuotesDOCX.docx',
                   '/workspace/home/_data/DogQuotes/DogQuotesPDF.pdf',
                   '/workspace/home/_data/DogQuotes/DogQuotesCSV.csv']

    quotes = list()
    
    for quote_file in quote_files:
        quotes += Ingestor.parse(quote_file)

    images_path = "./_data/photos/dog/"
    
    imgs = list()
    
    for file in os.listdir(images_path):
        if file.endswith(".jpg"):
            imgs.append(os.path.join(images_path, file))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    # select a random image from imgs array
    img = random.choice(imgs)
    # select a random quote from the quotes array
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)

@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    # Create temp file
    tmp = f'./tmp/{random.randint(0,100000000)}.png'
    # Use requests to save the image from the image_url
    # form param to a temp local file.
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')
    try:
        r = requests.get(image_url, verify=False)
        with open(tmp, 'wb') as img:
            img.write(r.content)  
            path = meme.make_meme(tmp, body, author)
            print(path)
            #Remove the temporary saved image.
            os.remove(tmp) 
    except:
        print("Invalid Image URL")
        return render_template('meme_form.html')

    return render_template('meme.html', path=path)

if __name__ == "__main__":
    app.run()
