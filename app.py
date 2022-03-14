from flask import Flask, render_template, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route("/")
def index():
    msg = Message('Hey There!', recipients = ['soboxid723@xindax.com'])
    msg.html = "<b>This is a test email sent from me.</b>"

    with app.open_resource('test.jpg') as test:
        msg.attach('test.jpg', 'image/jpeg', test.read())

    mail.send(msg)

    msg = Message(
        subject = '',
        recipients = '',
        body = '',
        html = '',
        sender = '',
        cc = [],
        bcc = [],
        attachments = [],
        reply_to = [],
        date = 'dateobject',
        charset = '',
        extra_headers = {'': ''},
        mail_options = [],
        rcpt_options = []
    )
    return 'Message has been sent!'

@app.route("/bulk")
def bulk():
    users = [{'name': 'Anthony', 'email': 'email@email.com'}]

    with mail.connect() as conn:
        for user in users:
            msg = Message('Bulk!', recipients = [user['email']])
            msg.body('Hey There!')

            conn.send(msg)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'GET':
        return '<form action = "/" method = "POST"><input name = "email"><input type = "submit"></form>'
    
    email = request.form['email']
    token = s.dumps(email, salt = 'email-confirm')

    msg = Message('Confirmation Email', sender = 'daffabilnadzary1@gmail.com', recipients = [email])
    link = url_for('confirm_email', token = token, _external = True)

    msg.body = 'Your activation link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt = 'email-confirm', max_age = 3600)

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    
    except BadTimeSignature:
        return '<h1>The token is incorrect!</h1>'

    return 'The token works!'

if __name__ == "__main__":
    app.run(debug = True)