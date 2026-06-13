# 台灣六大熱門 ETF 風險結構與配息可持續性：學術論文藍圖

> **文件用途**：將 `ETF.md` / `analyze-ETF.md` / SSRN 工作論文轉化為可投稿的學術研究架構。  
> **敘事主軸（不可偏離）**：六大 ETF 經濟本質為 **「包裝成現貨的遠期／期貨」**——日交易 NAV 是現貨外觀，投資人實際承擔月／季／年**指數交割、配息承諾、再平衡展期**義務（與民國生絲／標金、鬱金香合約同構）。  
> **建議標題（中）**：包裝成現貨的遠期：台灣熱門 ETF 之期限風險、集中度與配息可持續性  
> **建議標題（英）**：Spot-Wrapped Forwards: Tenor Risk, Concentration, and Dividend Sustainability in Taiwan's Popular ETFs  
> **SSRN 主檔**：`manuscript/SSRN-Taiwan-ETF-Risk-Budgeting.md`（**v2.2**，Forward Tenor Stack + 期限波動實證）  
> **最後更新**：2026-06-09（主軸對齊 `ETF.md`；新增 $\sigma_m/\sigma_q/\sigma_y$ 與 1912–1921 銀價年 tenor 對照）

---

## 零、中文摘要（Executive Summary）

### 0.1 研究主旨

台灣散戶將 0050、006208、0056、00878、00919、00929 六檔 ETF 視為「分散＋配息」的現貨工具，但其經濟本質是 **把指數與配息遠期包裝成每日可交易的 NAV**（spot-wrapped forward）。本文先建立 **Forward Tenor Stack**（月／季／年期限風險：$\sigma_m,\sigma_q,\sigma_y$、基差 $B_t$、展期 $Roll_t$、配息缺口 $G_t$），再疊加風險預算分解：HHI、MRC、Fama-French、CVaR 與**收益平準金**。核心命題：被動 ETF 的總風險不僅來自股價方差，更來自**外生交割日程與遠期現金流承諾**——使均值–方差在「充分分散、權重自主、無展期摩擦」假設下系統性失效。1912–1921 倫敦銀價年波動（σ≈23%）與 0050 年波動（2018–2025，σ≈23%）在**年 tenor** 上同級，印證歷史「標金遠期」與現代「台積電籃子遠期」的結構可比性。

### 0.2 主要發現（截至 SSRN v2.1，PCF 2026-06-08／08）

| 層次 | 0050／006208 | 0056 | 00878 | 00919 | 00929 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **個股 HHI** | **0.342**（Eff. N≈2.9） | 0.064 | 0.046 | **0.064** | 0.050 |
| **成分檔數 N** | 36 | 39 | 30 | **58** | 50 |
| **最大單一權重** | 台積電 **57.2%** | 9.3% | 廣達 **10.5%** | 國泰金 **12.2%** | 聯電 **12.7%** |
| **權重加總（%）** | 92.9 | 81.9 | 96.3 | 98.1 | 98.5 |
| **主導風險來源** | 台積電 idiosyncratic | 價值／高息因子 | 金融＋ODM 頭部集中 | 金融股頭部＋高換股 | 科技 SMB；**產業 HHI→1** |
| **配息機制** | 低 | 平準金依賴 | 平準金＋金融股股息 | 高換股＋平準金 | 科技股息＋成長股 |

**相對 v2 估算版的重要修正**：00919／00929 原以 max-weight + equal-tail 假設（最大權重 ~10%／~6%），完整 PCF 顯示頭部集中**明顯更高**——00919 HHI 由 0.027 升至 **0.064**（與 0056 同級）；00929 最大權重由 ~6% 修正為聯電 **12.7%**，HHI 由 0.022 升至 **0.050**。00878 HHI 由 0.025 升至 **0.046**（廣達 10.5%）。**H1b 仍成立**（0050 HHI 遠高於其餘五檔），但高息組內部排序需重述：00919 個股集中度不低於 0056。

**資料來源（六檔皆為可重現公開管線，無需手動蒐集權重）**：

| ETF | 來源 | 備註 |
| :--- | :--- | :--- |
| 0050／0056 | 元大 PCF 頁 NUXT payload | FinMind 驗證交易日 |
| 006208 | 沿用 0050 | 同 FTSE Taiwan 50 |
| 00878 | 國泰 `cwapi` `GetIndexStockWeights`（FundCode=CN） | 官網 SPA 背後之 JSON API |
| 00919／00929 | Pocket.tw 持股 API（DtNo 59449513，MajorTable M722） | 鏡像投信 PCF「持股明細」；僅股票列，排除現金／保證金／期貨 |

**權重加總 <100% 之 residual bucket**（非「未公開成分」）：0050／0056 差額多為現金／申贖緩衝；00919／00929 約 1.5–2% 為刻意排除之非股票部位；00878 約 3.7% 為現金等。HHI 比較以已揭露之個股權重為準，殘差對橫截面排序影響有限。

**政策與投資者教育意涵**：六檔 ETF 對應**不可互換的風險預算曲線**——0050 是「單一標的代理」（Eff. N≈3）而非五十檔分散組合；00929 個股 HHI 中等但產業集中度趨近 100%；00919「高息分散」敘事在個股層面並不成立（58 檔中金融股頭部權重逾 12%）。高宣告配息率不創造增量財富，僅重分配 NAV，且在淨申購放緩時可能依賴平準金（金管會，2024）。

