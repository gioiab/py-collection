"""
Created on 05/apr/2015

@author: gioia

The script provides my solution to the following Hackerrank challenge:

https://www.hackerrank.com/challenges/valid-pan-format

Input:
* the first line contains the number of test cases
* Each following line contains a word possibly representing a valid PAN number

Output:
* for each PAN number candidate: "YES" if it's valid, "NO" otherwise

Enjoy!
"""
from re import match

_PAN_REGEX = r'^[A-Z]{5}[0-9]{4}[A-Z]$'


def is_valid_pan(s):
    """
    Given a pan number, tells if it's valid or not.

    :param s: the input pan number
    :type s: str
    :return: "YES" if the PAN number if valid, "NO" otherwise
    :rtype: str in ("YES", "NO")
    """
    if match(_PAN_REGEX, s):
        return 'YES'
    return 'NO'


def main():
    """
    The main function of the program. It first collects the number of test cases N. Then, it iterates on N
    thus acquiring and evaluating all the input strings.
    """
    n = input()
    for _ in xrange(n):
        print is_valid_pan(raw_input())

if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()