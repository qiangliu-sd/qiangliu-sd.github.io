# What Can Be Wrong With Code Written By AI: Part 3?
    Claude identified most of the defects as presented in Part 1 of this series

Henry Liu tried the same prompt as shown in [Part 1](ql_md_template.html?my.md=coding/AI/what-wrong-w-ai-codes.md) with Opus 4.5, and obtained [match_universities.py](https://gist.github.com/liuhenry/34900d599550e93eabcd9fbc7a12d579), using the same two data files. The code has improved styles (i.e., using functions instead of scripts) and yields better matching results, but still has issues.

Interestingly, it creates a map to match *XYZ University* with *University of XYZ*, which arguably makes sense, and is what AI excels at. Notably, it is very verbose, tripling the lines of code.

Henry then asked Claude AI to read both [match_and_sum_universities.py](texts/match_and_sum_universities.py) and *match_universities.py* and analyze them separately.

Amazingly, Claude hits on many points that were discussed in Part 1 of this series. Read the thread [shared by Henry](https://claude.ai/share/7973cea6-34d5-4374-b380-225dcd781344) to appreciate the capability of Claude.