from flask import render_template, redirect, url_for, flash, Blueprint, request
from forms import CreateWalletForm, WalletAccessForm
from services import wallet_services, user_services
from flask_login import current_user
from data.models import Wallet, WalletResponse
from services import currency_services

wallet_bp = Blueprint('create_wallet', __name__)
wallet_access_bp = Blueprint('wallet_access', __name__)
remove_wallet_access_bp = Blueprint('remove_wallet_access', __name__)
add_wallet_access_bp = Blueprint('add_wallet_access', __name__)
view_wallets_bp = Blueprint('view_wallets', __name__)


@view_wallets_bp.route("/view_wallets")
def view_wallets():
    wallets = wallet_services.get_all_wallets_response(current_user.id)

    return render_template("wallets.html", current_user=current_user, wallets=wallets)


@wallet_bp.route("/create_wallet", methods=["GET", "POST"])
def create_wallet():
    form = CreateWalletForm()
    if form.validate_on_submit():
        name = form.currency.data
        currency = currency_services.get_all(name)

        current_wallet = Wallet(name=form.name.data, balance=0, currency_id=currency.id, user_id=current_user.id)
        add_wallet = wallet_services.create_wallet(current_wallet)

        flash(f"{current_wallet.name} Wallet Created!")
        return redirect(url_for("home.home"))

    return render_template("create_wallet.html", form=form)


@wallet_access_bp.route("/wallet_access", methods=["GET", "POST"])
def wallet_access():
    all_wallets = wallet_services.get_all_by_access(current_user.id)

    return render_template('wallet_access.html', wallets=all_wallets)


@remove_wallet_access_bp.route("/remove_wallet_access/<int:wallet_id>/<user_name>", methods=["GET", "POST"])
def remove_wallet_access(wallet_id, user_name):
    remove_access = wallet_services.remove_access(wallet_id, user_name)

    flash("Access removed!")

    return redirect(url_for('wallet_access.wallet_access'))


@add_wallet_access_bp.route("/add_wallet_access", methods=["GET", "POST"])
def add_wallet_access():
    form = WalletAccessForm()

    if form.validate_on_submit():
        user = user_services.get_by_email(form.user_email.data)
        if not user:
            flash("User with that email do not exist!")
            return render_template('wallet_access.html')
        get_wallet = wallet_services.get_by_wallet_name(form.wallet.data)

        add = wallet_services.add_access(get_wallet.id, user.id)

        flash("Access granted!")
        return redirect(url_for("wallet_access.wallet_access"))

    return render_template("wallet_access_form.html", form=form)
