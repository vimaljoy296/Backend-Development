import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def send_simple_message():
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox7c2266a590224ac2a617e34378064ece.mailgun.org/messages",
        auth=("api"),
        data={
            "from": "vimaljoy296@gmail.com <mailgun@sandbox7c2266a590224ac2a617e34378064ece.mailgun.org>",
            "to": ["vimal.j@atriauniversity.edu.in"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"
        }
    )
    return response

@app.route('/', methods=['GET'])
def index():
    response = send_simple_message()
    return f"Email sent! Status Code: {response.status_code}, Response: {response.text}"

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received")
    datas = request.get_json()
    print(datas)
    return jsonify({"message": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
