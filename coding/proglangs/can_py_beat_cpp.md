# Can Python Outperform C++?

[Speeding up Python and NumPy: C++ing the Way](https://medium.com/coding-with-clarity/speeding-up-python-and-numpy-c-ing-the-way-3b9658ed78f4) concludes that Python outperforms C++ for bigger arrays. This claim is hard to believe, however. If NumPy is optimized C++, NumPy and C++ would be more or less the same in speed, logically speaking. Therefore, something is probably incorrect in the implementation of the article.

Let’s see the C++ code, which is copied directly from the article:

```
static double standardDeviation(std::vector<double> v)
{
   double sum = std::accumulate(v.begin(), v.end(), 0.0);
   double mean = sum / v.size();

   double squareSum = std::inner_product(v.begin(), v.end(), v.begin(), 0.0);
   return sqrt(squareSum / v.size() - mean * mean);
}
```

What is wrong with the above function? There are at least two issues. First (and the main issue), **the function argument is passed by VALUE**. It leads to copying the vector when the function is called, which is expensive while utterly unnecessary. Second, using two STD algorithms to compute the sum and the sum of squares can be **inefficient because two separate loops are needed**. Minor issues are calling *size*() twice and using two divisions. Finally, it is unclear why the function is defined as static.

To fix those problems, I rewrote the code as follows:

```
double cppStdDeviation(const std::vector<double> & v)
{
   auto one_over_N = 1.0 / v.size();
   double sum = 0.0, squareSum =0.0;
   for (auto & x : v) {
	sum += x;
	squareSum += x * x;
   }
   double mean = sum * one_over_N;

   return sqrt(squareSum * one_over_N - mean * mean);
}
```
The vector argument is now passed in as a **const reference**, because the function does not modify it.

The C++ function is compiled with the **Py -m build** command on Windows 11 (Python v3.12, 64-bit) with the Python function name *cpp_stdev*. The results for small arrays are close to those of the article and are shown below.

![Executing times for small arrays](images/small_array.png)

The speed for bigger arrays is a very different story, however. The Python code from the article calls *numpy.array*() on the input *rand_array* (before passing it to *numpy.std*()), but does not time it inside *timeit.timeit*(). Not so sure why this call is needed. If I time *numpy.std(rand_array)* without calling *numpy.array*(), as compared to *cpp_stdev(rand_array)*, my C++ extension outperforms Python significantly (see below).

![Executing times for large arrays](images/big_array.png)

To conclude, **C++ significantly outperforms NumPy (and Python) for both small and big arrays**.



#### Warning:
Finally, I tried to wrap the call *numpy.std(rand_array)* inside *@jit(nopython=True)* as follows:

```
import numpy as np

from numba import jit

@jit(nopython=True)
def noPy_std(arr):
    return np.std(np.array(arr))
``` 
In the above, the call to *numpy.array*() is necessary; otherwise, Python will fail to run. The result turns out to be baffling unexpectedly. Instead of speeding up Numpy, **JIT increases the execution time by over an order of magnitude** (see below)!

![Executing times for large arrays under JIT](images/big_array-jit.png)

The lesson: We have to **be careful about the “speed-up features” of Python**.