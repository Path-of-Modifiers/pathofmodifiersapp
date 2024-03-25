# How to deposit new data?
1. Ready file in csv-format
   - Add comments that are recorded in `history.log` by starting initial lines with `#`
2. Paste file into `./new_data`
3. Run `deposit_new_data.py`

## Without a permanent database
While still testing and developing, files need to be moved from `.\deposited_data` into `.\new_data` again.

## Modifier types
These follow a mostly flat hierarchy, but there are some important distinctions. While all modifiers on uniques are considered explicits in-game, they should not be labled as such in our database. This is because many of these modifiers only appear on uniques. Because we use these modifier types to sort what modifiers are relevant to the data, it is unnecessary to load all the modifiers which only appear on uniques when considering rare items.

This does not mean a modifier cannot have both modifier types, but the reason it has it should not be from adding new unique modifier data.