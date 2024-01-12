import re
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from decimal import Decimal
from pydantic import BaseModel, root_validator, PositiveInt, EmailStr, constr, validator
from pydantic import BaseModel, root_validator, PositiveInt, PositiveFloat, EmailStr, constr
from datetime import datetime, timedelta, date
from typing import Optional, Union, List
from flask_login import UserMixin
from enum import Enum  # StrEnum <- doens't exist in my version !

PREDEFINED_BONUS = 50


# TODO: filters for the user history filtration
class BaseUser(UserMixin, BaseModel):
    id: PositiveInt = None
    email: EmailStr
    password: constr(min_length=8)
    name: constr()

    @classmethod
    def create_base_user(cls, id, email, password, name):
        return cls(id=id, email=email, password=password, name=name)


class Transactions(BaseModel):
    id: Optional[PositiveInt]
    sender_id: PositiveInt
    receiver_id: PositiveInt
    amount: float
    currency_id: Union[constr(), PositiveInt]
    date: Optional[datetime]

    @classmethod
    def from_query(cls, id, sender_id, receiver_id, amount, currency_id, date):
        return cls(id=id, sender_id=sender_id, receiver_id=receiver_id, amount=amount, currency_id=currency_id, date=date)


class TransactionResponse(BaseModel):
    id: Optional[PositiveInt]
    sender: constr()
    receiver: constr()
    amount: float
    currency: Union[constr(), PositiveInt]
    date: Optional[datetime]

    @classmethod
    def from_query(cls, id, sender, receiver, amount, currency, date):
        return cls(id=id, sender=sender, receiver=receiver, amount=amount, currency=currency, date=date)


class Wallet(BaseModel):
    id: PositiveInt = None
    name: constr()
    balance: float
    currency_id: PositiveInt = 1
    user_id: PositiveInt = None

    @classmethod
    def from_query(cls, id, name, balance, currency_id, user_id):
        return cls(id=id, name=name, balance=balance, currency_id=currency_id, user_id=user_id)


class WalletResponse(BaseModel):
    id: PositiveInt = None
    name: constr()
    balance: float
    currency: constr()
    user: constr()

    @classmethod
    def from_query(cls, id, name, balance, currency, user):
        return cls(id=id, name=name, balance=balance, currency=currency, user=user)


class Currency(BaseModel):
    id: PositiveInt
    name: constr()

    @classmethod
    def from_query(cls, id, name):
        return cls(id=id, name=name)
