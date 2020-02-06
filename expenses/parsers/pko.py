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
