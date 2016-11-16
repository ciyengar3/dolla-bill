import os
import sys
import json
#from dbHandler import addTransaction, totalCategoryCount, update_spending_timeline, updatePersonalExpenses, getPersonalExpenses, getTimelineTable, getTotalCategoryTable
import requests
from flask import Flask, request


ACCESS_TOKEN = ""
VERIFY_TOKEN = ""
app = Flask(__name__)

recentUser = ""

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    r = requests.get("http://intuit-mint.herokuapp.com/api/v1/user/transactions")
    r = r.json()
    transactions = requests.get('https://api.mlab.com/api/1/databases/dollabill/collections/transactions?apiKey=wLezyqn7VhF2KWrRGNisuVi_nJqKIvEB')
    transactions = transactions.json()
    personal_spending_by_category = requests.get("https://api.mlab.com/api/1/databases/dollabill/collections/personal_spending_category?apiKey=wLezyqn7VhF2KWrRGNisuVi_nJqKIvEB")
    personal_spending_by_category = personal_spending_by_category.json()
    print personal_spending_by_category
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    # recentUser = getRecentUser()
                    # if recentUser != str(sender_id):
                    # setRecentUser(str(sender_id))

                    payload = {'q': message_text, 'access_token': 'I4KSSLOIN2QRNWWD4RSAO7X6D4ZVMVNY'}
                    translation = (requests.get('https://api.wit.ai/message', params=payload)).json()
                    print translation
                    if "entities" in translation:
                        entities = translation.get('entities')
                        if "category" in entities and "amount_of_money" in entities:
                            send_message(sender_id, "Your " + str(entities.get('category')[0].get('value')) + " budget has been set to $" + str(entities.get('amount_of_money')[0].get('value')) + " per month.")
                        else:
                            send_message(sender_id, "Hi, I'm Bill!")
                            send_message(sender_id, "I can help you stay on top of your spending and better manage your money.")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def respond_to_message(messaging_event):
    message_text = messaging_event["message"]["text"]
    sender_id = messaging_event["sender"]["id"]
    if (message_text != "ignore"):
        # for transaction in r.json():
        send_message("Hi, it is BILL")
    else:
        send_message(sender_id, "Ignored")

def getRecentUser(self):
    return self.recentUser

def setRecentUser(self, user):
    self.recentUser = user

def send_message(recipient_id, message_text):
    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))


    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

'''
    def send_recipient(self, recipient_id, payload, notification_type=NotificationType.regular):
        payload['recipient'] = {
            'id': recipient_id
        }
        payload['notification_type'] = notification_type.value
        return self.send_raw(payload)

def send_message(self, recipient_id, message, notification_type=NotificationType.regular):
    return send_recipient(recipient_id, {
        'message': message
    }, notification_type)
'''


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
