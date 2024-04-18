# Overview
```
Simple meme generator created for Udacity Nanaodegree program.
Meme generator generates memes including an image with an overlaid quote.
```



## Setting up and Running
### Setup virtual environment inside project folder and activate.
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
### Install python deps
   ```sh
   pip install -r requirements.txt
   sudo apt install poppler-utils
   ```


## Usage

### On CLI
```
usage: meme.py [-h] [--body BODY] [--author AUTHOR] [--path PATH]

Generate meme!!

optional arguments:
  -h, --help       show this help message and exit
  --body BODY      the quote body
  --author AUTHOR  author of the quote
  --path PATH      file path of the image
```


### Flask Web Development Server

```sh
python3 app.py
```

and go to http://127.0.0.1:5000/