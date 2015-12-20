"""
Created on 20/dec/2015

@author: gioia

The script provides my solution to the repayment calculator challenge. The challenge regards the implementation of a
rate calculation system allowing prospective borrowers to obtain a quote from a provided pool of lenders for 36 months
loans.


Input:
* The market csv file containing the information about lenders (lender's name, lent amount, lent rate)
* The requested loan amount

Output:
* The request loan amount
* The rate of the loan
* the monthly repayment amount
* the total repayment amount

The programming language used is Python 2.7 and it is assumed you have it installed into your PC together with
SciPy (http://www.scipy.org/). The operating system of reference is Unix-based (Linux/Max OS-X). There are two basic
ways to execute this script in Unix:
1 - launching it by the command shell through the python command
2 - making it executable first and then launching it by the command shell

Enjoy!
"""
import csv
import math
import locale
import argparse
import scipy.optimize as opt

_CSV_DELIMITER = ','                # Defines the expected delimiter of the input market file
_YEARS = 3                          # Defines the years of duration of the loan
_MONTHS = 12                        # Defines the repayment basis (monthly)
_LOAD_DURATION = _MONTHS * _YEARS   # Defines the loan duration
_MIN_LOAN_AMOUNT = 1000             # Defines the minimum accepted loan amount
_MAX_LOAN_AMOUNT = 15000            # Defines the maximum accepted loan amount
_LOAN_INCREMENT = 100               # Defines the accepted loan increment


def _get_input():
    parser = argparse.ArgumentParser(description='**** TODO ***.')
    parser.add_argument('market_file', metavar='market_file', type=str, help='the full path to the market csv file')
    parser.add_argument('loan_amount', metavar='loan_amount', type=float, help='the requested loan amount')
    args = parser.parse_args()
    return args.market_file, args.loan_amount

def _is_loan_request_valid(loan_amount):
    is_greater_than_min = loan_amount >= _MIN_LOAN_AMOUNT
    is_lesser_than_max = loan_amount <= _MAX_LOAN_AMOUNT
    is_a_multiple = loan_amount % 100 == 0
    return  is_greater_than_min and is_lesser_than_max and is_a_multiple

def _get_rates_cache(market_file):
    rates_cache = {}
    with open(market_file, 'rb') as infile:
        csv_reader = csv.reader(infile, delimiter=_CSV_DELIMITER)
        csv_reader.next()
        for row in csv_reader:
            rate = float(row[1])
            lent_amount = float(row[2])
            rates_cache[rate] = rates_cache.get(rate, 0) + lent_amount
    return rates_cache

def _can_be_quoted(loan_amount, lent_amounts):
    return sum(lent_amounts) - loan_amount >= 0;

def _get_monthly_repay(rate, lent_amount):
    monthly_rate = math.pow(1 + rate, 1 / float(_MONTHS)) - 1
    return (lent_amount * monthly_rate) / (1 - (1 / float(math.pow(1 + monthly_rate, _LOAD_DURATION))))

def nr_input_f(x, y, z):
    return z - _get_monthly_repay(x, y)

def _get_repayments(loan_amount, rates_cache):
    rates = rates_cache.keys()
    rates.sort()

    rates_idx = 0
    sum_rates = 0.0
    total_repay = 0.0
    monthly_repay = 0.0
    to_borrow = loan_amount
    while (to_borrow > 0) and (rates_idx < len(rates)):
        rate = rates[rates_idx]
        lent_amount = rates_cache[rate]
        if to_borrow >= lent_amount:
            to_borrow -= lent_amount
            monthly_repay += _get_monthly_repay(rate, lent_amount)
        else:
            monthly_repay += _get_monthly_repay(rate, to_borrow)
            to_borrow = 0
        sum_rates += rate
        rates_idx += 1

    total_repay += monthly_repay * _LOAD_DURATION

    avg_rate = sum_rates / float(rates_idx)
    rate = opt.newton(nr_input_f, avg_rate, args=(loan_amount, monthly_repay)) * 100
    return rate, monthly_repay, total_repay

def _display_results(loan_amount, monthly_repay, rate, total_repay):
    print 'Requested amount: {}'.format(locale.currency(loan_amount))
    print 'Rate: {rate:.{digits}f}%'.format(rate=rate, digits=1)
    print 'Monthly repayment: {}'.format(locale.currency(monthly_repay))
    print 'Total repayment: {}'.format(locale.currency(total_repay))

def main():
    """
    The main function of the program. First, the input parameters are collected and validated.
    If the inputs pass the checks then...

    """
    locale.setlocale(locale.LC_ALL, 'en_gb') # Changes the locale settings to deal with pounds
    market_file, loan_amount = _get_input()  # Collects the inputs
    valid_request = _is_loan_request_valid(loan_amount)  # Validates the loan amount
    if valid_request: # If the request is valid...
        rates_cache = _get_rates_cache(market_file)  # Computes the hash map of the available rates/amounts
        quote_available = _can_be_quoted(loan_amount, rates_cache.values())  # Checks if a quote is available...
        if quote_available:  # If it is...
            rate, monthly_repay, total_repay = _get_repayments(loan_amount, rates_cache)  # Gets repayments information
            _display_results(loan_amount, monthly_repay, rate, total_repay)  # Displays the results
        else:  # ... else returns an error message
            print 'We''re very sorry but it''s not possible to provide a quote at this time.'
    else:
        print 'We''re very sorry but you entered an invalid request!'
        print 'You can request a loan for at least 1000 pound and at most 15000 pound with a 100 pound increment only.'


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
