from dataclasses import dataclass, field
from typing import List

from operation import OperationType

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
    operationDate: str
    currencyDate: str
    transactionType: str
    amount: str
    currency: str
    afterTransactionBalance: str
    description: List[str] = field(default_factory=list)

    def __str__(self):
        return f'{self.id:4}' \
               f' | {self.operationDate:10}' \
               f' | {self.transactionType:32}' \
               f' | {self.currency:3}' \
               f' | {self.amount:>8}' \
               f' | {self.afterTransactionBalance:>9}' \
               f' | {self.description[1]:{0 if self.description[1] is None else 90}}' \
               f' | {self.description[2]}' \
               f' | {self.description[3]}' \
               f' | {self.description[4]}' \
               f' | {self.description[5]}' \
               f' | {self.description[6]}' \
               f' | {self.description[0]:32}'

        # @classmethod
        # def get_mapping(cls, pko_operation_name: str) -> operation.OperationType:
        #     return cls.typeMappings[pko_operation_name]
