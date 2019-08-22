import csv
from enum import Enum

import itertools


class OperationType(Enum):
    CARD_PAYMENT, \
    CARD_PAYMENT_RETURN, \
    TRANSFER_OUT, \
    TRANSFER_IN, \
    ATM_OUT, \
    ATM_IN, \
    MOBILE_PAYMENT, \
    ZUS_PAYMENT, \
    US_PAYMENT, \
    TERMINAL_RETURN, \
    INTEREST, \
    PAYBYNET_BLIK, \
    GAIN, \
    *_ = range(100)


class PkoBpParser:
    typesMapping = {
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


class Location:
    def __init__(self):
        self.country = None
        self.city = None
        self.address = None


class Operation:
    def __init__(self):
        self.date = None
        self.type = None
        self.amount = None
        self.currency = None
        self.balance = None
        self.description = None
        self.location = Location()
        self.timestamp = None

        self.title = None

        # receiver
        self.receiverAccount = None
        self.receiverName = None
        self.receiverAddress = None

        # sender
        self.senderAccount = None
        self.senderName = None
        self.senderAddress = None

    def __str__(self):
        # return "{:>10} {:>8}".format(self.type.name, self.amount)
        # return "{0.type.name} {0.amount}".format(self)
        return "{type.name:>18} {amount:>10} {currency:>4}".format(**self.__dict__)

    def __lt__(self, other):
        return self.type.value > other.type.value


import collections
import re


def groupby_unsorted(seq, key=lambda x: x):
    indexes = collections.defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)


operations = []
missed = []

with open('./../data/history_csv_20190609_170438.csv') as csvfile:
    reader = csv.reader(csvfile)
    csvOperationsCount = -1
    for row in reader:
        csvOperationsCount += 1
        if csvOperationsCount < 100:
            # print(csvOperationsCount, ';  '.join(row))
            print(csvOperationsCount, row[6])
            # print(csvOperationsCount, row[7])
            # print(csvOperationsCount, row[8])
            # print(csvOperationsCount, row[6], " -> ", row[7], " -> ", row[8])
            # print(csvOperationsCount, row[6], " -> ", row[7], " -> ", row[8])
        if csvOperationsCount == 0:  # skip header line
            continue

        if row[2] not in PkoBpParser.typesMapping:
            missed.append(row)
            continue

        o = Operation()
        operations.append(o)

        o.id = csvOperationsCount
        o.date = row[0]
        o.type = PkoBpParser.typesMapping.get(row[2])
        o.amount = row[3]
        o.currency = row[4]
        o.balance = row[5]
        description = row[6]

        m = re.match('Rachunek odbiorcy: (?P<acc>.*)', description)
        if m:
            o.receiverAccount = m.group('acc')
        m = re.match('Rachunek nadawcy: (?P<acc>.*)', description)
        if m:
            o.senderAccount = m.group('acc')
        m = re.match('Tytuł: (?P<title>.*)', description)
        if m:
            o.title = m.group('title')

print('csv: ', csvOperationsCount, 'operations: ', len(operations))
print('missed')
for row in missed:
    print(row)
for o in sorted(operations, key=lambda o: o.type.value):
    print(o.type, o.amount, o.receiverAccount, o.senderAccount, o.title)
    # print(o)
# for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
#     print(k, len(list(v)))
