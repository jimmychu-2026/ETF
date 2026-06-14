# Risk Budgeting Curves You Cannot Turn Off: A Unified Framework for Taiwan's Six Most Popular ETFs

**SSRN Working Paper v2.2 — Draft for Upload**

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

Taiwan's retail investors hold six dominant ETFs—0050, 006208, 0056, 00878, 00919, and 00929—as if they were **spot portfolios** of many stocks with cash dividends. We argue the economic object is instead a **spot-wrapped forward**: daily-tradable NAV masks **monthly, quarterly, and annual delivery obligations** embedded in index rules (rebalance rolls), dividend promises ($D_t$), and equalization reserves. This contract structure is isomorphic to historical commodity-forward innovations (e.g., Republican-era Shanghai silk/silver tickets; Tulip forward contracts)—not merely analogous in "bubble rhetoric." We build a **Forward Tenor Stack** ($\sigma_m,\sigma_q,\sigma_y$; basis $B_t$; roll friction $Roll_t$; dividend gap $G_t$) and layer a **risk-budgeting stack** (HHI, MRC, Fama-French, CVaR, equalization). Empirically, 0050's annual return volatility (2018–2025, **23.2%**) is the same order of magnitude as London silver's annual volatility in 1912–1921 (**22.8%**), but the underlying forward is a **TSMC-heavy equity basket** rather than a metal price. High-dividend ETFs add **annual yield-screening forwards** and elevated $G_t$. Robertson (2019) and Li (2022) supply the delegation and roll-cost channels. **Not investment advice**; tenor volatilities are replicated from FinMind prices.

**Keywords:** ETF; Taiwan; spot-wrapped forward; tenor risk; risk budgeting; dividend sustainability; income equalization; index rebalancing

**JEL Classification:** G11, G12, G14, G23

---

## Declaration: Generative AI and AI-Assisted Technologies

During the preparation of this working paper, the author(s) used generative AI tools (including large language models) for **literature organization, English language refinement, section structuring, and cross-referencing prior draft notes**. After using these tools, the author(s) reviewed and edited all content and take full responsibility for the arguments, citations, and limitations stated herein. AI tools were **not** used to fabricate data, regression outputs, or empirical results. No AI tool is listed as an author.

---

## Disclaimer

This working paper is provided for **educational and research purposes only**. It does not constitute investment advice, an offer, or a solicitation. All numerical illustrations are model-based or approximate unless explicitly sourced. Past structure is not indicative of future performance. Readers should conduct their own due diligence and consult qualified professionals before making financial decisions.

---

## 1. Introduction

Over the past decade, Taiwan's ETF market has experienced rapid retail adoption. Six products alone—0050, 006208, 0056, 00878, 00919, and 00929—account for millions of beneficiary accounts and trillions of New Taiwan dollars in assets under management. They anchor retirement planning and " dividend stock " narratives for domestic investors. The Central Bank of the Republic of China (Taiwan) (2024–2025) and the Financial Supervisory Commission (FSC, 2024) have flagged industry concentration, procyclical flows, and dividend-disclosure practices as potential sources of financial stability risk.

Standard finance textbooks assign a clear language to indexed products. Modern Portfolio Theory (MPT) suggests that idiosyncratic risk can be diversified away as holdings increase (Markowitz, 1952). The Capital Asset Pricing Model (CAPM) summarizes systematic exposure with market beta (Sharpe, 1964). Fama and French (1993, 2015) decompose returns into market, size, value, profitability, and investment factors—frameworks widely used to interpret smart-beta and high-dividend strategies.

Yet a growing literature warns that **passive investing is not autonomous investing**. Robertson (2019) shows that " index funds " are a form of **delegated management**: portfolio weights and rebalance timing are outsourced to index providers, not chosen by the end investor. Li (2022) documents that U.S. ETFs tracking publicly announced indices suffer average execution shortfalls of roughly **67 basis points** per reconstitution trade—costs largely invisible in expense-ratio comparisons. Tasitsiomi (2025) and Morningstar (2025) emphasize that mechanical pursuit of zero tracking error can transfer wealth to anticipatory traders. Berk and van Binsbergen (2015) note that discussions of passive management long neglected transaction costs.

