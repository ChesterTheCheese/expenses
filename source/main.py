import csv
from _ast import Lambda
from enum import Enum
from operator import attrgetter
import itertools
from typing import List


class OperationType(Enum):
    [CARD_PAYMENT,
     CARD_PAYMENT_RETURN,
     TRANSFER_OUT,
     TRANSFER_IN,
     ATM_OUT,
     ATM_IN,
     MOBILE_PAYMENT,
     ZUS_PAYMENT,
     US_PAYMENT,
     TERMINAL_RETURN,
     INTEREST,
     PAYBYNET_BLIK,
     GAIN,
     *_] = range(100)

    def __lt__(self, other):
        return self.value < other.value


class PkoBpParser:
    typeMappings = {
        'Płatność kartą': OperationType.CARD_PAYMENT,
        'Przelew z rachunku': OperationType.TRANSFER_OUT,
        'Przelew na rachunek': OperationType.TRANSFER_IN,
        'Wypłata z bankomatu': OperationType.ATM_OUT,
        # '' : OperationType.ATM_IN,
        'Płatność web - kod mobilny': OperationType.MOBILE_PAYMENT,
        'Zwrot płatności kartą': OperationType.CARD_PAYMENT_RETURN,
        'Przelew do ZUS': OperationType.ZUS_PAYMENT,
        'Przelew podatkowy': OperationType.US_PAYMENT,
        'Zwrot w terminalu': OperationType.TERMINAL_RETURN,
        'Naliczenie odsetek': OperationType.INTEREST,
        'Przelew Paybynet BLIK': OperationType.PAYBYNET_BLIK,
        'Uznanie': OperationType.GAIN,
    }

    class PkoBpOperation:
        id = None
        operationDate = None
        currencyDate = None
        transactionType = None
        amount = None
        currency = None
        afterTransactionBalance = None
        description = []

        def __str__(self):
            return f'{self.id:4}' \
                   f' | {self.operationDate:10}' \
                   f' | {self.transactionType:32}' \
                   f' | {self.currency:3}' \
                   f' | {self.amount:>8}' \
                   f' | {self.afterTransactionBalance:>9}' \
                   f' | {self.description[1]:{0 if self.description[1] is None else 90}}' \
                   f' | {self.description[2]}' \
                   f' | {self.description[3]}' \
                   f' | {self.description[4]}' \
                   f' | {self.description[5]}' \
                   f' | {self.description[6]}' \
                   f' | {self.description[0]:32}'


class Location:
    def __init__(self):
        self.country = None
        self.city = None
        self.address = None


class Operation:
    date = None
    type = None
    amount = None
    currency = None
    balance = None
    description = None
    location = Location()
    timestamp = None

    noDefinedTitle = False
    title = None

    otherInfo = ''

    # receiver
    receiverAccount = None
    receiverName = None
    receiverAddress = None

    # sender
    senderAccount = None
    senderName = None
    senderAddress = None


def __str__(self):
    # return "{:>10} {:>8}".format(self.type.name, self.amount)
    # return "{0.type.name} {0.amount}".format(self)
    return "{type.name:>18} {amount:>10} {currency:>4}".format(**self.__dict__)


def __lt__(self, other):
    return self.type.__lt__(other)


import collections
import re


def groupby_unsorted(seq, key=lambda x: x):
    indexes = collections.defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)


def assignFromDescriptionsIfMatches(pkoOperation, targetObj, targetFieldName, regex, regexGroupName):
    for d in pkoOperation.description:
        m = re.match(regex, d)
        if m:
            if getattr(targetObj, targetFieldName) is not None:
                raise Exception('Field already assigned')
            setattr(targetObj, targetFieldName, m.group(regexGroupName))
            index = pkoOperation.description.index(d)
            pkoOperation.description[index] = '<OK>' + d


def print_list(l: List):
    print(f'bankOperations ({len(l)})')
    for e in l:
        print(e)


bankOperations = []
missedBankOperations = []
operations = []

