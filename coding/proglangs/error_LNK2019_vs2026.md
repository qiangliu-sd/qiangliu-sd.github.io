# Error LNK2019 unresolved external symbol due to forward declaration
    C++20 in Visual Studio 2026

### The LNK2019 error
Inside the *FiniteDifference.cpp* file， the `FiniteDifference` class uses the `Slide1D` class. Inside *Slide1D.cpp*, `Slide1D` uses the `FiniteDiffInputs` struct, which is forward declared in the header *Slide1D.h* file as:
```
namespace topeqx {
using DblVec = vector<double>;

class FiniteDiffInputs;

class Slide1D {
    Slide1D(int time_step, const DblVec & deriv_in, const DblVec & state_in, 
		const FiniteDiffInputs & fd);
};
}
```
`FiniteDiffInputs` is defined in *InputStructs.h* and included in *Slide1D.cpp* as:
```
#include "paramfinder/InputStructs.h"
```
The .cpp files mentioned above, among others, were compiled successfully into a **static library** via Visual Studio 2026.

When the main program tried to link to the static library, the compile failed with the **LNK2019** error:
> error LNK2019: unresolved external symbol 
"public: __cdecl topeqx::Slide1D::Slide1D(int,class std::vector<double,class std::allocator<double> > const &,class std::vector<double,class std::allocator<double> > const &,struct topeqx::FiniteDiffInputs const &)" 
(??0Slide1D@topeqx@@QEAA@HAEBV?$vector@NV?$allocator@N@std@@@std@@0AEBUFiniteDiffInputs@1@@Z) 
referenced in function 
"public: virtual double __cdecl topeqx::FiniteDifference::price(class topeqx::DBDate,double)" (?price@FiniteDifference@topeqx@@UEAANVDBDate@2@N@Z)

### A solution

It is not obvious what causes the linking error. After a few attempts, I found that the error disappears if I replace the forward declaration in *Slide1D.h* with a direct inclusion of *InputStructs.h* as follows:
```
//class FiniteDiffInputs; 
#include "paramfinder/InputStructs.h"
```