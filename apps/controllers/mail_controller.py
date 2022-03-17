from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message

def bulk(subject, recipients, html, sender, attachments, cc, bcc):

    with mail.connect() as conn:
        for rec in recipients:
            msg = Message(
                subject = subject,
                recipients = [rec],
                #html = 'Your activation link is {}'.format(link),
                html = html.format(link),
                sender = sender,
                attachments = attachments,
                cc = cc,
                bcc = bcc
            )

    return msg

def generate_mail(subject, recipients, html, sender, attachments, cc, bcc):
    if len(message_query.recipients) == 1:
        msg = Message(
            subject = subject,
            recipients = recipients,
            #html = 'Your activation link is {}'.format(link),
            html = html.format(link),
            sender = sender,
            attachments = attachments,
            cc = cc,
            bcc = bcc
        )
    elif len(message_query.recipients) > 1:
        msg = bulk(
            subject = subject,
            recipients = recipients,
            #html = 'Your activation link is {}'.format(link),
            html = html.format(link),
            sender = sender,
            attachments = attachments,
            cc = cc,
            bcc = bcc
        )
        
    return msg