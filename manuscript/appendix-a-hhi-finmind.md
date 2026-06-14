# Appendix A — Empirical HHI (FinMind + PCF / Index Weights)

**FinMind:** `TaiwanStockPrice` trading date & `TaiwanStockInfo` names  
**Generated:** 2026-06-09 17:35  

**Table A1. Herfindahl-Hirschman Index across six popular Taiwan ETFs**

| ETF | HHI | Eff. N | Max weight |
|---|---:|---:|---:|
| 0050 | 0.3505 | 2.85 | TSMC 58.0% |
| 006208 | 0.3505 | 2.85 | TSMC 58.0% |
| 0056 | 0.0588 | 17.01 | ku / top name 9.3% |
| 00878 | 0.0460 | 21.73 | Quanta 10.6% |
| 00919 | 0.0733 | 13.64 | Cathay Fin. 13.1% |
| 00929 | 0.0509 | 19.64 | UMC 13.4% |

**Method.** $HHI = \sum_i w_i^2$ where $w_i$ are portfolio weights (%/100). For Yuanta ETFs (0050, 0056), weights are extracted from public PCF pages (NUXT payload). FinMind supplies the latest Taiwan trading session (`TaiwanStockPrice`, date above) for pipeline validation. 006208 tracks the same index as 0050 (FTSE Taiwan 50) and uses 0050 weights. 00878 uses Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN). 00919/00929 use Pocket.tw ETF holdings API (DtNo 59449513, MajorTable M722), which mirrors issuer PCF constituent weights (equity rows only; cash/margin/futures excluded).

**Simple replication code**

```python
import pandas as pd

df = pd.read_csv("output/hhi_finmind.csv")
print(df[["ticker", "as_of_date", "hhi", "eff_n", "max_weight_name"]])
```

**Covariance matrix example**

```python
import pandas as pd

df = pd.read_csv("output/hhi_finmind.csv")
pivot = df.pivot(index="as_of_date", columns="ticker", values="hhi")
print(pivot.cov())
```

**Data sources by row**

- **0050:** Yuanta PCF (NUXT weights). residual bucket 7.1%
- **006208:** Proxy: same FTSE Taiwan 50 as 0050. residual bucket 7.1%; automated PCF incomplete—see Appendix notes
- **0056:** Yuanta PCF (NUXT weights). residual bucket 18.1%
- **00878:** Cathay cwapi GetIndexStockWeights (FundCode=CN, PCF posting date in payload). residual bucket 3.7%
- **00919:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 1.9%
- **00929:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 1.5%