### 0.3 方法與邊際貢獻

1. **理論**：提出 **Spot-Wrapped Forward** 框架，將 ETF 與商品遠期／民國標金、指數期貨之期限結構置於同一 Layer 0。  
2. **方法**：六檔 ETF 之 **HHI–MRC–FF5–CVaR–Tenor** 五層堆疊＋平準金面板（H5）＋遠期配息缺口（H6）。  
3. **實證**：**00919／00929** 空白補足；**2018–2025** 月／季／年 σ 實證（`compute_forward_horizon_risk.py`）。  
4. **歷史對照**：1912–1921 銀價年 tenor 與 0050 年 σ 同級，支撐 `ETF.md` §五歷史同構。  
5. **制度**：$EQ\_ratio$、Flow、Discount 作為遠期交割失敗之預警指標。

### 0.4 完成度對照（SSRN v2 → 期刊版）

| 項目 | SSRN v2 現況 | 期刊投稿最低門檻 |
| :--- | :--- | :--- |
| HHI 實證表 | ✅ Appendix A（六檔完整 PCF；00878 cwapi、00919／00929 Pocket.tw） | 六檔 PCF **時間序列**（月／季面板） |
| MRC／CVaR | 結構／示意 | Ledoit-Wolf $\Sigma$ + 全樣本估計 |
| FF5 回歸 | 假說與預期符號 | Table 3 完整係數 + Newey-West |
| 平準金 H5 | 制度描述 | Panel logit + FE（Table 6） |
| Robustness | 列於 Limitations | 至少 2 項（COVID 子樣本、FF3 vs FF5 等） |
| 語氣 | Working paper + AI 聲明 | 中性學術語、無示意標籤 |

**可重現腳本**：`code/compute_hhi_finmind.py` → `output/hhi_finmind.csv`、`output/appendix-a-hhi-finmind.md`。

### 0.5 版本路徑

| 版本 | 內容 | 狀態 |
| :--- | :--- | :--- |
| v1 | 框架 + 示意 HHI | 已完成 |
| **v2** | FinMind + Yuanta PCF 實證 HHI（0050／0056；三檔 equal-tail 估算） | 已取代 |
| **v2.1** | 六檔完整 PCF HHI | 已取代 |
| **v2.2** | **Forward Tenor Stack** + $\sigma_m/\sigma_q/\sigma_y$ 實證 + 歷史年 tenor 對照 | **目前** |
| v3（規劃） | FF3/FF5 回歸 + $G_t$／$B_t$ 面板 | 待 TEJ／FinMind |
| 期刊版 | Table 1–7 全填 + Discussion | 依 §十一 時程 |

### 0.6 2026-06 實證管線更新摘要

**已完成**

1. **HHI 橫截面實證（H1 之一）**：六檔 ETF 皆由公開 PCF／鏡像 API 自動取權重，腳本 `code/compute_hhi_finmind.py` 一鍵重跑。
2. **探測結論（無需再手動找權重）**：
   - 臺灣指數公司網站 NUXT **無**可解析成分權重（IX0179 等）。
   - 群益 `buyback`／`navPart` API 一律 HTTP 500；`items` 僅 ETF 清單。
   - 復華 `ETFPcf` API 持股陣列為空；Pocket.tw 與 PCF 頁 network 請求一致。
3. **產出物**：`output/hhi_finmind.csv`、`output/appendix-a-hhi-finmind.md`；文稿 `manuscript/SSRN-Taiwan-ETF-Risk-Budgeting.md` §2.1、Appendix A 已同步。

**待做（期刊版）**

- HHI **時間序列**（月／季 rebalance 面板）。
- MRC、FF5、CVaR 全樣本估計（v3）。
- 00919／00929 若審稿要求，可附群益／復華官網 PCF PDF 作交叉驗證（非重算必要步驟）。

**投稿披露建議**：00919／00929 註明資料取自 Pocket.tw 公開 API（DtNo 59449513），對照日 2026-06-08，與投信 PCF 持股明細一致；00878 註明 Cathay cwapi 與 PCF 公布日。

---

### 1.1 核心研究問題（Research Questions）

| 編號 | 問題 |
| :--- | :--- |
| **RQ1** | 名義成分分散的高股息／Smart Beta ETF，是否在**因子維度與尾部風險**上比 0050 更分散？ |
| **RQ2** | 0050／006208 的波動與 CVaR 是否主要由台積電的邊際風險貢獻（MRC）所驅動？ |
| **RQ3** | 高股息 ETF（0056、00878、00919、00929）的超額報酬是否可被 Fama-French 因子解釋（即 α 不顯著）？ |
| **RQ4** | 收益平準金依賴度與淨申購放緩，是否預測配息率下修或折溢價擴大？ |
| **RQ5** | 00919／00929 等新興高息 ETF 的因子結構是否較傳統 0056／00878 更偏週期性與尾部風險？ |
| **RQ6** | 若將 ETF 視為 spot-wrapped forward，**月／季／年 tenor** 是否呈現不同風險排序？高息 ETF 之 **$G_t$（配息遠期缺口）** 是否預測配息下修與折價？ |

