"""
Created on 08/dic/2013

@author: gioia

This script provides my solution to the challenge about writing a medical diagnosis utility. This utility should
compute the probability that someone has measles given various diagnostics.

Input:
* The file model.csv: it contains the probabilistic model.
* The prior probability that someone has measles.

Example format of the model.csv file:
Measles,Spots,Fever,Probability
1,1,1,0.6
1,0,1,0.25
1,1,0,0.1
1,0,0,0.05
0,1,1,0.05
0,0,1,0.2
0,1,0,0.35
0,0,0,0.4

Output:
* The system provides the probability a person has measles given either a subset or all the diagnostics observed.
  It is possible to define a custom set of diagnostic directly in the model.csv file.

The programming language used is Python and it is assumed you have it installed into your pc. The operating system
of reference is Linux. There are two basic ways to execute this script:
1 - launching it by the command shell through the python command: python path_to_the_script args
2 - making it executable first and then launching by the command shell as: ./file_name args
   (assuming we are into the folder containing the file)

Enjoy!
"""
import sys, csv
import argparse
import itertools


def _get_model_info(model_csv):
    """Given a csv file containing the model information, this methods returns the following as output:
       - a list of the features of the model
       - a dictionary representing the model
       Admitted feature values are concatenated in order to form the key of the model dictionary. To each key, 
       (i.e. combination of feature values), the corresponding probability value is assigned.
    """
    model_as_dict = dict()       
    with open(model_csv, 'r') as csvfile:
        dict_file = csv.DictReader(csvfile)
        features = [field.lower().strip() for field in dict_file.fieldnames[:-1]]
        for row in dict_file:
            dict_row = {key.lower().strip(): value.strip() for (key, value) in row.iteritems()}
            dict_key = ''.join(dict_row[field] for field in features)
            dict_value = float(dict_row['probability'])
            model_as_dict[dict_key] = dict_value
    return features, model_as_dict

def _compute_tmp_keys(features, args):
    """This function computes the keys used to retrieve the probabilities from the model dictionary. It handles the case in which some
       variables are not observed by generating all the possible 'labels' with the missing characters. The base assumption is that a 
       character may be set to a binary value only (0, 1).
    """
    tmp_key = ''
    tmp_keys = []
    placeholder = '%s'
    for idx in range(1, len(features)): # Assuming "measles" is always the first feature/column into the csv file
        f = features[idx]
        if f not in args or args[f] is None:
            tmp_key = tmp_key + placeholder # A temp placeholder for the absent features
        else:
            tmp_key = tmp_key + args[f]
    ph_count = tmp_key.count(placeholder)
    if ph_count > 0:
        permutations = [tuple(''.join(seq)) for seq in itertools.product("01", repeat=ph_count)]
        for perm in permutations:
            tmp_keys.append(tmp_key % perm)
    else:
        tmp_keys.append(tmp_key)
    return tmp_keys

def _compute_posterior_prob(features, model_as_dict, prior, **args):
    """This function is devoted to do the actual computation of the posterior probability. It computes:
       1. the set of keys used to compute the probability that a 'c'-ondition happens given the person has the measles (p_c_m_keys)
       2. the set of keys used to compute the probability that a 'c'-ondition happens given the person doesn't have the measles (p_c_nm_keys)
       3. the probability that a 'c'-ondition happens given the person has the measles (p_c_m) as the sum of the retrieved probability for all 
          the p_c_m_keys
       4. the probability that a 'c'-ondition happens given the person doesn't have the measles (p_c_m) as the sum of the retrieved probability 
          for all the p_c_nm_keys
       5. the probability that the person has the 'm'-easles given that a certain 'c'-ondition happened (p_m_c), by means of the Bayes Theorem
          and the Total Probability Theorem.
    """
    tmp_keys = _compute_tmp_keys(features, args)
    p_c_m_keys = ['1' + key for key in tmp_keys]  # Assuming "measles" is always the first feature/column into the csv file
    p_c_nm_keys = ['0' + key for key in tmp_keys] # Assuming "measles" is always the first feature/column into the csv file
    p_c_m = 0.0
    p_c_nm = 0.0
    for p_c_m_key in p_c_m_keys:
        p_c_m = p_c_m + model_as_dict[p_c_m_key]
    for p_c_nm_key in p_c_nm_keys:
        p_c_nm = p_c_nm + model_as_dict[p_c_nm_key]
    p_c = p_c_m * prior + p_c_nm * (1.0 - prior)  # Total probability theorem
    p_m_c = p_c_m * prior / p_c                   # Bayes theorem
    return p_m_c


def main():
    """The main function of the program. It is devoted to parse command line arguments, to compute the right input arguments and it
       finally returns the posterior probability based onto the input arguments given.
    """
    # Command line parsing
    parser = argparse.ArgumentParser(description = '''This script is my solution to the medical diagnosis challenge. The programming language used
                                                      is Python and it is assumed you have it installed into your pc. The operating system of reference 
                                                      is Linux. Script usage: python path_to_the_script prg_args''')
    main_group = parser.add_argument_group('Mandatory arguments')
    main_group.add_argument('-model', help='the full path where the model.csv file is stored into the system (mandatory)', required=True)
    main_group.add_argument('-prior', help='the prior probability that someone has measles (mandatory)', required=True, type=float)
    
    opt_group = parser.add_argument_group('Optional arguments')
    opt_group.add_argument('-fever', help='the presence/absence of fever among the symptoms')
    opt_group.add_argument('-spots', help='the presence/absence of spots among the symptoms')
    opt_group.add_argument('-other_features', help='a dictionary of other symptoms (use python syntax)', type=str)
    args = parser.parse_args()
    # Building the dictionary of the input arguments
    input_features = dict()
    input_features['fever'] = args.fever
    input_features['spots'] = args.spots
    
    if args.other_features is not None:
        try: 
            args.other_features = eval(args.other_features)
            input_features.update(args.other_features)
        except: 
            sys.stderr('Invalid syntax for the dictionary of the other features.')
    given_features, model_as_dict = _get_model_info(args.model)
    if (args.fever is None) and (args.spots is None) and not args.other_features:
        parser.print_help()
        print
        sys.exit('ERROR: Almost one optional argument, taken from (fever, spots, ..) should be given as input!')
    # Computing the posterior probability
    post_p = _compute_posterior_prob(given_features, model_as_dict, args.prior, **input_features)
    print 'The posterior probability is...', post_p
    
    
if __name__ == '__main__':
    """The entry point of the program. It simply recalls the main function.
    """
    main()