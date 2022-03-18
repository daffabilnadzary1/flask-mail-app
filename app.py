from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
from apps.models.model import MessageQuery
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
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
s = URLSafeTimedSerializer('tokenrandomizer')

@app.route("/email_confirmation", methods = ["POST"])
def send_email_confirmation():
    message_query = MessageQuery()

    message_query.subject = request.json['subject']
    message_query.recipients = request.json['recipients']
    message_query.html = (None if request.json["html"] == 0 else request.json["html"])
    message_query.sender = request.json['sender']
    message_query.cc = (None if request.json["cc"] == 0 else request.json["cc"])
    message_query.bcc = (None if request.json["bcc"] == 0 else request.json["bcc"])
    message_query.attachments = (None if request.json["attachments"] == 0 else request.json["attachments"])

    token = generate_token(message_query.recipients)

    generate_mail(
        mail = mail,
        token = token,
        type = "account_confirmation",
        subject = message_query.subject,
        recipients = message_query.recipients,
        html = message_query.html,
        sender = message_query.sender,
        attachments = message_query.attachments,
        cc = message_query.cc,
        bcc = message_query.bcc
    )
    
    return 'Email is sent to {}!'.format(message_query.recipients)

@app.route("/reset_password", methods = ["POST"])
def send_reset_password():
    message_query = MessageQuery()

    message_query.subject = request.json['subject']
    message_query.recipients = request.json['recipients']
    message_query.html = (None if request.json["html"] == 0 else request.json["html"])
    message_query.sender = request.json['sender']
    message_query.cc = (None if request.json["cc"] == 0 else request.json["cc"])
    message_query.bcc = (None if request.json["bcc"] == 0 else request.json["bcc"])
    message_query.attachments = (None if request.json["attachments"] == 0 else request.json["attachments"])

    token = generate_token(message_query.recipients)

    generate_mail(
        mail = mail,
        token = token,
        type = "reset_password",
        subject = message_query.subject,
        recipients = message_query.recipients,
        html = message_query.html,
        sender = message_query.sender,
        attachments = message_query.attachments,
        cc = message_query.cc,
        bcc = message_query.bcc
    )
    
    return 'Email is sent to {}!'.format(message_query.recipients)

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