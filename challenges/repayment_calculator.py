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
    """
    Gets the input parameters.

    :return: the pair (market_file, loan_about) as a tuple
    """
    parser = argparse.ArgumentParser(description='The rate calculation system allows borrowers to obtain a quote.')
    parser.add_argument('market_file', metavar='market_file', type=str, help='the full path to the market csv file')
    parser.add_argument('loan_amount', metavar='loan_amount', type=float, help='the requested loan amount')
    args = parser.parse_args()
    return args.market_file, args.loan_amount

def _is_loan_request_valid(loan_amount):
    """
    Checks whether the input loan is valid.

    :param loan_amount: the requested loan amount
    :return: True if the input loan is valid, False otherwise
    """
    # Checks if the loan amount is contained within well known boundaries
    is_greater_than_min = loan_amount >= _MIN_LOAN_AMOUNT
    is_lesser_than_max = loan_amount <= _MAX_LOAN_AMOUNT
    # Checks if the loan amount has an "accepted increment"
    is_a_multiple = loan_amount % 100 == 0
    return is_greater_than_min and is_lesser_than_max and is_a_multiple

def _get_rates_cache(market_file):
    """
    Given the market file as input, computes a hash map in which the keys are the
    available rates and the values represent the total amount available at a given rate.

    :param market_file: the input market file
    :return: the hash map of (key, value) pairs in which key is a rate and, value is the sum
             of the available amounts at that rate.
    """
    rates_cache = {}
    with open(market_file, 'rb') as infile:
        csv_reader = csv.reader(infile, delimiter=_CSV_DELIMITER)
        csv_reader.next()  # Skips the header
        for row in csv_reader:
            rate = float(row[1])
            lent_amount = float(row[2])
            rates_cache[rate] = rates_cache.get(rate, 0) + lent_amount
    return rates_cache

def _can_be_quoted(loan_amount, lent_amounts):
    """
    Checks if the borrower can obtain a quote. To this aim, the loan amount should be less than or
    equal to the total amounts given by lenders.

    :param loan_amount: the requested loan amount
    :param lent_amounts: the sum of the amounts given by lenders
    :return: True if the borrower can get a quote, False otherwise
    """
    return sum(lent_amounts) - loan_amount >= 0;

def _get_monthly_repay(rate, loan):
    """
    Gets the monthly repayment by computing the compound interest.

    :param rate: the nominal rate
    :param loan: the loan that should be returned
    :return: the monthly repayment for the given rate and loan
    """
    monthly_rate = math.pow(1 + rate, 1 / float(_MONTHS)) - 1
    return (loan * monthly_rate) / (1 - (1 / float(math.pow(1 + monthly_rate, _LOAD_DURATION))))

def nr_input_f(rate, loan, monthly_rate):
    """
    Function used to compute the interest from the monthly rate using the Newton-Raphson method.

    :param rate: the rate that should be used as initial point of the secant method
    :param loan: the requested loan amount
    :param monthly_rate: the computed monthly rate
    :return: the input equation of the secant method
    """
    return monthly_rate - _get_monthly_repay(rate, loan)

def _get_repayments(loan_amount, rates_cache):
    """
    Gets the repayment information by computing the compound interest for the loan. Following a greedy approach,
    the available rates are first ordered. Then, the monthly rate is computed starting from the more convenient
    rates till the less convenient ones.

    :param loan_amount: the requested loan amount
    :param rates_cache: the computed hash map of (rate, amount) pairs
    :return: the repayment information as a tuple (rate, monthly_repay, total_repay)
    """
    rates = rates_cache.keys()
    rates.sort()  # Sorts the collected rates

    rates_idx = 0
    sum_rates = 0.0
    total_repay = 0.0
    monthly_repay = 0.0
    to_borrow = loan_amount
    while (to_borrow > 0) and (rates_idx < len(rates)):
        rate = rates[rates_idx]
        lent_amount = rates_cache[rate]
        if to_borrow >= lent_amount:  # if the current lent amount is less then the amount needed...
            to_borrow -= lent_amount
            monthly_repay += _get_monthly_repay(rate, lent_amount)
        else:  # ...else
            monthly_repay += _get_monthly_repay(rate, to_borrow)
            to_borrow = 0
        sum_rates += rate
        rates_idx += 1
    # Computes the total repayment from the monthly repayment
    total_repay += monthly_repay * _LOAD_DURATION
    # Computes the average rate to feed it as initial point of the secant method
    avg_rate = sum_rates / float(rates_idx)
    rate = opt.newton(nr_input_f, avg_rate, args=(loan_amount, monthly_repay)) * 100
    return rate, monthly_repay, total_repay

def _display_results(loan_amount, rate, monthly_repay, total_repay):
    """
    Simply displays the repayment results with the right rounding.

    :param loan_amount: the requested loan amount
    :param rate: the computed loan rate
    :param monthly_repay: the computed monthly repayment
    :param total_repay: the computed total repayment
    """
    print 'Requested amount: {}'.format(locale.currency(loan_amount))
    print 'Rate: {rate:.{digits}f}%'.format(rate=rate, digits=1)
    print 'Monthly repayment: {}'.format(locale.currency(monthly_repay))
    print 'Total repayment: {}'.format(locale.currency(total_repay))

def main():
    """
    The main function of the program. First, the input parameters are collected and validated.
    Then the repayments information are computed and returned.
    """
    locale.setlocale(locale.LC_ALL, 'en_gb') # Changes the locale settings to deal with pounds
    market_file, loan_amount = _get_input()  # Collects the inputs
    valid_request = _is_loan_request_valid(loan_amount)  # Validates the loan amount
    if valid_request: # If the request is valid...
        rates_cache = _get_rates_cache(market_file)  # Computes the hash map of the available rates/amounts
        quote_available = _can_be_quoted(loan_amount, rates_cache.values())  # Checks if a quote is available...
        if quote_available:  # If it is...
            rate, monthly_repay, total_repay = _get_repayments(loan_amount, rates_cache)  # Gets repayments information
            _display_results(loan_amount, rate, monthly_repay, total_repay)  # Displays the results
        else:  # ... else returns an error message
            print 'We''re very sorry but it''s not possible to provide a quote at this time.'
    else:
        print 'We''re very sorry but you entered an invalid request!'
        print 'You can request a loan for at least 1000 pound and at most 15000 pound with a 100 pound increment only.'


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
