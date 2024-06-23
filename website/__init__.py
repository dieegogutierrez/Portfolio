import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from flask_recaptcha import ReCaptcha

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
mail = Mail(app)
app.config['RECAPTCHA_SITE_KEY'] = os.getenv("RECAPTCHA_SITE_KEY")
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv("RECAPTCHA_SECRET_KEY")
recaptcha = ReCaptcha(app)

from website import routes