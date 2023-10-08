# Pokédex

## Features
- Lookup by name OR pokédex number
- Print pokémon's info, including:
  - Name and number
  - Type(s)
  - Any pre- and post-evolutions
    - Will include evolution methods (level up, item, trade, etc)

- Option to compare looked-up pokémon with a type and indicate whether pokémon is:
  - Doubly weak (4x),
  - Weak (2x),
  - Resistant (.5x),
  - Immune (0x), or
  - Neither weak nor resitant (1x) to comparison type

## Pokédex file columns
- Number
- Name
- Type 1
- Type 2
- Evolution (level)
  - Blank = No evolution
    - Check will occur for pre-evolutions
  - -1 = First evolution of that line
  - 0 = Evolves via Method
  - Else = Evolution occurs normally at x level
- Pre-evolution
- Post-evolution
- Method
  - String = Evolution method is direct (e.g., Pokémon evolves via trade)
  - Int = Pokémon has various possible evolutions based on method
