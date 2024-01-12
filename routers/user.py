from pydantic_core import ValidationError
from flask import render_template, redirect, url_for, flash, Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from data.models import BaseUser, Wallet
from forms import RegisterForm, ContactForm, LoginForm
from services import wallet_services, user_services
from flask_login import current_user, login_user, logout_user
import os


register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)
my_contacts_bp = Blueprint('my_contacts', __name__)
add_contact_bp = Blueprint('add_contact', __name__)
remove_contact_bp = Blueprint('remove_contact', __name__)
logout_bp = Blueprint('logout', __name__)


@register_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        user = user_services.get_by_email(form.email.data)
        if user:
            # User already exists
            flash("You've already signed up with that email, log in insteaddd!")
            return redirect(url_for('login.login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        try:
            new_user = BaseUser(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password)
        except ValidationError:
            flash("Invalid credentials!")
            return render_template("register.html", form=form, current_user=current_user)

        insert_user = user_services.create_user(new_user)
        first_wallet = (wallet_services.create_first_wallet
                        (Wallet(name=f"{new_user.name} EUR Wallet", balance=0), new_user.name))
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("login.login"))
    return render_template("register.html", form=form, current_user=current_user)


#
#
@login_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = user_services.get_by_email(form.email.data)

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please sign in.")
            return redirect(url_for('register.register'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login.login'))
        else:
            login_user(user)
            return redirect(url_for('home.home'))

    return render_template("login.html", form=form, current_user=current_user)


@logout_bp.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('wellcome_page'))


@my_contacts_bp.route("/my_contacts")
def my_contacts():
    all_contacts = user_services.get_all_contacts_by_id(current_user.id)
    return render_template("contacts.html", current_user=current_user, contacts=all_contacts)


@add_contact_bp.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    form = ContactForm()

    if form.validate_on_submit():
        check_user = user_services.get_by_email(form.email.data)
        if not check_user:
            flash("User with that email doesn't exist!")
            return render_template("contact_form.html", current_user=current_user, form=form)
        elif check_user.email == current_user.email:
            flash("That's your own email!!")
            return render_template("contact_form.html", current_user=current_user, form=form)
        else:
            to_add = user_services.add_contact(current_user.id, check_user.id)
            flash("Contact added successfully!")
            return redirect(url_for("my_contacts.my_contacts"))
    return render_template("contact_form.html", form=form)


@remove_contact_bp.route("/remove_contact/<int:contact_id>")
def remove_contact(contact_id: int):
    to_remove = user_services.remove_contact_by_id(contact_id, current_user.id)
    flash("Contact removed!")
    return redirect(url_for("my_contacts.my_contacts"))
