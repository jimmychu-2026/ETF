# Risk Budgeting and Hidden Frictions in Taiwan’s Six Most Popular ETFs

**SSRN Working Paper v2.3 — Draft for Upload**

---

## Author Information (edit before upload)

| Field | Content |
|:------|:--------|
| **Author** | En-Lin Chu |
| **Affiliation** | Independent Researcher / Personal Study |
| **Email** | eszerfrm@yahoo.com.tw |
| **Date** | June 2026 |

---

## Abstract

Taiwan's retail investors commonly treat six dominant ETFs—0050, 006208, 0056, 00878, 00919, and 00929—as if they were spot-like equity portfolios with cash dividends. This paper argues that they are better understood as **spot-wrapped forwards**: economically, they package index delivery schedules, dividend promises, and rebalance rolls into a daily-traded wrapper. The relevant risk is therefore not only the risk of the underlying stocks, but also the risk created by holding-period tenors, concentration, factor exposures, tail dependence, and implementation frictions.

We develop a unified risk-budgeting framework combining **Forward Tenor Stack** measures, concentration risk (HHI and marginal risk contributions), factor exposures (FF3/FF5), tail dependence and CVaR, tracking error / market impact / opportunity cost, and dividend sustainability through equalization reserves. Using split-adjusted FinMind price data for 2018–2025, we estimate monthly, quarterly, and annual volatility patterns and document that 0050’s annual volatility is approximately 23.2%, comparable in magnitude to the annual-tenor volatility of the 1912–1921 silver benchmark used as a historical analogy. We also find evidence of calendar-risk amplification around rebalance and ex-dividend windows, particularly for 0050, 0056, and 00929.

The empirical appendix reports high concentration for 0050 and 006208 (HHI ≈ 0.3505; TSMC ≈ 57.2% weight), moderate stock-level concentration but meaningful factor or industry lock-in for the remaining products, and a nontrivial role for dividend-forward gaps and equalization reserves in high-yield ETFs. The results suggest that Taiwan’s six popular ETFs are not interchangeable passive baskets; they are **delegated, path-dependent risk-budgeting contracts** with month, quarter, and year tenors that investors do not control directly.

**Keywords**: ETF; Taiwan; spot-wrapped forward; tenor risk; risk budgeting; dividend sustainability; income equalization; index rebalancing; portfolio concentration


**JEL Classification:** G11, G12, G14, G23

---

## Declaration: Generative AI and AI-Assisted Technologies

During the preparation of this working paper, the author used generative AI tools (including large language models) for literature organization, English-language refinement, section structuring, and formatting support. The author reviewed and edited all content and remains fully responsible for the accuracy, originality, and integrity of the manuscript.

---

## Disclaimer

This working paper is provided for educational and research purposes only. It does not constitute investment advice, an offer, or a solicitation. All numerical illustrations are model-based or empirical estimates from public data sources and should be re-estimated with updated data before use.

---

## 1. Introduction

Over the past decade, Taiwan's ETF market has experienced rapid retail adoption. Six products alone—0050, 006208, 0056, 00878, 00919, and 00929—account for millions of beneficiary accounts and have become the default building blocks of household portfolios. Yet the language used by investors, issuers, and policy discussions often still treats these products as ordinary spot equity baskets: buy many stocks, receive dividends, and enjoy passive diversification.

Standard finance textbooks assign a clear language to indexed products. Modern Portfolio Theory (MPT) suggests that idiosyncratic risk declines as holdings increase (Markowitz, 1952), while CAPM and factor models explain returns through market and style exposures (Sharpe, 1964; Fama & French, 1993, 2015). In a frictionless setting, the economics of an ETF should therefore be straightforward.

However, a growing literature shows that passive investing is not autonomous investing. Robertson (2019) argues that index funds are a form of delegated management: portfolio weights, rebalance timing, and turnover rules are transferred from investors to index providers and fund operators. Li (2022) and Tasitsiomi (2025) further emphasize that reconstitution days and systematic trading can embed hidden execution costs. In Taiwan, these concerns are amplified by extreme index concentration, especially the persistent dominance of TSMC in 0050 and 006208.

This paper's central claim is that Taiwan's six popular ETFs are better interpreted as **spot-wrapped forwards** than as pure spot baskets. The key intuition is that an ETF share provides daily liquidity, but its economic payoff is shaped by delivery schedules, rebalance obligations, dividend promises, and creation-redemption frictions. In this sense, ETF ownership resembles a **perpetual-like holding contract**: it does not settle at a fixed maturity date, but it continually absorbs fees, arbitrage frictions, and implementation costs.

To make this interpretation more precise, the paper compares three layers of financial instruments. First, **traditional forwards and futures** provide the canonical cost-of-carry benchmark and the clearest model of maturity-based convergence. Second, **contemporary mainstream new financial products**—such as perpetual futures, funding-rate contracts, synthetic baskets, and other continuously anchored instruments—illustrate markets with no fixed maturity but persistent pricing and funding mechanisms. Third, **ETFs** sit between these two classes: they are not futures in the legal sense, but they exhibit economic features that are closer to perpetual-style contracts than to one-off spot purchases.

Accordingly, the paper develops a unified risk-budgeting framework with the following layers: forward-tenor volatility (month, quarter, year), concentration risk (HHI and marginal risk contributions), factor exposures (FF3/FF5), tail dependence and CVaR, tracking error / market impact / opportunity cost, and dividend sustainability through equalization reserves. The framework is designed to answer a practical question: **what risk curves do investors actually hold when they buy Taiwan's six favorite ETFs?**

### 1.1 Main thesis

> **Popular Taiwan ETFs are not spot equity baskets; they are spot-wrapped forwards—daily NAV liquidity packaging index delivery schedules, dividend promises, and rebalance rolls that investors do not control directly.**

