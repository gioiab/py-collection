"""
Created on 11/apr/2014

@author: gioia

This script aims to "hack" the _hash method. Given a hash and string length as input, 
it finds the string with the given length and hash. The characters of the string should be
taken from the set "acdegilmnoprstuw". In what follows, there is a brief analysis of the 
hashing method.

"Trial run" of the _hash method:
n = len(input_string)
for brevity: h[t=-1] = h[-1]

h[-1] = 7
h[0] = h[-1] * 37 + letters.idx[0]
h[1] = h[0] * 37 + letters[1] = (h[-1] * 37 + letters.idx[0]) * 37 + letters.idx[1] = 37^2 h[-1] + 37 letters.idx[0] + letters.idx[1] 
...
h[n-1] = 37^(n-1) * h[-1] + 37^(n-2) * letters.idx[0] + 37^(n-3) * letters.idx[1] + ... + 37 * letters.idx[n-2] + letters.idx[n-1]

"""
_LETTERS = 'acdegilmnoprstuw'

def _hash(input_string, input_letters):
    assert isinstance(input_string, str)
    assert isinstance(input_letters, str)
    h = 7
    for char in input_string:
        print h, h * 37, input_letters.index(char)
        h = (h * 37 + input_letters.index(char))
    return h
    
def _get_reminders(n_base_10, target_base):
    reminders = []
    n = n_base_10
    while n != 0:
        reminder = n % target_base
        n = n / target_base
        reminders.append(reminder)
    return reminders

def _get_string_from_hash(input_hash, input_length, input_letters):
    output_string = ''
    reminders = _get_reminders(input_hash, 37)
    useful_reminders = reminders[:input_length]
    for idx in range(input_length-1, -1, -1):
        useful_reminder = useful_reminders[idx]
        output_string = output_string + input_letters[useful_reminder]
    return output_string

def _get_challenge_solution(input_letters):
    return _get_string_from_hash(910897038977002, 9, input_letters)

def main():
    input_letters = _LETTERS
    
    challenge_solution = _get_challenge_solution(input_letters)
    print 'The challenge solution is...', challenge_solution
    print
    print 'Now you can play with this script!'
    input_hash = long(raw_input('Insert a computed hash...\n'))
    input_length = int(raw_input('Insert the length of the final string...\n'))
    output_string = _get_string_from_hash(input_hash, input_length, input_letters)
    print 'The challenge solution for your custom case is...', output_string
    
    
if __name__ == '__main__':
    main()

