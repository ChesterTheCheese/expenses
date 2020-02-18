import numpy as np
import pandas as pd

from operation import OperationType
from parsers import pko

if __name__ == '__main__':
    # df = pd.read_csv(file_path) # pandas
    # filename = './data/history_csv_20190609_170438.csv'
    filename = './data/history_csv_20190609_170438_sample.csv'
    # filename = './data/js_20200101_20200131.csv'
    operations = pko.load_file(filename)

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

    # TODO: general complex PaymentMatcher to properly categorize operations into PaymentTopics
    # TODO: topics hierarchy tree
