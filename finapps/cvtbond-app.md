# A C++ convertible bond pricing App
	A brief introduction
	
### CB business logic
	A convertible bond is a corporate debt that can be converted by the CB holder to the public traded stock of the CB issuer.

CB clauses or embedded choices (options) in the order of seniority:
1. Put (or hard-put). CB holder can return the CB to the issuer for cash.
2. Provisional Put (or soft-put). Conditional put.
3. Convert. CB holder can convert the CB to stock.
4. Call (or hard-call). CB issuer can call back the CB, and then forces CB holder to convert.
5. Provisional Call (or soft-call). Conditional call.

Notes:
1. No matter what happens, coupon will always be paid at accured amount.
2. When called, it is assumed the CB holder will always choose to convert.
3. Soft-put: Uncommon in the US, but common in China.

### CB Pricing
A CB can be priced by solving the Black-Scholes-Merton or [Ayache-Forsyth-Vetzal](#afv) PDE via finite difference method.

Provisional Call (Put), embedded options that conditional on the past close prices of the underlying stock, are difficult to handle. For example, a 20 out of 30 provisional call will be satified if in the past 30 trading days, the stock closed above a specific trigger price in 20 or more days. Approximations, such as [conditianl range probability (CRP)](#crp) or [auxiliary reversed binomial-tree (ARB)](#arb), can be utilized.

The App with GUI can [be downloded from GitHub](https://github.com/qiangliu-sd/cvt-bond-pricer).

### References:
<a name="afv"></a>AFV:\
Ayache, Forsyth, Vetzal (2003). The valuation of convertible bonds with credit risk. Journal of Derivatives.

<a name="crp"></a>CRP:\
Liu, Guo (2020). [An excellent approximation for the m out of n day provision. North American Journal of Economics and Finance](https://www.sciencedirect.com/science/article/pii/S1062940820301194).

<a name="arb"></a>ARB:\
Liu, Guo (2008). Approximating the embedded m out of n day soft-call option of a convertible bond: An auxiliary reversed binomial tree method. SSRN.


