from flask import Flask, render_template, url_for
from flask_mail import Mail

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)