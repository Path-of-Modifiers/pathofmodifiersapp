# How to deposit new data?
1. Ready file in csv-format
   - Add comments that are recorded in `history.log` by starting initial lines with `#`
2. Paste file into `./new_data`
3. Run `deposit_new_data.py`

## Limitations
If the file contains duplicate information, either duplicated infile or already present in the database. Information is considered duplicate when a previous entry contains the same combination of `position` and `effect`.