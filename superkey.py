from itertools import *
def main():
    relation = ['A','B','C','G','H']
    rawdependencies = [
        (['A','C'],       ['B']),
        (['G'],         ['H'])
        ]
    close_on = frozenset(['B'])
    
    dependencies = {}
    
    #put all the dependencies into a dictionary with frozensets so 
    #that they are hashable and unordered
    for dependency in rawdependencies:
        dependencies[frozenset(dependency[0])] = dependency[1]

    #get list of superkeys
    supers = getSuperKeys(getCombs(relation,dependencies,all=True),dependencies,len(relation))
    print("#of superkeys: ",len(list(supers)),"\n",supers,"\n")
    
    #get list of condidate keys
    candidates = getCandidateKeys(getCombs(relation,dependencies,all=True),dependencies,len(relation))
    print("#of candidatekeys: ",len(candidates),"\n",candidates,"\n")
    
    #computer closure on the close_onvariable
    result = calculateClosure(close_on,dependencies)
    printClosure(relation,close_on, result)


#This method will look through a list of superkeys to determine which ones 
# follow the candidate key criteria. It returns a list of all candidate keys
    #Candidate keys are those with no propper subset that is a superkey
#combs: This is a combination set that will be tested for candidate keys
#dependencies: This is the set of functional dependencies tested against
#len_for_superkey: This is the length of the relation, to test closure against
def getCandidateKeys(combs,dependencies,len_for_superkey):

    #get superkeys
    superKeys = getSuperKeys(combs,dependencies,len_for_superkey)

    to_remove = []
    #for every combination in the given list
    for combination in superKeys:
        temp_dependencies = dependencies.copy()#copy dependency to not edit the original
        """         #check if the combination is a superkey, if not, skip
        if len(calculateClosure(combination,temp_dependencies)) != len_for_superkey:
            to_remove.append(combination)
            continue     """

        subsets = getCombs(combination,dependencies,all=True)  
        subsets.remove(combination)

        #for every subset in the found superkey
        for subset in subsets:
            temp_dependencies = dependencies.copy()#copy dependency to not edit the original
            result = calculateClosure(subset,temp_dependencies)
            #check if any subset is a superkey, if so, remove
            if len(result) == len_for_superkey:
                to_remove.append(combination)
                break
    #return list of combinations that were found to be candidate keys
    return [item for item in superKeys if item not in to_remove]
                

#This method will return a list of all superkeys. It tests a list of combinations
# for which ones are superkeys
#relation_combs: This is the list to be tested
#dependencies: This is the set of functional dependencies tested against
#len_for_superkey: This is the length of the relation, to test closure against
def getSuperKeys(relation_combs,dependencies,len_for_superkey):
    superKeys = []
    for comb in relation_combs:
        temp_dependencies = dependencies.copy()#copy dependency to not edit the original
        result = calculateClosure(frozenset(comb),temp_dependencies,all=True)

        if len(result) == len_for_superkey:#if superkey      
            superKeys.append(comb)

    return superKeys


def printClosure(relation,close_on,result):
    print("R: " + str(relation))
    print("Compute: " + str(list(close_on)) + "+")
    print(str(list(close_on)) + "+: " + str(sorted(list(result))))

#This tests a combination for its closure. Returns a list of all attributes included
# in the closure.
#Closure: the combination to test
#dependencies: list of dependencies to test against.
#all: Check all possible subsets of the combination,
#       If false, will only check the combinations 
#       with size >= biggest functional dependency
def calculateClosure(closure,dependencies,all=False):

    combs = getCombs(closure,dependencies,all)

    #for each combination, check if there is a functional dependency 
    # that can be applied
    for comb in combs:
        x = dependencies.get(frozenset(comb),None) #get FD, or None
        #if FD exists, add it to the closure set
        if x is not None:
            closure = frozenset(closure).union(x)
            dependencies.pop(frozenset(comb))

            if(len(dependencies.keys()) == 0 or len(dependencies) == 0): return closure
            closure = calculateClosure(closure,dependencies)
        
    return closure


#return every possible combination of the attributes given
#attributes: The list of attributes that we will be creating tuples from
#dependencies: The list of functional dependencies (FDs)
#all: If True, this signifies we are returning all possible combinations
#     If False, we will only return combinations of size n or smaller,
#       where n is the maximum size of a possible key for "dependencies"
def getCombs(attributes,dependencies, all=False):
    largest_combination = len(max(dependencies.keys()))#get larges key size
    
    #if all is true, set largest combination size to get all possible combinations
    if all:
        largest_combination = len(attributes)+1

    combs = []
    for x in range(1, len(attributes)+1):
        #if the size of the tuple excedes that of largest combination, we are done.
        if x > largest_combination:
            return combs
        
        #use the combination method to pull out all combinations of size x
        result = list(combinations(attributes,x))
        
        #for each combination, if its a singleton, pull out value, then add to list
        for element in result:
            if len(element) == 1:
                combs += frozenset(element[0])
            else:
                combs += frozenset(result)
                break
    
    return combs


if __name__ == "__main__":
    main()
