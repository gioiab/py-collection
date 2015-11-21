"""
Created on 19/11/2015

@author: gioia

This script provides my solution to the challenge of flatting an array of arbitrarily nested arrays.

Input:
* an array of nested arrays - e.g.: [[1,2,[3]],4]

Output:
* the flattened array - e.g.: [1,2,3,4]

The code is organized as follows:
- the flat_list function performs the flatting task;
- the FlatListTest class provides test cases for the flat_list function.

The algorithm used by the flat_list function does not restrict the use of this code to array of integers. Indeed,
it is applicable even to characters, strings, dictionaries and generic objects.

The programming language used is Python 2.7 and it is assumed you have it installed into your PC. The operating system
of reference is Linux. There are two basic ways to execute this script in Linux:
1 - launching it by the command shell through the python command;
2 - making it executable first and then launching it by the command shell.


Enjoy!
"""
import unittest


def flat_list(l):
    """
    Flattens an input list made by arbitrarily nested lists.

    :param l: the input list
    :return: the flattened list
    """
    if not isinstance(l, list):
        return [l]
    else:
        return [e for k in l for e in flat_list(k)]


class FlatListTest(unittest.TestCase):
    """
    Provides test cases for the flat_list function.
    """

    def test_empty(self):
        self.assertEqual(flat_list([]), [])

    def test_no_list(self):
        self.assertEqual(flat_list(1), [1])
        self.assertEqual(flat_list('a'), ['a'])
        self.assertEqual(flat_list('hello'), ['hello'])
        self.assertEqual(flat_list({1: 2}), [{1: 2}])

    def test_no_nesting(self):
        self.assertEqual(flat_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flat_list(['a', 'b', 'c']), ['a', 'b', 'c'])
        self.assertEqual(flat_list(['Just', 'a', 'challenge']), ['Just', 'a', 'challenge'])
        self.assertEqual(flat_list([{1: 2}, {'a': 'b'}]), [{1: 2}, {'a': 'b'}])

    def test_one_level_testing(self):
        self.assertEqual(flat_list([1, [2, 3], 4]), [1, 2, 3, 4])
        self.assertEqual(flat_list([['a', 'b'], 'c']), ['a', 'b', 'c'])
        self.assertEqual(flat_list(['Just', ['a'], 'challenge']), ['Just', 'a', 'challenge'])
        self.assertEqual(flat_list([{1: 2}, [{'a': 'b'}], {'c': 3}]), [{1: 2}, {'a': 'b'}, {'c': 3}])

    def test_two_levels_testing(self):
        self.assertEqual(flat_list([1, [2, [3]], 4]), [1, 2, 3, 4])
        self.assertEqual(flat_list([['a', 'b'], ['c', ['d']]]), ['a', 'b', 'c', 'd'])
        self.assertEqual(flat_list(['Just', [['a'], 'challenge']]), ['Just', 'a', 'challenge'])
        self.assertEqual(flat_list([{1: 2}, [[{'a': 'b'}], {'c': 3}]]), [{1: 2}, {'a': 'b'}, {'c': 3}])

    def test_three_levels_testing(self):
        self.assertEqual(flat_list([1, [2, [3]], 4, [5, [6, [7, 8, 9]]]]), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(flat_list([['a', 'b'], ['c', ['d', 'e', ['f', 'g']]]]), ['a', 'b', 'c', 'd', 'e', 'f', 'g'])
        self.assertEqual(flat_list(['Just', [['a', ['big']], 'challenge']]), ['Just', 'a', 'big','challenge'])
        self.assertEqual(flat_list([{1: 2}, [[{3: 4}, [{5: 6}]], {7: 8}]]), [{1: 2}, {3: 4}, {5: 6}, {7: 8}])


if __name__ == '__main__':
    """The entry point of the program. It simply runs the test cases.
    """
    unittest.main()
