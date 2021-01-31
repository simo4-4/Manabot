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
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

goals = []
initg = 2
tagtofind = ""
question = ""
resp = ""
jsondict = {
  "tag": "Ford",
  "patterns": "Mustang",
  "response": "1964"
}
jsondict2 = {
  "user_name": "Ford",
  "receiver": "Mustang",
  "message": "1964"
}

print(classes)

#use the model by defining 4 functions

#breaks sentence into individual words and then lemmatizes each word in the sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#convert sentence into bag words, so a list of 0 and 1 indicating if the word is there or not
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words) #should be sentence_words i think
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

#create bag of words, predict result from that bag, then enumerate a
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True) #sort prob in reverse to get high prob first
    return_list = []

    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])}) #create
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def print_goals():

    global jsondict2
    global goals
    print(goals)
    for goal in goals:
            jsondict2["message"] = "You need to " + goal
            socketio.emit('manabot response', jsondict2, callback=messageReceived)


def find_tag(tag):
    for intent in intents['intents']:
        if tag in intent["tag"]:
            intent["patterns"].append(question)
            intent["responses"].append(resp)
            return
    
    jsondict['tag'] = tag
    jsondict['patterns'] = [question]
    jsondict['response'] = [resp]
    intents['intents'].append(jsondict)
    return


#needs to retrain model
def end_of_the_day():
    print("retrain model")



# initg 4 and 5
def wrong_response(wrong_message):
    global jsondict
    global initg
    global tagtofind
    global question
    global resp
    

    if initg == 5 :
        if wrong_message.lower() == "right":
            initg == 1
            return "Okay!"

        else:

            if "".__eq__(tagtofind):
                tagtofind = wrong_message
                #return "mmmh"
            
            elif "".__eq__(question):
                jsondict2["message"] = "What was your question?"
                socketio.emit('manabot response', jsondict2, callback=messageReceived)
                question = wrong_message
                #return "okay then"

            elif "".__eq__(question):
                jsondict2["message"] = "What should I have answered to that?"
                socketio.emit('manabot response', jsondict2, callback=messageReceived)
                resp = wrong_message
                initg = 1
                find_tag(tagtofind)
                return "thanks!"

    initg = 5
    jsondict2["message"] = "In which category would your question have fit in? If it fits in none, name a new category and I'll take it into account"
    socketio.emit('manabot response', jsondict2, callback=messageReceived)
    jsondict2["message"] = "If my answer was actually right just write RIGHT"
    socketio.emit('manabot response', jsondict2, callback=messageReceived)
    for tag in classes:
        jsondict2["message"] = tag
        socketio.emit('manabot response', jsondict2, callback=messageReceived)

       
def action_per_intent(tag,message_in):
    
    print("tag is " + tag)
    if (tag=="goals"):
        print_goals()
    
    elif (tag=="wrong_answer"):
        wrong_response(message_in)



def init_goals(message_in):
    global initg
    mess = message_in.lower()
    if (mess == "done"):
        initg = 1
        return "I've taken note of your tasks for the day!"
    goals.append(mess)
    return "Something else?"

def manabot_run(message_in):
        global initg
        if(initg == 2):
            initg = 0
            return "Hey! Please list your tasks for the day and enter DONE when you are done listing them! "

        elif (initg == 0):
            return init_goals(message_in)

        # initg = 5 means that the prev was wrong and recognized
        elif (initg == 5):
            return wrong_response(message_in)

        #initg 1 is this
        else:
            message = message_in
            ints = predict_class(message)
            res = get_response(ints, intents)
            action_per_intent(ints[0]['intent'],message_in) 
            return res




#flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('home.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('usernamee&receiiver: ' + json["user_name"] + json["receiver"])
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    if (json["receiver"]=="Manabot"):
        print('To Manabot:' + json["message"])
        json["message"]=manabot_run(json["message"])
        socketio.emit('manabot response', json, callback=messageReceived)
    


if __name__ == '__main__':
    socketio.run(app, debug=True)


#end flask

#print("GO! ManagementBot is running")
#print("What are your goals for the day? Press ENTER after each goal and type DONE when you are done listing your goals!")


# mess = ""
# while True:
#     print("Goal:")
#     mess = input("")
#     if (mess == "DONE"):
#         break
#     goals.append(mess)






            
