from flask import Flask, render_template, request, flash
import requests
import random
import pyttsx3
import pyperclip
import secrets
from pathlib import Path
import time

response = requests.get("https://zenquotes.io/api/quotes")          # gets response from pre determined api
quoteList = response.json()             # formats response into json
quote = "Start finding quotes by pressing the 'New Quote' button"
author = "System"


app = Flask(__name__)

''' Create or Find secret key -- create only used once -- afterwards creates key for session'''
SECRET_FILE_PATH = Path(".flask_secret")
try:
    with SECRET_FILE_PATH.open("r") as secret_file:
        app.secret_key = secret_file.read()
except FileNotFoundError:
    # Let's create a cryptographically secure code in that file
    with SECRET_FILE_PATH.open("w") as secret_file:
        app.secret_key = secrets.token_hex(32)
        secret_file.write(app.secret_key)

def getQuote(quoteList):
    quoteFull = random.choice(quoteList)        # selects random quote from quoteList
    quoteList.remove(quoteFull)         # removes quote from quoteList after uses
    
    quote = quoteFull["q"]          # gets the sub list value "q" for the quote
    author = quoteFull["a"]         # gets the sub list value "a" for the author

    return quote, author            # returns the quote and author values


@app.route("/", methods=['GET', 'POST'])
def index():
    
    global quoteList, quote, author        # gives access to quoteList var initialised at start of code
    status = ""
    
    if not quoteList:       # if the list is empty then get newList and set quoteList var to new list
        response = requests.get("https://zenquotes.io/api/quotes")      # access api
        quoteList = response.json()

    if request.method == 'POST':        # if <form> with method "post" is pressed

        if "new-quote" in request.form:
            quote, author = getQuote(quoteList)         # get quote information

        elif "text-to-speech" in request.form:
            engine = pyttsx3.init()         # initialise text-to-speech engine
            volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
            engine.setProperty('volume', 0.3)    # setting up volume level  between 0 and 1
            
            text = f"{quote} by {author}"
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            
            del(engine)           

        elif "copy-to-clipboard" in request.form:
            text = f"\"{quote}\" --{author}"
            pyperclip.copy(text)
            time.sleep(0.5)         # sleeps program for time to allow for copied popup to show
        
    return render_template('index.html', quoteText=quote, authorText=author)       # returns html page with quote and author values


if __name__ == "__main__":
    app.run(debug=True)
    