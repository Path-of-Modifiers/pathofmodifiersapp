# How to deposit new data?

1. Ready file in csv-format
   - Add comments that are recorded in `history.log` by starting initial lines with `#`
2. Paste file into `.{date type}/{data type}_data`
3. Run `main.py`

## Modifier types

These follow a mostly flat hierarchy, but there are some important distinctions. While all modifiers on uniques are considered explicits in-game, they should not be labled as such in our database. This is because many of these modifiers only appear on uniques. Because we use these modifier types to sort what modifiers are relevant to the data, it is unnecessary to load all the modifiers which only appear on uniques when considering rare items.

This does not mean a modifier cannot have both modifier types, but the reason it has it should not be from adding new unique modifier data.

## Item Base types

Only base types that are relevant are stored
