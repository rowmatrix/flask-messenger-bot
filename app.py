import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":   # make sure this is a page subscription

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):     # someone sent us a message
                    received_message(messaging_event)

                elif messaging_event.get("delivery"):  # delivery confirmation
                    pass
                    # received_delivery_confirmation(messaging_event)

                elif messaging_event.get("optin"):     # optin confirmation
                    pass
                    # received_authentication(messaging_event)

                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
                    # received_postback(messaging_event)

                else:    # uknown messaging_event
                    log("Webhook received unknown messaging_event: " + messaging_event)

    return "ok", 200


def received_message(event):

    sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
    
    # could receive text or attachment but not both
    message = event["message"]
    if message["text"]:
        message_text = message["text"] 
    elif message["attachments"]:
        message_attachments = message["attachment"]   

    # parse message_text and give appropriate response
    if message_text:    
        if message_text == 'image':
            # send_image_message(sender_id)
            pass

        elif message_text == 'button':
            # send_button_message(sender_id)
            pass

        elif message_text == 'generic':
            # send_generic_message(sender_id)
            pass

        elif message_text == 'receipt':
            # send_receipt_message(sender_id)
            pass

        else: # default
            send_text_message(sender_id, "Echo: " + message_text)
            # if message_text == '1':
            #     send_message(sender_id, "one\nHere's a link: https://en.wikipedia.org/wiki/1_%28number%29")
            # elif message_text == '2':
            #     send_message(sender_id, "two\nHere's a link: https://en.wikipedia.org/wiki/2_%28number%29")
            # elif message_text == '3':
            #     send_message(sender_id, "three\nHere's a link: https://en.wikipedia.org/wiki/3_%28number%29")
            # elif message_text == '4':
            #     send_message(sender_id, "four\nHere's a link: https://en.wikipedia.org/wiki/4_%28number%29")
            # else:
            #     send_message(sender_id, "What's this? Google: https://www.google.com/")

    elif message_attachments:
        send_text_message(sender_id, "Message with attachment received")



def send_text_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    call_send_api(message_data)
    

def call_send_api(message_data):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
