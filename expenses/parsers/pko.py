import csv
import datetime
import re
from dataclasses import dataclass, field
from typing import List

import operation
from operation import OperationType, Operation, Location
import utils

debug_check = True
debug_print = False

typeMappings = {
	'Płatność kartą': OperationType.CARD_PAYMENT,
	'Przelew z rachunku': OperationType.TRANSFER_OUT,
	'Przelew na rachunek': OperationType.TRANSFER_IN,
	'Wypłata z bankomatu': OperationType.ATM_OUT,
	# '' : OperationType.ATM_IN,
	'Obciążenie': OperationType.CHARGE,
	'Zlecenie stałe': OperationType.STANDING_ORDER,
	'Płatność web - kod mobilny': OperationType.MOBILE_PAYMENT,
	'Zwrot płatności kartą': OperationType.CARD_PAYMENT_RETURN,
	'Przelew do ZUS': OperationType.ZUS_PAYMENT,
	'Przelew podatkowy': OperationType.US_PAYMENT,
	'Zwrot w terminalu': OperationType.TERMINAL_RETURN,
	'Naliczenie odsetek': OperationType.INTEREST_TAX,
	'Przelew Paybynet BLIK': OperationType.PAYBYNET_BLIK,
	'Uznanie': OperationType.GAIN,
}


@dataclass(init=False)
class PkoBpOperation:
	id: int
	operation_date: str
	currency_date: str
	transaction_type: str
	amount: str
	currency: str
	after_transaction_balance: str
	descriptions: List[str] = field(default_factory=list)

	def __str__(self):
		ret = f'{self.id:4}' \
		      f' | {self.operation_date:10}' \
		      f' | {self.transaction_type:32}' \
		      f' | {self.currency:3}' \
		      f' | {self.amount:>8}' \
		      f' | {self.after_transaction_balance:>9}'
		for desc in self.descriptions:
			if len(desc) > 60:
				desc = desc[:57] + '...'
			ret += f' | {desc:60}'
		return ret


# @classmethod
# def get_mapping(cls, pko_operation_name: str) -> operation.OperationType:
#     return cls.typeMappings[pko_operation_name]


IGNORED = []


