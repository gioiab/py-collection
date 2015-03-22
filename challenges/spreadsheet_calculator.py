"""
Created on 08/feb/2015

@author: gioia

The script provides my solution to the challenge about implementing a basic spreadsheet calculator.

Input:
* The first line should contain two integers: n, m - where n is width of the spreadsheet while m is its height.
* The next n*m lines should contain the content of the related spreadsheet cell. This content is an RPN expression,
  which may contain references to other spreadsheet cells.

Output:
* The first line of the input as it was provided.
* The next n*m lines contain the computed value for every spreadsheet cell.

The programming language used is Python 2.7 and it is assumed you have it installed into your PC. The operating system
of reference is Linux. There are two basic ways to execute this script in Linux:
1 - launching it by the command shell through the python command
2 - making it executable first and then launching it by the command shell

Enjoy!

Started: Feb 8, at 12:20 CET time
Finished: Feb 8, at 15:40 CET time
"""
import re, sys, operator

_IS_NUM_REGEXP = '^-?[0-9]+\.?[0-9]*$'
_IS_CELL_REGEXP = '^[A-Z][1-9]+$'
 
operators = {'+': operator.add,
             '-': operator.sub,
             '*': operator.mul,
             '/': operator.div,
             '++': operator.iadd,
             '--': operator.isub
             }
    
def _calc_basic(expression):
    """This function actually computes the floating point value associated to a
       RPN expression in stack order.
       
       Args:
           expression: the expression which has to be evaluated.
       Returns:
           the stack containing the resulting value of the expression.
    """
    stack = []
    for token in expression:
        if re.match(_IS_NUM_REGEXP, str(token)):
            stack.append(float(token))
        elif operators.get(token, False):
            if len(token) < 2:
                a = stack.pop()
            else:
                a = 1
            b = stack.pop()
            op = operators[token]
            stack.append(op(b,a))
        else:
            sys.exit('An invalid operand was found within the expression! Please check your input.')
    return stack
    
def _calc_one(spreadsheet, callers, expression):
    """This function is called on every spreadsheet cell. It recursively compute the value of a cell.
       If the value of a cell contains itself a reference to another cell, the recursion is activated
       until a final value is obtained. The argument "callers" is updated each time in order to detect
       cyclic dependencies.
       
       Args:
           spreadsheet: the spreadsheet at issue.
           callers: the set of keys which refer the current expression.
           expression: the expression which has to be evaluated.
       Returns:
           the value computed for the input expression.
    """
    new_expression = []
    for token in expression:
        if re.match(_IS_CELL_REGEXP, str(token)):
            if token in callers:
                sys.exit('A cyclic dependence was found! Please check your input.')
            callers.extend(token)
            new_expression.extend(_calc_one(spreadsheet, callers, spreadsheet[token]))
        else:
            new_expression.append(str(token))
    return _calc_basic(new_expression)
        
def _calc(spreadsheet):
    """This function calls _calc_one for every spreadsheet cell. This means that the
       expression contained in each cell is recursively evaluated.
       
       Args:
           spreadsheet: the spreadsheet at issue.
    """
    for key, value in spreadsheet.items():
        spreadsheet[key] = _calc_one(spreadsheet, [key], value)
        
def main():
    """The main function of the program. It first collects the input into a proper data
       structure, then it executes the computations needed to get the final results and
       finally it prints the results in the required format.
    """
    n, m = map(int, raw_input().split())
    rows_range = map(chr, range(65, 65+m))
    cols_range = [i+1 for i in xrange(n)]
    spreadsheet = {}
    for r in rows_range:
        for c in cols_range:
            spreadsheet['%s%s' % (r,c)] = raw_input().split()
    _calc(spreadsheet)
    print n, m
    for r in rows_range:
        for c in cols_range:
            print '%.5f' % spreadsheet['%s%s' % (r,c)][0]

if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()