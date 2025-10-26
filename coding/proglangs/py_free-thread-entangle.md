# Does Free Threading Solve Parallel Entanglement?
    No, at least for the problem I tested here
    Worse, free threading is even slower than GIL builds

Python 3.14 was released with great fanfare, because **free threading** is supposed to speed up Python parallel execution, finally.

As I wrote in [Python Parallel Entanglement: A C++ Solution](ql_md_template.html?my.md=coding/proglangs/py_entangle.md), Python slows down when running in Parallel. Naturally, one wants to see whether free threading solves the problem of parallel slowdown or entanglement.

Let's use the same function:
```
def append_list(big_n=80000):
    test = []
    for j in range(big_n):
        test = test + [j]
    return len(test)
```
On the **same Windows 11 machine** (with 10 cores and 12 logical processors), I first run `append_list()` under `joblib.Parallel` with one task - one job (processor) to ten tasks - ten jobs (processor). With GIL build for both Python 3.13 and 3.14, the **mean running times** (in seconds) in the last Column, are quite close to the first table in [Python Parallel Entanglement: A C++ Solution](ql_md_template.html?my.md=coding/proglangs/py_entangle.md). 

For Python 3.13:

![Python 3.13](images/py3.13.png)

and Python 3.14:

![Python 3.14](images/py3.14.png)

Now it's time to try [free threading](#Note). I used `concurrent.futures.ThreadPoolExecutor`. Unbelievably, the free threading build with GIL disabled at runtime turns out to be slower. In nine cases, free threading takes around **twice as long to run**:

![Python 3.14t GIL=0](images/py3.14t-gil0.png)

Surprisingly, even the free threading build with GIL enabled at runtime can be faster (for 8 to 10 threads), but still lower than GIL build:

![Python 3.14t GIL=1](images/py3.14t-gil1.png)

**Note**:
<a name="Note"></a>
It took me some time to install and run free threading correctly. For your convenience, I summarize the main points below:
1. With **python-3.14.0-amd64.exe**, be sure to check **Download free-threaded binaries** to install the free threading build.
2. Check the installation first. For me, **py** points to 3.14t (i.e., free threading build), while **python** to 3.14 (i.e., GIL build).
3. To run 3.14t with GIL disabled at runtime:
> py -Xgil=0 myScript.py

To run 3.14t with GIL enabled at runtime:
> py -Xgil=1 myScript.py