### 1.2 邊際貢獻（Contribution Statement）

1. **理論貢獻**：**Spot-wrapped forward** 將 ETF、指數期貨、商品遠期與民國標金置於同一契約語言。  
2. **方法貢獻**：**Forward Tenor Stack**（$\sigma_m,\sigma_q,\sigma_y,B_t,Roll_t,G_t$）+ HHI–MRC–FF5–CVaR 同一樣本分解。  
3. **實證貢獻**：00919／00929 空白；**年 σ≈23%** 與 1912–1921 銀價同級之跨世紀對照。  
4. **制度貢獻**：平準金、Flow、折溢價作為**遠期交割失敗**之可檢驗變數（H5–H6）。

### 1.3 與既有文獻的差異（必寫進 Introduction 末段）

| 既有研究 | 缺口 | 本文填補 |
| :--- | :--- | :--- |
| 屏東大學（2021）高股息 ETF 績效 | 樣本未含 00919／00929；未做 MRC／CVaR | 擴充樣本 + 風險預算 |
| 碩論 COVID 前後 CAPM | 僅 CAPM + Sharpe | 升級為 FF5 + 尾部 |
| 央行 ETF 風檢報告 | 政策描述、無計量檢驗 | 可檢驗假說 + 估計值 |
| Li（2022）ETF 再平衡成本 | 美國市場、非台灣 six-ETF 比較 | 引用為理論基礎，TE 作為控制變數 |
| FTSE Capped Index 白皮書 | 指數設計，非 ETF 實證 | 0050 uncapped 集中度實證 |

---

## 二、五項可檢驗假說（Hypotheses）

### H1：個股集中度與 MRC 假說

> **H1a**：0050／006208 之台積電邊際風險貢獻佔比（$RC_{TSMC}$）在 2020–2025 顯著高於 50%。  
> **H1b**：0050 之 HHI 顯著高於 0056、00878、00919、00929（名義分散 ETF）。

- **預期符號**：$RC_{TSMC} > 0.50$；$HHI_{0050} > HHI_{others}$
- **檢驗方法**：每月以成分股日報酬估計 $\Sigma$（Ledoit-Wolf 收縮），計算 MRC；HHI 以公開成分權重計算
- **對立假說**：若 TSMC 權重下降或波動率結構改變，$RC_{TSMC}$ 可能下降但仍 > 50%

### H2：因子暴露假說（Fama-French）

> **H2a**：高股息 ETF 組（0056、00878、00919）之 HML 因子載荷 $h_p$ 顯著為正。  
> **H2b**：00929 之 SMB 載荷 $s_p$ 顯著為正，且 HML 不顯著或低於 00919。  
> **H2c**：六檔 ETF 之 Jensen's α 在 FF5 控制後**不顯著異於零**。

- **預期符號**：$h_p > 0$（高息組）；$s_p > 0$（00929）；$\alpha_p = 0$
- **檢驗方法**：月超額報酬對 TW FF3／FF5 因子回歸（Newey-West 標準誤，lag=3）
- **理論依據**：Fama & French (1993, 2015)；高股息篩選 ≈ value／dividend yield exposure

### H3：尾部風險假說

> **H3a**：00919 之 5% CVaR（月）絕對值顯著大於 00878。  
> **H3b**：00878 在「市場大跌月」（TAIEX 月報酬 < −5%）之條件報酬，顯著差於 0056（金融尾部共振）。  
> **H3c**：00929 與 0050 之下尾相依係數 $\lambda_L$ 高於 00878 與 TAIEX 之下尾相依。

- **預期符號**：$|CVaR_{00919}| > |CVaR_{00878}|$；$R_{00878}|_{crash} < R_{0056}|_{crash}$
- **檢驗方法**：Historical simulation CVaR；條件均值差異 t 檢定；Clayton copula 或 empirical $\lambda_L$

### H4：追蹤誤差與費率假說（006208 vs 0050）

> **H4**：006208 與 0050 追蹤同一指數，其超額報酬差異 $\alpha_{006208} - \alpha_{0050}$ 應統計上等同於 $-(TER_{006208} - TER_{0050})$ 的量級，而非顯著選股能力差異。

- **預期符號**：$\alpha_{diff} \approx -\Delta TER$
- **檢驗方法**：配對樣本 t 檢定；差分回歸

### H5：收益平準金可持續性假說

> **H5a**：配息中「平準金佔比」$EQ\_ratio_t = D^{eq}_t / D^{total}_t$ 越高，下一期配息率下修機率越高。  
> **H5b**：淨申購轉負（$Flow_t < 0$）後，高 $EQ\_ratio$ 的 ETF 出現較大折價（$Discount_t < 0$）。

- **預期符號**：$\partial \Delta Yield / \partial EQ\_ratio > 0$（下修）；$Flow < 0 \Rightarrow Discount \downarrow$
- **檢驗方法**：Panel logit（配息下修）+ panel FE 回歸（折溢價）
- **資料來源**：各 ETF 公開月報／配息公告／證交所折溢價

### H6：遠期期限與配息遠期缺口假說（**v2.2 新增**）

