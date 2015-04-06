"""
Created on 06/apr/2015

@author: gioia

The script provides my solution to an advanced version of the "K difference" challenge. The challenge is about counting
the total pairs of numbers whose difference is K in a list of N non-unique positive integers.

Input:
* the first line contains N (the number of positive integers) and K (the difference)
* the second line contains the N integers

Output:
* the number of pairs whose difference is K

Enjoy!
"""


def get_pairs(l, k):
    """
    Given a list L of N positive integers, returns the count of the total pairs of numbers whose difference is K.
    First, each integer is stored into a dictionary along with its frequency. Then, for each integer I in the input
    list, the presence of the integer I+K is checked within the dictionary. The computational time complexity of the
    algorithm is still O(N).

    :param k: the given difference
    :type k: int
    :param l: the list of input integers
    :type l: list
    :return: the count of the total pairs of numbers whose difference is k
    :rtype: int
    """
    hash_map = {}
    for i in l:
        hash_map[i] = hash_map.get(i, 0) + 1
    return sum([hash_map[i + k] for i in l if hash_map.get(i + k)])


def main():
    """
    The main function of the program. It collects the inputs and calls the get_pairs function.
    """
    _, k = map(int, raw_input().split())
    l = map(int, raw_input().split())
    print get_pairs(l, k)


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
