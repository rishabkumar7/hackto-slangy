from flask import Flask, request
import requests
import re
import os
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print (incoming_msg)
    filter_msg= re.findall('\(.*?\)', incoming_msg)
    string_without_parentheses = re.sub(r"[\(\)]",'',filter_msg[0])
    term = string_without_parentheses
    print (term)
    resp = MessagingResponse()
    msg = resp.message()
    
    url = "https://urban-dictionary7.p.rapidapi.com/v0/define"
    querystring = {"term":f'"{term}"'}
    headers = {
	            "X-RapidAPI-Key": os.getenv('APIKEY'),
	    "X-RapidAPI-Host": "urban-dictionary7.p.rapidapi.com"
    }
    responded = False
    if '(' in incoming_msg:
        # return the meaning of slang
        r = requests.request("GET", url, headers=headers, params=querystring)
        if r.status_code == 200:
            data = r.json()
            new_line='\n'
            quote = f'Meaning of {term}: {new_line}{data["list"][0]["definition"]} {new_line}{new_line}Here is an example {data["list"][0]["example"]}'
        else:
            quote = 'Sorry try again.'
        msg.body(quote)
        responded = True
    if not responded:
        msg.body('Sorry, didnt get that')
    return str(resp)


if __name__ == '__main__':
    app.run(port=6000)
