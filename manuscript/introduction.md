# 一、緒論（Introduction）

## 1.1 研究動機

過去十年間，台灣交易所買賣基金（Exchange-Traded Funds, ETFs）市場經歷空前的規模擴張與零售化浪潮。以元大台灣50（0050）、富邦台灣50（006208）、元大高股息（0056）、國泰永續高股息（00878）以及近年快速崛起的群益台灣精選高息（00919）、復華台灣科技優息（00929）為代表，六檔商品合計受益人數逾數百萬、資產規模達數兆新台幣，已成為國內散戶退休準備與「存股配息」的核心工具。央行（2024–2025）與金融監督管理委員會亦多次指出，ETF 在提升市場流動性與資產配置效率之餘，可能因成分集中度、申贖順周期性及配息機制而放大波動與風險傳染，值得以量化方法持續監測。

從理論面觀之，現代投資組合理論（Modern Portfolio Theory, MPT）與資本資產定價模型（Capital Asset Pricing Model, CAPM）為指數型商品提供了清晰的風險語言：投資人透過持有多元資產降低非系統性風險，並以市場 β 衡量系統性曝險（Markowitz, 1952; Sharpe, 1964）。Fama and French（1993, 2015）進一步將報酬分解為市場、規模、價值、獲利能力與投資模式等因子，使 Smart Beta 與高股息策略的績效歸因成為可能。在此框架下，ETF 常被視為「低成本、高透明、充分分散」的被動工具。

然而，既有文獻與實務觀察提示：**被動投資並非無人掌控，且投資人所承擔的總風險往往超過教科書模型在理想假設下所隱含者。** Robertson（2019）指出，指數型基金本質上是將組合管理權委託予指數編製者，投資人無法依個人風險偏好調整權重或減碼過熱標的——此為典型的委託管理（delegated management）而非真正的自主配置。Li（2022）以美國 ETF 日持倉資料估計，追蹤公開指數且於換股日機械再平衡者，單次執行落差平均約 67 個基點（basis points, bps），顯著高於同規模機構交易；對沖基金於再平衡前的 anticipatory trading 亦使 ETF 投資人承受「買高賣低」之隱含成本（EFMA, 2023; Tasitsiomi, 2025）。Berk and van Binsbergen（2015）更早提醒，關於被動投資的討論長期忽略交易成本；Morningstar（2025）綜述指出，執行落差（implementation shortfall）可能遠超年化管理費，卻未反映於 CAPM 或費率比較之中。

與全球指數集中度上升之趨勢相互強化（Antón et al., 2022; FTSE Russell, 2024），台灣市場呈現更極端型態：台積電權重於 0050／006208 中屢次突破 60%，使 Herfindahl-Hirschman Index（HHI）與邊際風險貢獻（Marginal Risk Contribution, MRC）大幅偏向單一標的，MPT「以檔數分散即消除 idiosyncratic risk」之前提在實務上接近失效。另一方面，高股息 ETF 雖在成分檔數上較為分散，其選股規則卻可能暴露於價值因子（HML）、景氣循環產業及尾部相依（tail dependence）——00878 之金融權重在危機中與大盤共振、00919 之航運與高波動半導體、00929 之100% 科技 SMB 曝險，皆無法僅以「成分股數目」加以刻畫。配息面更因**收益平準金**制度而產生現金流可持續性問題：金管會（2024）要求強化配息來源揭露，正是因部分商品之宣告配息可能偏離成分股自然股息，在淨申購放緩時面臨下修風險。

綜上，學界對美國市場已累積再平衡成本、指數集中與因子歸因之研究；台灣本土文獻則多聚焦於 0056、00878、00713 等較早商品之績效與追蹤誤差（如屏東大學, 2021；碩士論文, 2024），或停留於央行式政策描述而缺乏可複製之計量檢驗。**對 00919、00929 等新興高息 ETF，以及六檔最大熱門商品在同一風險預算框架下之系統比較，仍屬空白。** 本文即在此缺口上，回應一項具體但尚未被完整實證的命題：**被動 ETF 投資人所承擔之總風險，是否系統性地高於均值–方差模型在「充分分散、無摩擦、權重可自主」假設下所暗示者？** 我們將該命題操作化為集中度、因子暴露、尾部風險、追蹤誤差與配息可持續性五個可檢驗層次，而非停留於定性批判。

---

## 1.2 研究問題與假說

本文提出五項研究問題及對應假說，摘要如下。

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

---

## 1.3 研究貢獻

本文之邊際貢獻有四：

**第一（方法）**，在同一樣本期間（2018 年 1 月至 2025 年 12 月，依各檔上市日調整）與同一估計程序下，對六檔 ETF 進行 **HHI–MRC–FF5–CVaR** 四層風險分解，使「個股集中」（0050）、「因子／產業集中」（00929）與「尾部集中」（00919）可在統一風險預算（risk budgeting）語言中對照，超越僅報告報酬率或 Sharpe 比率之既有台灣文獻。

**第二（實證）**，將樣本延伸至 **00919、00929**，填補同儕審查研究中對新興高息 ETF 的覆蓋缺口，並以 Newey-West 標準誤估計因子載荷與 α，回應「高配息是否帶來超額報酬」之零售敘事。

**第三（制度）**，建構配息與平準金面板，檢驗 **H5**，直接對話金管會配息來源揭露與央行關於 ETF 金融穩定之政策關切，將監管理念轉化為可更新之計量指標（如 $C_t/D_t$、$EQ\_ratio$）。

**第四（政策與投資者教育）**，明確區分兩類常被混淆之風險：**名義分散 vs. 有效分散**、**配息率 vs. 總報酬**。本文不否定 ETF 作為配置工具之價值，而主張風險辨識應先於因子與尾部層面完成，再討論費率與流動性——此與 Li（2022）對隱藏執行成本之警告、以及 Robertson（2019）對委託管理本質之提醒前後一致，但首次給出台灣六檔最大熱門商品之整合實證。

---

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

因此，本文所處理之「被動由他人掌控之風險高於模型暗示」並非全新口號，而是將 **委託管理（Robertson, 2019）、執行成本（Li, 2022）、指數集中（FTSE Russell, 2024; 央行, 2025）與因子／尾部風險（Fama & French, 1993, 2015; Patton, 2006）** 整合於台灣最大六檔 ETF 之實證檢驗——此整合在本土同儕文獻中尚屬首次。

---

## 1.5 文章結構

其餘章節安排如下。第二章回顧指數集中度、ETF 微結構、因子模型、尾部風險及台灣配息制度文獻，並推導假說。第三章說明資料來源、變數建構（HHI、MRC、FF 因子、CVaR、$EQ\_ratio$、折溢價）與估計方法。第四章報告實證結果。第五章進行子樣本與估計方法之穩健性檢驗。第六章討論投資人與監理意涵及研究限制。第七章結論。

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

*【撰寫備註】正式投稿前請：(1) 補齊 Antón et al. 與 EFMA 2023 之完整書目；(2) 依目標期刊格式調整 RQ/H 是否併入一段式敘述而非條列；(3) 確認各中文引用與西文引用格式一致。*
