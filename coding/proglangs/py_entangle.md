# Python Parallel Entanglement: A C++ Solution

With multiple cores running concurrent independent Python tasks (or threads), the executing time roughly increases with the number of tasks executed sequentially, as reported in [Performance May Not Scale with CPU Cores in Python](https://superfastpython.com/performance-may-not-scale-with-cpu-cores-python/) for **a large list**. The independent Python tasks running in different threads (or processors) seem to interact with one another and slow down simultaneously. Let’s call this phenomenon **Python parallel entanglement** (with allusion to “quantum entanglement”).

To replicate the problem, I take the Python code from the article with minor modifications:

```
def append_list(big_n=80000):
    test = []
    for j in range(big_n):
        test = test + [j]
    return len(test)
```
On a Windows 11 with ten cores and twelve logical processors, I run `append_list()` under `joblib.Parallel` with one task - one job (thread) to ten tasks - ten jobs (threads) on average. The [running times](#Note1) (in seconds) in Column 5, which confirm those of the article, are shown in the following table. The run-time of ten tasks - ten jobs is eleven times that of one task - one job, which means that Python parallel fails completely. For five or fewer jobs, though, parallel runs require less execution time. The total size of lists used in tasks or jobs is reported in Column 2 to ensure that the lists are appended correctly.

![Table 1: Python one task per job](images/tab1Py-entangle.png)

Unbelievably, the parallel entanglement exists across different processors or independent Python instances (Column 6). How did I do that? *I launched Python processes (i.e., python.exe) asynchronously using Start-Process (and timing the execution time of all the Python instances via Wait-Process) in a PowerShell script*. What I did was roughly OS parallelism. Surprisingly, the independent Python instances also interact with one another or seem to be entangled.

Knowing that C++ extensions are much faster than Python (see [Can Python Outperform C++?](ql_md_template.html?my.md=coding/proglangs/can_py_beat_cpp.md)), I decided to give C++ a try. Translating `append_list()` into C++, I append elements to a vector and then copy the resultant vector explicitly ([to simulate the list assignment or copying in Python](#Note2)) as follows:

```
int cppAppendVector(int big_n=80000)
{
   std::vector<int> iv , iv_copy;	
   for (int k =0; k < big_n; ++k) {
	iv.push_back(k);
	iv_copy = iv;
   }
	
   return iv.size();
}
```
Similarly, I run `cppPy_appvec()`, the Python version of `cppAppendVector()` (compiled with the **Py -m build** command on Windows 11 with 64-bit Python v3.12), under `joblib.Parallel`. The following three tables summarize the running times (in seconds) for one task per job, 10 tasks per job, and 100 tasks per job on average.

![Table 2: C++ one task per job](images/tab2Py-entangle.png)

![Table 3: C++ 10 tasks per job](images/tab3Py-entangle.png)

![Table 4: C++ 100 tasks per job](images/tab4Py-entangle.png)

We can make two observations. First, **the C++ extension is much faster**. For one task - one job (ten tasks - ten jobs), the C++ extension is 51 (150) times faster than Python. Therefore, C++ alone significantly reduces the need for parallel executions in Python. Second, **the C++ extension entangles less**. For one task (10 tasks, 100 tasks) per job, the run-time of 10 tasks (100 tasks, 1000 tasks) - ten jobs is 3.3 (4.4, 4.9) times that of one task (10 tasks, 100 tasks) - one job. Therefore, Python paralleling with the C++ extension can save execution times by roughly half.

To conclude, **C++ extensions can be an excellent solution to the problem of Python parallel entanglement**.

 

**Note**:

<a name="Note1"></a>
Repeated executions of Python may show wildly different running times. The times reported in this article are from single runs.

<a name="Note2"></a>
`test = test + [j]` in the original Python function `append_list()` is inefficient, while `test += [j]` can run five times fast.