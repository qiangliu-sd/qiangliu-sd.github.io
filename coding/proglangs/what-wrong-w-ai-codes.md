# What's Wrong with Code Written by AI?
    Bad styles, bad implementation, inefficient double loops, and other issues

With the following prompt to [Gemini CLI](#Notes):
> match similar universities from [doc-univ_counts.txt and num-univ-country-2025.txt](#Notes), order the results by the sum of numbers, and write the ordered results to a file

Gemini created *match_and_sum_universities.py*, executed it and produced *matched_universities.txt*. The good news is that Gemini did it quickly, and the result seems to be OK.

The *bad* news is that the code in [match_and_sum_universities.py](texts/match_and_sum_universities.py) is bad with many potential problems -- Well, I am fully aware that *my prompt is poorly written*. Simply put, the AI code is **not ready for reuse** and will be **challenging to maintain** in the future.

### Bad styles
1. Hardcoded file names and constants. Such as `similarity_threshold = 85` (Line 80). The **magic 85** turns out to be [problematic](#Notes) as well.
2. Naming variables with numbers. Such as `file1, match1, univs1, matched_from_file2`.
3. Using `score` to name different concepts (Lines 97 & 98).
4. Multiple indentations. For example, five indentations inside `parse_file()`.
5. Variable and function names are similar. Such as `similarity_threshold` vs. `parse_file()`.
6. Mixing scripts and functions in the same file. It begins with a `try-except` block, defines two functions, and then lists the main script with numbers.

### Bad implementation
Function `parse_file(filepath)` is poorly implemented in Lines from 29 to 41 as follows:
```
    # Try to match 'Name: score' format
    match1 = re.match(r'^(.*?):\s*([\d\.]+)$', line)
    # Try to match 'score Name' format
    match2 = re.match(r'^([\d\.]+)\s+(.*)', line)

    if match1:
        score = float(match1.group(2))
        name = match1.group(1).strip()
        universities.append({'score': score, 'name': name})
    elif match2:
        score = float(match2.group(1))
        name = match2.group(2).strip()
        universities.append({'score': score, 'name': name})

```
Even if there are two data files, the function shall be defined to do one thing only. It is **terrible to hardcode two regular patterns** inside the function body. Further, it is bad and  inefficient to call `re.match` twice. For better design, the regular pattern for data lines shall be passed in as an argument.

Using a list of dictionaries is unnecessary and can be expensive; instead, a tuple will work here. 

A minor issue is that the two `.append`'s are redundant.

A better version, with better variable names, is as follows:
```
    twoPatMatch = re.match(str_patterns, line)

    if not twoPatMatch: continue
    if twoPatMatch.group(2).isnumeric():
        nameScoreList += [(twoPatMatch.group(1).strip(),float(twoPatMatch.group(2)))] 
    else:
	nameScoreList += [(twoPatMatch.group(2).strip(),float(twoPatMatch.group(1)))] 

```
Note that `str_patterns` is passed in as an argument.

The best is to use a dictionary directly, because the lines in the two data files are supposedly unique:
```
    twoPatMatch = re.match(str_patterns, line)

    if not twoPatMatch: continue
    if twoPatMatch.group(2).isnumeric():
	nameScoreDict[twoPatMatch.group(1).strip()] = float(twoPatMatch.group(2)) 
    else:
	nameScoreDict[twoPatMatch.group(2).strip()] = float(twoPatMatch.group(1)) 

```
Note that the function `normalize_name()` (Line 51) is not used. Why it is there is not clear.

### Inefficient double loops
The matching code basically loops over one dataset (`univs1`) again the other (`choices = [u['name'] for u in univs2]`) in Lines from 84 to 90, as follows:
```
for univ1 in univs1:
    best_match_name, score = process.extractOne(univ1['name'], choices, scorer=fuzz.WRatio)
    
    if score >= similarity_threshold:
        univ2 = next((u for u in univs2 if u['name'] == best_match_name), None)

        if univ2 and univ2['name'] not in matched_from_file2:
```
We can remove a matched name from `choices`, so that we do not need to match against it again. For a large dataset, this could reduce the running time by half on average. For the dataset with about 160 entries (lines) at hand, **the execution time is reduced by 25%**, resulting in a saving of one-quarter.

Note that `matched_from_file2` is searched inside the loop. Since `univs2` has longer names and the two datasets have roughly the same number of entries, `univs2` shall be placed in the outer loop instead.

Finally, the `univ2 = next(...)` statement (Line 88) will be unnecessary, if `parse_file()` returns a `dict`.

### Other issues
1. The three `import`'s are bad. Better with `from module import function`.
2. Utility functions should be put into a separate module (file).
3. Hardcoded variable should be isolated and placed inside `if __name__ == '__main__':`.
4. Package shall be installed manually, so the initial `try-except` block shall be deleted.


### Notes:
<a name="Notes"></a>
The project was initially done on Nov. 26, 2025. The Gemini CLI used probably the Gemini-2.5 model.

*doc-univ_counts.txt* contains lines such as:
- Columbia University: 24
- University of California, Berkeley: 23

*num-univ-country-2025.txt* contains lines such as:
- 19	California Institute of Technology, Pasadena, CA, USA
- 17	University of California, Berkeley, CA, USA

*matched_universities.txt* contains the following **six mis-matches** with `similarity_threshold = 85`:
- Total Score: 11.00 | File 1: University of Illinois at Urbana-Champaign (6.00) | File 2: University of Texas Southwestern Medical Center at Dallas, Dallas, TX, USA (5.00) (Similarity: 86%)
- Total Score: 9.00 | File 1: Imperial College London (2.00) | File 2: London University, London, United Kingdom (7.00) (Similarity: 86%)
- Total Score: 5.00 | File 1: Université de Montréal (1.00) | File 2: Collège de France, Paris, France (4.00) (Similarity: 86%)
- Total Score: 4.00 | File 1: Technische Universität Berlin (3.00) | File 2: Biozentrum der Universität, Basel, Switzerland (1.00) (Similarity: 86%)
- Total Score: 3.00 | File 1: Technische Universität Darmstadt (2.00) | File 2: Technische Hochschule (Institute of Technology), Munich, Germany (1.00) (Similarity: 86%)
- Total Score: 2.00 | File 1: Technische Hochschule München (1.00) | File 2: Landwirtschaftliche Hochschule (Agricultural College), Berlin, Germany (1.00) (Similarity: 86%)

Furthermore, my more efficient code yielded significantly different results. After setting the threshold to **88**, I obtained identical results with the two scripts.