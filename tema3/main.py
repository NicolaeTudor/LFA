regex = {}
eps_free_regex = {}
epsilonNT = []
startNT = 'S1'
dumpNT = 'D0'
finalNT = ['D0']
transitionNr = 0
finalStatesNr = 1
statesNr = 2
fin = open("input", "r")
fout = open("output", "w")

while True:
    expr = fin.readline().split()
    if not expr:
        break

    leftHand = expr[0]
    rightHand = expr[1]
    if rightHand == '*':
        epsilonNT += [leftHand]
    if leftHand in regex.keys():
        regex[leftHand].add(rightHand)
    else:
        regex[leftHand] = {rightHand}

for non_terminal, non_terminal_exprs in regex.items():
    statesNr += 1
    eps_free_exprs = set()
    for rightHand in non_terminal_exprs:
        if len(rightHand) == 2:
            if rightHand[1] in epsilonNT:
                eps_free_exprs.add(tuple((rightHand[0], dumpNT)))
                transitionNr +=1
            eps_free_exprs.add(tuple((rightHand[0], rightHand[1:])))
            transitionNr += 1
        elif rightHand != '*':
            eps_free_exprs.add(tuple((rightHand, dumpNT)))
            transitionNr += 1
    eps_free_regex[non_terminal] = eps_free_exprs

eps_free_exprs = set()
for rightHand in eps_free_regex['S']:
    eps_free_exprs.add(rightHand)
    transitionNr += 1
if '*' in regex['S']:
    finalStatesNr += 1
    finalNT += [startNT]
eps_free_regex[startNT] = eps_free_exprs

print(statesNr, file=fout)
print(transitionNr, file=fout)
for leftHand, non_terminal_exprs in eps_free_regex.items():
    for rightHand in non_terminal_exprs:
        print(leftHand + ' ' + rightHand[1] + ' ' + rightHand[0], file=fout)
print(finalStatesNr, file=fout)
print(finalNT, file=fout)