def load_and_parse_operations(filename):
	bank_operations = []
	missed_bank_operations = []
	all_operations: List[Operation] = []

	with open(filename) as csv_file:
		reader = csv.reader(csv_file)
		csv_count = -1
		for row in reader:
			csv_count += 1

			# parse data
			if csv_count == 0:  # skip header line
				continue

			pko_operation = PkoBpOperation()
			pko_operation.id = csv_count
			pko_operation.operation_date = row[0]
			pko_operation.currency_date = row[1]
			pko_operation.transaction_type = row[2]
			pko_operation.amount = row[3]
			pko_operation.currency = row[4]
			pko_operation.after_transaction_balance = row[5]
			pko_operation.descriptions = []
			for data in row[6:]:  # 7th column = start of 'descriptions', total number of columns varies
				pko_operation.descriptions.append(data)
			bank_operations.append(pko_operation)

	# map PkoBpOperation to Operation
	for pko_operation in bank_operations:
		o = Operation()
		all_operations.append(o)

		o.id = pko_operation.id
		o.date = datetime.datetime.strptime(pko_operation.currency_date, '%Y-%m-%d')
		o.transaction_type = typeMappings.get(pko_operation.transaction_type)
		o.amount = float(pko_operation.amount)
		o.currency = pko_operation.currency
		o.balance = pko_operation.after_transaction_balance

		parse_description_by_regex(pko_operation, o, 'receiver_account', 'Rachunek odbiorcy: (?P<acc>.*)', 'acc')
		parse_description_by_regex(pko_operation, o, 'receiver_name', 'Nazwa odbiorcy: (?P<name>.*)', 'name')
		parse_description_by_regex(pko_operation, o, 'receiver_address', 'Adres odbiorcy: (?P<addr>.*)', 'addr')
		parse_description_by_regex(pko_operation, o, 'sender_account', 'Rachunek nadawcy: (?P<acc>.*)', 'acc')
		parse_description_by_regex(pko_operation, o, 'sender_name', 'Nazwa nadawcy: (?P<name>.*)', 'name')
		parse_description_by_regex(pko_operation, o, 'sender_address', 'Adres nadawcy: (?P<addr>.*)', 'addr')
		parse_description_by_regex(pko_operation, o, 'conversion_date', 'Data przetworzenia: (?P<date>\\d{4}-\\d{2}-\\d{2})', 'date')
		parse_description_by_regex(pko_operation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')
		parse_original_payment_amount(pko_operation, o)
		parse_simple_location(pko_operation, o)
		parse_full_location(pko_operation, o)

		# ignore unimportant descriptions
		parse_ignore_description(pko_operation, 'Data i czas operacji: (?P<date>\\d{4}-\\d{2}-\\d{2})')
		parse_ignore_description(pko_operation, 'Numer telefonu: \\+48 665 396 588')
		parse_ignore_description(pko_operation, 'KAPIT\\.ODSETEK KARNYCH-OBCIĄŻENIE')
		parse_ignore_description(pko_operation, 'Referencje własne zleceniodawcy:')
		if o.transaction_type is OperationType.US_PAYMENT:
			parse_ignore_description(pko_operation, 'Nazwa i nr identyfikatora:')
			parse_ignore_description(pko_operation, 'Symbol formularza:')
			parse_ignore_description(pko_operation, 'Okres płatności:')
		if o.transaction_type in [OperationType.MOBILE_PAYMENT, OperationType.TERMINAL_RETURN]:
			parse_ignore_description(pko_operation, 'Numer referencyjny:')
		if o.transaction_type in [OperationType.CARD_PAYMENT, OperationType.CARD_PAYMENT_RETURN, OperationType.ATM_OUT]:
			parse_ignore_description(pko_operation, 'Numer karty: 425125.*452')

		# aggregate unmapped values to other field
		for desc in pko_operation.descriptions:
			if desc and '<OK>' not in desc:
				o.other += desc + ' | '

		# override payment type if it was a forwarded ZUS payment
		if o.title and ' ZUS ' in o.title:
			o.transaction_type = OperationType.ZUS_PAYMENT

	valid_operations = operation.get_valid_operations(all_operations)

	if debug_print:
		# sort bank all_operations using all description columns and transaction type
		for i in reversed(range(len(bank_operations[0].descriptions))):
			bank_operations.sort(key=lambda bo: bo.descriptions[i])
		bank_operations.sort(key=lambda bo: bo.transaction_type)
		utils.print_bank_operations_list(bank_operations)

		valid_operations.sort(key=lambda o: o.transaction_type)
		utils.print_bank_operations_list(valid_operations)

		print()  # separator

	if debug_check:
		# operations.check_ignored_descriptions(IGNORED)
		operation.check_entries_count(all_operations, csv_count)
		operation.check_untyped(all_operations)
		operation.check_unassigned_descriptions(all_operations)
		operation.check_untopiced(all_operations)

	return all_operations


def parse_description_by_regex(pko_operation: PkoBpOperation, target_obj, target_field_name, regex: str,
                               regex_group_name: str):
	for d in pko_operation.descriptions:
		m = re.match(regex, d)
		if m:
			if hasattr(target_obj, target_field_name) and getattr(target_obj, target_field_name) is not None:
				raise Exception('Field already assigned')
			setattr(target_obj, target_field_name, m.group(regex_group_name))
			index = pko_operation.descriptions.index(d)
			pko_operation.descriptions[index] = '<OK>' + d


def parse_full_location(pko_operation: PkoBpOperation, o: Operation):
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


def parse_simple_location(pko_operation: PkoBpOperation, o: Operation):
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


def parse_original_payment_amount(pko_operation, o):
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


def parse_ignore_description(pko_operation: PkoBpOperation, regex: str):
	""" mark given description part with <OK> marker so that it will be considered mapped """
	for d in pko_operation.descriptions:
		if re.match(regex, d):
			IGNORED.append(d)
			index = pko_operation.descriptions.index(d)
			pko_operation.descriptions[index] = '<OK>' + d