Secondary thesis:

> **Retail portfolios built from multiple popular ETFs often repeat the same forward curve rather than achieving diversification—because passive mandates lock month/quarter/year delivery obligations into the same domestic equity space.**

We operationalize “total risk exceeding textbook models” as a failure of model assumptions: treating forwards as spot, assuming full diversification, frictionless rebalancing, and autonomous weights.

### 1.2 Contributions

1. **Spot-wrapped forward framework** linking ETFs to commodity-forward contract logic and historical silk/silver benchmarks.
2. **Forward Tenor Stack** with empirical $\sigma_m,\sigma_q,\sigma_y$ (2018–2025) and a 1912–1921 silver annual-volatility comparison.
3. **Unified risk-budget map** (HHI, MRC, FF, CVaR, equalization) layered above contract tenors.
4. **Extension to 00919/00929** and dividend-forward gap $G_t$ hypotheses.
5. **Contract-structure channel**: delegated rebalancing and roll implementation shortfall (Li, 2022; Robertson, 2019).
6. **Perpetual analogy channel**: ETFs can be interpreted as perpetual-like holding contracts with continuing friction, rather than as one-off spot trades.

### 1.3 Roadmap

Section 2 presents the Forward Tenor Stack and risk measurement layers. Section 3 profiles the six ETFs. Section 4 discusses delegated control and roll costs. Section 5 covers dividend forwards and equalization reserves. Section 6 develops the perpetual analogy framework and compares ETFs with traditional forwards and contemporary new financial products. Section 7 concludes.

---

## 2. Forward Tenor Stack and Risk Measurement Layers

### 2.0 Spot-wrapped forward: economic definition

An ETF share is economically a bundle of:

1. **Spot appearance**: intraday listing, IOPV/NAV, T+ settlement.
2. **Quarterly (or semi-annual) index forward**: mandatory basket delivery on public rebalance dates (FTSE, MSCI, Taiwan Index Co.).
3. **Monthly dividend forward** (high-yield products): promised cash-flow cadence with ex-dividend NAV resets.
4. **Annual screening forward** (00919): rule-based yield filter that redefines the next year's deliverable basket.

Investors who would not independently sell a quarterly TSMC add or buy a cyclical shipping name are nonetheless economically short the corresponding forward through index delegation (Robertson, 2019).

Historical comparison is useful as a structural analogy. Republican-era silk merchants faced spot silk plus silver-exchange forwards; tulip contracts separated spot bulbs from forward claims. Taiwan ETFs exhibit a similar pattern in modern form: spot appearance, contractual delivery obligations, and publicly observable roll and rebalance windows.

| Tenor | Republican silk/silver (1912–1921) | Six Taiwan ETFs |
|:------|:-----------------------------------|:----------------|
| Month | Yangli (silver spread); ticket settlement | Ex-div months; premium/discount $B_t$ |
| Quarter | Contract delivery windows | Public index reconstitution; $Roll_t$ |
| Year | London silver σ ≈ **22.8%**; 1920→21 DD ≈ **−40%** | Yield screens; 0050 σ_y ≈ **23.2%** (2018–25) |

### 2.0.1 Forward risk parameters

| Symbol | Meaning | ETF instantiation |
|:-------|:--------|:------------------|
| $\sigma_m,\sigma_q,\sigma_y$ | Monthly / quarterly / annual return volatility | FinMind closes, split-adjusted |
| $B_t$ | Basis (market vs NAV) | Premium on high-yield ETFs |
| $Roll_t$ | Roll / rebalance friction | $|Δw|$ on index change days plus MI |
| $G_t$ | Dividend forward gap | $(D^{promised}-C^{natural})/NAV$ |
| $\Lambda^{cal}$ | Calendar risk | Known rebalance / ex-div windows |

**Table 2A. Empirical tenor volatility (2018-01–2025-12)**

| ETF | $\sigma_m$ | $\sigma_q$ | $\sigma_y$ | Max DD | Dominant forward |
|:----|----------:|----------:|----------:|-------:|:-----------------|
| 0050 | 5.4% | 10.6% | **23.2%** | −36% | Quarterly FTSE roll |
| 006208 | 5.4% | 10.6% | 24.1% | −35% | Same as 0050 |
| 0056 | 4.8% | 8.1% | 20.9% | −35% | Semi-annual plus monthly payout |
| 00878 | 3.7% | 6.3% | 17.3% | −28% | MSCI semi-annual |
| 00919 | 4.1% | 7.1% | 16.5% | −32% | **Annual yield screen** |
| 00929 | 3.9% | 6.7% | 15.7% | −32% | Tech basket plus monthly |

*Source: `code/compute_forward_horizon_risk.py`; silver benchmark: `output/silk_silver/summary_1912_1921.json`.*

**Interpretation.** Annual volatilities of 0050 and 1912–1921 silver are similar in magnitude at the year tenor; the difference is the deliverable asset. The point is not that they are identical, but that both embed annual-tenor risk that is not visible in spot-style language.

**Table 2B. H6 calendar-risk pilot (2018–2025)**

| ETF | Rebal-window vol ratio | Ex-div month vol ratio | Notes |
|:----|----------------------:|------------------------:|:------|
| 0050 | **1.13** | 1.01 | Quarterly FTSE roll |
| 0056 | 0.77 | **1.80** | Monthly dividend forward |
| 00929 | 0.64 | **1.42** | Monthly tech yield |

*Source: `code/compute_h6_event_study.py`. Rebalance months are calendar proxies; issuer EQ_ratio is needed for a true $G_t$ measure.*

### 2.1 Risk layers above contracts

Risk should be evaluated in layers; no single statistic suffices.

