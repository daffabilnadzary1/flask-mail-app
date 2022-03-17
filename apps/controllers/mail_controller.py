from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

def render_html(type, email, link):
    if type == "account_confirmation":
        return render_template('account_confirmation.html', email = email, link =  link)
    elif type == "reset_password":
        return render_template('apps/templates/account_confirmation.html')

def generate_token(recipients):
    if len(recipients) == 1:
        s = URLSafeTimedSerializer('tokenrandomizer')
        token = s.dumps(recipients[0], salt = 'email-confirm')
    elif len(recipients) > 1:
        s = URLSafeTimedSerializer('tokenrandomizer')
        token = []
        for rec in recipients:
            unique_token = s.dumps(rec, salt = 'email-confirm')
            token.append(unique_token)
    return token

def bulk(mail, token, **kwargs):
    with mail.connect() as conn:
        i = 0
        for rec in kwargs["recipients"]:
            link = url_for('confirm_email', token = token[i], _external = True)
            msg = Message(
                subject = kwargs["subject"],
                recipients = [rec],
                #html = 'Your activation link is {}'.format(link),
                html = render_html(type = "account_confirmation", email = rec, link = link),
                sender = kwargs["sender"],
                attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
            )
            mail.send(msg)
            i += 1

def generate_mail(mail, token, **kwargs):
    if len(kwargs["recipients"]) == 1:
        link = url_for('confirm_email', token = token, _external = True)
        msg = Message(
            subject = kwargs["subject"],
            recipients = kwargs["recipients"],
            html = render_html(type = "account_confirmation", email = kwargs["recipients"], link = link),
            sender = kwargs["sender"],
            attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
            cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
            bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
        )
        mail.send(msg)

    elif len(kwargs["recipients"]) > 1:
        bulk(
            mail,
            token, 
            subject = kwargs["subject"],
            recipients = kwargs["recipients"],
            #html = kwargs["html"],
            sender = kwargs["sender"],
            attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
            cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
            bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
        )   