Taiwan amplifies global index-concentration trends (FTSE Russell, 2024; Antón et al., 2022). Taiwan Semiconductor Manufacturing Company (TSMC) repeatedly exceeds **60%** of the weight in 0050 and 006208, rendering the " fifty-stock " label misleading for risk purposes. High-dividend ETFs appear more granular at the stock level but may concentrate **factor** and **industry** risk—financials for 00878, shipping and cyclical semiconductors for 00919, and 100% technology for 00929. Dividend marketing further interacts with Taiwan's **income equalization reserve** regime, which FSC (2024) has tightened through enhanced payout-source disclosure.

Prior Taiwan studies examine early high-dividend ETFs (e.g., National Pingtung University, 2021; master's theses comparing CAPM performance pre/post COVID). They rarely place **00919 and 00929** in the same framework as 0050, and rarely combine **MRC, factor attribution, and tail risk** in one comparative design. This working paper fills that gap at the **conceptual and structural** level, proposing testable hypotheses for future full-sample econometrics.

### 1.1 Main thesis

> **Popular Taiwan ETFs are not spot equity baskets; they are spot-wrapped forwards—daily NAV liquidity packaging index delivery schedules, dividend promises, and rebalance rolls that investors cannot refuse.**

Secondary thesis:

> **Retail portfolios built from multiple popular ETFs often repeat the same forward curve rather than achieving diversification—because passive mandates lock month/quarter/year delivery obligations.**

We operationalize " total risk exceeding textbook models " as a failure of **model assumptions**: treating forwards as spot, full diversification, frictionless rebalancing, and autonomous weights.

### 1.2 Contributions

1. **Spot-wrapped forward framework** linking ETFs to commodity-forward contract logic and historical silk/silver benchmarks.
2. **Forward Tenor Stack** with empirical $\sigma_m,\sigma_q,\sigma_y$ (2018–2025) and 1912–1921 silver annual-volatility comparison.
3. **Unified risk-budget map** (HHI, MRC, FF, CVaR, equalization) layered above contract tenors.
4. **Extension to 00919/00929** and dividend-forward gap $G_t$ hypotheses.
5. **Contract-structure channel**: delegated rebalancing + roll implementation shortfall (Li, 2022; Robertson, 2019).

### 1.3 Roadmap

Section 2 presents the Forward Tenor Stack and risk measurement layers. Section 3 profiles the six ETFs. Section 4 discusses delegated control and roll costs. Section 5 covers dividend forwards and equalization. Section 6 addresses portfolio-level overlap. Section 7 concludes with limitations and a replication agenda.

---

## 2. Forward Tenor Stack and Risk Measurement Layers

### 2.0 Spot-wrapped forward: economic definition

An ETF share is **economically** a bundle of:

1. **Spot appearance**: intraday listing, IOPV/NAV, T+ settlement.
2. **Quarterly (or semi-annual) index forward**: mandatory basket delivery on public rebalance dates (FTSE, MSCI, Taiwan Index Co.).
3. **Monthly dividend forward** (high-yield products): promised cash-flow cadence with ex-dividend NAV resets.
4. **Annual screening forward** (00919): rule-based yield filter that redefines next year's deliverable basket.

Investors who would not independently sell a quarterly TSMC add or buy a cyclical shipping name are nonetheless **short the corresponding forward** via index delegation (Robertson, 2019).

**Historical isomorphism (not decorative analogy).** Republican-era silk merchants faced spot silk plus **silver-exchange forwards**; tulip contracts separated spot bulbs from forward claims. Taiwan ETFs institutionalize the same pattern with prospectuses and equalization reserves—making the forward **more liquid and less visibly labeled**.

| Tenor | Republican silk/silver (1912–1921) | Six Taiwan ETFs |
|:------|:-----------------------------------|:----------------|
| Month | Yangli (silver spread); ticket settlement | Ex-div months; premium/discount $B_t$ |
| Quarter | Contract delivery windows | Public index reconstitution; $Roll_t$ |
| Year | London silver σ ≈ **22.8%**; 1920→21 DD ≈ **−40%** | Yield screens; 0050 σ_y ≈ **23.2%** (2018–25) |

### 2.0.1 Forward risk parameters

| Symbol | Meaning | ETF instantiation |
|:-------|:--------|:------------------|
| $\sigma_m,\sigma_q,\sigma_y$ | Monthly / quarterly / annual return vol | FinMind closes, split-adjusted |
| $B_t$ | Basis (market vs NAV) | Premium on high-yield ETFs |
| $Roll_t$ | Roll / rebalance friction | $|Δw|$ on index change days + MI |
| $G_t$ | Dividend forward gap | $(D^{promised}-C^{natural})/NAV$ |
| $\Lambda^{cal}$ | Calendar risk | Known rebalance / ex-div windows |

**Table 2A. Empirical tenor volatility (2018-01–2025-12)**

| ETF | $\sigma_m$ | $\sigma_q$ | $\sigma_y$ | Max DD | Dominant forward |
|:----|----------:|----------:|----------:|-------:|:-----------------|
| 0050 | 5.4% | 10.6% | **23.2%** | −36% | Quarterly FTSE roll |
| 006208 | 5.4% | 10.6% | 24.1% | −35% | Same as 0050 |
| 0056 | 4.8% | 8.1% | 20.9% | −35% | Semi-annual + monthly payout |
| 00878 | 3.7% | 6.3% | 17.3% | −28% | MSCI semi-annual |
| 00919 | 4.1% | 7.1% | 16.5% | −32% | **Annual yield screen** |
| 00929 | 3.9% | 6.7% | 15.7% | −32% | Tech basket + monthly |

*Source: `code/compute_forward_horizon_risk.py`; silver benchmark: `output/silk_silver/summary_1912_1921.json`.*

**Interpretation.** Annual volatilities of 0050 and 1912–1921 silver are **similar in magnitude** at the year tenor; the difference is the **deliverable asset** (TSMC-forward basket vs metal forward) and the **depth of packaging** (regulated NAV vs merchant tickets).

**Table 2B. H6 calendar-risk pilot (2018–2025)**

| ETF | Rebal-window vol ratio | Ex-div month vol ratio | Notes |
|:----|----------------------:|------------------------:|:------|
| 0050 | **1.13** | 1.01 | Quarterly FTSE roll |
| 0056 | 0.77 | **1.80** | Monthly dividend forward |
| 00929 | 0.64 | **1.42** | Monthly tech yield |

*Source: `code/compute_h6_event_study.py`. Rebalance months are calendar proxies; issuer EQ_ratio needed for true $G_t$.*

### 2.1 Risk layers above contracts

Risk should be evaluated in layers; no single statistic suffices.

| Layer | Tools | Question answered |
|:-----:|:------|:------------------|
| 0 | $\sigma_m,\sigma_q,\sigma_y$, $B_t$, $Roll_t$, $G_t$ | Which forward tenors bite? |
| 1 | Expected return, TER, tracking error | Are fees low? |
| 2 | σ, β, Σ, **MRC** | Who drives volatility? |
| 3 | FF3/FF5 exposures | Factor bets, not alpha? |
| 4 | VaR, **CVaR**, tail dependence λ_L | Crisis behavior? |
| 5 | Equalization, flows, public calendars | When do forwards fail to deliver? |

### 2.2 Concentration: HHI

For portfolio weights \(w_i\):

\[
HHI = \sum_{i=1}^{n} w_i^2
\]

| ETF | Max single weight | HHI (empirical)* | Eff. N (=1/HHI) | Interpretation |
|:----|:------------------|:-----------------|:----------------|:---------------|
| 0050 / 006208 | **57.2%** (TSMC, 2330) | **0.342** | 2.9 | Far above " effective diversification " heuristics (HHI < 0.10) |
| 0056 | **9.3%** | **0.064** | 15.6 | Stock-level dispersion; factor/industry clustering remains |
| 00878 | **10.5%** (Quanta, 2382) | **0.046** | 21.5 | Moderate stock HHI; financial factor concentration |
| 00919 | **12.2%** (Cathay Fin., 2882) | **0.064** | 15.6 | Top-heavy financials; high turnover of high-yield names |
| 00929 | **12.7%** (UMC, 2303) | **0.050** | 20.2 | Stock HHI moderate; **industry HHI → 1** (technology) |

\***Table source:** Appendix A. 0050/0056 from Yuanta PCF weights + FinMind trading-date validation; 006208 proxied from 0050; 00878 from Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN); 00919/00929 from Pocket.tw ETF holdings API (DtNo 59449513, M722), equity rows only.