> **H6a**：六檔 ETF 之 $\sigma_q$（季報酬波動）在再平衡窗（季末 ±10 交易日）顯著高於非再平衡窗。  
> **H6b**：高息組（0056、00919、00929）之 $\sigma_m$ 在除息月顯著高於非除息月（$G_t$ 顯性化）。  
> **H6c**：0050 之 $\sigma_y$ 與 1912–1921 倫敦銀價年波動同階（~20–25%），但驅動因子為 TSMC 權重遠期而非商品價。  
> **H6d**：$G_t = (D^{promised}_t - C^{natural}_t)/NAV_t$ 越高，下一季 $EQ\_ratio$ 上升與配息下修機率越高。

- **預期符號**：$\sigma_{q,rebal} > \sigma_{q,other}$；$\partial EQ\_ratio / \partial G_t > 0$
- **檢驗方法**：事件研究（rebalance／ex-div 窗）；$G_t$ 由配息公告與成分股息推算
- **實證現況（已完成）**：2018–2025 $\sigma_m,\sigma_q,\sigma_y$ + **H6 pilot**（0050 rebal 1.13×；0056 ex-div **1.80×**；00929 ex-div **1.42×**）。銀價 σ 見 `output/silk_silver/`。
- **待做**：指數公司精準生效日重跑 H6a；投信 **EQ_ratio** → 真 $G_t$（H6d）。

---

## 三、論文大綱（Academic Outline）

```
1. Introduction
   1.1 Motivation（台灣 ETF 規模、零售化、高息熱潮）
   1.2 Spot-Wrapped Forward Thesis（ETF = 現貨外觀 + 月/季/年遠期義務）
   1.3 Research Questions & Hypotheses（含 RQ6 / H6）
   1.4 Contributions
   1.5 Structure

2. Literature Review
   2.1 Commodity Forwards, Futures, and Contract Innovation（鬱金香、標金）
   2.2 Index Concentration and Effective Number of Stocks
   2.3 ETF Microstructure: Tracking Error, Roll/Rebalance Costs（Li 2022）
   2.4 Factor Models and Smart Beta / High-Dividend Products
   2.5 Tail Risk and Dependence in Equity Portfolios
   2.6 Dividend Policy, Equalization Reserves, and Taiwan Regulatory Context
   2.7 Hypothesis Development

3. Data and Methodology
   3.1 Sample: Six ETFs, TAIEX, Risk-Free Rate, FF Factors; 1912–1921 Silver（對照）
   3.2 Variable Construction
       - Forward Tenor: σ_m, σ_q, σ_y, B_t, Roll_t, G_t, Λ^cal
       - HHI, Effective N, Industry HHI
       - MRC / Component VaR
       - FF3 / FF5 Time-Series Regressions
       - CVaR, Tail Dependence
       - EQ_ratio, Flow, Discount
   3.3 Estimation Details
   3.4 Summary Statistics（Table 1 + Table 1A Tenor Vol）

4. Empirical Results
   4.1 Forward Tenor Volatility（H6a–c）→ Table 1A, Figure 0（銀價年 σ 對照）
   4.2 Concentration and Risk Budgeting（H1）→ Table 2, Figure 1
   4.3 Factor Exposures and Alphas（H2）→ Table 3
   4.4 Tail Risk and Crash Performance（H3）→ Table 4, Figure 2
   4.5 Fee Parity: 0050 vs 006208（H4）→ Table 5
   4.6 Dividend Forward Gap & Equalization（H5–H6d）→ Table 6

5. Robustness Checks
   5.1 COVID Subsample（2020Q1–2020Q2）
   5.2 Alternative Covariance（Sample vs Ledoit-Wolf）
   5.3 FF3 vs FF5
   5.4 NAV vs Market Price Returns

6. Discussion and Policy Implications
   6.1 For Retail Investors
   6.2 For Regulators（平準金揭露、集中度警示）
   6.3 Limitations

7. Conclusion

References

Appendix A: Index Methodology Summary of Six ETFs
Appendix B: Additional Tables
```

---

## 四、實證表格結構（Empirical Table Blueprint）

### Table 1：描述統計（Descriptive Statistics）

| 變數 | 0050 | 006208 | 0056 | 00878 | 00919 | 00929 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 月報酬均值 | | | | | | |
| 月報酬標準差 | | | | | | |
| Sharpe | | | | | | |
| Max Drawdown | | | | | | |
| TER (%) | 0.20 | 0.20 | 0.70–0.86 | 0.55–0.65 | 0.75–0.85 | 0.65–0.75 |
| AUM（期末，兆元） | | | | | | |
| 樣本期間 | 2018/01–2025/12（依上市日調整） | | | | | |

**資料來源註記**：TEJ／CMoney／Yahoo Finance（需統一）；無風險利率用 91 天公債或銀行定存（需一致）

---

### Table 1A：遠期期限波動（H6）— **v2.2 已填**

FinMind 收盤價，2018-01–2025-12，拆股調整；腳本 `code/compute_forward_horizon_risk.py`。