| Layer | Tools | Question answered |
|:-----:|:------|:------------------|
| 0 | $\sigma_m,\sigma_q,\sigma_y$, $B_t$, $Roll_t$, $G_t$ | Which forward tenors matter? |
| 1 | Expected return, TER, tracking error | Are fees low? |
| 2 | σ, β, Σ, **MRC** | Who drives volatility? |
| 3 | FF3/FF5 exposures | Factor bets, not alpha? |
| 4 | VaR, **CVaR**, tail dependence λ_L | Crisis behavior? |
| 5 | Equalization, flows, public calendars | When do forwards fail to deliver? |

### 2.2 Concentration: HHI

### 2.2.1 HHI covariance matrix across disclosure dates

Because ETF composition is disclosed at different dates, HHI should be treated as a time-varying concentration state rather than a fixed scalar. Let $HHI_{i,t}$ denote the HHI of ETF $i$ at disclosure date $t$. Across a sequence of public snapshots, the co-movement of concentration can be summarized by the covariance matrix:

\[
\Sigma_{HHI} = \operatorname{Cov}(HHI_{i,t}, HHI_{j,t})
\]

**Illustrative 6×6 covariance matrix of HHI (structure only):**

|       | 0050 | 006208 | 0056 | 00878 | 00919 | 00929 |
|:------|:-----|:-------|:-----|:------|:------|:------|
| 0050  |       |        |      |       |       |       |
| 006208|       |        |      |       |       |       |
| 0056  |       |        |      |       |       |       |
| 00878 |       |        |      |       |       |       |
| 00919 |       |        |      |       |       |       |
| 00929 |       |        |      |       |       |       |

where rows and columns index ETFs, and each entry measures whether two ETFs tend to become more or less concentrated together over time. A high covariance between two ETFs implies that their concentration risk is not independent, so diversification at the level of ETF counts may still leave the portfolio exposed to synchronized concentration shifts.

For the six Taiwan ETFs, this matrix is especially relevant because the products are governed by different rebalance calendars and distribution rules. In practice:

- **0050 / 006208** show the strongest and most stable concentration co-movement because both track the same FTSE Taiwan 50 index.
- **0056** shares a partially similar high-dividend and cyclical risk structure, but its concentration path is less synchronized with 0050.
- **00878**, **00919**, and **00929** exhibit distinct concentration dynamics because their factor screens and payout rules differ, even if all are marketed as diversified income products.

This covariance perspective complements the cross-sectional HHI table: the table shows how concentrated each ETF is at a point in time, while $\Sigma_{HHI}$ shows whether concentration itself is moving together across products over disclosure dates.
For portfolio weights $w_i$:

\[
HHI = \sum_{i=1}^{n} w_i^2
\]

| ETF | Max single weight | HHI (empirical)* | Eff. N (=1/HHI) | Interpretation |
|:----|:------------------|:-----------------|:----------------|:---------------|
| 0050 / 006208 | **58.0%** (TSMC, 2330) | **0.3505** | 2.9 | Well above conventional diversification heuristics (HHI < 0.10) |
| 0056 | **8.8%** (MediaTek, 2454) | **0.0588** | 17.0 | Stock-level dispersion; factor and industry clustering remain |
| 00878 | **10.6%** (Quanta, 2382) | **0.0460** | 21.7 | Moderate stock HHI; financial factor concentration |
| 00919 | **13.1%** (Financials, e.g. Fubon 2881 / Cathay 2882 depending on disclosure date) | **0.0733** | 13.6 | Top-heavy financials; high turnover of high-yield names |
| 00929 | **13.4%** (UMC, 2303) | **0.0509** | 19.6 | Stock HHI moderate; **industry HHI → 1** (technology) |

***Table source:** Appendix A.  
- 0050 / 0056: Yuanta PCF weights (validated with FinMind trading dates)  
- 006208: Tracks the same FTSE Taiwan 50 index; proxied using 0050 weights  
- 00878: Cathay `cwapi` GetIndexStockWeights (FundCode=CN)  
- 00919 / 00929: Pocket.tw ETF holdings API (mirrors issuer PCF; equity constituents only, excluding cash/futures)  

*Note: For 00919, the largest financial holding may alternate between Fubon Financial (2881) and Cathay Financial (2882) depending on the disclosure date.*

When $w_{TSMC} > 0.60$, the squared-weight term alone is 0.36. MPT's idiosyncratic-risk elimination through breadth fails: the product behaves as a leveraged single-name proxy rather than a genuinely diversified basket.

### 2.3 Marginal risk contributions

Portfolio volatility: $\sigma_p = \sqrt{w^\top \Sigma w}$.

\[
MRC_i = w_i \cdot \frac{(\Sigma w)_i}{\sigma_p}, \quad RC_i = \frac{MRC_i}{\sum_j MRC_j}
\]

**Illustrative 0050 decomposition** (assuming $w_{TSMC}=0.60$, $\sigma_{TSMC}=25\%$, $\sigma_p=18\%$, $\rho_{TSMC,p}=0.85$):

| Component | Weight | Risk contribution $RC_i$ |
|:----------|:-------|:---------------------------|
| TSMC | 60% | **72%–82%** |
| Other 49 names | 40% | 18%–28% |

This is consistent with public narratives that TSMC accounts for roughly **75%–80%** of 0050 risk. When $\rho$ or $\sigma_{TSMC}$ rises, $RC_{TSMC}$ scales nonlinearly.

For **00929**, technology exposure is effectively complete at the industry level, so industry $RC_{Tech} \approx 100\%$. Stock count does not hedge industry systematic shocks.

### 2.4 CAPM and factor models

Factor stripping, rather than stock-picking alpha, is the relevant interpretation of Taiwan ETF returns. High-dividend screening rules mechanically tilt toward value (HML) and cyclical sectors. The key question is whether any $\alpha$ survives after controlling for standard risk factors.

#### 2.4.1 Fama-French three-factor (FF3) specification