When \(w_{TSMC} > 0.60\), the squared-weight term alone is \(0.36\). MPT's idiosyncratic-risk elimination through breadth ** fails **: the product behaves as a leveraged single-name proxy, not a fifty-stock portfolio.

### 2.3 Marginal risk contributions

Portfolio volatility: \(\sigma_p = \sqrt{w^\top \Sigma w}\).

\[
MRC_i = w_i \cdot \frac{(\Sigma w)_i}{\sigma_p}, \quad RC_i = \frac{MRC_i}{\sum_j MRC_j}
\]

**Illustrative 0050 decomposition** (assuming \(w_{TSMC}=0.60\), \(\sigma_{TSMC}=25\%\), \(\sigma_{p}=18\%\), \(\rho_{TSMC,p}=0.85\)):

| Component | Weight | Risk contribution \(RC_i\) |
|:----------|:-------|:---------------------------|
| TSMC | 60% | **72%–82%** |
| Other 49 names | 40% | 18%–28% |

This aligns with public narratives that TSMC accounts for roughly **75%–80%** of 0050 risk. When \(\rho\) or \(\sigma_{TSMC}\) rises, \(RC_{TSMC}\) scales ** nonlinearly **.

For **00929**, industry-level technology weight ≈ 100% ⇒ industry \(RC_{Tech} \approx 100\%\). Stock count does not hedge industry systematic shocks.

