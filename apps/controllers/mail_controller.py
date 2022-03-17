from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

def render_account_confirm(email, link):
    return render_template('account_confirmation.html', email = email, link =  link)

def render_reset_password(email, link):
    return render_template('reset_password.html', email = email, link =  link)

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

def bulk(type, mail, token, **kwargs):
    if type == "account_confirmation":
        with mail.connect() as conn:
            i = 0
            for rec in kwargs["recipients"]:
                link = url_for('confirm_email', token = token[i], _external = True)
                msg = Message(
                    subject = kwargs["subject"],
                    recipients = [rec],
                    #html = 'Your activation link is {}'.format(link),
                    html = render_account_confirm(email = rec, link = link),
                    sender = kwargs["sender"],
                    attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                    cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                    bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
                )
                mail.send(msg)
                i += 1
    elif type == "reset_password":
        with mail.connect() as conn:
            i = 0
            for rec in kwargs["recipients"]:
                link = url_for('confirm_email', token = token[i], _external = True)
                msg = Message(
                    subject = kwargs["subject"],
                    recipients = [rec],
                    #html = 'Your activation link is {}'.format(link),
                    html = render_reset_password(email = rec, link = link),
                    sender = kwargs["sender"],
                    attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                    cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                    bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
                )
                mail.send(msg)
                i += 1

def generate_mail(type, mail, token, **kwargs):
    if type == "account_confirmation":
        if len(kwargs["recipients"]) == 1:
            link = url_for('confirm_email', token = token, _external = True)
            msg = Message(
                subject = kwargs["subject"],
                recipients = kwargs["recipients"],
                html = render_account_confirm(email = kwargs["recipients"], link = link),
                sender = kwargs["sender"],
                attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
            )
            mail.send(msg)

        elif len(kwargs["recipients"]) > 1:
            bulk(
                type = "account_confirmation",
                mail = mail,
                token = token, 
                subject = kwargs["subject"],
                recipients = kwargs["recipients"],
                #html = kwargs["html"],
                sender = kwargs["sender"],
                attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
            )
    elif type == "reset_password":
        if len(kwargs["recipients"]) == 1:
            link = url_for('confirm_email', token = token, _external = True)
            msg = Message(
                subject = kwargs["subject"],
                recipients = kwargs["recipients"],
                html = render_reset_password(email = kwargs["recipients"], link = link),
                sender = kwargs["sender"],
                attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
            )
            mail.send(msg)

        elif len(kwargs["recipients"]) > 1:
            bulk(
                type = "reset_password",
                mail = mail,
                token = token, 
                subject = kwargs["subject"],
                recipients = kwargs["recipients"],
                #html = kwargs["html"],
                sender = kwargs["sender"],
                attachments = (kwargs["attachments"] if kwargs["attachments"] is not None else None),
                cc = (kwargs["cc"] if kwargs["attachments"] is not None else None),
                bcc = (kwargs["bcc"] if kwargs["attachments"] is not None else None)
            )