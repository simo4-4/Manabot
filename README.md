## Inspiration
The growing need of project managers and a social network for the work place

## What it does
Manabot resides in the encrypted Mana Network where you can communicate with your peers but also schedule your day. If Manabot ever gives you an odd reply, you can simply 
tell it that its previous reply was wrong or weird and it'll prompt you on how it could improve. 

## How we built it
I used python for the backend, socket.io for its realtime bidirectional communication, flask to connect python to the frontend, and tensorflow to train a sequential neural network. For the frontend, I used html, css, and jquery.  



## Challenges we ran into
Connecting socket.io and training the model for all the different options and then basing actions on those different options.

## Accomplishments that we're proud of
It works really well for a prototype and I'm happy that its auto-learn function works !

## What we learned
Learned a lot !
Learned to use flask, socketio and tensor flow


## What's next for ManaBot 
A better front-end, gather more data, more customization, and most importantly authentication using firebase! I also want Manabot to remind you of your tasks according to their level of difficulty, but also to break long-term tasks into short-term ones and remind you to complete those accordingly.  


## To run:
Go to the folder where chatbot.py is saved on the command line
then enter "python chatbot.py"
Make sure you have flask installed !

![alt-text](taskfunction.png)
