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
        self.location = Location()
        self.timestamp = None
        
    def __str__(self):
        return self.type
    
    def __lt__(self, other):
        return self.type.value > other.type.value


class OperationWithReceiver(Operation):
    def __init__(self):
        super().__init__()
        self.receiverAccount = None
        self.receiverName = None
        self.receiverAddress = None


class OperationWithSender(Operation):
    def __init__(self):
        super().__init__()
        self.senderAccount = None
        self.senderName = None
        self.senderAddress = None

import collections

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
        print(len(row), csvOperationsCount, '; '.join(row))

        literalType = row[2]
        operationType = PkoBpParser.typesMapping.get(literalType, None)
        if operationType is not None:
            o = Operation()
            o.type = operationType
            operations.append(o)
        else:
            missed.append(row)

print('csv: ', csvOperationsCount, 'operations: ', len(operations))
print('missed')
for row in missed:
    print(row)
# sorted(operations, key=lambda o: o.type.value)
for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
    print(k, len(list(v)))
