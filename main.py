import csv
import re
from operator import attrgetter

import numpy as np
import pandas as pd

import utils
from operation import Operation, OperationType, Location
from parsers import pko

IGNORED = []


def assign_from_descriptions_if_matches(pko_operation: pko.PkoBpOperation, target_obj, target_field_name, regex: str, regex_group_name: str):
    for d in pko_operation.descriptions:
        m = re.match(regex, d)
        if m:
            if hasattr(target_obj, target_field_name) and getattr(target_obj, target_field_name) is not None:
                raise Exception('Field already assigned')
            setattr(target_obj, target_field_name, m.group(regex_group_name))
            index = pko_operation.descriptions.index(d)
            pko_operation.descriptions[index] = '<OK>' + d


def ignore_description(pko_operation: pko.PkoBpOperation, regex: str):
    """ mark given description part with <OK> marker so that it will be considered mapped """
    for d in pko_operation.descriptions:
        if re.match(regex, d):
            IGNORED.append(d)
            index = pko_operation.descriptions.index(d)
            pko_operation.descriptions[index] = '<OK>' + d


def try_assign_full_location(pko_operation: pko.PkoBpOperation, o: Operation):
    regex = 'Lokalizacja: Kraj: (?P<country>.*) Miasto: (?P<city>.*) Adres: (?P<addr>.*)'
    for desc in pko_operation.descriptions:
        if m := re.match(regex, desc):
            country = m.group('country')
            city = m.group('city')
            address = m.group('addr')
            o.location = Location()
            o.location.country = country
            o.location.city = city
            o.location.address = address
            index = pko_operation.descriptions.index(desc)
            pko_operation.descriptions[index] = '<OK>' + desc


def try_assign_simple_location(pko_operation: pko.PkoBpOperation, o: Operation):
    regex = 'Lokalizacja: Adres: (?P<addr>.*)'
    for desc in pko_operation.descriptions:
        if m := re.match(regex, desc):
            address = m.group('addr')
            o.location = Location()
            o.location.country = ''
            o.location.city = ''
            o.location.address = address
            index = pko_operation.descriptions.index(desc)
            pko_operation.descriptions[index] = '<OK>' + desc


def try_assign_original_payment_amount(pko_operation, o):
    regex = 'Oryginalna kwota operacji: (?P<amount>\\d*,\\d*) (?P<curr>.*)'
    for desc in pko_operation.descriptions:
        if m := re.match(regex, desc):
            amount = m.group('amount')
            currency = m.group('curr')
            if 'PLN' not in currency:
                o.original_amount = amount
                o.original_currency = currency
            index = pko_operation.descriptions.index(desc)
            pko_operation.descriptions[index] = '<OK>' + desc


