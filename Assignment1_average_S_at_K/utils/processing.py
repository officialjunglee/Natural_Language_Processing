from nltk.corpus import wordnet as wn
from nltk.metrics import edit_distance
import json
import pytrec_eval
import numpy as np
import matplotlib.pyplot as plt

def MED(word):
    """
    Returns a list containing the distance and word from dictionary using Minimum Edit Distance (MED) algorithm
    """
    dictionary = wn.words()
    suggestions_dist=[]
    for dict_word in dictionary:
        distance = edit_distance(word, dict_word)
        if distance <=10:
            suggestions_dist.append((distance,dict_word))

    return sorted(suggestions_dist, key=lambda val:val[0])


def analyze_words(agl):
    incorrect,correct=agl[0],agl[1]
    temp_result={'incorrect':incorrect, 'correct':correct}
    suggestion_list=MED(incorrect)
    for n in [1,5,10]:
        temp_result[n]=list(np.array([word[1] for word in suggestion_list if word[0]<=suggestion_list[n-1][0]]))
    print(f'done for word: ',{incorrect})
    return temp_result

def final_eval(results_list):
    arguments_taken_ordered={}
    output_list={}
    for result in results_list:
        arguments_taken_ordered[result["incorrect"]]={result["correct"]:1}
        output_list[result["incorrect"]]={}
        for n,words in [(1,result[1]), (5,result[5]), (10,result[10])]:
            for word in words:
                if word not in output_list[result["incorrect"]].keys():
                    output_list[result["incorrect"]][word]=1/n
    evaluater=pytrec_eval.RelevanceEvaluator(arguments_taken_ordered,{'success'})
    print(json.dumps(evaluater.evaluate(output_list),indent=1))
    eval=evaluater.evaluate(output_list)
    print('averages success at s@k for k=[1,5,10] for a set of 120 random mispelled words from BirkBeck corpus')
    print(eval[list(eval.keys())[0]].keys())
    print(list(eval[list(eval.keys())[0]].keys()))
    for measure in sorted(list(eval[list(eval.keys())[0]].keys())):
        print(measure, 'average: ',pytrec_eval.compute_aggregated_measure(measure,[query_measures[measure] for query_measures in eval.values()]))

   