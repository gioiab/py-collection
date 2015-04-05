"""
Created on 05/apr/2015

@author: gioia

The script provides my solution to the following Hackerrank challenge:

https://www.hackerrank.com/challenges/funny-string

Input:
* the first line contains the number of test cases
* each following line contains one input string

Output:
* either "Funny" or "Not Funny" whether the string follows the "funny" constraint or not

Enjoy!
"""


def is_funny_str(s):
    """
    Given an input string, tells if the string if funny or not.

    :param s: the input string
    :type s: str
    :return: either "Funny" or "Not Funny" whether the string follows the "funny" constraint or not
    :rtype: str in ("Funny", "Not Funny")
    """
    n = len(s)
    for i in xrange(1, n):
        if abs(ord(s[i])-ord(s[i-1])) != abs(ord(s[n-i])-ord(s[n-i-1])):
            return 'Not Funny'
    return 'Funny'

def main():
    """
    The main function of the program. It first collects the number of test cases T. Then, it iterates on T
    thus acquiring and evaluating all the input strings.
    """
    t = input()
    for _ in xrange(t):
        print is_funny_str(raw_input())

if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()

