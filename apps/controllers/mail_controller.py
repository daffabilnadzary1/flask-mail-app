from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

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

def bulk(mail, token, subject, recipients, html, sender):

    with mail.connect() as conn:
        i = 0
        for rec in recipients:
            link = url_for('confirm_email', token = token[i], _external = True)
            msg = Message(
                subject = subject,
                recipients = [rec],
                #html = 'Your activation link is {}'.format(link),
                html = html.format(link),
                sender = sender,
                #attachments = attachments,
                #cc = cc,
                #bcc = bcc
            )
            mail.send(msg)
            i += 1

def generate_mail(mail, token, subject, recipients, html, sender):
    if len(recipients) == 1:
        link = url_for('confirm_email', token = token, _external = True)
        msg = Message(
            subject = subject,
            recipients = recipients,
            html = html.format(link),
            sender = sender,
            #attachments = attachments,
            #cc = cc,
            #bcc = bcc
        )
        mail.send(msg)

    elif len(recipients) > 1:
        bulk(
            mail,
            token, 
            subject = subject,
            recipients = recipients,
            html = html,
            sender = sender,
            #attachments = attachments,
            #cc = cc,
            #bcc = bcc
        )    