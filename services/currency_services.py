from data.database import read_query, insert_query, update_query, delete_query
from data.models import Currency
import requests


def convert_currency(sender_value: str, receiver_value: str, amount: float = 1):
    if sender_value == receiver_value:
        return amount
    try:
        result = requests.get(f"https://api.apilayer.com/fixer/convert%sto={receiver_value}"
                              f"&from={sender_value}&amount={amount}",
                              headers={"apikey": "OEyWGDiRdkYIhAj5CdDxLIwQlHUHgPxz"})
        current = result.json()
        return float(current["result"])
    except KeyError:
        if sender_value == "EUR":
            return float(amount) * 1.95
        elif sender_value == "BGN":
            return float(amount) * 0.51


def get_all(search: str = None):
    if search:
        data = read_query("SELECT * FROM \"walletdb\".\"currency\" WHERE name = %s", (search,))
        return next((Currency.from_query(*row) for row in data), None)
    else:
        data = read_query("SELECT * FROM \"walletdb\".\"currency\"")
        return (Currency.from_query(*row) for row in data)


def get_by_id(id: int):
    data = read_query("SELECT * FROM \"walletdb\".\"currency\" WHERE id = %s", (id,))

    return next((Currency.from_query(*row) for row in data), None)


def create(name: str):
    data = insert_query("INSERT INTO \"walletdb\".\"currency\" (name) VALUES(%s)", (name,))
    return data
