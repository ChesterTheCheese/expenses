from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List

from topics import Topic


class OperationType(Enum):
	[CARD_PAYMENT,
	 CARD_PAYMENT_RETURN,
	 TRANSFER_OUT,
	 TRANSFER_IN,
	 ATM_OUT,
	 ATM_IN,
	 CHARGE,
	 STANDING_ORDER,
	 MOBILE_PAYMENT,
	 ZUS_PAYMENT,
	 US_PAYMENT,
	 TERMINAL_RETURN,
	 INTEREST_TAX,
	 PAYBYNET_BLIK,
	 GAIN,
	 *_] = range(100)

	def __lt__(self, other):
		return self.value < other.value


class Location:
	country = None
	city = None
	address = None

	def __str__(self) -> str:
		country = self.country + ' - ' if self.country else ''
		city = self.city + ' - ' if self.city else ''
		return f"{country}{city}{self.address}"


@dataclass(init=False)  # initialize all to None so that attributes can be checked for emptiness
class Operation:
	date: str = None
	transaction_type: OperationType = None
	amount: float = None
	currency: str = None
	balance: float = None
	description: str = None
	location: Location = None
	timestamp: str = None
	title: str = None
	topic: Topic = None

	other: str = ''

	original_amount: float = None
	original_currency: str = None
	conversion_date: str = None

	# receiver
	receiver_account: str = None
	receiver_name: str = None
	receiver_address: str = None

	# sender
	sender_account: str = None
	sender_name: str = None
	sender_address: str = None

	def get_init_location(self) -> Location:
		self.location = Location()
		return self.location

	def __str__(self):
		title_str = f"{self.title if self.title else '(noTitle)'}"
		location_str = f"{self.location if self.location else '(noLocation)'}"
		orig_amount_str = self.original_amount if self.original_amount else ""
		orig_curr_str = self.original_currency if self.original_currency else ""
		return \
			f'{self.transaction_type if self.transaction_type else "-- UNKNOWN --":36}' \
			f' || {self.amount:>10}' \
			f' || loc: {location_str:64}' \
			f' || title: {title_str:90}' \
			f' || rec: {self.receiver_account!s:32} - {self.receiver_name !s:32}' \
			f' || sen: {self.sender_account!s:32} - {self.sender_name!s:32}' \
			f' || orig: {orig_amount_str:>10} {orig_curr_str :3}' \
			f' || other:{self.other}'

	def __lt__(self, other):
		return self.transaction_type.__lt__(other)

	def __eq__(self, o: object) -> bool:
		return super().__eq__(o)

	def __hash__(self) -> int:
		return super().__hash__()


def get_valid_operations(all_operations):
	valid = [o for o in all_operations if o.transaction_type]
	return valid


def check_entries_count(operations: List[Operation], csv_count):
	""" check csv lines count vs operation count """
	print(f'csv entries: {csv_count} all_operations: {len(operations)}')
	return csv_count == len(operations)


def check_untyped(operations: List[Operation]) -> List[Operation]:
	""" check if all bank operation have an TransactionType """
	untyped = [o for o in operations if not o.transaction_type]
	print(f'untyped operations: {len(untyped)}')
	for row in untyped:
		print(f'\t{row}')
	# if len(missed_bank_operations):
	# 	print(f'missed bank all_operations: {len(missed_bank_operations)} ^')
	print(f'untyped operations: {len(untyped)} ^')
	return untyped


def check_untopiced(operations: List[Operation]) -> List[Operation]:
	""" check if all descriptions were mapped or ignored (should print nothing) """
	untopiced = [o for o in operations if not o.topic]
	print(f'untopiced operations: {len(untopiced)}')
	for o in untopiced:
		print(f'\t{o.transaction_type}, {o.title}, {o.location}')
	# if len(untopiced):
	# 	print(f'unmapped description parts: {len(untopiced)} ^')
	print(f'untopiced operations: {len(untopiced)} ^')
	return untopiced


def check_unassigned_descriptions(operations: List[Operation]) -> List[Operation]:
	# check if all descriptions were mapped or ignored (should print nothing)
	unassigned = [o for o in operations if o.other]
	print(f'unassigned description parts: {len(unassigned)}')
	for o in unassigned:
		print(f'\t{o.transaction_type}, {o.other}')
	# if len(unassigned):
	# 	print(f'unassigned description parts: {len(unassigned)} ^')
	print(f'unassigned description parts: {len(unassigned)} ^')
	return unassigned


def check_ignored_descriptions(ignored: List[str]):
	""" check ignored entries (should print long list) """
	ignored.sort()  # sort alphabetically
	print(*ignored, sep='\n')
