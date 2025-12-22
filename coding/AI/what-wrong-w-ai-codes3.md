# What Can Be Wrong With Code Written By AI: Part 3?
    Opus 4.5 has many issues, too
    Claude identified most of the defects as presented in Part 1 of this series

[Henry Liu](https://liuhenry.com/) tried the same prompt as shown in [Part 1](ql_md_template.html?my.md=coding/AI/what-wrong-w-ai-codes.md) with Opus 4.5, and obtained [match_universities.py](https://gist.github.com/liuhenry/34900d599550e93eabcd9fbc7a12d579), using the same two data files. The code has improved styles (i.e., using functions instead of scripts) and yields better matching results, but still has issues.

### Bad styles
1. Badly named variables or functions, such as `MANUAL_MAPPINGS`, `replacements`, and `normalize_name()`.
2. Hard to read statements, such as `normalized_name = normalize_name(name)`.
3. Hardcoded numbers, such as **1.0, 0.9, 0.15, and 0.5** in `find_best_match_with_score()` and **80** in `main()` .
4. Very long functions. `main()` numbers **96** lines, and `find_best_match_with_score()` does 55.
5. The function `main()` does many things that are not defined as functions.
6. Bad that a `main()` function is only called inside `if __name__ == '__main__':`. The **scripts** for steps to get the job done shall be placed inside `if __name__ == '__main__':`, instead of inside a `main()` that takes no argument.

### Bad implementation
1. *match_universities.py* is very verbose (339 lines of code), tripling the lines of code of *match_and_sum_universities.py* (115 lines of code).
2. Defining a `dict` inside `normalize_name()`, which is hard to maintain.
3. Defining a file-level dict, MANUAL_MAPPINGS, to map *XYZ University* to *University of XYZ*. This makes sense and is what AI excels at. Unfortunately, such mapping is better placed in a data file. Furthermore, entries such as `"University of Texas, Austin": "University of Texas"` may lead to miscounts. Worse, entries like `"University of California, Irvine": "University of California, Irvine"` are erronous.
4. Defining two functions to read in two data files, but returning two different data objects. The repetition may be unnecessary.
5. Reinvent the wheel and hard to follow: `find_best_match()` and `find_best_match_with_score()`.

### Inefficient codes
1. Double loops as in *match_and_sum_universities.py*.
2. Calling `normalize_name()` multiple times for every university name in both datasets.

### Other issues
1. Defining a function `normalize_name()` to map non-English characters to English is unnecessary, and inefficient.
2. Defining a function `extract_core_name()` with eleven `replace()`s is bad and unnecessary.
3. Not used: `find_best_match()`.

### Code review by Claude
Henry then asked Claude AI to read both [match_and_sum_universities.py](texts/match_and_sum_universities.py) and *match_universities.py* and analyze them separately.

Amazingly, Claude hits on many points that were discussed in Part 1 of this series. Read the thread [shared by Henry](https://claude.ai/share/7973cea6-34d5-4374-b380-225dcd781344) to appreciate the capability of Claude.