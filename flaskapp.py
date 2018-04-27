from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello():
    return render_template('index.html')

def genpassword(wordbank):    
    #find words that fit the min and max word lengths specified in the form
    validchoices = []
    for word in wordbank:
        #print(len(word) <= int(request.args['maxword']))
        if len(word) >= int(request.args['minword']) and len(word) <= int(request.args['maxword']):
            validchoices.append(word.strip())
    #print(validchoices)

    #find a group of four words that fit the min and max password lengths specified in the form
    validpassword = False
    while not validpassword:
        mypassword = []
        length = 0
        for i in range(4):
            randomword = validchoices[random.randrange(0, len(validchoices))]
            mypassword.append(randomword)
            length += len(randomword)

        #print(mypassword)
        #print(length)
        #print(request.args['minpass'])
        #print(request.args['maxpass'])
        #print(length >= int(request.args['minpass']))
        #print(length <= int(request.args['maxpass']))

        if length <= int(request.args['maxpass']):
            if length >= int(request.args['minpass']):
                validpassword = True
    try:
        if request.args['make'] == 'numsub':
            for j in range(0, len(mypassword)):
                word = mypassword[j]
                word = list(word)
                #print(word)
                for i in range(0, len(word)): 
                    #print(word[i])               
                    if word[i] == 'a':
                        word[i] = '4'
                    if word[i] == 'e':
                        word[i] = '3'
                    if word[i] == 'o':
                        word[i] = '0'
                word = ''.join(word)
                #print(word)
                mypassword[j] = word
    except:
        pass

    return mypassword

@app.route('/processform')
def render_table():
    #read file
    datafile = open("static/wordbank.txt", 'r')
    wordbank = datafile.readlines()
    datafile.close()
    #print(wordbank)
    #print(request.args['maxword'])
    #print(request.args['minword'])
    
    #get an array of passwords
    passwords = []
    for i in range(0, 10):
        passwords.append(genpassword(wordbank))
    
    return render_template('passtable.html', passlist = passwords)

if __name__=='__main__':
    app.run(debug=True)