from data.database import read_query, insert_query, update_query, delete_query
from data.models import Transactions, TransactionResponse


def get_by_id(id):
    data = read_query("SELECT * FROM \"walletdb\".\"transaction\" WHERE id=%s"), (id,)

    return next((Transactions.from_query(*row) for row in data), None)


def get_by_username(name, date_sort, search_term=None):
    new = '''SELECT t.id, s.name, r.name, t.amount, c.name, t.date FROM \"walletdb\".\"transaction\" t
     JOIN \"walletdb\".\"user\" s on s.id = t.sender_id 
     JOIN \"walletdb\".\"user\" r on r.id = t.receiver_id 
     JOIN \"walletdb\".\"currency\" c on c.id = t.currency_id '''

    if not search_term:
        new += f"WHERE s.name = '{name}' OR r.name = '{name}'"
    else:
        new += f"WHERE s.name = '{name}' AND r.name = '{search_term}' or s.name = '{search_term}' and r.name = '{name}'"

    new += f" ORDER BY t.date {date_sort}"
    data = read_query(new)

    return (TransactionResponse.from_query(*row) for row in data)


def get_by_username_amount(name, amount_sort):
    data = read_query(f"SELECT t.id, s.name, r.name, t.amount, c.name, t.date FROM \"walletdb\".\"transaction\" t "
                      "JOIN \"walletdb\".\"user\" s on s.id = t.sender_id "
                      "JOIN \"walletdb\".\"user\" r on r.id = t.receiver_id "
                      "JOIN \"walletdb\".\"currency\" c on c.id = t.currency_id "
                      f"WHERE s.name = '{name}' or r.name='{name}' "
                      f"ORDER BY t.amount {amount_sort}")

    return (TransactionResponse.from_query(*row) for row in data)
