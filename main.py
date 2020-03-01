import numpy as np
import pandas as pd

from operation import OperationType
from parsers import pko
from topics import *

GENERAL = Topic("GENERAL")
EXPENSES = Topic("EXPENSES", GENERAL)
HOME = Topic("HOME", EXPENSES)
RENT = Topic("RENT", HOME)
SHOPPING = Topic("SHOPPING", HOME)
DELIVERY_FOOD = Topic("DELIVERY_FOOD", HOME)
CAT = Topic("CAT", HOME)
WORK = Topic("WORK", EXPENSES)
LUNCHES = Topic("LUNCHES", WORK)
FROG = Topic("FROG", WORK)
SUBWAY = Topic("SUBWAY", WORK)

FOOD = Topic("FOOD", EXPENSES)
FAST_FOODS = Topic("FAST_FOODS", FOOD)
RESTAURANTS = Topic("RESTAURANTS", FOOD)

SPORT = Topic("SPORT", EXPENSES)
MULTISPORT = Topic("MULTISPORT", SPORT)
SNOWBOARDING = Topic("SNOWBOARDING", SPORT)
CLIMBING = Topic("CLIMBING", SPORT)
CLIMBING_EQUIPMENT = Topic("CLIMBING_EQUIPMENT", CLIMBING)
ENTRANCE = Topic("ENTRANCE", CLIMBING)
POOL = Topic("POOL", SPORT)
BADMINTON = Topic("BADMINTON", SPORT)
BOXING = Topic("BOXING", SPORT)

ENTERTAINMENT = Topic("ENTERTAINMENT", EXPENSES)
NIGHTS_OUT = Topic("NIGHTS_OUT", ENTERTAINMENT)
SPECTACLES = Topic("SPECTACLES", ENTERTAINMENT)
NETFLIX_ISH = Topic("NETFLIX_ISH", ENTERTAINMENT)

CAR = Topic("CAR", EXPENSES)
FUEL = Topic("FUEL", CAR)
REPAIRS = Topic("REPAIRS", CAR)
HIGHWAYS = Topic("HIGHWAYS", CAR)
CAR_FOOD = Topic("CAR_FOOD", CAR)
CAR_EQUIPMENT = Topic("CAR_EQUIPMENT", CAR)

HOLIDAY = Topic("HOLIDAY", EXPENSES)
TRIP = Topic("TRIP", HOLIDAY)
TRANSPORT = Topic("TRANSPORT", HOLIDAY)
AT_THE_PLACE = Topic("AT_THE_PLACE", HOLIDAY)

INCOMES = Topic("INCOMES", GENERAL)
LUFTHANSA = Topic("LUFTHANSA", INCOMES)
LUFTHANSA_INCOME = Topic("LUFTHANSA_INCOME", LUFTHANSA)
LUFTHANSA_DELEGATION = Topic("LUFTHANSA_DELEGATION", LUFTHANSA)

print_assignment_code_for_structure(GENERAL)
print_structure(GENERAL)

if __name__ == '__main__':
	#

	# df = pd.read_csv(file_path) # pandas
	# filename = './data/history_csv_20190609_170438.csv'
	filename = './data/history_csv_20190609_170438_sample.csv'
	# filename = './data/js_20200101_20200131.csv'
	operations = pko.load_and_parse_operations(filename)

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
