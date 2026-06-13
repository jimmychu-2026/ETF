# Appendix A — Empirical HHI (FinMind + PCF / Index Weights)

**FinMind:** `TaiwanStockPrice` trading date & `TaiwanStockInfo` names  
**Generated:** 2026-06-09 17:35  

**Table A1. Herfindahl-Hirschman Index across six popular Taiwan ETFs**

| ETF | N (reported) | Max weight | Max wt (%) | HHI | Eff. N | Wt sum (%) |
|:----|-------------:|:-----------|-----------:|----:|-------:|-----------:|
| **0050** | 36 | 台積電 (2330) | 57.2 | **0.3422** | 2.9 | 92.9 |
| **006208** | 36 | 台積電 (2330) | 57.2 | **0.3422** | 2.9 | 92.9 |
| **0056** | 39 | ku (kE) | 9.3 | **0.0643** | 15.6 | 81.9 |
| **00878** | 30 | 廣達 (2382) | 10.5 | **0.0464** | 21.5 | 96.3 |
| **00919** | 58 | 國泰金 (2882) | 12.2 | **0.0640** | 15.6 | 98.1 |
| **00929** | 50 | 聯電 (2303) | 12.7 | **0.0496** | 20.2 | 98.5 |

**Method.** $HHI = \sum_i w_i^2$ where $w_i$ are portfolio weights (%/100). For Yuanta ETFs (0050, 0056), weights are extracted from public PCF pages (NUXT payload). FinMind supplies the latest Taiwan trading session (`TaiwanStockPrice`, date above) for pipeline validation. 006208 tracks the same index as 0050 (FTSE Taiwan 50) and uses 0050 weights. 00878 uses Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN). 00919/00929 use Pocket.tw ETF holdings API (DtNo 59449513, MajorTable M722), which mirrors issuer PCF constituent weights (equity rows only; cash/margin/futures excluded).

**Data sources by row**

- **0050:** Yuanta PCF (NUXT weights). residual bucket 7.1%
- **006208:** Proxy: same FTSE Taiwan 50 as 0050. residual bucket 7.1%; automated PCF incomplete—see Appendix notes
- **0056:** Yuanta PCF (NUXT weights). residual bucket 18.1%
- **00878:** Cathay cwapi GetIndexStockWeights (FundCode=CN, PCF posting date in payload). residual bucket 3.7%
- **00919:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 1.9%
- **00929:** Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF). residual bucket 1.5%