### 2.4 CAPM and factor models

\[
R_{p,t} - R_{f,t} = \alpha_p + \beta_{MKT}(R_{M,t}-R_{f,t}) + s_p SMB_t + h_p HML_t + \epsilon_{p,t}
\]

**Expected sign pattern (hypotheses for future regression):**

| ETF | β_MKT | SMB | HML | Interpretation |
|:----|:------|:----|:----|:---------------|
| 0050 / 006208 | ≈1 | Low | Low | Market proxy; TSMC idiosyncrasy embedded in " market " |
| 0056 | + | Mid | **+** | Dividend screen ≈ value exposure |
| 00878 | + | Low | Mid | ESG + **financial sector** channel |
| 00919 | + | Mid | **+** | High-yield cyclicals (shipping, mature semis) |
| 00929 | + | **+** | Low/Mid | Technology SMB lock-in |

**Factor stripping (not stock-picking alpha):** High-dividend rules mechanically tilt toward HML and cyclical sectors. Rolling 36-month FF regressions with Newey-West errors can test whether \(\alpha_p \approx 0\) while \(h_p > 0\).

### 2.5 Tail risk

In crises, correlations surge (tail dependence; Patton, 2006). **CVaR** (expected shortfall) better captures capital-at-risk than variance alone.

**Relative tail ranking (illustrative):**

| ETF | CVaR tier | Primary driver |
|:----|:----------|:---------------|
| 00919 | **Highest** | Shipping / high-volatility semis + payout expectations |
| 0050 / 006208 | High | TSMC single-name tail |
| 00929 | High | Tech SMB + liquidity discount |
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

**Key distinction:** 0050 fails at **stock** concentration; 00929 fails at **industry** concentration; 00878 fails at **factor** (financial) concentration despite similar stock counts.

---

## 4. Delegated Management and Hidden Costs

### 4.1 Passive in name only