| ETF | $\sigma_m$ | $\sigma_q$ | $\sigma_y$ | Max DD | 主導 tenor |
| :--- | ---: | ---: | ---: | ---: | :--- |
| 0050 | 5.4% | 10.6% | **23.2%** | −36% | 季 FTSE + 年累積 |
| 006208 | 5.4% | 10.6% | 24.1% | −35% | 同 0050 |
| 0056 | 4.8% | 8.1% | 20.9% | −35% | 季／半年 + 月配 |
| 00878 | 3.7% | 6.3% | 17.3% | −28% | 半年 MSCI |
| 00919 | 4.1% | 7.1% | 16.5% | −32% | **年篩高息** + 季 |
| 00929 | 3.9% | 6.7% | 15.7% | −32% | 季 + 月配 |

**對照列**：1912–1921 倫敦銀價 $\sigma_y \approx$ **22.8%**；1920→1921 DD ≈ **−40%**。

**H6 pilot（Table 1B）**

| ETF | H6a rebal σ ratio | H6b ex-div σ ratio | Ann. yield proxy |
| :--- | ---: | ---: | ---: |
| 0050 | **1.13** | 1.01 | 1.4% |
| 0056 | 0.77 | **1.80** | 9.2% |
| 00919 | 0.88 | 0.91 | 9.7% |
| 00929 | 0.64 | **1.42** | 6.1% |

來源：`output/forward_horizon/h6_event_study.json`（2018–2025）。

---

### Table 2：集中度與邊際風險貢獻（H1）

**Panel A：橫截面（最新一季成分權重）**

