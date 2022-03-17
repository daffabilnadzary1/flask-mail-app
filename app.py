from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
from apps.models.model import MessageQuery, TokenQuery
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

from apps.controllers.mail_controller import generate_mail, generate_token
import json

app = Flask(__name__, template_folder = 'apps/templates')

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'daffabilnadzary1@gmail.com'
app.config['MAIL_PASSWORD'] = 'jctwpcjsizzapyub'
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
s = URLSafeTimedSerializer('tokenrandomizer')

@app.route("/email_confirmation", methods = ["GET", "POST"])
def index():
    message_query = MessageQuery()
    token_query = TokenQuery()

    message_query.subject = request.json['subject']
    message_query.recipients = request.json['recipients']
    message_query.html = (None if request.json["html"] is 0 else request.json["html"])
    message_query.sender = request.json['sender']
    message_query.cc = (None if request.json["cc"] is 0 else request.json["cc"])
    message_query.bcc = (None if request.json["bcc"] is 0 else request.json["bcc"])
    message_query.attachments = (None if request.json["attachments"] is 0 else request.json["attachments"])

    token_query.age = request.json['age']
    token = generate_token(message_query.recipients)

    #link = url_for('confirm_email', token = token, _external = True)
    generate_mail(
        mail,
        token,
        subject = message_query.subject,
        recipients = message_query.recipients,
        #html = 'Your activation link is {}'.format(link),
        html = message_query.html,
        sender = message_query.sender,
        attachments = message_query.attachments,
        cc = message_query.cc,
        bcc = message_query.bcc
    )
    
    return '<h1>The email you entered is {}. The token is {}'.format(message_query.recipients, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt = 'email-confirm', max_age = 60)

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    
    except BadTimeSignature:
        return '<h1>The token is incorrect!</h1>'

    return 'The token works!'

if __name__ == "__main__":
    app.run(debug = True)