import concurrent
from concurrent.futures import ProcessPoolExecutor
import random
from utils.processing import analyze_words, final_eval

if __name__=="__main__":

    correct_spellings = []
    incorrect_spellings = []
    file_ = open('/Users/officialjunglee/Downloads/Average_S_at_K/Data/missp.dat', 'r')
    Lines = file_.readlines()

    # Strips the newline character
    corr=''
    incr=''
    for line in Lines:
        if '$' in line:
            corr = line.replace('$', '').replace('\n', '').lower()
        else:
            incr = line.lower().replace('\n', '')
            correct_spellings.append(corr)
            incorrect_spellings.append(incr)

    print(f'Total no of incorrect words in Birkbeck corpus: ',{len(incorrect_spellings)})

    argument_list=[(incr,corr) for incr,corr in zip(incorrect_spellings,correct_spellings)]

    #selecting ranadom 100 words from corpus
    new_argument_list=random.sample(argument_list,2)
    #print(new_argument_list)

    result_list=[]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(analyze_words, new_argument_list):
            result_list.append(result)
    print(result_list)

    final_eval(result_list)






