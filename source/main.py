import csv
from enum import Enum
from operator import attrgetter
import itertools


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

        self.noDefinedTitle = False
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


def tryAssignIfMatches(obj, fieldName, titleRegex, description):
    m = re.match(titleRegex, description)
    if m and getattr(obj, fieldName) is None:
        setattr(obj, fieldName, m.group('title'))
    pass


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

        if row[2] not in PkoBpParser.typeMappings:
            missed.append(row)
            continue

        o = Operation()
        operations.append(o)

        o.id = csvOperationsCount
        o.date = row[0]
        o.type = PkoBpParser.typeMappings.get(row[2])
        o.amount = row[3]
        o.currency = row[4]
        o.balance = row[5]
        description1 = row[6].strip()
        description2 = row[7].strip()
        description3 = row[8].strip()
        description4 = row[9].strip()

        m = re.match('Rachunek odbiorcy: (?P<acc>.*)', description1)
        if m:
            o.receiverAccount = m.group('acc')
        m = re.match('Rachunek nadawcy: (?P<acc>.*)', description1)
        if m:
            o.senderAccount = m.group('acc')

        # TODO: CardPayments has no sense without parsed Location
        # TODO: Transfers have semi sense whithout ReceiverName ('NazwaOdbiorcy' or mapped ReceiverAccount)
        # TODO: general complex PaymentMatcher to properly categorize operations into PaymentTopics

        titleRegex = 'Tytuł: (?P<title>.*)'
        tryAssignIfMatches(o, 'title', titleRegex, description1)
        tryAssignIfMatches(o, 'title', titleRegex, description2)
        tryAssignIfMatches(o, 'title', titleRegex, description3)
        tryAssignIfMatches(o, 'title', titleRegex, description4)
        if o.title is None:
            o.title = f'{description1} | {description2} | {description3} | {description4}'
            o.noDefinedTitle = True

        # override payment type if it was a forwarded ZUS payment    
        if ' ZUS ' in o.title:
            o.type = OperationType.ZUS_PAYMENT

print('csv: ', csvOperationsCount, 'operations: ', len(operations))
print('missed')
for row in missed:
    print(row)

operations.sort(key=attrgetter('type'))
operations.sort(key=attrgetter('noDefinedTitle'))
for o in operations:
    print(f'{o.type:32}'
          f' || {o.amount:>10}'
          f' || rec: {o.receiverAccount!s:32}'
          f' || sen: {o.senderAccount!s:32}'
          f" || title{'(noTitle)' if o.noDefinedTitle else ''}: {o.title}")
    # print('type:{:32} {:>10}  rec:{!s:32}   sen:{!s:32}   title:{}'
    #       .format(o.type, o.amount, o.receiverAccount, o.senderAccount, o.title))
    # print(o)
# for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
#     print(k, len(list(v)))
