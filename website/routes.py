import os
from website import app, mail
from website.forms import MyForm
from datetime import datetime
from flask import render_template, request
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


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if form.validate_on_submit():
        msg = Message('New Message',
                      sender='noreply@gmail.com',
                      recipients=[os.getenv('MAIL_HOTMAIL')])
        msg.body = f"Name: {request.form['name']***REMOVED***\n"\
                   f"Email: {request.form['email']***REMOVED***\n"\
                   f"Phone: {request.form['phone']***REMOVED***\n"\
                   f"Message: {request.form['message']***REMOVED***"
        mail.send(msg)
        return render_template("contact.html", msg_sent=True, form=form)
    return render_template("contact.html", msg_sent=False, form=form)


# Data Engineering route
@app.route('/portfolio/dataengineering')
def data_engineering():
    return render_template('dataengineering.html')

# Data Analysis route
@app.route('/portfolio/dataanalysis')
def data_analysis():
    return render_template('dataanalysis.html')

# Web Development route
@app.route('/portfolio/webdevelopment')
def web_development():
    return render_template('webdevelopment.html')

# GUI Applications route
@app.route('/portfolio/guiapplications')
def gui_applications():
    return render_template('guiapplications.html')


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500