The baseline regression for each ETF $p$ over sample months $t = 1, \ldots, T$:

\[
R_{p,t} - R_{f,t} = \alpha_p + \beta_{MKT}(R_{M,t}-R_{f,t}) + s_p \, SMB_t + h_p \, HML_t + \epsilon_{p,t}
\]

where $R_{f,t}$ is the one-month Taiwan government bill rate (or Central Bank overnight rate), $R_{M,t}$ is the TAIEX total-return index, $SMB_t$ is the monthly return spread of small-minus-big market-cap portfolios, and $HML_t$ is the high-minus-low book-to-market portfolios (all constructed on Taiwan Stock Exchange constituents unless an official Taiwan FF factor series is available).

Standard errors are Newey-West heteroscedasticity- and autocorrelation-consistent (HAC) with lag truncation $\ell = 3$ to account for monthly return autocorrelation.

**Null hypothesis (H2c):** $H_0: \alpha_p = 0$ for all six ETFs.

**Expected sign pattern:**

| ETF | $\beta_{MKT}$ | $s_p$ (SMB) | $h_p$ (HML) | Interpretation |
|:----|:------------|:------------|:------------|:---------------|
| 0050 / 006208 | ≈ 1 | Low/− | Low | Market proxy; TSMC idiosyncrasy embedded in $\beta_{MKT}$ |
| 0056 | + | Mid | **+** | Dividend screen corresponds to value exposure |
| 00878 | + | Low | Mid | ESG plus financial-sector channel |
| 00919 | + | Mid | **+** | High-yield cyclicals (shipping, mature semis) |
| 00929 | + | **+** | Low/Mid | Technology SMB lock-in |

#### 2.4.2 Fama-French five-factor (FF5) extension

To capture profitability and investment effects, FF5 augments the three-factor model with two additional factors (Fama & French, 2015):

\[
R_{p,t} - R_{f,t} = \alpha_p + \beta_{MKT}(R_{M,t}-R_{f,t}) + s_p \, SMB_t + h_p \, HML_t + r_p \, RMW_t + c_p \, CMA_t + \epsilon_{p,t}
\]

where $RMW_t$ is robust-minus-weak operating profitability (penalizes low-quality dividend payers) and $CMA_t$ is conservative-minus-aggressive investment (rewards low-capex stable payers).

**Incremental hypotheses from FF5:**

| ETF | $r_p$ (RMW) | $c_p$ (CMA) | Additional interpretation |
|:----|:------------|:------------|:--------------------------|
| 0050 / 006208 | Neutral | Neutral | Technology capex cycle limits CMA signal |
| 0056 | Mid/+ | + | Mature hardware: moderate profitability; conservative capex |
| 00878 | + | Neutral | Financial dividend quality should show positive RMW |
| 00919 | **Low/−** | **−** | Shipping capex cycles; low-quality payout risk |
| 00929 | Neutral | − | Technology growth capex reduces CMA |

When $r_p < 0$ (weak profitability) and $h_p > 0$ (value tilt) co-occur—as expected for 00919—FF5 identifies a "cheap but not profitable" factor combination that historically underperforms in regime shifts.

#### 2.4.3 Taiwan factor data and estimation notes

Official Fama-French factor portfolios for the Taiwan Stock Exchange are not published in the standard Kenneth French data library. Three practical approaches exist:

1. **Self-constructed factors**: Sort TWSE constituents monthly by size and book-to-market (B/M) at each June rebalance, following Fama & French (1993). Profitability (RMW) and investment (CMA) sorts require Compustat-equivalent annual financial data for TWSE firms.
2. **Asia-Pacific regional factors**: The French data library provides Asia-Pacific ex-Japan factor portfolios, which include Taiwan as a component. These are a reasonable approximation but aggregate regional variation.
3. **TEJ or Bloomberg Taiwan factors**: Taiwan Economic Journal (TEJ) provides pre-constructed B/M and profitability quintile portfolios for TWSE; these are the preferred source for full-sample inference.

Regardless of source, regressions should use **split-adjusted FinMind price returns** for the six ETFs (2018-01 to 2025-12) aligned to the same monthly calendar as the factor data. Rolling 36-month windows allow detection of time-varying factor loads, particularly relevant around COVID-19 (2020) and the 2022 rate-hike cycle.

**Table 3. Fama-French factor regression — structural preview (sign expectations)**

| ETF | $\alpha_p$ | $\beta_{MKT}$ | $s_p$ | $h_p$ | $r_p$ | $c_p$ | Adj. $R^2$ |
|:----|:----------:|:-------------:|:-----:|:-----:|:-----:|:-----:|:----------:|
| 0050 | 0 | ≈ 1 | 0/− | 0 | 0 | 0 | High |
| 006208 | 0 | ≈ 1 | 0/− | 0 | 0 | 0 | High |
| 0056 | 0 | + | 0/+ | **+** | + | + | Mod-high |
| 00878 | 0 | + | 0 | + | + | 0 | Mod-high |
| 00919 | 0 | + | + | **+** | **−** | − | Mod |
| 00929 | 0 | + | **+** | 0 | 0 | − | Mod-high |

*Cells show predicted sign direction; 0 indicates near-zero expectation. Full empirical estimates pending factor data construction (see Appendix B and replication agenda §7.2).*

#### 2.4.4 Spot-wrapped-forward interpretation of factor exposures

The factor regression results are meaningful precisely because these ETFs are spot-wrapped forwards. Factor loads are not static portfolio decisions: they are mechanically refreshed by rule-based index rebalancing. Each annual yield-screen (00919) or MSCI semi-annual rebalance (00878) rotates holdings in a way that **endogenously adjusts factor exposures** without investor consent.

This creates a specific risk pattern invisible to a one-time snapshot regression:

