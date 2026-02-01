# Python Parallel Entanglement: Final Note
    C++ is over one order of magnitude faster than Python
    Parallelism in C++ is almost twice as fast

As [Python Parallel Entanglement: A C++ Solution](ql_md_template.html?my.md=coding/proglangs/py_entangle.md) and [Does Free Threading Solve Parallel Entanglement?](ql_md_template.html?my.md=coding/proglangs/py_free-thread-entangle.md) show, Python slows down when running in Parallel and C++ can do much better. My final question is, can we do better within Python or C++ separately?

As I mentioned previously, `test += [j]` is much more efficient than `test = test + [j]`. Actually, `test.append(j)` is even better. With a list size of 8*10e6, `append()` finishes in about 3.7 seconds.

On the other hand, C++ can be improved by combining `reserve()` with `emplace_back()` under C++11. Further, one can do even better by moving parallel code into C++.

Let's look at the results below.

### Python and C++ functions
The Python method is now defined as:
```
def append_list(big_n=80000):
    test = []
    for j in range(big_n):
        test.append(j)
    return len(test)  
```
The new C++ function is as follows:
```
int cppAppendVector(int big_n=80000)
{
    std::vector<int> iv;	
    iv.reserve(big_n);
    for (int k =0; k < big_n; ++k) {
	iv.emplace_back(k);		// C++11
    }
	
    return iv.size();
}
```
which will be used in Python as `cppPy_appvec()`, after compiling.

### Python 3.14 free threading

Results for `ThreadPoolExecutor` are shown in the tables below.

First, `append_list()`:

![append_list()](images/append_list.png)

The execution length for ten threads is 5.4 times that of one thread. Even though the list `append()` method runs much faster, **multiple threading in Python still exhibits parallel entanglement**.

Second, `cppPy_appvec()`:

![cppPy_appvec()](images/cppPy_appvec.png)

**C++ is about 22 times faster than Python**, but parallel entanglement in Python is roughly the same (i.e., ten threads need 4.9 times that of one thread).

### Parallel in C++

In the cases discussed in this article, we can move the parallel run from Python to C++. For simplicity, I use **OpenMP** here:
```
int cppAppendVectorOMP(int num_jobs, int num_tasks, int big_n=80000)
{		
    std::vector<int> _sizes(num_tasks, 0);
	
#pragma omp parallel num_threads(num_jobs)
    {		
#pragma omp for
	for (int p = 0; p < num_tasks; ++p) {
	    _sizes[p] += cppAppendVector(big_n);
	}
    }
    int _sizes_sum = 0;
    for (auto & sz: _sizes) _sizes_sum += sz;
    return _sizes_sum;
}
```
which will be called in Python as `cppPy_appvecOMP()`, after compiling.

![cppPy_appvecOMP()](images/cppPy_appvecOMP.png)

The execution length for ten threads is only 3.1 times that of one thread. Therefore, **parallel entanglement in Python can be reduced by parallelism in C++**.