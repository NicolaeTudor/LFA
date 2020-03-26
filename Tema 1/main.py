import queue


def go_to_next_state(states, currentStates, value):
    result = set()
    for currentState in currentStates:
        if value in states[currentState]:
            result.update(states[currentState][value])

    if result.__sizeof__() == 0:
        return -1

    return result


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


def generate_first_valid_inputs(initialState, states, finalStates, wordGeneratingStates):
    generatedWords = set()
    fout = open("output", "w")
    validInputs = 100
    q = queue.Queue(maxsize=0)
    q.put((initialState, ''))
    while validInputs > 0 and not q.empty():
        (currentState, generatedWord) = q.get()
        for value, transitionStates in states[currentState].items():
            word = generatedWord + value
            for state in transitionStates:
                if wordGeneratingStates[state] is True:
                    if state in finalStates:
                        if word not in generatedWords:
                            generatedWords.add(word)
                            fout.write(word + '\n')
                            validInputs -= 1
                    q.put((state, word))
    if q.empty():
        fout.write('\n' + "No more words can be generated! Words generated: " + str(100-validInputs))


# start main
fin = open("input", "r")

statesNumber = int(fin.readline())
transitionsNumber = int(fin.readline())
states = [{} for _ in range(statesNumber)]
reverseTransitionStates = [set() for _ in range(statesNumber)]

for transition in range(transitionsNumber):
    line = fin.readline().split()
    stateSt = int(line[0])
    stateFn = int(line[1])
    value = line[2]

    if value not in states[stateSt]:
        states[stateSt][value] = [stateFn]
    else:
        states[stateSt][value] += [stateFn]

    reverseTransitionStates[stateFn].add(stateSt)

initialState = int(fin.readline())
finalStatesNumber = int(fin.readline())
finalStates = set()
line = fin.readline().split()
for finalState in line:
    finalStates.update({int(finalState)})

wordsNumber = int(fin.readline())
for _ in range(wordsNumber):
    word = fin.readline().rstrip('\n')
    currentStates = {initialState}

    for value in word:
        currentStates = go_to_next_state(states, currentStates, value)
        if currentStates == -1:
            break

    acceptedResult = currentStates.intersection(finalStates)

    if acceptedResult:
        print(acceptedResult)
    else:
        print("input is not accepted")

wordGeneratingStates = find_word_generating_states(reverseTransitionStates, finalStates, statesNumber)
generate_first_valid_inputs(initialState, states, finalStates, wordGeneratingStates)
