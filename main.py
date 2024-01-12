import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, abort, render_template, request, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager, current_user
from routers import transaction, user, wallet
from forms import LoginForm
from services import user_services
import smtplib
from dotenv import load_dotenv

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''
load_dotenv()
my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(transaction.transaction_bp)
app.register_blueprint(transaction.friend_transaction_bp)
app.register_blueprint(user.register_bp)
app.register_blueprint(user.login_bp)
app.register_blueprint(user.my_contacts_bp)
app.register_blueprint(user.add_contact_bp)
app.register_blueprint(user.remove_contact_bp)
app.register_blueprint(transaction.add_money_bp)
app.register_blueprint(user.logout_bp)
app.register_blueprint(transaction.home_bp)
app.register_blueprint(transaction.home_amount_bp)
app.register_blueprint(wallet.wallet_bp)
app.register_blueprint(wallet.wallet_access_bp)
app.register_blueprint(wallet.add_wallet_access_bp)
app.register_blueprint(wallet.remove_wallet_access_bp)
app.register_blueprint(wallet.view_wallets_bp)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None and user_id.isdigit():
        return user_services.get_by_id(int(user_id))
    return None


@app.route('/')
def wellcome_page():
    form = LoginForm()

    return render_template("wellcome_page.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            # Construct the email message
            subject = 'New Contact Form Submission'
            body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'
            sender_email = my_email
            recipients = [my_email]  # Add recipient email address

            msg = MIMEMultipart()
            msg['From'] = my_email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            connection.sendmail(sender_email, recipients, msg.as_string())

            flash('Your message has been sent!', 'success')
        return render_template("contact.html", current_user=current_user)
    return render_template("contact.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
