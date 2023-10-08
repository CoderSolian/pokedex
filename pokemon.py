import pandas as pd
import math

def pokemon():
    pokedex = pd.read_excel('Pokedex.xlsx')
    entry = input("Enter a Pokédex # between 1-151 or a Pokémon name: ")
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
    evolves = pokedex.at[index, 'Evolution']
    preEvo = pokedex.at[index, 'Pre-evolution']
    postEvo = pokedex.at[index, 'Post-evolution']
    method = pokedex.at[index, 'Method(s)']
    
    if isinstance(type2, str):
        print(f"a dual {type1} and {type2} type.")
    else:
        if type1[0] in ['E', 'I']:
            print(f"an {type1} type.")
        else:
            print(f"a {type1} type.")
    print()

    if not isinstance(evolves, int) and not isinstance(preEvo, str):
        print(f"{name} does not evolves.")

    elif isinstance(evolves, int):
        if evolves > 0:
            print(f"{name} evolves into {postEvo} at level {evolves}.")
        else:
            if isinstance(method, str):
                print(f"{name} can evolve into {postEvo} via {method}.")
            else:
                branches = pd.read_excel('Pokedex.xlsx', sheet_name='Branch Evos')
                evIndex = branches[branches['Name'] == name].index.tolist()[0]
                indexEnd = evIndex + method
                level = branches.at[evIndex, 'Level']
                if not math.isnan(level):
                    print(f"At level {level:.0f}, {name} evolves into ", end="")  
                else:
                    print(f"{name} can evolve into ", end="")
                possible_branches = []
                for i in range(evIndex, indexEnd):
                    trigger = branches.at[i, 'Methods']
                    branch = branches.at[i, 'Evolution']
                    possible_branches.append(f"{branch} via {trigger}")
                if method > 2:
                    branchList = ", ".join(possible_branches[:-1]) + f", or {possible_branches[-1]}."
                else:
                    branchList = " or ".join(possible_branches) + "."
                print(branchList)
    
    elif isinstance(preEvo, str):
        preIndex = int(pokedex[pokedex['Name'] == preEvo].iloc[0]['Number']) - 1
        prePre = pokedex.at[preIndex, 'Name']
        print(f"{preEvo} and {prePre}")

    if isinstance(evolves, int):
        print(evolves)
    if isinstance(preEvo, str):
        print(preEvo)
    if isinstance(postEvo, str):
        print(postEvo)
    if isinstance(method, int) or isinstance(method, str):
        print(method)


    """nextForm = ""
    if not math.isnan(evolves):
        nextForm = pokedex.at[index + 1, 'Name']
        if evolves > 0:
            print(f"{name} evolves at level {evolves} into {nextForm}.")
            if nextForm == pokedex.at[index + 2, 'Pre-evolution']:
                secEv = pokedex.at[index + 2, 'Name']
                if pokedex.at[index + 1, 'Evolution'] > 0:
                    print(f"{nextForm} then evolves at level {pokedex.at[index + 1, 'Evolution']} into {secEv}.")
                else:
                    print(f"{nextForm} can then evolve via a {pokedex.at[index + 1, 'Method(s)']} into {secEv}.")
        else:
            method = pokedex.at[index, 'Method(s)']
            if isinstance(method, int):
                print(f"{name} can evolve in {method} ways: ", end="")
                for i in range(method):
                    print(f"{pokedex.at[index + i + 1, 'Name']} with a {pokedex.at[index + i + 1, 'Method(s)']}", end="")
                    if method > 2:
                        if i < method - 2:
                            print(f", ", end="")
                        elif i < method - 1:
                            print(f", or ", end="")
                    else:
                        if i < method - 1:
                            print(f" or ", end="")
                print(".")
            else:
                print(f"{name} can evolve with a {method} into {nextForm}.")
    else:
        preEvo = pokedex.at[index, 'Pre-evolution']
        if preEvo != pokedex.at[index - 1, 'Name']:
            print(f"{name} does not evolve.")
        else:
            print(f"{name} is the evolved form of {preEvo}.")
            if pokedex.at[index - 2, 'Name'] == pokedex.at[index - 1, 'Pre-evolution']:
                print(f"It is the final evolution of {pokedex.at[index - 2, 'Name']}.")
        
        preType1 = pokedex.at[index - 1, 'Type 1']
        preType2 = pokedex.at[index - 1, 'Type 2']

        if type1 != preType1:
            print(f"{name} becomes a {type1} type upon evolution.")

        if type2.isalpha() and ~preType2.isalpha():
            print(f"{name} gains its {type2} typing upon evolution.")

        firstStage = pokedex.at[index - 1, 'Pre-evolution']
        if firstStage.isalpha():
            print(f"It is the final evolution of {firstStage}.")

    if pokedex.at[index, 'Methods'] != " ":
        options = int(pokedex.at[index, 'Methods']) + 1
        print(f"{name} can evolve in {options - 1} ways:", end=" ")

        for i in range(1, options):
            print(f"{pokedex.at[index + i, 'Name']} via a {pokedex.at[index + i, 'Evolution']}", end="")
            if i < options - 2:
                print(f", ", end="")
            elif i < options - 1:
                print(f", or ", end="")
        print(".")

    elif name == pokedex.at[index + 1, 'Pre-evolution']:
        index += 1
        evoMethod = pokedex.at[index, 'Evolution']
        secEvo = pokedex.at[index, 'Name']
        if isinstance(evoMethod, str):
            print(f"It can evolve into {secEvo} via a {evoMethod}.")
        else:
            print(f"It evolves into {secEvo} at level {evoMethod}.")
        
        if pokedex.at[index + 1, 'Pre-evolution'] == secEvo:
            index += 1
            thirdEvo = pokedex.at[index, 'Name']
            evoMethod = pokedex.at[index, 'Evolution']
            if isinstance(evoMethod, str):
                print(f"{secEvo} can then evolve into {thirdEvo} via a {evoMethod}.")
            else:
                print(f"{secEvo} then evolves into {thirdEvo} at level {evoMethod}.")"""
    print()

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