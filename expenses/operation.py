from dataclasses import dataclass
from enum import Enum


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

	def __str__(self):
		title_str = f"{self.title if self.title else '(noTitle)'}"
		location_str = f"{self.location if self.location else '(noLocation)'}"
		orig_amount_str = self.original_amount if self.original_amount else ""
		orig_curr_str = self.original_currency if self.original_currency else ""
		return \
			f'{self.transaction_type:36}' \
			f' || {self.amount:>10}' \
			f' || loc: {location_str:64}' \
			f' || title: {title_str:90}' \
			f' || rec: {self.receiver_account!s:32} - {self.receiver_name !s:32}' \
			f' || sen: {self.sender_account!s:32} - {self.sender_name!s:32}' \
			f' || orig: {orig_amount_str:>10} {orig_curr_str :3}' \
			f' || other:{self.other}'

	def __lt__(self, other):
		return self.transaction_type.__lt__(other)