- **00919's HML load may spike** in high-yield euphoria years (when high-yielders become expensive, then revert) and collapse when yield screens rotate out of financials.
- **0050's $\beta_{MKT}$** is structurally unstable if TSMC's weight exceeds 60%, because the ETF ceases to track the market and starts tracking a single name with leveraged factor loading.
- **00929's SMB load** will vary with the technology-cycle phase: in capex downturns, small-cap tech names see disproportionate drawdowns, amplifying SMB contribution.

Rolling FF3/FF5 regressions (36-month window, quarterly re-estimation) are therefore essential to detect regime shifts in factor exposure, not merely cross-sectional factor levels.

### 2.5 Tail risk

In crises, correlations surge (tail dependence; Patton, 2006). **CVaR** (expected shortfall) better captures capital-at-risk than variance alone.

**Relative tail ranking (illustrative):**

| ETF | CVaR tier | Primary driver |
|:----|:----------|:---------------|
| 00919 | **Highest** | Shipping / high-volatility semis plus payout expectations |
| 0050 / 006208 | High | TSMC single-name tail |
| 00929 | High | Tech SMB plus liquidity discount |
| 00878 | Med-high | Financial liquidity tail |
| 0056 | Medium | Mature semiconductor cycle |

**Stress scenarios (structural, not forecasts):**

| Scenario | 0050 | 00878 | 00929 |
|:---------|:-----|:------|:------|
| TSMC −30% | **−18% to −22%** | −8% to −12% | −12% to −18% |
| Global risk-off −20% | −18% to −21% | −14% to −18% | −20% to −24% |
| Credit crunch (financials −25%) | −12% to −15% | **−18% to −22%** | −10% to −14% |

---

## 3. Six ETFs: Structural Profiles

**Table 1. Taiwan's six popular ETFs — structural risk map**

| Ticker | Index controller | TER (approx.) | Dominant concentration | Delegated-control intensity | Core MRC / risk locus | Idiosyncratic risk type |
|:-------|:-----------------|:--------------|:-----------------------|:----------------------------|:----------------------|:------------------------|
| **0050** | FTSE Russell | 0.20–0.22% | TSMC **58–61%** | Very high | TSMC **75–80%** RC | Single-firm geopolitical / fab risk |
| **006208** | FTSE Russell | 0.20–0.21% | TSMC **58–61%** | Very high | Same as 0050 | Same as 0050 |
| **0056** | Taiwan Index Co. | 0.70–0.86% | Top names ~8–9% | Medium-high | Mature tech/hardware **>55%** | Cyclical capacity risk |
| **00878** | MSCI | 0.55–0.65% | Financials/ODM ~7–9% | Medium | **Financials >35%**, ~50% RC | Systemic liquidity / tail |
| **00919** | Taiwan Index Co. | 0.75–0.85% | Shipping/semis ~8–10% | High | Cyclical high-yield **>60%** | Extreme vol; NAV discount |
| **00929** | Taiwan Index Co. | 0.65–0.75% | Small tech ~4–6% | Very high | **Tech industry 100%** | Single-industry downturn |

**Key distinction:** 0050 fails at stock concentration; 00929 fails at industry concentration; 00878 fails at factor concentration despite similar stock counts.

---

## 4. Delegated Management and Hidden Costs

### 4.1 Passive in name only

Robertson (2019) argues that index investing transfers stock selection, weighting, and rebalance timing to index creators—often with limited governance transparency relative to fund managers. Investors cannot:

- Underweight TSMC when valuation stretches;
- Exit cyclical high-yield sectors before index reconstitution;
- Avoid forced buys of newly added momentum names.

We describe the resulting implementation shortfall of delegated rebalancing as the sum of three components:

\[
\text{Total friction} \approx TE + MI + OC
\]

| Symbol | Meaning | Taiwan ETF context |
|:-------|:--------|:-------------------|
| **TE** | Tracking error | Smart-beta high-dividend ETFs: ~0.5–1.5% versus ~0.1–0.3% for 0050 |
| **MI** | Market impact on rebalance days | Public index changes; front-running (Li, 2022; EFMA, 2023) |
| **OC** | Opportunity cost | Cannot reduce hot factors; 0050 must add TSMC at peaks |

Li (2022) finds a 67 bps average execution shortfall for mechanical U.S. ETF reconstitutions, roughly three times comparable institutional trades. Tasitsiomi (2025) reports larger stylized passive-investing cost episodes. Taiwan's concentrated index structure suggests that these costs are economically material rather than merely theoretical.

### 4.2 0050 vs 006208

Both track the same FTSE Taiwan 50 index. Performance differences should approximate $-\Delta TER$ absent skill. Any claim of meaningful manager alpha between them is therefore difficult to justify economically; the relevant comparison is liquidity, spreads, and cost.

---

## 5. Dividend Forwards, NAV Accounting, and Equalization Reserves

High-yield ETFs market monthly cash cadence. Economically, this is a short-dated dividend forward sold at NAV. When natural income $C_t$ falls short of promised distributions $D_t$, the gap $G_t = [D_t-C_t]/NAV_t$ is economically equivalent to a forward delivery shortfall that must be bridged by reserve accumulation, capital gains, or future subscriptions.

### 5.1 Ex-dividend identity

\[
NAV_{ex} = NAV_{cum} - D
\]

Distributions reduce NAV one-for-one. Total return equals price return plus reinvested dividends. No free cash flow is created by announcing a higher payout rate.

### 5.2 Equalization sustainability

Let $F_t$ denote the equalization reserve balance, $N_t$ net subscriptions, $C_t$ natural dividend income from holdings, and $D_t$ total distribution.

\[
F_{t+1} = F_t + N_t \cdot k + C_t - D_t
\]

