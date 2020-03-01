import numpy as np
import pandas as pd

from operation import OperationType
from parsers import pko
from topics import *

GENERAL = Topic("GENERAL")
GENERAL.EXPENSES = EXPENSES = Topic("EXPENSES", GENERAL)
GENERAL.EXPENSES.HOME = EXPENSES.HOME = HOME = Topic("HOME", EXPENSES)
GENERAL.EXPENSES.HOME.RENT = EXPENSES.HOME.RENT = HOME.RENT = RENT = Topic("RENT", HOME)
GENERAL.EXPENSES.HOME.SHOPPING = EXPENSES.HOME.SHOPPING = HOME.SHOPPING = SHOPPING = Topic("SHOPPING", HOME)
GENERAL.EXPENSES.HOME.DELIVERY_FOOD = EXPENSES.HOME.DELIVERY_FOOD = HOME.DELIVERY_FOOD = DELIVERY_FOOD = Topic("DELIVERY_FOOD", HOME)
GENERAL.EXPENSES.HOME.CAT = EXPENSES.HOME.CAT = HOME.CAT = CAT = Topic("CAT", HOME)
GENERAL.EXPENSES.WORK = EXPENSES.WORK = WORK = Topic("WORK", EXPENSES)
GENERAL.EXPENSES.WORK.LUNCHES = EXPENSES.WORK.LUNCHES = WORK.LUNCHES = LUNCHES = Topic("LUNCHES", WORK)
GENERAL.EXPENSES.WORK.FROG = EXPENSES.WORK.FROG = WORK.FROG = FROG = Topic("FROG", WORK)
GENERAL.EXPENSES.WORK.SUBWAY = EXPENSES.WORK.SUBWAY = WORK.SUBWAY = SUBWAY = Topic("SUBWAY", WORK)
GENERAL.EXPENSES.FOOD = EXPENSES.FOOD = FOOD = Topic("FOOD", EXPENSES)
GENERAL.EXPENSES.FOOD.FAST_FOODS = EXPENSES.FOOD.FAST_FOODS = FOOD.FAST_FOODS = FAST_FOODS = Topic("FAST_FOODS", FOOD)
GENERAL.EXPENSES.FOOD.RESTAURANTS = EXPENSES.FOOD.RESTAURANTS = FOOD.RESTAURANTS = RESTAURANTS = Topic("RESTAURANTS", FOOD)
GENERAL.EXPENSES.SPORT = EXPENSES.SPORT = SPORT = Topic("SPORT", EXPENSES)
GENERAL.EXPENSES.SPORT.MULTISPORT = EXPENSES.SPORT.MULTISPORT = SPORT.MULTISPORT = MULTISPORT = Topic("MULTISPORT", SPORT)
GENERAL.EXPENSES.SPORT.SNOWBOARDING = EXPENSES.SPORT.SNOWBOARDING = SPORT.SNOWBOARDING = SNOWBOARDING = Topic("SNOWBOARDING", SPORT)
GENERAL.EXPENSES.SPORT.CLIMBING = EXPENSES.SPORT.CLIMBING = SPORT.CLIMBING = CLIMBING = Topic("CLIMBING", SPORT)
GENERAL.EXPENSES.SPORT.CLIMBING.CLIMBING_EQUIPMENT = EXPENSES.SPORT.CLIMBING.CLIMBING_EQUIPMENT = SPORT.CLIMBING.CLIMBING_EQUIPMENT = CLIMBING.CLIMBING_EQUIPMENT = CLIMBING_EQUIPMENT = Topic("CLIMBING_EQUIPMENT", CLIMBING)
GENERAL.EXPENSES.SPORT.CLIMBING.ENTRANCE = EXPENSES.SPORT.CLIMBING.ENTRANCE = SPORT.CLIMBING.ENTRANCE = CLIMBING.ENTRANCE = ENTRANCE = Topic("ENTRANCE", CLIMBING)
GENERAL.EXPENSES.SPORT.POOL = EXPENSES.SPORT.POOL = SPORT.POOL = POOL = Topic("POOL", SPORT)
GENERAL.EXPENSES.SPORT.BADMINTON = EXPENSES.SPORT.BADMINTON = SPORT.BADMINTON = BADMINTON = Topic("BADMINTON", SPORT)
GENERAL.EXPENSES.SPORT.BOXING = EXPENSES.SPORT.BOXING = SPORT.BOXING = BOXING = Topic("BOXING", SPORT)
GENERAL.EXPENSES.ENTERTAINMENT = EXPENSES.ENTERTAINMENT = ENTERTAINMENT = Topic("ENTERTAINMENT", EXPENSES)
GENERAL.EXPENSES.ENTERTAINMENT.NIGHTS_OUT = EXPENSES.ENTERTAINMENT.NIGHTS_OUT = ENTERTAINMENT.NIGHTS_OUT = NIGHTS_OUT = Topic("NIGHTS_OUT", ENTERTAINMENT)
GENERAL.EXPENSES.ENTERTAINMENT.SPECTACLES = EXPENSES.ENTERTAINMENT.SPECTACLES = ENTERTAINMENT.SPECTACLES = SPECTACLES = Topic("SPECTACLES", ENTERTAINMENT)
GENERAL.EXPENSES.ENTERTAINMENT.NETFLIX_ISH = EXPENSES.ENTERTAINMENT.NETFLIX_ISH = ENTERTAINMENT.NETFLIX_ISH = NETFLIX_ISH = Topic("NETFLIX_ISH", ENTERTAINMENT)
GENERAL.EXPENSES.CAR = EXPENSES.CAR = CAR = Topic("CAR", EXPENSES)
GENERAL.EXPENSES.CAR.FUEL = EXPENSES.CAR.FUEL = CAR.FUEL = FUEL = Topic("FUEL", CAR)
GENERAL.EXPENSES.CAR.REPAIRS = EXPENSES.CAR.REPAIRS = CAR.REPAIRS = REPAIRS = Topic("REPAIRS", CAR)
GENERAL.EXPENSES.CAR.HIGHWAYS = EXPENSES.CAR.HIGHWAYS = CAR.HIGHWAYS = HIGHWAYS = Topic("HIGHWAYS", CAR)
GENERAL.EXPENSES.CAR.CAR_FOOD = EXPENSES.CAR.CAR_FOOD = CAR.CAR_FOOD = CAR_FOOD = Topic("CAR_FOOD", CAR)
GENERAL.EXPENSES.CAR.CAR_EQUIPMENT = EXPENSES.CAR.CAR_EQUIPMENT = CAR.CAR_EQUIPMENT = CAR_EQUIPMENT = Topic("CAR_EQUIPMENT", CAR)
GENERAL.EXPENSES.HOLIDAY = EXPENSES.HOLIDAY = HOLIDAY = Topic("HOLIDAY", EXPENSES)
GENERAL.EXPENSES.HOLIDAY.TRIP = EXPENSES.HOLIDAY.TRIP = HOLIDAY.TRIP = TRIP = Topic("TRIP", HOLIDAY)
GENERAL.EXPENSES.HOLIDAY.TRANSPORT = EXPENSES.HOLIDAY.TRANSPORT = HOLIDAY.TRANSPORT = TRANSPORT = Topic("TRANSPORT", HOLIDAY)
GENERAL.EXPENSES.HOLIDAY.AT_THE_PLACE = EXPENSES.HOLIDAY.AT_THE_PLACE = HOLIDAY.AT_THE_PLACE = AT_THE_PLACE = Topic("AT_THE_PLACE", HOLIDAY)
GENERAL.INCOMES = INCOMES = Topic("INCOMES", GENERAL)
GENERAL.INCOMES.LUFTHANSA = INCOMES.LUFTHANSA = LUFTHANSA = Topic("LUFTHANSA", INCOMES)
GENERAL.INCOMES.LUFTHANSA.LUFTHANSA_INCOME = INCOMES.LUFTHANSA.LUFTHANSA_INCOME = LUFTHANSA.LUFTHANSA_INCOME = LUFTHANSA_INCOME = Topic("LUFTHANSA_INCOME", LUFTHANSA)
GENERAL.INCOMES.LUFTHANSA.LUFTHANSA_DELEGATION = INCOMES.LUFTHANSA.LUFTHANSA_DELEGATION = LUFTHANSA.LUFTHANSA_DELEGATION = LUFTHANSA_DELEGATION = Topic("LUFTHANSA_DELEGATION", LUFTHANSA)
GENERAL.INCOMES.PARENTS = INCOMES.PARENTS = PARENTS = Topic("PARENTS", INCOMES)
GENERAL.INCOMES.PARENTS.PARENT_PRESENTS = INCOMES.PARENTS.PARENT_PRESENTS = PARENTS.PARENT_PRESENTS = PARENT_PRESENTS = Topic("PARENT_PRESENTS", PARENTS)
GENERAL.INCOMES.PARENTS.PARENT_RETURNS = INCOMES.PARENTS.PARENT_RETURNS = PARENTS.PARENT_RETURNS = PARENT_RETURNS = Topic("PARENT_RETURNS", PARENTS)

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
