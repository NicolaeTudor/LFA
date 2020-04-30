import queue
import copy

def print_to_output_automat(states, statesNumber, outputFile, finalStates, initialState):
    for i in range(statesNumber):
        state = states[i]
        for value, toStates in state.items():
            for toState in toStates:
                outputFile.write(str(i) + ' ' + str(toState) + ' ' + value + '\n')
    outputFile.write(str(initialState) + '\n')
    outputFile.write(str(finalStates.__len__()) + '\n')
    for state in finalStates:
        outputFile.write(str(state) + ' ')


def go_to_next_state(states, currentStates, value):
    result = set()
    for currentState in currentStates:
        if value in states[currentState]:
            result.update(states[currentState][value])

    # if result.__len__() == 0:
    #     return -1

    return result


def find_reachable_states(states, statesNumber, initialState):
    reachableStates = [False]*statesNumber
    q = queue.Queue(maxsize=0)
    q.put(initialState)
    reachableStates[initialState] = True
    while not q.empty():
        currentState = q.get()
        for toStates in states[currentState].values():
            for toState in toStates:
                if reachableStates[toState] is False:
                    q.put(toState)
                    reachableStates[toState] = True

    return reachableStates


def find_word_generating_states(reverseTransitionStates, finalStates, statesNumber):
    wordGeneratingStates = [False]*statesNumber
    q = queue.Queue(maxsize=0)
    for finalState in finalStates:
        q.put(finalState)
        wordGeneratingStates[finalState] = True

    while not q.empty():
        currentState = q.get()
        for state in reverseTransitionStates[currentState]:
            if wordGeneratingStates[state] is False:
                q.put(state)
                wordGeneratingStates[state] = True

    return wordGeneratingStates



def get_alphabet(states):
    alphabet = set()
    for state in states:
        for value in state:
            alphabet.add(value)

    return alphabet


def get_epsilon_closure(states, statesNumber):
    statesEpsilonClosure = {}

    for i in range(statesNumber):
            statesEpsilonClosure[i] = states[i]['*']
    changed = True
    while changed:
        changed = False
        for i in range(statesNumber):
            updatedClosure = set()
            stateClosure = statesEpsilonClosure[i]
            for state in stateClosure:
                updatedClosure = updatedClosure.union(statesEpsilonClosure[state])
            if updatedClosure != stateClosure:
                changed = True
                statesEpsilonClosure[i] = updatedClosure
    return statesEpsilonClosure


def epsilon_NFA_to_NFA(epsilonStates, statesNumber, alphabet):
    nfaStates = [{} for _ in range(statesNumber)]
    for value in alphabet:
        if value == '*':
            continue
        for i in range(statesNumber):
            afterValueStates = go_to_next_state(epsilonStates, states[i]['*'], value)
            afterEpsilonStates = go_to_next_state(epsilonStates, afterValueStates, '*')
            if afterEpsilonStates.__len__() != 0:
                nfaStates[i][value] = afterEpsilonStates

    return nfaStates


def NFA_to_DFA(nfaStates, statesNumber, alphabet, finalStates):
    dfaStates = copy.deepcopy(nfaStates)
    nfa_to_dfa_map = {(i,): i for i in range(statesNumber)}
    dfa_to_nfa_map = {i: set([i]) for i in range(statesNumber)}

    i = 0
    while i < statesNumber:
        for value in alphabet:
            afterValueStates = go_to_next_state(nfaStates, dfa_to_nfa_map[i], value)
            if afterValueStates.__len__() == 0:
                continue
            if tuple(afterValueStates) in nfa_to_dfa_map:
                newFinalState = nfa_to_dfa_map[tuple(afterValueStates)]
                dfaStates[i][value] = set([newFinalState])
            else:
                nfa_to_dfa_map.update({tuple(afterValueStates): statesNumber})
                dfa_to_nfa_map.update({statesNumber: afterValueStates})
                if finalStates.intersection(afterValueStates).__len__() != 0:
                    finalStates.add(statesNumber)
                statesNumber += 1
                dfaStates += [{}]
                newFinalState = nfa_to_dfa_map[tuple(afterValueStates)]
                dfaStates[i][value] = set([newFinalState])
        i += 1
    return dfaStates, finalStates, statesNumber


def remove_redundant_states(states, statesNumber, functionalStates, finalStates):
    nextFreeState = 0
    reserializedStates = []
    minimizeReadyFinalStates = set()
    for i in range(statesNumber):
        if functionalStates[i] is True:
            reserializedStates += [nextFreeState]
            if i in finalStates:
                minimizeReadyFinalStates.add(nextFreeState)
            nextFreeState += 1
        else:
            reserializedStates += [-1]
    minimizeReadyStates = []
    for i in range(statesNumber):
        if reserializedStates[i] == -1:
            statesNumber -= 1
            continue
        minimizeReadyStates += [{}]
        for value, toStates in states[i].items():
            minimizeReadyToStates = set()
            for toState in toStates:
                if reserializedStates[toState] == -1:
                    continue
                minimizeReadyToStates.add(reserializedStates[toState])
            minimizeReadyStates[reserializedStates[i]][value] = minimizeReadyToStates
    return minimizeReadyStates, statesNumber, minimizeReadyFinalStates