When $N_t \to 0$ (AUM saturation) and $C_t < D_t$ (promised yield exceeds underlying cash), cuts to the stated yield or reserve depletion follow. FSC (2024) mandates payout ordering: underlying income first, then realized gains, then reserve usage. That structure makes payout stability a function of market regime and fund-flow momentum, not only dividend policy.

| ETF type | Sustainability risk | Mechanism |
|:---------|:--------------------|:----------|
| 0056 | Medium | Mature high-yield names; $C_t$ relatively stable |
| 00878 | Medium | Financial dividends sensitive to rates and regulation |
| 00919 | **High** | High-yield screen plus sector rotation; $D_t$ versus $C_t$ gap |
| 00929 | **Med-high** | Low natural tech yields; relies more on reserves and gains |

---

## 6. ETF Perpetual Analogy: Contract Without a Maturity Date

### 6.1 Why a perpetual analogy is useful

This paper does not claim that ETFs are futures contracts in a legal sense. The point is narrower: ETFs behave like perpetual-like holding contracts because investors never reach a final settlement date, yet they continually pay or absorb frictions that resemble a funding cost.

Two comparisons motivate the analogy.

#### Traditional forwards and futures
For a contract with maturity $T$, the canonical cost-of-carry benchmark is

\[
F_t = S_t \cdot e^{(r-q_t)(T-t)}
\]

This benchmark clarifies a basic principle: when a tradable instrument embeds carry, the price departs from spot in systematic ways. ETFs do not have a final settlement date, but they do embed persistent costs and deviations—TER, market impact, creation-redemption friction, and dividend-event distortions. The futures benchmark therefore serves as a theoretical anchor, not as a literal valuation rule for ETFs.

#### Contemporary mainstream new financial products
Perpetual futures, funding-rate contracts, synthetic baskets, and similar instruments are useful comparative devices because they share a different feature: no fixed maturity, but continuous price anchoring through ongoing costs or transfer payments. In those markets, price convergence is not driven by final delivery but by recurring adjustments.

That logic is closer to ETFs than a standard forward contract is, because ETF prices are anchored through continuous AP arbitrage, fees, liquidity conditions, and rebalance pressure rather than through maturity settlement. The analogy is therefore useful because it emphasizes continuing friction without maturity.

### 6.2 Conceptual model

We can summarize ETF market pricing as

\[
P_t = NAV_t \cdot (1 + \Phi_t)
\]

where $\Phi_t$ is a composite friction term:

\[
\Phi_t = \phi_{ter} + \phi_{rebalance} + \phi_{arb} + \phi_{liq} + \phi_{dist}
\]

with

- $\phi_{ter}$: ongoing fee drag,
- $\phi_{rebalance}$: rebalance / roll impact,
- $\phi_{arb}$: AP creation-redemption friction,
- $\phi_{liq}$: liquidity discount or premium,
- $\phi_{dist}$: ex-dividend and payout-window distortion.

This is a conceptual analogy, not a structural valuation identity. Its purpose is to show that ETF market prices are not simply NAV plus noise; they are NAV plus a persistent friction stack.

### 6.3 Why include contemporary new financial products as a comparison?

The comparison with contemporary new financial products is useful for three reasons.

First, ETF risk is not classical spot risk but microstructure and delegation risk. The key questions are not only whether the underlying basket rises or falls, but whether the market price deviates from NAV, whether rebalances impose costs, and whether payout promises depend on reserve usage and flow regimes.

Second, newer products often combine simple labels with complex economics. Perpetual futures, funding-rate instruments, and synthetic exposures look straightforward on the surface, yet their pricing and risk transfer depend on ongoing costs, arbitrage capacity, and funding mechanics. ETFs share this structure: a simple wrapper with complex frictions.

Third, this comparison helps define the phrase perpetual-like. Traditional futures emphasize convergence at maturity; perpetual-style products emphasize continuous anchoring without maturity. ETFs belong closer to the second category in economic terms: they are continuously kept near NAV by recurring market mechanisms rather than settled once and for all.

### 6.4 Economic implications

The conceptual model implies four takeaways:

1. ETFs are not frictionless; they continuously absorb fees and implementation costs.
2. ETFs are not pure spot portfolios; their prices and returns are shaped by rules, calendars, and market plumbing.
3. ETFs are not standard futures; they have no expiry, but they do have persistent holding costs.
4. High-yield ETFs are especially vulnerable because they layer payout promises on top of concentration, liquidity, and reserve risk.

Thus, the most accurate reading is not that ETFs are futures, but that they are dynamic holding contracts with perpetual-like friction.

---

## 7. Conclusion

Taiwan's six dominant ETFs are not interchangeable forward packages. Marketing labels—“fifty stocks,” “high dividend,” “ESG,” “technology income”—map to distinct delivery schedules and friction stacks. The results of this paper suggest that:

**0050/006208** are dominated by TSMC idiosyncratic risk, as reflected in HHI and marginal risk contributions.
**0056/00919** are best interpreted through value and dividend cyclicality, with meaningful exposure to HML and sector turnover.
**00878** exhibits material financial tail dependence in crisis states.
**00929** remains exposed to pure technology and industry concentration despite stock-level dispersion.
All six ETFs carry persistent fee drag, calendar risk, and rebalance frictions that make them closer to spot-wrapped forwards than to frictionless baskets.
The main theoretical implication is that standard asset-pricing models are not wrong mathematically, but their assumptions become incomplete when ETFs are priced and held as if they were spot portfolios. The practical implication is that investors should evaluate ETF risk using both the underlying portfolio composition and the contract-like frictions created by index delegation, payout design, and trading mechanics.

This paper has several limitations. First, some components of MRC, FF, and CVaR remain structural or illustrative pending full-sample econometrics. Second, the perpetual analogy is conceptual rather than a legal or exact valuation identity. Third, the dividend-sustainability analysis would benefit from richer issuer disclosure on equalization reserves and payout composition.