if __name__ == '__main__':

    bank_operations = []
    missed_bank_operations = []
    operations = []

    # df = pd.read_csv(file_path) # pandas
    with open('./data/history_csv_20190609_170438.csv') as csv_file:
        # with open('./data/history_csv_20190609_170438_sample.csv') as csv_file:
        reader = csv.reader(csv_file)
        csv_count = -1
        for row in reader:
            csv_count += 1

            # parse data
            if csv_count == 0:  # skip header line
                continue

            pko_operation = pko.PkoBpOperation()
            pko_operation.id = csv_count
            pko_operation.operation_date = row[0]
            pko_operation.currency_date = row[1]
            pko_operation.transaction_type = row[2]
            pko_operation.amount = row[3]
            pko_operation.currency = row[4]
            pko_operation.after_transaction_balance = row[5]
            pko_operation.descriptions = [row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
            bank_operations.append(pko_operation)

            if pko_operation.transaction_type not in pko.typeMappings:
                missed_bank_operations.append(pko_operation)
                continue

            o = Operation()
            operations.append(o)
            o.id = pko_operation.id
            o.date = pko_operation.currency_date
            o.type = pko.typeMappings.get(pko_operation.transaction_type)
            o.amount = pko_operation.amount
            o.currency = pko_operation.currency
            o.balance = pko_operation.after_transaction_balance

            # TODO: Transfers have semi sense whithout ReceiverName ('NazwaOdbiorcy' or mapped ReceiverAccount)
            # TODO: general complex PaymentMatcher to properly categorize operations into PaymentTopics

            assign_from_descriptions_if_matches(pko_operation, o, 'receiver_account', 'Rachunek odbiorcy: (?P<acc>.*)', 'acc')
            assign_from_descriptions_if_matches(pko_operation, o, 'receiver_name', 'Nazwa odbiorcy: (?P<name>.*)', 'name')
            assign_from_descriptions_if_matches(pko_operation, o, 'receiver_address', 'Adres odbiorcy: (?P<addr>.*)', 'addr')
            assign_from_descriptions_if_matches(pko_operation, o, 'sender_account', 'Rachunek nadawcy: (?P<acc>.*)', 'acc')
            assign_from_descriptions_if_matches(pko_operation, o, 'sender_name', 'Nazwa nadawcy: (?P<name>.*)', 'name')
            assign_from_descriptions_if_matches(pko_operation, o, 'sender_address', 'Adres nadawcy: (?P<addr>.*)', 'addr')
            assign_from_descriptions_if_matches(pko_operation, o, 'conversion_date', 'Data przetworzenia: (?P<date>\\d{4}-\\d{2}-\\d{2})', 'date')
            assign_from_descriptions_if_matches(pko_operation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')
            try_assign_original_payment_amount(pko_operation, o)
            try_assign_simple_location(pko_operation, o)
            try_assign_full_location(pko_operation, o)

            # ignore unimportant descriptions
            ignore_description(pko_operation, 'Data i czas operacji: (?P<date>\\d{4}-\\d{2}-\\d{2})')
            ignore_description(pko_operation, 'Numer telefonu: \\+48 665 396 588')
            ignore_description(pko_operation, 'KAPIT\\.ODSETEK KARNYCH-OBCIĄŻENIE')
            ignore_description(pko_operation, 'Referencje własne zleceniodawcy:')
            if o.type is OperationType.US_PAYMENT:
                ignore_description(pko_operation, 'Nazwa i nr identyfikatora:')
                ignore_description(pko_operation, 'Symbol formularza:')
                ignore_description(pko_operation, 'Okres płatności:')
            if o.type in [OperationType.MOBILE_PAYMENT, OperationType.TERMINAL_RETURN]:
                ignore_description(pko_operation, 'Numer referencyjny:')
            if o.type in [OperationType.CARD_PAYMENT, OperationType.CARD_PAYMENT_RETURN, OperationType.ATM_OUT]:
                ignore_description(pko_operation, 'Numer karty: 425125.*452')

            # aggregate unmapped values to other field
            for desc in pko_operation.descriptions:
                if desc and '<OK>' not in desc:
                    o.other += desc + ' | '

            # override payment type if it was a forwarded ZUS payment
            if o.title and ' ZUS ' in o.title:
                o.type = OperationType.ZUS_PAYMENT

    bank_operations.sort(key=lambda bo: bo.descriptions[0])
    bank_operations.sort(key=lambda bo: bo.descriptions[6])
    bank_operations.sort(key=lambda bo: bo.descriptions[5])
    bank_operations.sort(key=lambda bo: bo.descriptions[4])
    bank_operations.sort(key=lambda bo: bo.descriptions[3])
    bank_operations.sort(key=lambda bo: bo.descriptions[2])
    bank_operations.sort(key=lambda bo: bo.descriptions[1])

    utils.print_bank_operations_list(bank_operations)

    operations.sort(key=attrgetter('type'))
    # operations.sort(key=attrgetter('noDefinedTitle'))
    # utils.print_bank_operations_list(operations[:10])
    utils.print_bank_operations_list(operations)

    print()  # separator

    # check ignored entries (should print long list)
    # IGNORED.sort() # sort alphabetically
    # print(*IGNORED, sep='\n')

    # check if all descriptions were mapped or ignored (should print nothing)
    unmapped = [o for o in operations if o.other]
    print(f'unmapped description parts: {len(unmapped)}')
    for o in unmapped:
        print(f'\t{o.type}, {o.other}')
    if len(unmapped):
        print(f'unmapped description parts: {len(unmapped)} ^')

    # check csv lines count vs operation count
    print(f'csv entries: {csv_count} operations: {len(operations)}')

    # check if all bank operation have an OperationType
    print(f'missed bank operations: {len(missed_bank_operations)}')
    for row in missed_bank_operations:
        print(f'\t{row}')
    if len(missed_bank_operations):
        print(f'missed bank operations: {len(missed_bank_operations)} ^')

    # for k, v in itertools.groupby(sorted(operations, key=lambda o: o.type.value), lambda o: o.type):
    #     print(k, len(list(v)))

    # for k, v in utils.groupby_unsorted(operations, lambda o: o.type):
    #     print(k, len(list(v)))

    ###################
    # pandas analysis #
    ###################

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 0)
    operations_df = pd.DataFrame([vars(o) for o in operations])
    operations_df = operations_df.replace(np.nan, '-', regex=True)  # TODO safe with non-string attributes?
    operations_df['date'] = operations_df['date'].transform(lambda d: pd.to_datetime(d))
    operations_df['amount'] = operations_df['amount'].transform(lambda a: float(a))
    print(operations_df.head(20))
    print(operations_df.shape)
    print(f'Operations shape: {operations_df.shape} sum: {operations_df.amount.sum()}')

    ################################################
    # calculate average monthly (regular) expenses #
    ################################################

    # prepare data set, expenses without unnecessary cashflow variations (zus, taxes, Rolczyński operations)
    regular_expenses_df = operations_df
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')
    regular_expenses_df = regular_expenses_df[regular_expenses_df.amount <= 0]
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')
    regular_expenses_df = regular_expenses_df[regular_expenses_df['type'] != OperationType.ZUS_PAYMENT]
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')
    regular_expenses_df = regular_expenses_df[regular_expenses_df['type'] != OperationType.US_PAYMENT]
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')
    regular_expenses_df = regular_expenses_df[~regular_expenses_df['receiver_name'].str.contains('ROLCZYŃSKI')]  # case sensitive
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')

    # reduce columns
    regular_expenses_df = regular_expenses_df[['date', 'amount']]
    print(f'Expenses shape: {regular_expenses_df.shape} sum: {regular_expenses_df.amount.sum()}')
    # print(regular_expenses_df.head(20))

    # groupby
    month_period = regular_expenses_df['date'].dt.to_period('M')  # convert to PeriodIndex to allow grouping
    month_groupby = regular_expenses_df.groupby(month_period)
    print(month_groupby.agg(['count', 'sum']))  # multiple aggregation types
