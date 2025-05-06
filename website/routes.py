import os
import requests
from website import app, mail, recaptcha
from website.forms import MyForm
from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from flask_mail import Message


@app.context_processor
def inject_year():
    current_year = datetime.now().year
    return dict(year=current_year)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    recaptcha_site_key = app.config['RECAPTCHA_SITE_KEY']
    recaptcha_secret_key = app.config['RECAPTCHA_SECRET_KEY']
    
    if form.validate_on_submit():
        # Get the honeypot field value
        honeypot = request.form.get('username')
        
        # Check if the honeypot field is filled
        if honeypot:
            # Honeypot is filled; treat this as a bot submission
            flash('Your submission was flagged as spam.', 'danger')
            return redirect(url_for('contact'))
        
        # Get the reCAPTCHA response token from the form
        recaptcha_response = request.form.get('recaptcha-token')
        
        # Verify the reCAPTCHA response with Google's API
        payload = {'secret': recaptcha_secret_key, 'response': recaptcha_response}
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()

        if result.get('success'):
            # If reCAPTCHA validation is successful, send the email
            msg = Message('New Message',
                          sender=os.getenv('MAIL_USERNAME'),
                          recipients=[os.getenv('MAIL_HOTMAIL')])
            msg.body = f"Name: {request.form['name']}\n"\
                       f"Email: {request.form['email']}\n"\
                       f"Phone: {request.form['phone']}\n"\
                       f"Message: {request.form['message']}"
            mail.send(msg)
            return render_template("contact.html", msg_sent=True, form=form, recaptcha_site_key=recaptcha_site_key)
        else:
            # If reCAPTCHA validation fails, display an error
            return render_template("contact.html", msg_sent=False, form=form, recaptcha_site_key=recaptcha_site_key, recaptcha_failed=True)
    
    return render_template("contact.html", msg_sent=False, form=form, recaptcha_site_key=recaptcha_site_key)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500