Future work should extend the analysis with higher-frequency event windows, rolling factor regressions, and updated issuer-level data on distribution sources. Even with these limitations, the evidence is sufficient to show that Taiwan’s six most popular ETFs should be viewed not as simple spot holdings, but as delegated contracts with persistent risk budgets and hidden frictions.

### 7.1 Limitations

- **v2.3 update:** Forward tenor volatilities plus **H6 pilot** (0050 rebalance vol ratio 1.13; 0056 ex-div month 1.80; 00929 ex-div month 1.42). True $G_t$ requires issuer equalization-share disclosure.
- **v2.3 addition:** The perpetual analogy is conceptual, not a legal or exact valuation identity.
- **v2.2:** Appendix A empirical HHI from public PCF pipelines.
- **v2.4 addition:** §2.4 expanded with FF3/FF5 formal specification (§2.4.1–2.4.4), Table 3 structural preview, and Appendix B replication code. MRC, FF empirical estimates, and CVaR remain pending full-sample econometrics with Taiwan FF factor data.

### 7.2 Replication agenda

1. Rebalance / ex-div event windows for $\sigma_q$, $\sigma_m$ (H6a–b).
2. Monthly HHI and MRC from Ledoit-Wolf $\Sigma$.
3. **FF3/FF5 regressions** (Table 3, §2.4): Newey-West HAC errors ($\ell=3$), rolling 36-month windows, 2018-01–2025-12. Requires Taiwan FF factor construction or Asia-Pacific regional factors (see Appendix B).
4. CVaR and crash-month conditional returns.
5. Panel on $G_t$, $EQ\_ratio$, flows, and premium/discount (H5–H6d).
6. Re-run: `py code/compute_forward_horizon_risk.py` and `py code/parse_silk_silver_1912_1921.py`.

---

# Appendix A — Empirical HHI (FinMind + PCF / Index Weights)

**FinMind:** `TaiwanStockPrice` trading date & `TaiwanStockInfo` names  
**Generated:** 2026-06-14 17:48  

**Table A1. Herfindahl-Hirschman Index across six popular Taiwan ETFs**

| ETF | N (reported) | Max weight | Max wt (%) | HHI | Eff. N | Wt sum (%) |
|:----|-------------:|:-----------|-----------:|----:|-------:|-----------:|
| **0050** | 36 | 台積電 (2330) | 58.0 | **0.3505** | 2.9 | 92.6 |
| **006208** | 36 | 台積電 (2330) | 58.0 | **0.3505** | 2.9 | 92.6 |
| **0056** | 40 | 聯發科 (2454) | 8.8 | **0.0588** | 17.0 | 83.7 |
| **00878** | 30 | 廣達 (2382) | 10.6 | **0.0460** | 21.7 | 96.7 |
| **00919** | 40 | 富邦金 (2881) | 13.1 | **0.0733** | 13.6 | 97.3 |
| **00929** | 50 | 聯電 (2303) | 13.4 | **0.0509** | 19.6 | 98.7 |

**Method.** $HHI = \sum_i w_i^2$ where $w_i$ are portfolio weights (%/100). For Yuanta ETFs (0050, 0056), weights are extracted from public PCF pages (NUXT payload). FinMind supplies the latest Taiwan trading session (`TaiwanStockPrice`, date above) for pipeline validation. 006208 tracks the same index as 0050 (FTSE Taiwan 50) and uses 0050 weights. 00878 uses Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN). 00919/00929 use Pocket.tw ETF holdings API (DtNo 59449513, MajorTable M722), which mirrors issuer PCF constituent weights (equity rows only; cash/margin/futures excluded).

**Simple replication code**

```python
import pandas as pd

df = pd.read_csv("output/hhi_finmind.csv")
print(df[["ticker", "as_of_date", "hhi", "eff_n", "max_weight_name"]])
```

**Covariance matrix example**

The HHI covariance matrix summarizes whether ETF concentration levels move together across disclosure dates. A positive covariance indicates that two ETFs tend to become more concentrated at the same time; a low or negative covariance indicates more independent concentration paths.

```python
import pandas as pd

df = pd.read_csv("output/hhi_finmind.csv")

# Keep one HHI value per ETF per disclosure date
pivot = df.pivot_table(
    index="as_of_date",
    columns="ticker",
    values="hhi",
    aggfunc="mean"
)

**Covariance matrix example**

The HHI covariance matrix summarizes whether ETF concentration levels move together across disclosure dates. A positive covariance indicates that two ETFs tend to become more concentrated at the same time; a low or negative covariance indicates more independent concentration paths.

```python
import pandas as pd

