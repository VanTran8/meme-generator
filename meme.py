import os
import random

import argparse
from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeGenerator


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        if path.split('.')[-1] != 'jpg':
            raise Exception(f'Unsupported file type {path.split(".")[-1]}')
        img = path
    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeGenerator('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default=None, help="Path to an image file.")
    parser.add_argument('-b', '--body', type=str, default=None, help="Quote body.")
    parser.add_argument('-a', '--author', type=str, default=None, help="Quote author.")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
