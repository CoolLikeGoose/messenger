import time
from datetime import datetime
from flask import Flask, request

messages = [
    {'username': 'Jack', 'text': 'hello', 'time': time.time()},
    {'username': 'Marry', 'text': 'Hi jack', 'time': time.time()}
]

app = Flask(__name__)

users = {
    'jack': 'black',
    'marry': '12345'
}

@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/status')
def status():
    return {
        'status': True,
        'time': datetime.now().strftime('%Y/%m/%d - %H:%M:%S'),
        'users': len(users),
        'messages': len(messages)

    }


@app.route('/send', methods=["POST"])
def send():
    """
    request: {'username': 'str','password': 'str' ,'text': 'str'}
    response: {'ok': true}
    """
    data = request.json
    username = data['username']
    password = data['password']
    text = data['text']

    if username in users:
        password_real = users[username]
        if password_real != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'time': time.time()})
    return {'ok': True}


@app.route('/history')
def history():
    """
    request: ?after = float
    response: {
        'messages': [
            {'username': 'str', 'text': 'str', 'time': float},
            ...
        ]
    }
    """
    after = float(request.args['after'])

    filter_messages = [message for message in messages if after < message['time']]

    return {'messages': filter_messages}


app.run()