def complete_DFA(states, statesNumber, alphabet):
    completeStates = [{} for _ in range(statesNumber)]
    sinkState = False
    for i in range(statesNumber):
        for value in alphabet:
            if value in states[i]:
                completeStates[i][value] = states[i][value].pop()
            else:
                sinkState = True
                completeStates[i][value] = statesNumber
    if sinkState:
        completeStates += [{value: statesNumber for value in alphabet}]
    return completeStates, sinkState

def minimize_DFA(dfaStates, finalStates, statesNumber, initialState):
    minimizedDfaStates = []
    minimizedFinalStates = set()
    minimizedStatesNumber = 2

    if finalStates.__len__() == 0:
        minimizedDfaStates += [{value: 0 for value in alphabet}]
        return minimizedDfaStates, minimizedFinalStates, 1, 0
    if finalStates.__len__() == statesNumber:
        minimizedDfaStates += [{value: 0 for value in alphabet}]
        return minimizedDfaStates, set([0]), 1, 0

    minimizedFinalStates.add(0)
    partition = [finalStates, set()]
    partitionRep = [0, 0]
    stateRepartization = []
    for i in range(statesNumber):
        if i not in finalStates:
            stateRepartization += [1]
            partitionRep[1] = i
            partition[1].add(i)
        else:
            stateRepartization += [0]
            partitionRep[0] = i

    changed = True
    while changed:
        changed = False
        oldStateRepartization = copy.deepcopy(stateRepartization)
        updatedPartition = []
        updatedRep = []
        for i in range(minimizedStatesNumber):
            repState = partitionRep[i]
            newPartition = set()
            newRepartization = minimizedStatesNumber
            for state in partition[i]:
                for value in alphabet:
                    if oldStateRepartization[dfaStates[state][value]] != oldStateRepartization[dfaStates[repState][value]]:
                        newPartition.add(state)
                        newRepresentant = state
                        changed = True
                        stateRepartization[state] = newRepartization
                        minimizedStatesNumber = newRepartization + 1
                        break
            if newPartition.__len__() != 0:
                partition[i] = partition[i].difference(newPartition)
                partition += [newPartition]
                partitionRep += [newRepresentant]
                if i in minimizedFinalStates:
                    minimizedFinalStates.add(newRepartization)

    for state in partitionRep:
        minimizedDfaStates += [{value:set([stateRepartization[dfaStates[state][value]]]) for value in alphabet}]

    initialState = stateRepartization[initialState]

    return minimizedDfaStates, minimizedFinalStates, minimizedStatesNumber, initialState


# start main
fin = open("input", "r")
fout = open("output", "w")

statesNumber = int(fin.readline())
transitionsNumber = int(fin.readline())
states = [{'*' : set([i])} for i in range(statesNumber)]


for transition in range(transitionsNumber):
    line = fin.readline().split()
    stateSt = int(line[0])
    stateFn = int(line[1])
    value = line[2]

    if value not in states[stateSt]:
        states[stateSt][value] = set([stateFn])
    else:
        states[stateSt][value].add(stateFn)

initialState = int(fin.readline())
finalStatesNumber = int(fin.readline())
finalStates = set()
line = fin.readline().split()
for finalState in line:
    finalStates.update({int(finalState)})

fout.write('*-NFA:\n')
print_to_output_automat(states, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')

alphabet = get_alphabet(states)

statesEpsilonClosure = get_epsilon_closure(states, statesNumber)

for i in range(statesNumber):
    states[i]['*'] = statesEpsilonClosure[i]

if initialState not in finalStates and finalStates.intersection(go_to_next_state(states, set([initialState]), '*')).__len__() != 0:
    finalStates.add(initialState)

nfaStates = epsilon_NFA_to_NFA(states, statesNumber, alphabet)
alphabet.remove('*')

fout.write('NFA:\n')
print_to_output_automat(nfaStates, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')

dfaStates, finalStates, statesNumber = NFA_to_DFA(nfaStates, statesNumber, alphabet, finalStates)

fout.write('DFA:\n')
print_to_output_automat(dfaStates, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')

reachableStates = find_reachable_states(dfaStates, statesNumber, initialState)

reverseTransitionStates = [set() for _ in range(statesNumber)]

for i in range(statesNumber):
    for value, toStates in dfaStates[i].items():
        for toState in toStates:
            reverseTransitionStates[toState].add(i)


wordGeneratingStates = find_word_generating_states(reverseTransitionStates, finalStates, statesNumber)

functionalStates = []

for i in range(statesNumber):
    if reachableStates[i] == True and wordGeneratingStates[i] == True:
        functionalStates += [True]
    else:
        functionalStates += [False]

minimizeReadyStates, statesNumber, finalStates = remove_redundant_states(dfaStates, statesNumber, functionalStates, finalStates)
completeStates, sinkState = complete_DFA(minimizeReadyStates, statesNumber, alphabet)
if sinkState:
    statesNumber += 1

minimizedDfaStates, finalStates, statesNumber, initialState = minimize_DFA(completeStates, finalStates, statesNumber, initialState)

fout.write('DFA-min:\n')
print_to_output_automat(minimizedDfaStates, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')
