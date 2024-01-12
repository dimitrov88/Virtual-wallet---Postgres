from data.models import BaseUser
from data.database import read_query, insert_query, update_query, delete_query


def create_user(user: BaseUser):
    data = insert_query("INSERT INTO \"walletdb\".\"user\" (email, password, name) VALUES(%s,%s,%s)",
                        (user.email, user.password, user.name))

    return data


def get_by_id(id):
    data = read_query("SELECT * FROM \"walletdb\".\"user\" WHERE id=%s", (id,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def get_by_email(email):
    data = read_query("SELECT * FROM \"walletdb\".\"user\" WHERE email=%s", (email,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def get_by_name(name):
    data = read_query("SELECT * FROM \"walletdb\".\"user\" WHERE name=%s", (name,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def add_contact(user1_id, user2_id):
    data = insert_query("INSERT INTO \"walletdb\".\"contacts\" (user_id1, user_id2) VALUES(%s,%s)", (user1_id, user2_id))

    return data


def get_all_contacts_by_id(id):
    data = read_query("SELECT u.id, u.email, u.password, u.name FROM \"walletdb\".\"user\" u "
                      "JOIN \"walletdb\".\"contacts\" c  ON (c.user_id1 = u.id OR c.user_id2 = u.id) "
                      "WHERE c.user_id1 = %s and u.id != %s;", (id, id))

    return (BaseUser.create_base_user(*row) for row in data)


def remove_contact_by_id(id, current_user_id: int):
    data = update_query("DELETE FROM \"walletdb\".\"contacts\" WHERE user_id1 = %s and user_id2 = %s or user_id2 = %s and user_id1 = %s",
                        (id, current_user_id, id, current_user_id))

    return data