#
# class TransactionFilter(str, Enum):
#     period = "period"
#     sender = "sender"
#     recipient = "recipient"
#     credit = "credit (+)"
#     debit = "debit (-)"
#     amount = "amount"
#     date = "date"
#
#
#
#
# class UsersSearchCriteria(str, Enum):
#     id = "id"
#     username = "username"
#     email = "email"
#     phone = "phone"
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     id: int
#     username: str
#     is_blocked: bool
#     is_verified: bool
#     is_admin: bool
#     email: Optional[str]
#
#     def get_mailing_parameters(self):
#         # ATTENTION:
#         # The user must be inscribed in the database, otherwise self.id will return None !
#         return {"username": self.username,
#                 "email": self.email,
#                 "phone": self.phone,
#                 "conf_link": "/".join(["http://127.0.0.1:8000", "users", f"{self.id}/confirmation"]),
#                 "edit_link": "/".join(["http://127.0.0.1:8000", "users", f"{self.id}/edit_registration"])}
#
#
# class AddedOrDeletedUserContacts(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     phone: str
#
#
# class InvitedUser(BaseModel):
#     id: Optional[int]
#     name: constr(min_length=2, max_length=20)
#     email: EmailStr
#     expiration_date: datetime = datetime.now() + timedelta(days=7)
#     bonus: PositiveFloat = PREDEFINED_BONUS
#     confirmed: bool = False
#
#     def get_mailing_parameters(self):
#         # ATTENTION:
#         # The user must be inscribed in the database, otherwise self.id will return None !
#         return {"name": self.name,
#                 "email": self.email,
#                 "expiration_date": self.expiration_date,
#                 "bonus": self.bonus,
#                 "new_registration": "/".join(["http://127.0.0.1:8000",
#                                               "userinvitations",
#                                               f"{self.id}/new_registration"]),
#                 "decline": "/".join(["http://127.0.0.1:8000",
#                                      "userinvitations",
#                                      f"{self.id}/decline"])}
#
#     def export_to_database_parameter(self):
#         return (self.name, self.email, self.bonus, self.expiration_date)
#
#
# class CollectionInvitedUsers(BaseModel):
#     sender_username: str
#     invitations: List[InvitedUser]
#
#
# class BankCard(BaseModel):
#     id: Optional[int]
#     card_number: str
#     holder: constr(min_length=2, max_length=30)
#     check_number: str
#
#     @classmethod
#     def create_bank_card_no_id(cls, card_number, holder, check_number):
#         return cls(card_number=card_number,
#                    holder=holder,
#                    check_number=check_number)
#
#     @classmethod
#     def create_bank_card_all_params(cls, id, card_number, holder, check_number):
#         return cls(id=id,
#                    card_number=card_number,
#                    holder=holder,
#                    check_number=check_number)
#
#
# def _validate_number_length(val_len, value):
#     pat = r"^\d{%s}$" % val_len
#     if not re.match(pat, value):
#         raise ValueError(f"Your number {value=} must be exactly {val_len} digits")
#     return value
#
#
# class WalletCreateRequest(BaseModel):
#     wallet_name: str
#     currency: constr(max_length=3)
#
#     @validator('wallet_name')
#     def wallet_name_must_not_be_empty(cls, value):
#         if not value.strip():
#             raise ValueError('Wallet name must not be empty or contain only whitespace')
#         return value
#
#
#
#
#
#
# class WalletResponse(BaseModel):
#     id: int
#     user_id: Optional[int]
#     wallet_name: str
#     is_default: Optional[bool]
#     currency: Union[constr(max_length=3), int]
#     balance: ConstrainedDecimal
#     blocked: Optional[ConstrainedDecimal]
#
#     @classmethod
#     def from_query(cls, id, user_id, wallet_name, is_default, currency, balance, blocked):
#         return cls(id=id, user_id=user_id, wallet_name=wallet_name,
#                    is_default=is_default, currency=currency, balance=balance, blocked=blocked)
#
#     @validator("balance")
#     def validate_balance(cls, value):
#         if value < 0:
#             raise ValueError("Balance must be greater than or equal to zero")
#         return value
#
#
# class Transactions(BaseModel):
#     id: Optional[int]
#     sender_id: PositiveInt
#     receiver_id: PositiveInt
#     amount: ConstrainedDecimal
#     currency: Union[str, int]
#     date: Optional[datetime]
#     confirmed: bool = False
#     approved: bool = False
#     category_id: Optional[int]
#
#     @classmethod
#     def from_query(cls, id, sender_id, receiver_id, amount, currency,
#                    date, confirmed, approved, category_id=None):
#         return cls(id=id, sender_id=sender_id, receiver_id=receiver_id, amount=amount, currency=currency,
#                    date=date, confirmed=confirmed, approved=approved, category_id=category_id)
#
#
# class TransactionResponse(BaseModel):
#     sender: str
#     receiver: str
#     amount: ConstrainedDecimal
#     currency: str
#     date: datetime
#
#     @classmethod
#     def from_query(cls, sender, receiver, amount, currency, date):
#         return cls(sender=sender, receiver=receiver, amount=amount, currency=currency, date=date)
#
#
# class CreateTransaction(BaseModel):
#     sender_wallet: Union[int, str, None]
#     receiver_username: str
#     receiver_wallet: Union[int, str, None]
#     amount: ConstrainedDecimal
#     category: Optional[str]
#
#
# class CreateTransactionByEmail(BaseModel):
#     sender_wallet: Union[int, str, None]
#     receiver_email: str
#     receiver_wallet: Union[int, str, None]
#     amount: ConstrainedDecimal
#     category: Optional[str]
#
#
# class Currency(BaseModel):
#     id: Optional[PositiveInt]
#     name: constr(max_length=3)
#
#     @classmethod
#     def from_query(cls, id, name):
#         return cls(id=id, name=name)
#
#
# class Categories(BaseModel):
#     id: Optional[PositiveInt]
#     name: str
#
#     @classmethod
#     def from_query(cls, id, name):
#         return cls(id=id, name=name)
#
#
# class CardBase(BaseModel):
#     card_number: constr(regex=r'^\d{16}$')
#     expiration_date: date
#     card_holder: constr(min_length=2, max_length=30)
#     check_number: constr(regex=r'^\d{3}$')
#
#
# class CardCreateRequest(CardBase):
#     user_id: int
#
#
# class CardResponse(BaseModel):
#     card_number: str
#     expiration_date: date
#     card_holder: str
#     check_number: str
#
#     @classmethod
#     def from_query(cls, card_number, expiration_date, card_holder, check_number):
#         return cls(card_number=card_number, expiration_date=expiration_date,
#                    card_holder=card_holder, check_number=check_number)
#
#
# class CardListResponse(BaseModel):
#     cards: List[CardResponse]
#
#
# class CreateRecurringTransaction(CreateTransaction):
#     interval: Optional[PositiveInt]
#     interval_type: Optional[constr(regex=r"^(days|weeks|months)$")]
#
#
# class RecurringTransaction(BaseModel):
#     id: Optional[PositiveInt]
#     interval: str
#     user_id: PositiveInt
#     transaction_id: PositiveInt
#     next_date: datetime
#
#     @classmethod
#     def from_query(cls, id, interval, user_id, transaction_id, next_date):
#         return cls(id=id, interval=interval, user_id=user_id, transaction_id=transaction_id, next_date=next_date)
#
#
# class WalletAccessCreateRequest(BaseModel):
#     wallet_id: int
#     user_id: int
#     spend_access: bool
#     add_access: bool
#
#     # spend_access: constr(regex=r'^[01]$')
#     # add_access: constr(regex=r'^[01]$')
#
#
# class WalletAccessResponse(BaseModel):
#     wallet_id: int
#     user_id: int
#     spend_access: bool
#     add_access: bool
#     # spend_access: constr(regex=r'^[01]$')
#     # add_access: constr(regex=r'^[01]$')
#
#
# class WalletAccessUpdateRequest(BaseModel):
#     spend_access: bool
#     add_access: bool
#     # spend_access: constr(regex=r'^[01]$')
#     # add_access: constr(regex=r'^[01]$')
