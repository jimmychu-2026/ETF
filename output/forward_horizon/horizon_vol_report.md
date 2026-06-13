# Forward-horizon return volatility (ETF)

Window: **2018-01-01** – **2025-12-31** (FinMind `TaiwanStockPrice` close-to-close).

| ETF | σ monthly | σ quarterly | σ annual | Max DD | n months |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 0050 | 5.39% | 10.56% | 23.19% | -36.38% | 96 |
| 006208 | 5.41% | 10.58% | 24.10% | -35.05% | 96 |
| 0056 | 4.77% | 8.14% | 20.87% | -35.47% | 96 |
| 00878 | 3.70% | 6.26% | 17.26% | -27.58% | 66 |
| 00919 | 4.11% | 7.15% | 16.50% | -31.91% | 39 |
| 00929 | 3.91% | 6.65% | 15.68% | -31.83% | 31 |

**Interpretation (spot-forward packaging):**
- Monthly σ ≈ dividend / ex-date noise tenor.
- Quarterly σ ≈ index rebalance roll tenor (FTSE / MSCI / TIC calendars).
- Annual σ ≈ screening / methodology forward (high-dividend rules).
