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
                change = True
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


# start main
fin = open("input", "r")
fout = open("output", "w")

statesNumber = int(fin.readline())
transitionsNumber = int(fin.readline())
states = [{'*' : set([i])} for i in range(statesNumber)]
reverseTransitionStates = [set() for _ in range(statesNumber)]

for transition in range(transitionsNumber):
    line = fin.readline().split()
    stateSt = int(line[0])
    stateFn = int(line[1])
    value = line[2]

    if value not in states[stateSt]:
        states[stateSt][value] = set([stateFn])
    else:
        states[stateSt][value].add(stateFn)

    reverseTransitionStates[stateFn].add(stateSt)

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

nfaStates = epsilon_NFA_to_NFA(states, statesNumber, alphabet)
alphabet.remove('*')

fout.write('NFA:\n')
print_to_output_automat(nfaStates, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')

dfaStates, finalStates, statesNumber = NFA_to_DFA(nfaStates, statesNumber, alphabet, finalStates)

fout.write('DFA:\n')
print_to_output_automat(dfaStates, statesNumber, fout, finalStates, initialState)
fout.write('\n\n')

