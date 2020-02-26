import csv
import re
from dataclasses import dataclass, field
from operator import attrgetter
from typing import List

import utils
from operation import OperationType, Operation, Location

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
		return f'{self.id:4}' \
		       f' | {self.operation_date:10}' \
		       f' | {self.transaction_type:32}' \
		       f' | {self.currency:3}' \
		       f' | {self.amount:>8}' \
		       f' | {self.after_transaction_balance:>9}' \
		       f' | {self.descriptions[1]:{0 if self.descriptions[1] is None else 90}}' \
		       f' | {self.descriptions[2]}' \
		       f' | {self.descriptions[3]}' \
		       f' | {self.descriptions[4]}' \
		       f' | {self.descriptions[5]}' \
		       f' | {self.descriptions[6]}' \
		       f' | {self.descriptions[0]:32}'

		# @classmethod
		# def get_mapping(cls, pko_operation_name: str) -> operation.OperationType:
		#     return cls.typeMappings[pko_operation_name]


IGNORED = []


def load_and_parse_operations(filename):
	bank_operations = []
	missed_bank_operations = []
	operations = []

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
			pko_operation.descriptions = [row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
			bank_operations.append(pko_operation)

			if pko_operation.transaction_type not in typeMappings:
				missed_bank_operations.append(pko_operation)
				continue

			o = Operation()
			operations.append(o)
			o.id = pko_operation.id
			o.date = pko_operation.currency_date
			o.type = typeMappings.get(pko_operation.transaction_type)
			o.amount = pko_operation.amount
			o.currency = pko_operation.currency
			o.balance = pko_operation.after_transaction_balance

			parse_description_to_field_with_regex(pko_operation, o, 'receiver_account', 'Rachunek odbiorcy: (?P<acc>.*)', 'acc')
			parse_description_to_field_with_regex(pko_operation, o, 'receiver_name', 'Nazwa odbiorcy: (?P<name>.*)', 'name')
			parse_description_to_field_with_regex(pko_operation, o, 'receiver_address', 'Adres odbiorcy: (?P<addr>.*)', 'addr')
			parse_description_to_field_with_regex(pko_operation, o, 'sender_account', 'Rachunek nadawcy: (?P<acc>.*)', 'acc')
			parse_description_to_field_with_regex(pko_operation, o, 'sender_name', 'Nazwa nadawcy: (?P<name>.*)', 'name')
			parse_description_to_field_with_regex(pko_operation, o, 'sender_address', 'Adres nadawcy: (?P<addr>.*)', 'addr')
			parse_description_to_field_with_regex(pko_operation, o, 'conversion_date', 'Data przetworzenia: (?P<date>\\d{4}-\\d{2}-\\d{2})', 'date')
			parse_description_to_field_with_regex(pko_operation, o, 'title', 'Tytuł: (?P<title>.*)', 'title')
			parse_original_payment_amount(pko_operation, o)
			parse_simple_location(pko_operation, o)
			parse_full_location(pko_operation, o)

			# ignore unimportant descriptions
			parse_ignore_description(pko_operation, 'Data i czas operacji: (?P<date>\\d{4}-\\d{2}-\\d{2})')
			parse_ignore_description(pko_operation, 'Numer telefonu: \\+48 665 396 588')
			parse_ignore_description(pko_operation, 'KAPIT\\.ODSETEK KARNYCH-OBCIĄŻENIE')
			parse_ignore_description(pko_operation, 'Referencje własne zleceniodawcy:')
			if o.type is OperationType.US_PAYMENT:
				parse_ignore_description(pko_operation, 'Nazwa i nr identyfikatora:')
				parse_ignore_description(pko_operation, 'Symbol formularza:')
				parse_ignore_description(pko_operation, 'Okres płatności:')
			if o.type in [OperationType.MOBILE_PAYMENT, OperationType.TERMINAL_RETURN]:
				parse_ignore_description(pko_operation, 'Numer referencyjny:')
			if o.type in [OperationType.CARD_PAYMENT, OperationType.CARD_PAYMENT_RETURN, OperationType.ATM_OUT]:
				parse_ignore_description(pko_operation, 'Numer karty: 425125.*452')

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

	return operations


def parse_description_to_field_with_regex(pko_operation: PkoBpOperation, target_obj, target_field_name, regex: str, regex_group_name: str):
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
