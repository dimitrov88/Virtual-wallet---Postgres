from flask import render_template, redirect, url_for, flash, Blueprint, request
from forms import CreateTransactionForm, CreateFriendTransactionForm, AddFromCardForm
from services import wallet_services, user_services, transaction_services, currency_services
from flask_login import current_user

transaction_bp = Blueprint('create_transaction', __name__)
friend_transaction_bp = Blueprint('send_to_friend', __name__)
add_money_bp = Blueprint('add_money', __name__)
home_bp = Blueprint('home', __name__)
home_amount_bp = Blueprint('home_amount', __name__)


@home_bp.route('/home')
def home():
    date_sort = request.args.get('date', 'DESC').upper()
    search_term = request.args.get('search', None)

    user_wallet = wallet_services.get_by_user_name(current_user.name)
    user_transactions = transaction_services.get_by_username(current_user.name, date_sort, search_term)

    return render_template("index1.html", current_user=current_user, wallet=user_wallet, transactions=user_transactions)


@home_amount_bp.route('/home/amount')
def home_amount():
    amount_sort = request.args.get('amount', 'ASC').upper()

    user_wallet = wallet_services.get_by_user_name(current_user.name)
    user_transactions = transaction_services.get_by_username_amount(current_user.name, amount_sort)

    return render_template("index1.html", current_user=current_user, wallet=user_wallet, transactions=user_transactions)


@transaction_bp.route("/create_transaction/<int:current_wallet_id>", methods=["GET", "POST"])
def create_transaction(current_wallet_id: int):
    form = CreateTransactionForm()
    if form.validate_on_submit():
        if form.wallet.data:
            sender_wallet = wallet_services.get_by_wallet_name(form.wallet.data)
        else:
            sender_wallet = wallet_services.get_by_id(current_wallet_id)

        receiver_wallet = wallet_services.get_by_email(form.receiver.data)
        if not receiver_wallet:
            flash("User with that email doesn't exist!")
            return redirect(url_for("create_transaction.create_transaction", current_wallet_id=sender_wallet.id))

        amount = float(form.amount.data)
        if sender_wallet.balance < amount:
            flash("You do not have enough money.")
            return redirect(url_for("create_transaction.create_transaction", current_wallet_id=sender_wallet.id))

        if sender_wallet.currency_id == receiver_wallet.currency_id:
            to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount, amount)

        else:
            if sender_wallet.currency_id == 1:
                check_currency = currency_services.convert_currency("EUR", "BGN")
            else:
                check_currency = currency_services.convert_currency("BGN", "EUR")

            to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount, amount * check_currency)

        flash("Transaction complete!")
        return redirect(url_for("home.home"))

    return render_template("make_transaction.html", form=form)


@friend_transaction_bp.route("/send_to_friend/<int:contact_id>", methods=["GET", "POST"])
def send_to_friend(contact_id: int):
    form = CreateFriendTransactionForm()
    friend = user_services.get_by_id(contact_id)
    if form.validate_on_submit():
        if form.wallet.data:
            sender_wallet = wallet_services.get_by_wallet_name(form.wallet.data)
        else:
            sender_wallet = wallet_services.get_by_user_id(current_user.id)

        receiver_wallet = wallet_services.get_by_email(friend.email)
        if not receiver_wallet:
            flash("User with that email doesn't exist!")
            return redirect(url_for("send_to_friend.send_to_friend", contact_id=contact_id))

        amount = float(form.amount.data)
        if sender_wallet.balance < amount:
            flash("You do not have enough money.")
            return redirect(url_for("send_to_friend"))

        if sender_wallet.currency_id == receiver_wallet.currency_id:
            to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount, amount)

        else:
            if sender_wallet.currency_id == 1:
                check_currency = currency_services.convert_currency("EUR", "BGN")
            else:
                check_currency = currency_services.convert_currency("BGN", "EUR")
            to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount, amount * check_currency)

        flash("Transaction complete!")
        return redirect(url_for("home.home"))
    return render_template("send_to_friend.html", form=form, contact=friend)


@add_money_bp.route("/add_money", methods=["GET", "POST"])
def add_money():
    form = AddFromCardForm()
    if form.validate_on_submit():
        amount = form.amount.data
        wallet = wallet_services.get_by_wallet_name(form.wallet_name.data)
        to_add = wallet_services.add_from_card(wallet, float(amount))

        flash("Money added successfully!")
        return redirect(url_for("home.home"))
    return render_template("add_from_card.html", form=form)
