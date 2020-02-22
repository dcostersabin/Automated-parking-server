from user.models import Economy, UserDetails, Transaction
from django.http import HttpResponse
from Request_Handler.Economy.create import createHash
from datetime import datetime


def verify(hash):
    if Economy.objects.filter(hash=hash, validity=True).exists():
        return True
    else:
        return False


def creditAccount(user, hash):
    if verify(hash):
        check = UserDetails.objects.filter(user_id=user).get()
        hash_update = Economy.objects.filter(hash=hash, validity=True).get()
        check.balance += hash_update.value
        check.save()
        hash_update.validity = False
        hash_update.save()
        transaction = Transaction()
        transaction.user = user
        transaction.amount = hash_update.value
        transaction.type = 'credited'
        transaction.created_at = datetime.now()
        transaction.save()
        maintainEconomy()
        return True

    else:
        return False


def maintainEconomy():
    total = Economy.objects.filter(validity=True).count()
    while total != 100:
        new = Economy()
        new.hash = createHash()
        new.value = 100
        new.save()
        total = Economy.objects.filter(validity=True).count()


def getBalance(user):
    balance = UserDetails.objects.filter(user_id=user).get()
    return balance.balance


def debitUserAccount(user, amount):
    users = UserDetails.objects.filter(user_id=user).get()
    users.balance -= amount
    users.save()
    transaction = Transaction()
    transaction.user = user
    transaction.amount = amount
    transaction.type = 'debited'
    transaction.created_at = datetime.now()
    transaction.save()
    if transaction.id > 0:
        return True
    else:
        return False
