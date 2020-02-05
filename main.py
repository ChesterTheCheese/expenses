import csv
import re
from operator import attrgetter

from parsers import pko
import operation
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

            o = operation.Operation()
            operations.append(o)
            o.id = pkoOperation.id
            o.date = pkoOperation.operationDate
            o.type = pko.typeMappings.get(pkoOperation.transactionType)
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
            assignFromDescriptionsIfMatches(pkoOperation, o, 'senderAddress', 'Adres nadawcy: (?P<addr>.*)', 'addr')
            assignFromDescriptionsIfMatches(pkoOperation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')

            for desc in pkoOperation.description:
                if '<OK>' not in desc:
                    o.otherInfo += desc + ' | '

            # override payment type if it was a forwarded ZUS payment    
            if o.title is not None and ' ZUS ' in o.title:
                o.type = operation.OperationType.ZUS_PAYMENT

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

    utils.print_bank_operations_list(bankOperations)

    operations.sort(key=attrgetter('type'))
    # operations.sort(key=attrgetter('noDefinedTitle'))
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
