import random
import json
import pickle
import numpy as np 

from flask import Flask, render_template
from flask_socketio import SocketIO

import nltk 

from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('ogintents.json').read())

pattern = "i love you"
response = "i love you too"
newtag = "love"

jsondict = {
  "tag": "Ford",
  "patterns": "Mustang",
  "response": "1964"
}

#intents['intents'] is a list which contains dicts

#print(intents['intents'][0])

jsondict['tag'] = newtag
jsondict['patterns'] = [pattern]
jsondict['response'] = [response]

#appends a new intent with a new tag
# intents['intents'].append(jsondict)

# for i,intent in enumerate(intents['intents']):
#     print(intent["tag"])



#find the tag and adds a response
for i,intent in enumerate(intents['intents']):
    if "love" in intent["tag"]:
        intent["response"].append("luv u")


with open("ogintents.json", "w") as write_file:
    json.dump(intents, write_file)

# for key in intents['intents']:
#     print(tag)
#     print("\n")
