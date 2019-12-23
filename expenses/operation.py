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
     INTEREST,
     PAYBYNET_BLIK,
     GAIN,
     *_] = range(100)

    def __lt__(self, other):
        return self.value < other.value


class Location:
    country = None
    city = None
    address = None


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
        # return "{:>10} {:>8}".format(self.type.name, self.amount)
        # return "{0.type.name} {0.amount}".format(self)
        return "{type.name:>18} {amount:>10} {currency:>4}".format(**self.__dict__)

    def __lt__(self, other):
        return self.type.__lt__(other)