| ETF | N | Max Weight | HHI | Eff. N (=1/HHI) | Wt sum (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 0050 | 36 | 台積電 57.2% | **0.342** | 2.9 | 92.9 |
| 006208 | 36 | 台積電 57.2% | **0.342** | 2.9 | 92.9 |
| 0056 | 39 | 9.3% | 0.064 | 15.6 | 81.9 |
| 00878 | 30 | 廣達 10.5% | 0.046 | 21.5 | 96.3 |
| 00919 | 58 | 國泰金 12.2% | 0.064 | 15.6 | 98.1 |
| 00929 | 50 | 聯電 12.7% | 0.050 | 20.2 | 98.5 |

*資料日：2026-06-08（00878：2026-06-09）。來源見 §0.2。Industry HHI（Tech）待 v3 補算。*

**Panel B**：0050 台積電 MRC 時間序列

| 期間 | $w_{TSMC}$ | $RC_{TSMC}$ | 95% CI |
| :--- | :---: | :---: | :---: |
| 2020 | | | |
| 2021 | | | |
| … | | | |

**預期結果**：$RC_{TSMC}$ 多數月份 > 0.65；0050 HHI > 0.35

**迴歸（可選）**：
$$\sigma_{p,t} = a + b_1 w_{TSMC,t} + b_2 HHI_t + \epsilon_t$$
- 預期：$b_1 > 0$，$b_2 > 0$

---

### Table 3：Fama-French 因子回歸（H2）

**模型**：
$$R_{p,t} - R_{f,t} = \alpha_p + \beta_{MKT} MKT_t + s_p SMB_t + h_p HML_t + r_p RMW_t + c_p CMA_t + \epsilon_{p,t}$$

| ETF | $\alpha$ | $\beta_{MKT}$ | $s_p$ (SMB) | $h_p$ (HML) | $r_p$ (RMW) | $c_p$ (CMA) | Adj. R² |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0050 | 0 | + | 0/? | 0 | | | |
| 0056 | 0 | + | | **+** | | | |
| 00878 | 0 | + | | + | | | |
| 00919 | 0 | + | | **+** | | **+?** | |
| 00929 | 0 | + | **+** | 0/? | | | |

**預期 sign 摘要**：

| 係數 | 0050 | 高息組 | 00929 |
| :--- | :---: | :---: | :---: |
| $\alpha$ | 不顯著 | 不顯著 | 不顯著 |
| $\beta_{MKT}$ | ≈1 | 0.6–0.9 | 1.0–1.2 |
| $h_p$ | 低 | **顯著 +** | 低 |
| $s_p$ | 低 | 中 | **顯著 +** |

**台灣 FF 因子**：若無官方因子，需自行依 TWSE 市值／帳面市值比建構（方法需附錄說明，或引用既有 working paper）

---

### Table 4：尾部風險與危機表現（H3）

**Panel A：CVaR / VaR（月報酬，%）**

| ETF | VaR 5% | CVaR 5% | VaR 1% | CVaR 1% |
| :--- | :---: | :---: | :---: | :---: |
| 0050 | | | | |
| 00919 | | | | |
| … | | | | |

**Panel B：市場大跌月條件報酬（TAIEX < −5%）**

| ETF | N(crash) | Mean $R_p$ | vs 0050 diff | t-stat |
| :--- | :---: | :---: | :---: | :---: |
| 0056 | | | | |
| 00878 | | **更差?** | | |
| 00919 | | | | |

**Panel C：下尾相依 $\lambda_L$（與 TAIEX）**

| 配對 | $\lambda_L$ | $\lambda_U$ |
| :--- | :---: | :---: |
| 0050–TAIEX | 高 | |
| 00878–TAIEX | 中 | |
| 00929–TAIEX | 高 | |

---

### Table 5：0050 vs 006208 配對檢定（H4）

| 指標 | 0050 | 006208 | Diff | t-stat |
| :--- | :---: | :---: | :---: | :---: |
| 年化報酬 | | | | |
| 年化 $\sigma$ | | | | |
| TE（vs 指數） | | | | |
| 累積報酬差（2020–2025） | | | ≈ −ΔTER×T | |

---

### Table 6：收益平準金與配息可持續性（H5）

**樣本**：0056、00878、00919、00929（有配息＋平準金揭露者）

**Panel A：Logit 配息下修**
$$P(\Delta Yield_{t+1} < 0) = \Lambda(\gamma_0 + \gamma_1 EQ\_ratio_t + \gamma_2 Flow_t + \gamma_3 AUM_t + Controls)$$

| 變數 | Coef | z | 預期 sign |
| :--- | :---: | :---: | :---: |
| $EQ\_ratio$ | | | **+** |
| $Flow$ | | | **−**（淨贖回 → 下修） |
| $AUM$ | | | ? |

**Panel B：折溢價 FE 迴歸**
$$Discount_{i,t} = \delta_i + \tau_t + \phi_1 EQ\_ratio_{i,t} + \phi_2 Flow_{i,t} + \epsilon_{i,t}$$

| 變數 | Coef | 預期 sign |
| :--- | :---: | :---: |
| $EQ\_ratio$ | | **−**（依賴平準金 → 折價） |
| $Flow$ | | **+**（淨申購 → 溢價） |

---

### Table 7：穩健性（Robustness）

| 規格 | H1 $RC_{TSMC}$ | H2 $h_p$(0056) | H3 CVaR rank |
| :--- | :---: | :---: | :---: |
| Baseline | | | |
| COVID 排除 | | | |
| FF3 替代 FF5 | | | |
| 價格報酬替代 NAV | | | |

---

## 五、資料清單與取得方式

| 資料 | 用途 | 可能來源 | 頻率 |
| :--- | :--- | :--- | :--- |
| ETF NAV／收盤價 | 報酬、TE | TEJ、證交所、元大／群益官網 | 日 |
| 成分股權重 | HHI、MRC | ETF 月報、索引公司 | 月／季 |
| 成分股日報酬 | $\Sigma$ | TEJ、FinMind | 日 |
| 無風險利率 | 超額報酬 | 央行、TEJ | 月 |
| TW FF 因子 | Table 3 | 自建或學術 WP | 月 |
| 配息／平準金 | Table 6 | ETF 配息公告、月報 | 季 |
| 折溢價 | Table 6 | 證交所 iVIX／ETF 專頁 | 日 |
| 淨申購 Flow | Table 6 | ETF 規模變動 − 報酬貢獻 | 月 |

**樣本建議**：2018-01 至 2025-12（00919 2013/06 上市前以實際 IPO 日為起點）

---

## 六、核心文獻清單（Literature List）

### 6.1 理論基礎

1. Markowitz, H. (1952). Portfolio Selection. *Journal of Finance*.
2. Sharpe, W. F. (1964). Capital Asset Prices. *Journal of Finance*.
3. Fama, E. F., & French, K. R. (1993). Common Risk Factors in Stock and Bond Returns. *Journal of Financial Economics*.
4. Fama, E. F., & French, K. R. (2015). A Five-Factor Asset Pricing Model. *Journal of Financial Economics*.
5. Artzner, P., et al. (1999). Coherent Measures of Risk. *Mathematical Finance*.
6. Patton, A. J. (2006). Modelling Asymmetric Exchange Rate Dependence. *International Economic Review*（尾部相依）.

### 6.2 ETF 微結構與被動投資成本

7. Li, S. (2022). Should Passive Investors Actively Manage Their Trades? AEA Conference / Working Paper（67 bps execution shortfall）.
8. Ben-David, I., Franzoni, F., & Moussawi, R. (2018). Do ETFs Increase Volatility? *Journal of Finance*.
9. Da, Z., & Shive, S. (2018). Exchange Traded Funds and Asset Return Correlations. *European Financial Management*.
10. ETF Rebalancing, Hedge Fund Trades, and Capital Markets (2023). EFMA Annual Meeting.
11. On the Hidden Costs of Passive Investing (2025). arXiv:2506.21775.

### 6.3 指數集中度

12. FTSE Russell (2024). FTSE Taiwan RIC Capped Index Research.
13. Lazard Asset Management (2026). Index Concentration in Emerging Markets.
14. Antón, M., et al. (2022). Concentration in US Equity Markets. *Journal of Finance*（方法參考）.

### 6.4 台灣市場與高股息 ETF

15. 央行（2024–2025）. 《ETF 對金融穩定之影響》.
16. 何依潔. The Impact of ETFs on Financial Stability in Taiwan. 高科大商管學院論文.
17. 屏東大學（2021）. 台灣高股息 ETF 投資績效與追蹤能力之探討. *屏東大學學報管理類*.
18. 碩士論文（2024）. 台股高股息 ETF 績效實證分析—新冠疫情前後比較. NCL.
19. 金管會（2024）. 收益平準金揭露強化措施、配息來源順序規範.
20. 證交所. Clarifying the Equalization Reserve Mechanism（投資人教育）.

### 6.5 方法參考

21. Ledoit, O., & Wolf, M. (2004). Honey, I Shrunk the Sample Covariance Matrix. *Journal of Portfolio Management*（MRC 用）.
22. Newey, W. K., & West, K. D. (1987). A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. *Econometrica*.
23. Christie-David, R., & Chaudhry, M. (2003). Coskewness and Cokurtosis in Futures Markets. *Journal of Empirical Finance*（高階矩，可選）.

---

## 七、投稿策略（依目標分級）

### 7.1 碩士論文（可行性：★★★★★）

| 項目 | 建議 |
| :--- | :--- |
| **篇幅** | 80–120 頁 |
| **必做表格** | Table 1–4 + 至少 Table 3（FF）或 Table 6（平準金）擇一深度做 |
| **時程** | 資料 4–6 週、估計 2–3 週、撰寫 3–4 週 |
| **答辯賣點** | 「六檔統一框架 + 00919/00929 首次系統比較」 |
| **風險** | 台灣 FF 因子需自建，答辯委員常問 |

### 7.2 台灣中文期刊（可行性：★★★★）

| 期刊 | 定位 | 策略 |
| :--- | :--- | :--- |
| **《證券市場發展季刊》** | 台灣市場、政策 | 強調 H5 平準金 + 央行政策呼應 |
| **《管理評論》** | 管理＋實證 | 強調 risk budgeting 對 RETAIL 投資者教育 |
| **《台灣經濟論叢》** | 經濟政策 | 產業集中度 + 金融穩定 |
| **《財信月刊學術版／政大學報** | 財金 | FF + 高股息績效 |

**投稿前 checklist**：
- [ ] 語氣中性、無「謊言」「神話」用語
- [ ] 至少 2 項 robustness
- [ ] 英文 abstract + 5 keywords
- [ ] 資料來源可複製聲明

### 7.3 英文 Regional Journal（可行性：★★★）

| 期刊 | IF 區間 | 策略 |
| :--- | :--- | :--- |
| **Pacific-Basin Finance Journal** | ~2–4 | 主打 Taiwan ETF boom + concentration |
| **International Review of Financial Analysis** | ~8+ | 需 H5 或 H3 有顯著 novel finding |
| **Emerging Markets Review** | ~3–5 | EM retailization + dividend ETF |
| **Asia-Pacific Journal of Financial Studies** | ~1–2 | 門檻較低，適合 first paper |

**Cover letter 貢獻句模板**：
> We provide the first unified risk-budgeting comparison of Taiwan's six largest retail ETFs, including the recently launched high-yield products 00919 and 00929. Unlike prior Taiwan studies focusing on performance or tracking error alone, we decompose concentration (HHI), marginal risk contributions, Fama-French exposures, and tail dependence within a common sample period.

### 7.4 不建議首投

- *Journal of Finance / JFE / RFS*：除非有全球 identification（如 natural experiment on index rule change）
- 純 policy commentary without econometrics：改投 **央行工作論文** 或 **金管會研究專刊**

---

## 八、寫作語氣對照（評論稿 → 學術稿）

| 原報告用語 | 學術替代 |
| :--- | :--- |
| 被動投資的核心謊言 | The embedded rigidity of passive rebalancing rules |
| 羊毛神話 | Dividend distribution does not create incremental shareholder wealth |
| 因子剝削 | Factor exposure without significant Jensen's alpha |
| LCP 溢價 | Implementation shortfall and opportunity cost of rule-based rebalancing |
| 合法的流動性肉墊 | Predictable index reconstitution and front-running costs (Li, 2022) |
| 鬱金香狂熱 | Elevated flow-driven premium and yield expectations（需附指標） |

---

## 九、建議執行時程（12 週）

| 週次 | 任務 | 產出 |
| :---: | :--- | :--- |
| 1–2 | 資料收集、FF 因子建構 | 清洗後 panel CSV |
| 3–4 | HHI、MRC、Table 1–2 | 集中度結果 |
| 5–6 | FF5 回歸 Table 3 | 因子載荷 |
| 7 | CVaR、crash month Table 4 | 尾部結果 |
| 8 | 平準金 panel Table 6 | H5 檢驗 |
| 9 | Robustness Table 7 | |
| 10–11 | 撰寫初稿 | 完整 manuscript |
| 12 | 潤稿、格式、reference | 投稿版 |

---

## 十、下一步（可交付物）

若你繼續推進，建議在 `d:\ETF\` 下新增：

1. **`data/`** — 原始與清洗資料  
2. **`code/`** — Python/R 估計腳本（MRC、FF、CVaR）✅ HHI 腳本已有  
3. **`manuscript/`** — 依本 outline 撰寫的 `.docx` / `.tex` ✅ SSRN v2 已有  

我可下一步直接為你生成：
- **Python 資料抓取 + MRC/FF 估計腳本骨架**，或  
- **Introduction + Literature Review 初稿（中文或英文）** ✅ 緒論初稿已有 `manuscript/introduction.md`

請告知你的目標（碩論 / 台灣期刊 / 英文期刊）與可用資料庫（TEJ、FinMind、僅免費源）。

---

## 十一、SSRN 工作論文與期刊升級路徑

### 11.1 沒有固定的「下載／引用門檻」

學界**不存在**「SSRN 下載滿 500 次／引用滿 10 次就該投期刊」的通則。Heckman et al.（2024, *Review of Finance*）分析 2001–2019 年 SSRN FEN 逾 5 萬篇金融論文後指出：下載與引用反映**能見度與影響力**，但能否進期刊取決於**實證完整度、方法正統性（conventionality）與議題新穎度（novelty）的平衡**，以及是否通過 AFA／WFA 等會議篩選（入選 AFA 或 WFA 者，進 top-3 金融期刊的機率約高 48%）。

對**個人進修、非升等**用途：SSRN v2 本身已是合理終點；投期刊是**品質與同儕審查**的選項，而非 SSRN 數字達標後的義務。

### 11.2 SSRN 指標如何解讀（參考區間，非門檻）

| 指標 | 狀態 | 常見解讀 |
| :--- | :--- | :--- |
| **下載量** | 小眾台灣 ETF 題材，首年 **50–300** 次已屬正常；**500+** 表示跨社群傳播 | 反映議題熱度與 abstract／關鍵字品質；Willey & Knapp 發現高被引論文 abstract 較長、關鍵字較多 |
| **引用數** | 工作論文階段 **0–5** 很常見；**2 年內 10+** 對 regional 題材已屬不錯 | SSRN 預印本與最終期刊版引用常合併計算；期刊版「同儕認可 stamp」約使年引用翻倍（Economics 實證，2021） |
| **編輯主動邀稿** | 極少見，通常 **0 下載** 也可能因 fit 被邀 | 勿把 SSRN 當 placement 策略（Eric Goldman 實務觀察） |

**重點**：下載高只代表「有人看」；要投期刊，仍需 §0.4 表格中「期刊投稿最低門檻」欄全綠。

### 11.3 何時適合從 SSRN 升級為期刊投稿？

| 時機 | 說明 | 與本專案對照 |
| :--- | :--- | :--- |
| **實證就緒** | 核心假說（H1–H5）至少 4/5 有全樣本估計 + robustness | H1 **HHI 橫截面已完成**（六檔 PCF）；MRC／FF／H5 待做 |
| **草稿可送審** | 達「願意公開被批評」水準（Goldman：通常等同準備投期刊的 circulation 版） | v2 仍標 **illustrative** MRC／CVaR，尚非送審版 |
| **議題仍新** | 00919／00929 上市未滿 3 年，窗口約 **2026–2028** | 宜在 v3（FF 表）完成後 12 個月內投稿 |
| **收到建設性回饋** | SSRN 留言、研討會、同事質疑指向需補 robustness | 可將回饋寫入 cover letter |
| **個人目標改變** | 升等、轉職、或欲被政策引用需 peer review | 你目前以進修為主 → **不急** |

**不建議**僅因 SSRN 數字好看就投稿：desk reject 成本高（如 *Journal of Empirical Finance* 投稿費 US$175，且 scope 不符可直接拒）。

### 11.4 類型範例

| 類型 | 路徑 | 啟示 |
| :--- | :--- | :--- |
| **Conference → Top journal** | 美國 ETF 再平衡成本（Li, 2022）：working paper → AEA／WFA → 期刊 | 本題若要做國際版，可先投 **Asian Finance Association** 或 **TFA 年會** poster |
| **Regional journal + SSRN 並行** | 許多 *Pacific-Basin Finance Journal*、*Emerging Markets Review* 論文先掛 SSRN，審稿期間累積下載 | 本題 fit **PBFJ**（Taiwan ETF boom + concentration） |
| **本土期刊、無 SSRN 要求** | 《證券市場發展季刊》重政策呼應（H5 平準金），不看重 SSRN 指標 | 中文精簡版 + Table 6 可能是更快路徑 |
| **Working paper 即終點** | 央行／金管會研究專刊、NBER-style note | 個人進修 + AI 聲明已揭露 → **v2–v3 即可** |

### 11.5 本專案建議時程（個人進修版）

```
現在 ──► SSRN v2（HHI 實證）上傳，累積 6–12 個月能見度
   │
   ├─► v3：FF 回歸一表（FinMind 月報酬）→ SSRN 更新
   │
   ├─► 若下載/引用/回饋 positive + Table 1–4 完成
   │       → 投 PBFJ 或《證券市場發展季刊》（擇一）
   │
   └─► 若維持進修、無升等需求
           → 停在 v3 SSRN 即可，不必強求期刊
```

### 11.6 投稿前 checklist（相對 SSRN v2 的增量）

- [x] 六檔 HHI 皆來自完整 PCF（非 equal-tail 估算）
- [ ] MRC 時間序列（2020–2025）+ 95% CI
- [ ] FF5 回歸 Table 3（Newey-West lag=3）
- [ ] CVaR + crash month Table 4
- [ ] 平準金 Panel Table 6（至少 0056、00878、00919、00929）
- [ ] Robustness Table 7（≥2 規格）
- [ ] 移除 "illustrative" 標籤；SSRN 改列 Accepted Paper Series（若被接受）
- [ ] 確認目標期刊 preprint 政策（多數 Elsevier 財金刊允許 SSRN 預印本）

---

*本文件為研究藍圖，不構成投資建議。*
