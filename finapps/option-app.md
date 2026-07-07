# A Unifying Option Pricing App

If you have ever wondered whether it is possible to see options' pricing results from 
the Black-Scholes-Merton formula, binomial tree, finite difference, or 
Monte Carlo simulation in one place, this App is for you!

The App with GUI allows you to specify the option type, the underlying type, the pricing method, and other parameters.

The App with GUI will output price, delta, and gamma or implied volatility and can [be downloded from GitHub](https://github.com/qiangliu-sd/option-pricer).

Even better, you can [price options on your phone](https://qiang-liu.com/ql_opt_px/index.html).

### Option supported:
- American
- European

### Underlying supported:
- Stock
- Stock index
- Foreign currency
- Futures

### Pricing method supported:
- Anthithetic Monte Carlo
- Anthithetic least-square Monte Carlo
- Black-Sholes-Merton formula with [balanced dividend adjustment (BDA)](#bda)
- Binomial-tree
- BDA recombining binomial tree
- Non-recombining binomial tree
- Finite difference with:
  - Crank-Nicolson
  - Explicit difference
  - Implicit difference

#### Cash (dollar) dividends
ONE dividend or multiple dividends

### Notes
<a name="bda"></a>
For BDA, see: [A simple accurate binomial tree for pricing options on stocks with known dollar dividends, Journal of Derivatives](https://www.proquest.com/openview/2be03fbe6deff07a799f6bb7bd93405b/1?pq-origsite=gscholar&cbl=32822)

Put can be priced as call in DUAL-space by simply *swapping stock price (dividend yield) for strike price (risk-free rate) simultaneously*. See: [The Black-Scholes-Merton dual equation](http://arxiv.org/abs/1912.10380). Try this out using the App!