with open('./../data/history_csv_20190609_170438.csv') as csvfile:
    reader = csv.reader(csvfile)
    csvOperationsCount = -1
    for row in reader:
        csvOperationsCount += 1

        # print input date
        if csvOperationsCount < 100:
            # print(csvOperationsCount, row[6])
            # print(csvOperationsCount, ';  '.join(row))
            # print(csvOperationsCount, row[7])
            # print(csvOperationsCount, row[8])
            # print(csvOperationsCount, row[6], " -> ", row[7], " -> ", row[8])
            # print(csvOperationsCount, row[6], " -> ", row[7], " -> ", row[8])
            pass

        # parse data
        if csvOperationsCount == 0:  # skip header line
            continue

        pkoOperation = PkoBpParser.PkoBpOperation()
        bankOperations.append(pkoOperation)
        pkoOperation.id = csvOperationsCount
        pkoOperation.operationDate = row[0]
        pkoOperation.currencyDate = row[1]
        pkoOperation.transactionType = row[2]
        pkoOperation.amount = row[3]
        pkoOperation.currency = row[4]
        pkoOperation.afterTransactionBalance = row[5]
        pkoOperation.description = [row[6], row[7], row[8], row[9], row[10], row[11], row[12]]

        if pkoOperation.transactionType not in PkoBpParser.typeMappings:
            missedBankOperations.append(pkoOperation)
            continue

        o = Operation()
        operations.append(o)

        o.id = pkoOperation.id
        o.date = pkoOperation.operationDate
        o.type = PkoBpParser.typeMappings.get(pkoOperation.transactionType)
        o.amount = pkoOperation.amount
        o.currency = pkoOperation.currency
        o.balance = pkoOperation.afterTransactionBalance

        # TODO: CardPayments has no sense without parsed Location
        # TODO: Transfers have semi sense whithout ReceiverName ('NazwaOdbiorcy' or mapped ReceiverAccount)
        # TODO: general complex PaymentMatcher to properly categorize operations into PaymentTopics

        assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverAccount', 'Rachunek odbiorcy: (?P<acc>.*)', 'acc')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverName', 'Nazwa odbiorcy: (?P<name>.*)', 'name')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverAddress', 'Adres odbiorcy: (?P<addr>.*)', 'addr')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'senderAccount', 'Rachunek nadawcy: (?P<acc>.*)', 'acc')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'senderName', 'Nazwa nadawcy: (?P<name>.*)', 'name')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'senderAddress', 'Adres nadawcy: (?P<address>.*)', 'address')
        assignFromDescriptionsIfMatches(pkoOperation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')

        for desc in pkoOperation.description:
            if '<OK>' not in desc:
                o.otherInfo += desc + ' | '

        # override payment type if it was a forwarded ZUS payment    
        if o.title is not None and ' ZUS ' in o.title:
            o.type = OperationType.ZUS_PAYMENT

print('csv: ', csvOperationsCount, 'operations: ', len(operations))
print('missed')
for row in missedBankOperations:
    print(row)

bankOperations.sort(key=lambda bo: bo.description[0])
bankOperations.sort(key=lambda bo: bo.description[6])
bankOperations.sort(key=lambda bo: bo.description[5])
bankOperations.sort(key=lambda bo: bo.description[4])
bankOperations.sort(key=lambda bo: bo.description[3])
bankOperations.sort(key=lambda bo: bo.description[2])
bankOperations.sort(key=lambda bo: bo.description[1])

print_list(bankOperations)

operations.sort(key=attrgetter('type'))
operations.sort(key=attrgetter('noDefinedTitle'))
for o in operations:
    print(f'{o.type:32}'
          f' || {o.amount:>10}'
          f' || rec: {o.receiverAccount!s:32}'
          f' || sen: {o.senderAccount!s:32}'
          f" || title{'(noTitle)' if o.title is None else ''}: {o.title}"
          f' || other:{o.otherInfo}')

# print('type:{:32} {:>10}  rec:{!s:32}   sen:{!s:32}   title:{}'
#       .format(o.type, o.amount, o.receiverAccount, o.senderAccount, o.title))
# print(o)

# for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
#     print(k, len(list(v)))