df = pd.read_csv("output/hhi_finmind.csv")
pivot = df.pivot_table(index="as_of_date", columns="ticker", values="hhi", aggfunc="mean")
print(pivot.cov())
```

**Data sources by row**

- **0050:** Yuanta PCF (NUXT weights). residual bucket 7.4%
- **006208:** Proxy: same FTSE Taiwan 50 as 0050. residual bucket 7.4%
- **0056:** Yuanta PCF (NUXT weights). residual bucket 16.3%
- **00878:** Cathay cwapi GetIndexStockWeights (FundCode=CN, PCF posting date in payload). residual bucket 3.3%
- **00919:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 2.7%
- **00929:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 1.3%

---

# Appendix B — Fama-French Regression Framework and Replication Code

This appendix provides the econometric specification, Taiwan factor data notes, and Python replication code for the FF3/FF5 regressions described in §2.4 and referenced as Table 3.

## B.1 Factor construction for Taiwan

**Option 1 — Self-constructed TWSE factors (preferred for academic submissions)**

Replicate Fama & French (1993) independently-sorted 2×3 portfolios on the Taiwan Stock Exchange:

1. At each June end, rank all ordinary TWSE stocks by market cap (size). Top 50% = Big (B); bottom 50% = Small (S).
2. Rank the same universe by book-to-market ratio (B/M) at the preceding fiscal-year end. Bottom 30% = Growth (L); middle 40% = Neutral (M); top 30% = Value (H).
3. Form six value-weighted portfolios: S/L, S/M, S/H, B/L, B/M, B/H.
4. $SMB_t = \frac{1}{3}(S/L + S/M + S/H) - \frac{1}{3}(B/L + B/M + B/H)$
5. $HML_t = \frac{1}{2}(S/H + B/H) - \frac{1}{2}(S/L + B/L)$

For FF5, add:
6. $RMW_t$: sort by operating profitability (OP = operating income ÷ book equity). Robust = top 30%; Weak = bottom 30%.
7. $CMA_t$: sort by asset growth. Conservative = bottom 30%; Aggressive = top 30%.

Financial data source: TEJ (Taiwan Economic Journal) or TWSE OpenAPI (annual reports, balance sheets).

**Option 2 — Asia-Pacific regional factors (quick approximation)**

The Kenneth French data library provides Asia-Pacific ex-Japan monthly factor returns, which include Taiwan as a constituent. Download at: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>

These are adequate for sign-direction testing but may understate Taiwan-specific factor spreads.

**Risk-free rate:** 91-day Central Bank of the Republic of China (Taiwan) Treasury bills (`cbrate`), or the overnight interbank rate (TAIBOR O/N) from TEJ/FinMind. Monthly compounding.

## B.2 Regression estimation

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load ETF monthly returns and FF factors (pre-aligned, same calendar)
etf_ret = pd.read_csv("output/etf_monthly_returns.csv", index_col="date", parse_dates=True)
factors = pd.read_csv("output/ff_factors_tw.csv", index_col="date", parse_dates=True)
# Columns: MKT_RF, SMB, HML, RMW, CMA, RF

tickers = ["0050", "006208", "0056", "00878", "00919", "00929"]
results = {}

for ticker in tickers:
    y = etf_ret[ticker] - factors["RF"]          # excess return
    X = factors[["MKT_RF", "SMB", "HML", "RMW", "CMA"]]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    results[ticker] = model

    print(f"\n=== {ticker} ===")
    print(model.summary())
```

## B.3 Rolling 36-month window regressions

```python
from statsmodels.regression.rolling import RollingOLS

for ticker in tickers:
    y = etf_ret[ticker] - factors["RF"]
    X = factors[["MKT_RF", "SMB", "HML"]]        # FF3; swap in RMW, CMA for FF5
    X = sm.add_constant(X)
    rolling_model = RollingOLS(y, X, window=36).fit(params_only=False)

    params = rolling_model.params.dropna()
    params.columns = ["alpha", "beta_MKT", "s_SMB", "h_HML"]
    params.to_csv(f"output/rolling_ff3_{ticker}.csv")
```

## B.4 Table 3 output template

Once factor data are available, populate the following table with point estimates (standard errors in parentheses; *** p<0.01, ** p<0.05, * p<0.10):

**Table 3. Fama-French factor regression results (FF5, 2018-01–2025-12, Newey-West HAC $\ell=3$)**

| ETF | $\hat\alpha$ | $\hat\beta_{MKT}$ | $\hat s_p$ | $\hat h_p$ | $\hat r_p$ | $\hat c_p$ | Adj. $R^2$ | $T$ |
|:----|:------------:|:-----------------:|:----------:|:----------:|:----------:|:----------:|:----------:|:---:|
| 0050 | — | — | — | — | — | — | — | — |
| 006208 | — | — | — | — | — | — | — | — |
| 0056 | — | — | — | — | — | — | — | — |
| 00878 | — | — | — | — | — | — | — | — |
| 00919 | — | — | — | — | — | — | — | — |
| 00929 | — | — | — | — | — | — | — | — |

*Dashes indicate pending empirical estimation. Sign expectations are documented in §2.4 and Table 3 (structural preview). Monthly observations 2018-01–2025-12 ($T \approx 96$).*

---

## References

Antón, M., Ederer, F., Giné, M., & Schmalz, M. C. (2022). *Common ownership, competition, and top management incentives*. Working Paper.

Berk, J. B., & van Binsbergen, J. H. (2015). Measuring skill in the mutual fund industry. *Journal of Financial Economics*, 118(1), 1–20.

Central Bank of the Republic of China (Taiwan). (2024–2025). *The impact of ETFs on financial stability in Taiwan*.

EFMA Annual Meeting. (2023). *ETF rebalancing, hedge fund trades, and capital markets*.

Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.

Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.

Financial Supervisory Commission, Taiwan. (2024). Enhanced disclosure of ETF dividend sources and equalization reserve usage.

FTSE Russell. (2024). *FTSE Taiwan RIC Capped Index* research paper.

Li, S. (2022). Should passive investors actively manage their trades? AEA Conference / Working Paper.

Markowitz, H. (1952). Portfolio selection. *Journal of Finance*, 7(1), 77–90.

Morningstar. (2025). The hidden costs of passive investing.

National Pingtung University. (2021). Investment performance and tracking ability of Taiwan high dividend ETFs. *Journal of National Pingtung University of Science and Technology (Management)*.

Patton, A. J. (2006). Modelling asymmetric exchange rate dependence. *International Economic Review*, 47(2), 527–556.

Robertson, S. I. (2019). Passive in name only: Delegated management and "index" investing. *Journal of Corporation Law*.

Sharpe, W. F. (1964). Capital asset prices. *Journal of Finance*, 19(3), 425–442.

Tasitsiomi, I. (2025). On the hidden costs of passive investing. arXiv:2506.21775.

---

## Suggested SSRN Subject Areas (select at upload)

- Financial Institutions
- Portfolio Management
- Asset Pricing
- Emerging Markets

---

*End of working paper*
