import pandas as pd
import math

pokedex = pd.read_excel('Pokedex.xlsx')
paths = pd.read_excel('Pokedex.xlsx', sheet_name='Branch Evos')

def nextEvolve(name, index, level, method):
    nextStage = pokedex.at[index, 'Post-evolution']
    branched = False

    if not isinstance(method, str):
        branched = True
    
    if level > 0:
        print(f"{name} evolves into {nextStage} at level {level}.")
    else:
        if not branched:
            print(f"{name} can evolve into {nextStage} via {method}.")
        else:
            start = paths[paths['Name'] == name].index.tolist()[0]
            print(paths.at[start, 'Method'])
            end = start + method
            fork = paths.at[start, 'Level']
            if not math.isnan(fork):
                print(f"At level {fork:.0f}, {name} evolves into ", end="")
            else:
                print(f"{name} can evolve into ", end="")
            options = []
            for i in range(start, end):
                branch = paths.at[i, 'Evolution']
                if isinstance(paths.at[i, 'Method'], str):
                    trigger = f" via {paths.at[i, 'Method']}"
                else:
                    trigger = f" at level {paths.at[i, 'Method']}"
                options.append(branch + trigger)
            if method > 2:
                branchList = ", ".join(options[:-1]) + f", or {options[-1]}."
            else:
                branchList = " or ".join(options) + "."
            print(branchList)

def pastEvolve(name, prevStage, level, method):
    print(f"evolves from {prevStage} ", end="")
    if level > 0:
        print(f"at level {level}.")
    else:
        if not isinstance(method, str):
            index = paths[paths['Evolution'] == name].index.tolist()[0]
            method = paths.at[index, 'Method']
        print(f"via {method}.")
            
def pokemon():
    entry = input("Enter a Pokédex # or a Pokémon name: ")
    found = False
    name = ""
    number = 0
    print()

    for rowIndex, row in pokedex.iterrows():
        if entry.isalpha():
            if row['Name'] == entry:
                found = True
                index = rowIndex
                number = int(pokedex.at[index, 'Number'])
                name = entry
                print(f"{name} is Pokémon #{number},", end=" ")
        else:
            if row['Number'] == int(entry):
                found = True
                index = rowIndex
                number = entry
                name = pokedex.at[index, 'Name']
                print(f"Pokémon #{number} is {name},", end=" ")
    if not found:
        return input("Pokémon not found. Do you want to try again? Enter Yes or No: ")

    type1 = pokedex.at[index, 'Type 1']
    type2 = pokedex.at[index, 'Type 2']
    
    if isinstance(type2, str):
        print(f"a dual {type1} and {type2} type.")
    else:
        if type1[0] in ['E', 'I']:
            print(f"an {type1} type.")
        else:
            print(f"a {type1} type.")
    print()

    oneStage = False
    twoStages = False
    threeStages = False
    preEvo = False
    postEvo = False
    first = False
    second = False
    third = False

    level = pokedex.at[index, 'Evolution']
    method = pokedex.at[index, 'Means']
    
    if isinstance(level, int):
        postEvo = True

    if isinstance(pokedex.at[index, 'Pre-evolution'], str):
        preEvo = True
        prevStage = pokedex.at[index, 'Pre-evolution']
        prevIndex = int(pokedex[pokedex['Name'] == prevStage].iloc[0]['Number']) - 1
        prevLevel = pokedex.at[prevIndex, 'Evolution']
        prevMethod = pokedex.at[prevIndex, 'Means']
        if isinstance(pokedex.at[prevIndex, 'Pre-evolution'], str):
            threeStages = True
            third = True
            firstStage = pokedex.at[prevIndex, 'Pre-evolution']

    if isinstance(pokedex.at[index, 'Post-evolution'], str):
        postEvo = True
        nextStage = pokedex.at[index, 'Post-evolution']
        nextIndex = int(pokedex[pokedex['Name'] == nextStage].iloc[0]['Number']) - 1
        nextLevel = pokedex.at[nextIndex, 'Evolution']
        nextMethod = pokedex.at[nextIndex, 'Means']
        if isinstance(pokedex.at[nextIndex, 'Post-evolution'], str):
            threeStages = True
            first = True
            finalStage = pokedex.at[nextIndex, 'Post-evolution']

    if preEvo and postEvo:
        threeStages = True
        second = True
    elif (preEvo and not postEvo) and not threeStages:
        twoStages = True
        second = True
    elif (not preEvo and postEvo) and not threeStages:
        twoStages = True
        first = True
    elif not twoStages and not threeStages:
        oneStage = True

    if (first or (second and not twoStages)) or (second and threeStages):
        nextEvolve(name, index, level, method)
        if first and threeStages:
            print(f"{nextStage} then evolves into {finalStage} ", end="")
            if nextLevel > 0:
                print(f"at level {nextLevel}.")
            else:
                print(f"via {nextMethod}.")
        if second or third:
            print("It ", end="")
            pastEvolve(name, prevStage, prevLevel, prevMethod)
    if third and threeStages:
        print(f"{name} ", end="")
        pastEvolve(name, prevStage, prevLevel, prevMethod)
        print(f"It is the fully evolved form of {firstStage}.")
    elif second and twoStages:
        print(f"It is the fully evolved form of {prevStage} ", end="")
        if prevLevel > 0:
            print(f"(level {prevLevel}).")
        else:
            print(f"({method}).")

    if oneStage: print(f"{name} does not evolve.")

    #######

    """typeSearch = False
    user = input(f"Do you want to do a type match up for {name}? Yes or No: ")
    if user == 'Yes':
        typeSearch = True
    
    if typeSearch:
        typeChart = pd.read_excel('Gen1Typing.xlsx')
        attack = input(f"\nSelect a type for {name} to defend against: ")
        print()

        for rowIndex, row, in typeChart.iterrows():
            if row['Attacking'] == attack:
                index = rowIndex

        totalMatch = 1
        matchOne = typeChart.at[index, type1]
        matchTwo = 1
        if math.isnan(matchOne):
            matchOne = 1

        if isinstance(type2, str):
            matchTwo = typeChart.at[index, type2]
            if math.isnan(matchTwo):
                matchTwo = 1
        
        totalMatch = totalMatch * matchOne * matchTwo

        if totalMatch == 4:
            print(f"{name} is doubly weak against {attack}-type moves.")
        elif totalMatch == 2:
            print(f"{name} is weak against {attack}-type moves.")
        elif totalMatch < 1 and totalMatch > 0:
            print(f"{name} is resistant to {attack}-type moves.")
        elif totalMatch == 0:
            print(f"{name} is immune to {attack}-type moves.")
        else:
            print(f"{name} is neither weak against nor resistant to {attack}-type moves.")
    print()"""
    
    return #input("Do you want to look up another Pokémon? Enter Yes or No: ")

def main():
    while 1:
        print()
        lookup = pokemon()
        if lookup == 'No':
            print("\nThank you for using my Pokédex.")
            break

#main()
pokemon()