#Import os
import os

#Import find_qualifying_loans
from app import find_qualifying_loans

# Import pathlib
from pathlib import Path

# Import fileio
from qualifier.utils import fileio

# Import Calculators
from qualifier.utils import calculators

# Import Filters
from qualifier.filters import credit_score
from qualifier.filters import debt_to_income
from qualifier.filters import loan_to_value
from qualifier.filters import max_loan_size

## Global mock data ##

test_csv_header = ['Lender','Max Loan Amount','Max LTV','Max DTI','Min Credit Score','Interest Rate']
test_csv_data = [
    ['Always Loans, Inc.', '999999', '99.9', '99.9', '0', '2'], 
    ['Sometimes Loans, Corp.', '500000', '0.5', '0.5', '500', '5'],
    ['Never Loans, LLC.', '1', '0.01', '0.01', '999', '100']
]

## File IO Tests ##

def test_save_csv():
    
    # write test CSV using global dummy data
    test_csv_path = Path("tests/data/output/qualifying-loans.csv") 
    test_csv_contents = [test_csv_header] + test_csv_data
    fileio.save_csv(test_csv_path, test_csv_contents)

    # ensure file was written at the correct path
    assert Path.exists(test_csv_path)

    # ensure file contents are as expected
    reloaded_csv = fileio.load_csv(test_csv_path)
    # assert file length is correct (load_csv automatically removes the header row)
    assert len(reloaded_csv) == len(test_csv_data)
    # assert file entries match the test data (compare first two bank names)
    assert reloaded_csv[0][0] == test_csv_data[0][0]
    assert reloaded_csv[1][0] == test_csv_data[1][0]

    # delete the test file output 
    os.remove(test_csv_path)


## Calculator Tests ##

def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84


## Filter Tests ##

def test_filter_credit_score():
    assert len(credit_score.filter_credit_score(1000, test_csv_data)) == 3
    assert len(credit_score.filter_credit_score(500, test_csv_data)) == 2
    assert len(credit_score.filter_credit_score(0, test_csv_data)) == 1

def test_filter_debt_to_income():
    assert len(debt_to_income.filter_debt_to_income(0.01, test_csv_data))== 3
    assert len(debt_to_income.filter_debt_to_income(0.5, test_csv_data))== 2
    assert len(debt_to_income.filter_debt_to_income(99.9, test_csv_data))== 1

def test_filter_loan_to_value():
    assert len(loan_to_value.filter_loan_to_value(0.01, test_csv_data))== 3
    assert len(loan_to_value.filter_loan_to_value(0.5, test_csv_data))== 2
    assert len(loan_to_value.filter_loan_to_value(99.9, test_csv_data))== 1 

def test_filter_max_loan_size():
    assert len(max_loan_size.filter_max_loan_size(1, test_csv_data))== 3
    assert len(max_loan_size.filter_max_loan_size(400000, test_csv_data))== 2
    assert len(max_loan_size.filter_max_loan_size(700000, test_csv_data))== 1

## End to end Tests ##

def test_one_qualifying_loan_available():
    result = find_qualifying_loans(
        bank_data=test_csv_data,
        credit_score=100,
        debt=10,
        income=100,
        loan=100,
        home_value=100)
    assert len(result) == 1
    assert result[0][0] == "Always Loans, Inc."

def test_no_qualifying_loans_available():
    # temporarily remove "Always Loans, Inc." from the mock dataset
    no_lenders = test_csv_data[1:]
    result = find_qualifying_loans(
        bank_data=no_lenders,
        credit_score=499,
        debt=0,
        income=100,
        loan=100,
        home_value=100)
    assert len(result) == 0

def test_multiple_qualifying_loans_available():
    result = find_qualifying_loans(
        bank_data=test_csv_data,
        credit_score=501,
        debt=0,
        income=10000,
        loan=1000,
        home_value=100000)
    assert len(result) == 2
    assert result[0][0] == "Always Loans, Inc."
    assert result[1][0] == "Sometimes Loans, Corp."