Robertson (2019) argues index investing transfers ** stock selection, weighting, and rebalance timing ** to index creators—often unregulated relative to fund managers. Investors cannot:

- Underweight TSMC when valuation stretches;
- Exit cyclical high-yield sectors before index reconstitution;
- Avoid forced buys of newly added momentum names.

We label the composite friction ** implementation shortfall of delegated rebalancing **, decomposable as:

\[
\text{Total friction} \approx TE + MI + OC
\]

| Symbol | Meaning | Taiwan ETF context |
|:-------|:--------|:-------------------|
| **TE** | Tracking error | Smart-beta high-dividend ETFs: ~0.5–1.5% vs ~0.1–0.3% for 0050 |
| **MI** | Market impact on rebalance days | Public index changes; front-running (Li, 2022; EFMA, 2023) |
| **OC** | Opportunity cost | Cannot reduce hot factors; 0050 must add TSMC at peaks |

Li (2022) finds **67 bps** average execution shortfall for mechanical U.S. ETF reconstitutions—** ~3× ** comparable institutional trades. Tasitsiomi (2025) reports hundreds of bps in stylized models when managers prioritize zero tracking error at the close. These costs are ** absent ** from CAPM and from TER league tables.

### 4.2 0050 vs 006208

Both track the same FTSE Taiwan 50 index. Performance differences should approximate **−ΔTER** absent skill. Any claimed " manager alpha " between them is economically suspect; choose on liquidity, premium/discount, and fees.

---

## 5. Dividend Forwards, NAV Accounting, and Equalization Reserves

High-yield ETFs market **monthly cash cadence**—economically a **short-dated dividend forward** sold at NAV. When natural income $C_t$ falls short of promised distributions $D_t$, the gap $G_t=(D_t-C_t)/NAV_t$ is bridged by equalization (borrowing from future subscribers) until flows stop (Financial Supervisory Commission, 2024).

### 5.1 Ex-dividend identity

\[
NAV_{ex} = NAV_{cum} - D
\]

Distributions ** reduce ** NAV one-for-one. Total return = price return + reinvested dividends. ** No free cash flow is created ** by announcing a higher payout rate.

### 5.2 Equalization sustainability

Let \(F_t\) = equalization reserve balance, \(N_t\) = net subscriptions, \(C_t\) = natural dividend income from holdings, \(D_t\) = total distribution.

\[
F_{t+1} = F_t + N_t \cdot k + C_t - D_t
\]

When \(N_t \to 0\) (AUM saturation) and \(C_t < D_t\) (promised yield exceeds underlying cash), ** cuts to stated yield or reserve depletion ** follow. FSC (2024) mandates payout ordering: underlying dividends and capital gains first, equalization last—with enhanced disclosure.

| ETF type | Sustainability risk | Mechanism |
|:---------|:--------------------|:----------|
| 0056 | Medium | Mature high-yield names; \(C_t\) relatively stable |
| 00878 | Medium | Financial dividends sensitive to rates/regulation |
| 00919 | **High** | High-yield screen + sector rotation; \(D_t\) vs \(C_t\) gap |
| 00929 | **Med-high** | Low natural tech yields; relies more on reserves/gains |

---

## 6. Portfolio-Level Illusion: Holding " Many " Popular ETFs

Consider: **50% 0050 + 30% 00929 + 20% 00919**.

- 0050 and 00929 ** overlap in technology ** ⇒ effective independent assets < 3.
- 00919 shares ** HML / dividend-factor ** exposure with 0056 and 00878.
- The bundle remains in the subspace ** " Taiwan equity + high-yield cyclicality " **—not multi-asset diversification.

**Risk-budget ranking (composite score, illustrative):**

00919 > 00929 ≈ 0050/006208 > 0056 > 00878 (tail/factor dimensions; 00878 looks calm in calm times).

---

## 7. Conclusion

Taiwan's six dominant ETFs are ** not interchangeable ** forward packages. Marketing labels—" fifty stocks, " " high dividend, " " ESG, " " technology income "—map to distinct ** delivery schedules and risk-budget curves ** that passive mandates lock in:

1. **0050/006208:** TSMC idiosyncratic dominance (HHI, MRC).
2. **0056/00919:** Value/dividend cyclicality (FF HML; shipping/semiconductor cycles).
3. **00878:** Financial tail dependence in crises.
4. **00929:** Pure technology SMB/industry risk despite stock-level dispersion.

Standard models are not " wrong " mathematically; their ** assumptions ** fail when forwards are priced as spot—under delegated, concentrated, roll-friction, and dividend-gap constraints. Total investor risk exceeds mean-variance summaries when we add **tenor structure**, concentration, factor overlap, tail co-movement, implementation shortfall, and forward payout failure.

### 7.1 Limitations

- **v2.2 update:** Forward tenor volatilities + **H6 pilot** (0050 rebalance vol ratio 1.13; 0056 ex-div month 1.80; 00929 ex-div month 1.42). True \(G_t\) requires issuer equalization-share disclosure (H6d).
- **v2.1:** Appendix A empirical HHI from public PCF pipelines.
- MRC, FF, and CVaR remain ** structural / illustrative ** pending full-sample econometrics.

### 7.2 Replication agenda

1. Rebalance / ex-div **event windows** for \(\sigma_q\), \(\sigma_m\) (H6a–b).
2. Monthly HHI and MRC from Ledoit-Wolf \(\Sigma\).
3. FF3/FF5 regressions with Newey-West errors (2018–2025).
4. CVaR and crash-month conditional returns.
5. Panel on \(G_t\), \(EQ\_ratio\), flows, and premium/discount (H5–H6d).
6. Re-run: `py code/compute_forward_horizon_risk.py` and `py code/parse_silk_silver_1912_1921.py`.

---

## Appendix A — Empirical HHI from FinMind and Public PCF Weights

**Data pipeline:** Python script `code/compute_hhi_finmind.py` (FinMind API `TaiwanStockPrice` / `TaiwanStockInfo`; Yuanta PCF NUXT parser; Cathay cwapi; Pocket.tw holdings API).  
**Price validation date (FinMind):** 2026-06-08. **PCF posting dates:** Yuanta 2026-06-08; Cathay 2026-06-09; Pocket 2026-06-08.

**Table A1. Herfindahl-Hirschman Index — six popular Taiwan ETFs**

| ETF | N (reported) | Max weight (name / ID) | Max wt (%) | HHI | Eff. N | Wt sum (%) |
|:----|-------------:|:-----------------------|-----------:|----:|-------:|-----------:|
| **0050** | 36 | TSMC (2330) | 57.2 | **0.3422** | 2.9 | 92.9 |
| **006208** | 36 | TSMC (2330) | 57.2 | **0.3422** | 2.9 | 92.9 |
| **0056** | 39 | top name (9.3%) | 9.3 | **0.0643** | 15.6 | 81.9 |
| **00878** | 30 | Quanta (2382) | 10.5 | **0.0464** | 21.5 | 96.3 |
| **00919** | 58 | Cathay Fin. (2882) | 12.2 | **0.0640** | 15.6 | 98.1 |
| **00929** | 50 | UMC (2303) | 12.7 | **0.0496** | 20.2 | 98.5 |

**Method.** \(HHI = \sum_i w_i^2\) with \(w_i\) in decimal form. For 0050 and 0056, weights are taken from Yuanta's public PCF pages (embedded NUXT payload). FinMind confirms the latest Taiwan trading session. 006208 tracks the same FTSE Taiwan 50 index as 0050 and inherits 0050 weights. For 00878, weights come from Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN). For 00919 and 00929, equity constituent weights are taken from Pocket.tw ETF holdings API (DtNo 59449513, MajorTable M722), which mirrors issuer PCF disclosures; cash, margin, and futures legs are excluded.

**Replication.** Re-run: `py code/compute_hhi_finmind.py` → outputs `output/hhi_finmind.csv` and `output/appendix-a-hhi-finmind.md`.

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

Robertson, S. I. (2019). Passive in name only: Delegated management and " index " investing. *Journal of Corporation Law*.

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
