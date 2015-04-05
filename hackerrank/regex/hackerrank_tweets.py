"""
Created on 05/apr/2015

@author: gioia

The script provides my solution to the following Hackerrank challenge:

https://www.hackerrank.com/challenges/hackerrank-tweets

Input:
* the first line contains the number of test cases
* Each following line contains a tweet

Output:
* the number of tweets containing the word "hackerrank"

Enjoy!
"""
from re import search, IGNORECASE

_TWEET_REGEX = r'hackerrank'


def has_hashtag(tweet):
    """
    Given a tweet, tells if it contains the static hashtag.

    :param tweet: the input tweet
    :type tweet: str
    :return: True if the tweet contains the hashtag, False otherwise
    :rtype: bool
    """
    return bool(search(_TWEET_REGEX, tweet, IGNORECASE))


def main():
    """
    The main function of the program. It simply sums the results coming from the has_hashtag function.
    """
    n = input()
    print sum([has_hashtag(raw_input()) for _ in xrange(n)])

if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
