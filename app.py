from flask import Flask, request
import openai

app = Flask(__name__)
openai.api_key = "API_KEY"

virtues = ["proactivo", "gusta de la programación", "curioso", "aprende rápido", "extrovertido", "responsable", "alegre"]

def generate_conversation(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must return back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "VERIFY_TOKEN":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    prompt = generate_conversation(message_text)
                    send_message(sender_id, prompt)

    return "ok", 200

def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "PAGE_ACCESS_TOKEN"
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

def log(message):
print(message)

if name == 'main':
app.run()