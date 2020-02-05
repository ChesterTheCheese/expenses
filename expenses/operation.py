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


@dataclass(init=False)
class Operation:
    date: str = None
    type: OperationType = None
    amount: int = None
    currency: str = None
    balance: int = None
    description: str = None
    location: Location = None
    timestamp: str = None

    title = None

    otherInfo: str = ''

    # receiver
    receiverAccount: str = None
    receiverName: str = None
    receiverAddress: str = None

    # sender
    senderAccount: str = None
    senderName: str = None
    senderAddress: str = None

    def __str__(self):
        title_str = f"{self.title if self.title else '(noTitle)'}"
        location_str = f"{self.location if self.location else '(noLocation)'}"
        return \
            f'{self.type:36}' \
            f' || {self.amount:>10}' \
            f" || loc: {location_str:64}  " \
            f" || title: {title_str:90}" \
            f' || rec: {self.receiverAccount!s:32}' \
            f' || sen: {self.senderAccount!s:32}' \
            f' || other:{self.otherInfo}'

    def __lt__(self, other):
        return self.type.__lt__(other)
