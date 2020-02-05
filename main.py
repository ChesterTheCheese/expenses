import csv
import re
from operator import attrgetter

from parsers import pko
from operation import Operation, OperationType, Location
import utils


def assignFromDescriptionsIfMatches(pkoOperation, targetObj, targetFieldName, regex, regexGroupName):
    for d in pkoOperation.description:
        m = re.match(regex, d)
        if m:
            if hasattr(targetObj, targetFieldName) and getattr(targetObj, targetFieldName) is not None:
                raise Exception('Field already assigned')
            setattr(targetObj, targetFieldName, m.group(regexGroupName))
            index = pkoOperation.description.index(d)
            pkoOperation.description[index] = '<OK>' + d


def tryAssingFullLocation(pkoOperation: pko.PkoBpOperation, o: Operation):
    regex = 'Lokalizacja: Kraj: (?P<country>.*) Miasto: (?P<city>.*) Adres: (?P<addr>.*)'
    for desc in pkoOperation.description:
        m = re.match(regex, desc)
        if m:
            country = m.group('country')
            city = m.group('city')
            address = m.group('addr')
            o.location = Location()
            o.location.country = country
            o.location.city = city
            o.location.address = address
            index = pkoOperation.description.index(desc)
            pkoOperation.description[index] = '<OK>' + desc


def tryAssingSimpleLocation(pkoOperation: pko.PkoBpOperation, o: Operation):
    regex = 'Lokalizacja: Adres: (?P<addr>.*)'
    for desc in pkoOperation.description:
        m = re.match(regex, desc)
        if m:
            address = m.group('addr')
            o.location = Location()
            o.location.country = ''
            o.location.city = ''
            o.location.address = address
            index = pkoOperation.description.index(desc)
            pkoOperation.description[index] = '<OK>' + desc
    pass


if __name__ == '__main__':

    bankOperations = []
    missedBankOperations = []
    operations = []

    # df = pd.read_csv(file_path) # pandas
    with open('./data/history_csv_20190609_170438_sample.csv') as csvfile:
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

            pkoOperation = pko.PkoBpOperation()
            pkoOperation.id = csvOperationsCount
            pkoOperation.operationDate = row[0]
            pkoOperation.currencyDate = row[1]
            pkoOperation.transactionType = row[2]
            pkoOperation.amount = row[3]
            pkoOperation.currency = row[4]
            pkoOperation.afterTransactionBalance = row[5]
            pkoOperation.description = [row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
            bankOperations.append(pkoOperation)

            if pkoOperation.transactionType not in pko.typeMappings:
                missedBankOperations.append(pkoOperation)
                continue

            o = Operation()
            operations.append(o)
            o.id = pkoOperation.id
            o.date = pkoOperation.operationDate
            o.type = pko.typeMappings.get(pkoOperation.transactionType)
            o.amount = pkoOperation.amount
            o.currency = pkoOperation.currency
            o.balance = pkoOperation.afterTransactionBalance

            # TODO: Transfers have semi sense whithout ReceiverName ('NazwaOdbiorcy' or mapped ReceiverAccount)
            # TODO: general complex PaymentMatcher to properly categorize operations into PaymentTopics

            assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverAccount', 'Rachunek odbiorcy: (?P<acc>.*)', 'acc')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverName', 'Nazwa odbiorcy: (?P<name>.*)', 'name')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'receiverAddress', 'Adres odbiorcy: (?P<addr>.*)', 'addr')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'senderAccount', 'Rachunek nadawcy: (?P<acc>.*)', 'acc')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'senderName', 'Nazwa nadawcy: (?P<name>.*)', 'name')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'senderAddress', 'Adres nadawcy: (?P<addr>.*)', 'addr')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')
            tryAssingFullLocation(pkoOperation, o)
            if o.location is None:
                tryAssingSimpleLocation(pkoOperation, o)

            # aggregate unmapped values to otherInfo field
            for desc in pkoOperation.description:
                if '<OK>' not in desc:
                    o.otherInfo += desc + ' | '

            # override payment type if it was a forwarded ZUS payment
            if o.title and ' ZUS ' in o.title:
                o.type = OperationType.ZUS_PAYMENT

    print('csv: ', csvOperationsCount, 'operations: ', len(operations))
    print(f'missed {len(missedBankOperations)}')
    for row in missedBankOperations:
        print(row)

    bankOperations.sort(key=lambda bo: bo.description[0])
    bankOperations.sort(key=lambda bo: bo.description[6])
    bankOperations.sort(key=lambda bo: bo.description[5])
    bankOperations.sort(key=lambda bo: bo.description[4])
    bankOperations.sort(key=lambda bo: bo.description[3])
    bankOperations.sort(key=lambda bo: bo.description[2])
    bankOperations.sort(key=lambda bo: bo.description[1])

    utils.print_bank_operations_list(bankOperations)

    operations.sort(key=attrgetter('type'))
    # operations.sort(key=attrgetter('noDefinedTitle'))
    # utils.print_bank_operations_list(operations[:10])
    utils.print_bank_operations_list(operations)

    # for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
    #     print(k, len(list(v)))
