from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

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

if __name__ == '__main__':
    app.run(debug = True)