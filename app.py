from flask import Flask, render_template, request
import requests
import random



response = requests.get("https://zenquotes.io/api/quotes")      # gets response from pre determined api
quoteList = response.json()             # formats response into json

app = Flask(__name__)

def getQuote(quoteList):
    quoteFull = random.choice(quoteList)        # selects random quote from quoteList
    quoteList.remove(quoteFull)         # removes quote from quoteList after uses
    
    quote = quoteFull["q"]          # gets the sub list value "q" for the quote
    author = quoteFull["a"]         # gets the sub list value "a" for the author

    return quote, author            # returns the quote and author values


@app.route("/", methods=['GET', 'POST'])
def index():
    
    global quoteList        # gives access to quoteList var initialised at start of code
    
    if not quoteList:       # if the list is empty then get newList and set quoteList var to new list
        response = requests.get("https://zenquotes.io/api/quotes")      # access api
        quoteList = response.json()

    if request.method == 'POST':        # if button with method "post" is pressed
        quote, author = getQuote(quoteList)         # get quote information
        return render_template('index.html', quoteText=quote, authorText=author)        # returns html page with new quote and author values
    else:
        return render_template('index.html', quoteText="", authorText="")       # initial template, empty

if __name__ == "__main__":
    app.run(debug=True)
    