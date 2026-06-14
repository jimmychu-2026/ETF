# 一、緒論（Introduction）

## 1.1 研究動機

過去十年間，台灣交易所買賣基金（Exchange-Traded Funds, ETFs）市場經歷空前的規模擴張與零售化浪潮。以元大台灣50（0050）、富邦台灣50（006208）、元大高股息（0056）、國泰永續高股息（00878）、國泰台灣領袖50（00919）與復華台灣科技優息（00929）為代表的六檔熱門 ETF，已不再只是單純的被動投資工具，而逐步成為台灣散戶資產配置、現金流管理與因子暴露承載的核心載體。

從理論面觀之，現代投資組合理論（Modern Portfolio Theory, MPT）與資本資產定價模型（Capital Asset Pricing Model, CAPM）為指數型商品提供了清晰的風險語言：隨著持股數增加，非系統性風險理應下降；資產報酬則可由市場因子與若干風格因子加以解釋。然而，當 ETF 產品同時承載高集中度權重、公開再平衡、配息承諾、收益平準金、折溢價與申贖套利等制度性約束時，教科書中的「被動持有」與「充分分散」前提便不再完整成立。

本研究的核心問題即在於：**台灣六大熱門 ETF 的風險，是否應被理解為一組「現貨外觀下的遠期／永續類比契約」？** 若答案為是，則 ETF 的報酬與風險不僅來自底層成分股的價格變動，也來自持續性的制度摩擦、再平衡衝擊、配息承諾與流動性折價。此一視角有助於重新理解投資人所承擔的總風險，並將「名義分散」與「有效分散」區分開來。

此外，台灣市場的集中度問題較其他成熟市場更為尖銳。台積電在 0050／006208 中的權重長期極高，使得投資人實際上承擔的是「被台積電放大的市場」；高股息 ETF 則以配息率作為行銷主軸，但其配息來源、平準金使用與成分輪動，使其更接近一種具有短期現金流承諾的遠期結構，而非單純的股票現金流再分配。故本文不僅討論資產配置意義，也試圖從制度與契約結構層次說明：ETF 為何看似被動，實則具有高度的規則性與內耗性。

為了建立概念性對照，本文同時引入**當代主流新興金融商品**作為比較對象。這些商品通常具備「名義簡單、實質複雜」的特徵：例如 perpetual futures、資金費率合約、合成資產與部分槓桿／再平衡型產品，往往沒有固定到期日，卻依賴持續性的費率、套利與錨定機制維持價格穩定。本文比較傳統遠期／期貨與當代主流新興金融商品，目的不是主張 ETF 在法律上等同於這些商品，而是強調 ETF 在經濟行為上更接近一種 **perpetual-like holding contract**：它沒有終點收斂，但持續承受費用、套利摩擦、再平衡成本與事件窗失真。

## 1.2 研究問題與假說

本研究提出五項研究問題及對應假說，摘要如下。

**RQ1**：名義成分分散之高股息／Smart Beta ETF，是否在因子維度與尾部風險上較 0050 更為分散？  
→ **H1**：0050／006208 之台積電 MRC 佔比（$RC_{TSMC}$）顯著高於 50%，且 HHI 顯著高於其餘五檔（**H1a, H1b**）。

**RQ2**：0050／006208 之波動與條件在險值（Conditional Value-at-Risk, CVaR）是否主要由台積電驅動？  
→ 與 H1 合併檢驗；並以壓力情境驗證單一特異性衝擊之組合傳導。

**RQ3**：高股息 ETF 之超額報酬是否可被 Fama-French 五因子（FF5）解釋，即 Jensen's α 不顯著異於零？  
→ **H2**：高息組（0056、00878、00919）之 HML 載荷顯著為正；00929 之 SMB 載荷顯著為正（**H2a–H2c**）。

**RQ4**：00919／00929 是否較傳統高息 ETF 具更高週期性與尾部風險？  
→ **H3**：00919 之 CVaR 絕對值大於 00878；00878 於市場大跌月之條件報酬差於 0056（**H3a–H3c**）。

**RQ5**：收益平準金依賴度與淨申購放緩，是否預測配息率下修或折溢價擴大？  
→ **H5**：平準金佔比（$EQ\_ratio$）越高，下期配息下修機率越高；淨贖回期間折價擴大（**H5a–H5b**）。

此外，對追蹤同一指數之 0050 與 006208，我們檢驗 **H4**：超額報酬差異應近似費率差（$-\Delta TER$），以分離「選股能力」與「契約成本」之迷思。

## 1.3 研究貢獻

本文之邊際貢獻有四：

**第一（方法）**，在同一樣本期間（2018 年 1 月至 2025 年 12 月，依各檔上市日調整）與同一估計程序下，對六檔 ETF 進行 **HHI–MRC–FF5–CVaR** 四層風險分解，並將再平衡、除息與配息承諾納入制度性風險分析。

