# How to Debug C++ Compiling Errors Pointing to Standard Library Headers in Visual Studio?
    Visual Studio 2026 & 2022
    Follow your header files to missing braces

While updating my options pricing platform, I encountered **compilation errors pointing to the std Library** in Visual Studio 2022 and 2026. After spending a day in frustration and desperation trying to decipher the error messages, I finally caught the bug. I report the process here for your convenience.

Let's follow the trail.

Compiling a static library for my binomial tree method, I got the following errors:

![binomial lib](images/bt-lib.png)

With **429** errors that mostly point to the std library, such as `functional` and `list`, those error messages were not helpful at all.

The IDE showed that the virtual base class `PricingMethod` was underlined:

![pricing method](images/pricingmethod.png)

I checked `PricingMethod` carefully and found it was defined and properly included. In its constructor, the class name `DerivativeFactory` was underlined, however:

![deriv-factory](images/deriv-factory.png)

Now opening up `DerivativeFactory`, I saw the class `Convertible` was underlined:

![conv-bond](images/convbond.png)

Checking `Convertible`, nothing seemed to be wrong. So it was a dead end.

What else can be wrong? Well, `DerivativeFactory` includes only three header files:
```
#include "options/OptionFactory.h"
#include "cvtbond/Convertible.h"
#include "cbparams/CBParameters.h"
```
After commenting out `Convertible.h` and `CBParameters.h`, I was looking at `OptionFactory.h`:

![opt-factory](images/opt-factory.png)

A first glance did not show any problem with `OptionFactory.h`. Going line by line, I noticed that the **braces** (or **curly brackets**) did not match up because one right brace was missing. After adding the missing brace, I was able to compile without problems.

A final note. Later on, I did notice a small **red tilde ~** below the `#endif` in `OptionFactory.h`. Moving my cursor over **the tilde**, I saw 'E0065: expected a ";"', which was a wrong message, unfortunately.