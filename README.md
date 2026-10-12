# r-d

A handful of Turkish funds were posting outsized, steady gains. This repo watches whether that could continue: a daily TEFAS series (price, shares, cash buffer) and a KAP book (holdings and concentration). On **16.09.2026**, the last published TEFAS row before the halt, the unit price still looked fine.

| | |
|---|---|
| [**Terminal**](fon_terminal/README.md) | Daily TEFAS series: whale radar, cash buffer. Screenshot is TLY on **16.09.2026**, the last published row before the halt. The four alert rules were added on 30.09, after the event. |
| [**KAP pipeline**](fon_terminal/kap_pdf_downloader/README.md) | Holdings and trades through **16.09.2026**. Weights use that day's BIST closes over the TEFAS row dated 16.09, which is the 15.09 valuation. |
| [**Case study**](fon_terminal/case_study/CASE_STUDY_2026_09.md) | What those series showed before the September 2026 run. |

The tag [`pre-crisis-2026-09-14`](https://github.com/Raknero/r-d/releases/tag/pre-crisis-2026-09-14) is the last commit from before the event. Later commits are dated and say what was added after.