**第二（實證）**，將樣本延伸至 **00919、00929**，填補同儕審查研究中對新興高息 ETF 的覆蓋缺口，並以 Newey-West 標準誤估計因子載荷與 α，回應「高息 ETF 是否只是風格暴露，而非 α」之爭議。

**第三（制度）**，建構配息與平準金面板，檢驗 **H5**，直接對話金管會配息來源揭露與央行關於 ETF 金融穩定之政策關切，將監管理念轉化為可更新的風險指標。

**第四（概念）**，提出「ETF 的永續類比模型（conceptual analogy）」：ETF 不是標準期貨，但其經濟效果接近一種沒有固定到期日、卻持續支付費用、承擔套利摩擦與再平衡衝擊的動態持有契約。此一框架有助於理解 ETF 的價格偏離、內耗與制度摩擦，並將其與傳統遠期／期貨及當代主流新興金融商品進行對照。

## 1.4 與既有文獻之定位

本文與下列研究對話，並指出填補之處：

| 文獻 | 重點 | 本文之差異 |
| :--- | :--- | :--- |
| 屏東大學（2021） | 高股息 ETF 績效與追蹤誤差 | 樣本未含 00919／00929；未估 MRC／CVaR |
| 台股高股息 ETF 碩士論文（2024） | COVID 前後 CAPM 比較 | 升級為 FF5 + 尾部 + 六檔統一框架 |
| 央行（2024–2025） | ETF 集中度與金融穩定 | 政策描述 → 可檢驗假說與估計值 |
| Li（2022）; Tasitsiomi（2025） | 美國被動再平衡隱藏成本 | 理論基礎；台灣 TE 作控制，非本文主因變數 |
| FTSE Russell（2024） | 台股 uncapped 集中與 capped 設計 | 指數方法論 → 0050 實證 MRC／HHI |
| Robertson（2019） | 指數投資即委託管理 | 治理面向 → 本文聚焦風險量化 |

因此，本文所處理之「被動由他人掌控之風險高於模型暗示」並非全新口號，而是將 **委託管理（Robertson, 2019）、執行成本（Li, 2022）、指數集中（FTSE Russell, 2024）與台灣制度摩擦** 統合為一個可估計的風險架構。

## 1.5 文章結構

其餘章節安排如下。第二章回顧指數集中度、ETF 微結構、因子模型、尾部風險及台灣配息制度文獻，並推導假說。第三章說明資料來源、變數建構（HHI、MRC、FF5、CVaR、折溢價、平準金比例）與估計方法。第四章呈現六檔 ETF 的集中度、因子載荷、尾部風險與市場摩擦結果。第五章討論配息永續性與收益平準金。第六章檢驗 ETF 的永續類比模型與制度風險。第七章總結，並提出監理與投資者教育之政策含意。

---

## 參考文獻（Introduction 引用）

Antón, M., Ederer, F., Giné, M., & Schmalz, M. C. (2022). *Common ownership, competition, and top management incentives*（方法參考）. Working Paper.

Berk, J. B., & van Binsbergen, J. H. (2015). Measuring skill in the mutual fund industry. *Journal of Financial Economics*, 118(1), 1–20.

EFMA Annual Meeting. (2023). *ETF rebalancing, hedge fund trades, and capital markets*.

Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.

Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.

FTSE Russell. (2024). *FTSE Taiwan RIC Capped Index* research paper.

Li, S. (2022). Should passive investors actively manage their trades? AEA Conference / Working Paper.

Markowitz, H. (1952). Portfolio selection. *Journal of Finance*, 7(1), 77–91.

Morningstar. (2025). The hidden costs of passive investing.

Patton, A. J. (2006). Modelling asymmetric exchange rate dependence. *International Economic Review*, 47(2), 527–556.

Robertson, S. I. (2019). Passive in name only: Delegated management and “index” investing. *Journal of Corporation Law*（及 NYU Law Working Paper）.

Sharpe, W. F. (1964). Capital asset prices. *Journal of Finance*, 19(3), 425–442.

Tasitsiomi, I. (2025). On the hidden costs of passive investing. arXiv:2506.21775.

央行.（2024–2025）.《ETF 對金融穩定之影響》.

金管會.（2024）. 收益平準金揭露強化措施、配息來源順序規範.

屏東大學.（2021）. 台灣高股息 ETF 投資績效與追蹤能力之探討. *屏東大學學報－管理類*.

---

*【撰寫備註】正式投稿前請：(1) 補齊 Antón et al. 與 EFMA 2023 之完整書目；(2) 依目標期刊格式調整 RQ/H 是否併入一段式敘述而非條列；(3) 確認各中文參考文獻之正式出版資訊。*
