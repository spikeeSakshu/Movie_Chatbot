# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 23:07:02 2019

@author: Spikee
"""


#https://privacypolicies.com/privacy/view/62250556b849b30c64e2dc77758e50f1

from flask import Flask, request as req
import os, sys
from witIntegration import wit_response
import movie as mov
from pymessenger import Bot
import random
import requests

app = Flask(__name__)

user = dict()


FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
PAGE_ACCESS_TOKEN = 'EAAFiW7LUD7MBAAh3iYYz3WzvMMOryCVUtsB0BZAzgySIZCARQq4Nbd9gYQ1OQZAq65BofDyvFgaQyWfPydz5tLVKao29qpoWCFjeZClUokWJ7pZCDMgnPoVUMheJKchAzgG9zH1DCkHi5RAZBQ2kNT3s5hW4xFcmZCYfpfmEfdzquFNcWOo9UgH'# paste your page access token here>"
   
bot = Bot(PAGE_ACCESS_TOKEN)

greeting_responses=['Hi','Hey','Hello','I am glad! You are talking to me....']

emoji= ['\U0001F642', '\U0001F607', '\U0001F929', '\U0001F643', '\U0001F609']
@app.route("/", methods=['GET'])
def listen():
    if req.args.get("hub.mode") == 'subscribe' and req.args.get('hub.challenge'):
       if not req.args.get('hub.verify_token') =='hello_chat':
           return 'Mismatch', 403
       return req.args.get("hub.challenge")
    else:
        return "hello world", 200

def log(message):
    print(message)
    sys.stdout.flush()

def greeting():
    return random.choice(greeting_responses)
        
@app.route("/", methods=['POST'])
def webhook():

    data =req.get_json()
    log(data)
    
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                
                #ID's
                sender_id = messaging_event['sender']['id']
                recipient_id =  messaging_event['recipient']['id']
#                
#                log("SENDER ID")
#                log(sender_id)
                
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    
                    else:
                        messaging_text = 'no text' 
                

                    response = ""
                    response2 = ""
                    hell = "1. Find Rating of any Movie... Just Type 'Rating of Movie_Name' "+"\n"+"2. Suggest you a Movie"
                    name =""
                    trigger=0
                    try:
                        if sender_id not in user:
                            trigger+=1
                
                            user_details_url = "https://graph.facebook.com/v2.6/%s"%sender_id
                            user_details_params = {'fields':'first_name,last_name,profile_pic,id', 'access_token':PAGE_ACCESS_TOKEN} 
                            user_details = requests.get(user_details_url, user_details_params).json() 
                            
                            response2= hell
                        
                            if 'error' in user_details:
                                user[sender_id]={'first_name': ''}
                            else:
                                user[sender_id] = user_details
                    
                    except:
                        user[sender_id] = ""
                        print("Not present")
                    
                    
                    log("TEXT "+messaging_text)                    
                    entity = wit_response(messaging_text)
                    
                    
                    
                        
                    if 'greet' in entity:
                        response+= greeting()+" "+user[sender_id]['first_name']+"\n"
                    
                    
                    elif 'alvida' in entity:
                        response+= 'BYE'
                    
                    elif 'ok' in entity:
                        response+= random.choice(emoji)
                        
                    elif 'rate_movie' in entity:
                        log("Inside "+messaging_text)
                        name = messaging_text.split(' ',2)
                        log(name)
                        response+= mov.call(name[2])
                        name=""
                        
                    
                    else:
                        response= "Sorry, I didn't Understand!!"   
                    
                    if 'help' in entity:
                        response= ""
                        response2= hell
                    
                    bot.send_text_message(sender_id, response)
                
                    log("Response="+response)
                    
                    if response2 is not "" and 'IMDB' not in response :
                        bot.send_text_message(sender_id, response2)
 

                    
                
    return "ok", 200



if __name__ == '__main__':
   app.run(host= '0.0.0.0', debug= True)
   
#
#user=dict()
#sender_id = 2221169804813128
#try:
#    if sender_id not in user:
#                
#        user_details_url = "https://graph.facebook.com/v2.6/%s"%sender_id
#        user_details_params = {'fields':'first_name,last_name,profile_pic,id', 'access_token':PAGE_ACCESS_TOKEN} 
#        user_details = requests.get(user_details_url, user_details_params).json() 
#        
#        if 'error' in user_details:
#            user[sender_id]={'first_name': ''}
#        else:
#            user[sender_id] = user_details
#except:
#    user[sender_id]['first_name']=""
#    print("Not present")
#   
#user[sender_id]['first_name']
#
#user = dict()
   
