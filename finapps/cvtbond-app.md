# A C++ convertible bond pricing App
	A brief introduction
	
### CB business logic
A convertible bond is a corporate debt that can be converted by the CB holder to the public traded stock of the CB issuer.

CB clauses or choices (i.e., embedded options) in the order of seniority:
1. Put (or hard-put). CB holder can return the CB to the issuer for cash.
2. Provisional Put (or soft-put). CB holder's conditional put.
3. Convert. CB holder can convert the CB to stock.
4. Call (or hard-call). CB issuer can call back the CB, and then forces CB holder to convert.
5. Provisional Call (or soft-call). CB issuer's conditional call.

Notes:
1. No matter what happens, coupon will always be paid at accured amount.
2. When called, it is assumed the CB holder will always choose to convert.
3. Soft-put: Uncommon in the US, but common in China.

### CB Pricing
In its simplest form, a CB can be converted to the stock or worth the par value at maturity. Therefore, the payoff is either S(T) or Par, whichever is greater (assume a conversion ratio of one). In math notation,
```
payoff = max[S(T), Par] = max[S(T)-Par, 0] + Par
```
which is a portfolio of a call option with Par as the strike price and a zero-coupon bond. In this case, the value of CB is the sum of prices of European call and zero-coupon bond.

Hence, a CB can be priced by solving the Black-Scholes-Merton or [Ayache-Forsyth-Vetzal](#afv) PDE via finite difference method.

Provisional Call (Put), embedded choice to the issuer (holder) that conditional on the past close prices of the underlying stock, are difficult to handle. For example, a 20 out of 30 provisional call will be satified if in the past 30 trading days, the stock closed above a specific trigger price in 20 or more days. Approximations, such as [conditianl range probability (CRP)](#crp) or [auxiliary reversed binomial-tree (ARB)](#arb), can be utilized.

The App with GUI can [be downloded from GitHub](https://github.com/qiangliu-sd/cvt-bond-pricer).

Even better, you can [price CBs on your phone](https://qiang-liu.com/ql_cvt_px/index.html).

The CB fair values can be validated with the default parameters when the App or webpage is launched. The following table shows the results for zero-coupon and semi-annual coupons:

![CB fair values](images/cvt_fair_vals.png)

To get the numers in the above table, make sure to choose *bsm_pde* as the **PDE model**, and *2* as the **coupon frequency**.

Note that in principle, the holder's (issuer's) choice will increase (decrease) the fair value.

The fair value of European call can be obtained easily from [price CBs on your phone](https://qiang-liu.com/ql_opt_px/index.html).

The bond values can be simply verified by an Excel spreadsheet:

![Bond values](images/bond_vals.png)

### References:
<a name="afv"></a>AFV:\
Ayache, Forsyth, Vetzal (2003). The valuation of convertible bonds with credit risk. Journal of Derivatives.

<a name="crp"></a>CRP:\
Liu, Guo (2020). [An excellent approximation for the m out of n day provision. North American Journal of Economics and Finance](https://www.sciencedirect.com/science/article/pii/S1062940820301194).

<a name="arb"></a>ARB:\
Liu, Guo (2008). Approximating the embedded m out of n day soft-call option of a convertible bond: An auxiliary reversed binomial tree method. SSRN.


