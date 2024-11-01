# How to deposit new data?

1. Ready file in csv-format
    - Add comments that are recorded by relevant logger by starting initial lines with `#`
    - Add the comments needed for data processing (See [Modifier Types](#modifier-types))
2. Paste file into `./{date type}/{data type}_data`
3. Run `main.py`

## Modifier types

These follow a mostly flat hierarchy, but there are some important distinctions. While all modifiers on uniques are considered explicits in-game, they should not be labled as such in our database. This is because many of these modifiers only appear on uniques. Because we use these modifier types to sort what modifiers are relevant to the data, it is unnecessary to load all the modifiers which only appear on uniques when considering rare items.This does not mean a modifier cannot have both modifier types, but the reason it has it should not be from adding new unique modifier data.

The related uniques are tracked by comments in the modifier file, identified by `# Unique Name: ...`.

Additional information is also needed, in order to make realistic test data. These fields are explained below

| Field                        | Type                            | How to parse                                                                                                                | Notes                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Base Types                   | list\[str\]                     | Made into a list by splitting by `\|`                                                                                       |                                                                                                                                                                                                                                                                                                                                                        |
| Total modifiers              | list\[int\]                     | Made into a list by splitting by `\|`                                                                                       |                                                                                                                                                                                                                                                                                                                                                        |
| Can have duplicate modifiers | list\[bool\]                    | Made into a list by splitting by `\|`                                                                                       | Must have same length as number of keys in `Modifier distrubution`. If `True`, the same modifier can be chosen multiple times from the pool specified by `Modifier distrubution`                                                                                                                                                                       |
| Modifier distrubution        | dict\[int \| str, list\[int\]\] | Each key-value-pair is seperated by `,`, and the pair is then split by `:`. Values are made into lists by splitting by `\|` | The value tells you how many modifiers to choose from the pool specified by the key. If the length of the value list is greater than 1, a random elemnt must be chosen. The pool of modifiers to choose from is specified by the interval `\[prev_key, key)` where `prev_key=0` if no key has previously been used and `key="rest"` == `key=len(dict)` |

## Item Base types

Only base types that are relevant are stored

The related uniques are tracked by comments in the item base types file, identified by `# Unique Name: ...`.
