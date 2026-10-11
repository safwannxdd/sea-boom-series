# Q0 · What Have SEA's Digital-Economy Booms Been?

**Status:** DRAFT v1 research design. Approved as a skeleton on 2026-10-11. No code yet.
**Series position:** Q0 is the foundation of the series. Its boom catalogue is the input for Q1 (which regions lead SEA booms).

---

## 0. Why this study

The e-Conomy SEA 2025 report (Google, Temasek, Bain), the tenth edition, already tells the headline story. SEA's digital
economy grew from about US$40B to over US$300B in gross merchandise value (GMV) in a decade. E-commerce is the largest sector.

What it does not do, and what no study found so far does:

* date **when and where** each sector took off, using a consistent and validated rule;
* separate **booms** (sustained growth) from **spikes** (rise, then collapse);
* check the timing against **independent data** (e-Conomy SEA figures are modelled estimates that are revised every year).

> **Positioning:** e-Conomy SEA measures how much SEA's digital economy grew. This study dates when and where each
> sector took off, separates booms from spikes, and checks the timing across sources.

---

## 1. Research questions

| # | Question |
|---|---|
| **RQ0.1** | Which digital-economy sectors boomed in which SEA countries, and when did each take off? |
| **RQ0.2** | Which were real booms (sustained growth) and which were spikes (rise, then collapse)? |
| **RQ0.3** | Where is each sector × country in its lifecycle today: emerging, booming, mature or declining? |
| **RQ0.4** | Do independent sources agree on the timing (e-Conomy SEA vs Passport vs IMF)? |
| **RQ0.5** | Is there a pattern in who booms first, by country, sector or income? |

---

## 2. Scope

### 2.1 Countries: all 11 SEA states

| Tier | Countries | Data |
|---|---|---|
| **A** | Indonesia, Malaysia, Philippines, Singapore, Thailand, Vietnam | Passport, e-Conomy SEA (all editions), IMF FAS |
| **B** | Brunei, Cambodia, Laos, Myanmar, Timor-Leste | IMF FAS; e-Conomy SEA 2025 (first edition to cover four of them); Passport where available |

### 2.2 Period

As far back as each source allows, up to 2025. The start year is recorded per series in the P0 audit.

### 2.3 Sectors: the digital economy

The sector list follows e-Conomy SEA's framework, the standard definition for the region. Each sector is tagged
with its stock-market classification (GICS) so it can be described correctly. None falls in the GICS Information
Technology sector or the OECD's narrow ICT sector; all are digitally enabled. *GICS tags to be verified in P0.*

| Group | Sector | GICS sector (to verify) | Data strength (expected) |
|---|---|---|---|
| **Established data** | E-commerce | Consumer Discretionary | Strong |
| | Ride-hailing | Industrials | Medium |
| | Food delivery | Consumer Discretionary | Medium |
| | Online travel | Consumer Discretionary | Medium |
| | Online media (gaming, video, music, ads) | Communication Services | Medium |
| | Digital payments / e-wallets | Financials | Strong |
| | Digital banking (mobile and internet) | Financials | Strong |
| **Data to be built** | Digital lending / BNPL | Financials | Weak → upgrade in P0 |
| | Digital remittances | Financials | Weak → upgrade in P0 |
| | Digital investment and insurance | Financials | Weak → upgrade in P0 |
| | Crypto | Financials | Weak → upgrade in P0 |

**All 11 sectors get the full analysis**: the same definitions, tests, validation and robustness checks. The four
"data to be built" sectors have short or biased public series, so P0 searches for better sources, chiefly **monthly
regulator statistics**. Twelve observations a year make the break and bubble tests usable on short windows.

**Minimum-data rule (applies to every sector equally):** a test runs on a series only if the series meets that
test's minimum length (set in P1, e.g. ≥ 8 annual or ≥ 36 monthly observations for takeoff dating). A series that
falls short is reported as **"not testable"**, not dropped and not forced. This keeps the same standard everywhere,
so a weak sector cannot pass on weaker evidence.

**Excluded:** enablers (internet use, smartphones, 4G). They are conditions for booms, not booms, and enter later
questions as controls.

---

## 3. Data

| Sector | Primary source | Cross-check | Expected start |
|---|---|---|---|
| E-commerce, ride-hailing, food delivery, travel, media | Euromonitor Passport (UCL licence) | e-Conomy SEA (chain-linked across editions) | to confirm in P0 |
| Payments, banking | IMF Financial Access Survey (FAS) | Central-bank statistics, World Bank Findex | 2004 |
| Digital lending / BNPL | Regulator statistics, e.g. Indonesia OJK fintech-lending (P2P) data, monthly (to confirm in P0) | e-Conomy SEA, Passport (if covered) | ~2018 |
| Digital investment and insurance | Regulator statistics: securities-account and digital-insurance data from securities and insurance regulators (to confirm in P0) | e-Conomy SEA | to confirm |
| Digital remittances | Findex "received remittances via mobile" (2014, 2017, 2021, 2024); World Bank RPW digital-channel costs | World Bank remittance inflows (% GDP), as context | 2011–2014 |
| Crypto | Exchange trading volumes by fiat currency, regulator registrations (e.g. Thailand SEC, Malaysia SC) | Chainalysis adoption index, Orbis firm formation (UCL licence), Google Trends | to confirm |

**Units:** value as % of GDP, which removes most exchange-rate and inflation effects, plus per capita as a check.

**Licensed data:** Passport and Orbis stay in `data/licensed/`, git-ignored. They are never published, raw or
derived. Notebooks that use them are committed without outputs.

---

## 4. Definitions (carried over from Project 2, where they were validated)

| Term | Rule | Source |
|---|---|---|
| **Takeoff** | First year growth exceeds a threshold that falls as the base level rises; Project 2's calibrated parameters | Golder & Tellis (1997); Tellis, Stremersch & Yin (2003) |
| **Slowdown** | First year after takeoff that is followed by two lower years | Golder & Tellis (2004), as stated in Stremersch & Tellis (2004) |
| **Boom** | Takeoff followed by at least 3 growth years | Project 2 |
| **Spike** | Falls more than 50% from its peak within 2 years | Project 2 |
| **Lifecycle stage** | Emerging (no takeoff yet) / booming (after takeoff, before slowdown) / mature (after slowdown, level stable) / declining (two or more falling years after slowdown) | to be frozen in P1 |

---

## 5. Methods

| Step | Method | Answers |
|---|---|---|
| 1 | Takeoff and slowdown rules applied to every series | RQ0.1, RQ0.3 |
| 2 | **Bai–Perron multiple structural-break test** on growth rates, as an independent second dating method | RQ0.1 |
| 3 | **Phillips–Shi–Yu GSADF test** for explosive (bubble) behaviour, boom vs spike. Run only on series with roughly 15 or more observations, mainly IMF FAS. | RQ0.2 |
| 4 | **Sensitivity:** vary the takeoff threshold parameters and report a takeoff-year range, not just a single year | RQ0.1 |
| 5 | **Source agreement:** takeoff year across Passport, e-Conomy SEA and IMF (share within ±1 year, Spearman correlation) | RQ0.4 |
| 6 | **Timing regression:** OLS of takeoff year on GDP per capita and internet use at the start of the window, with sector fixed effects and robust SEs. **Kendall's W** for consistency of country order across sectors. | RQ0.5 |

All tests are frozen in P1 before outcome data are linked to any explanatory variable.

---

## 6. Validation

A **blind visual coding** round, as in Project 2. Anonymised charts of a sample of the new series (about 25–30, at least two per sector, mostly
Passport) are coded by hand, without knowing the country or sector, then compared with the rule.

* **Pass:** at least 75% agreement within ±1 year.
* **Fail:** one permitted recalibration, logged as a deviation.

---

## 7. Phases (stop for review after each)

| Phase | What | Output |
|---|---|---|
| **Q0-P0** | Literature note and data audit: how far back Passport goes, country coverage, verified GICS tags | Audit table with a go/no-go per sector |
| **Q0-P1** | Pre-registration | `PREREGISTRATION.md`: frozen definitions, tests and thresholds |
| **Q0-P2** | Build the panel | Clean sector × country × year dataset |
| **Q0-P3** | Blind coding check | Rule validated or recalibrated |
| **Q0-P4** | Catalogue and tests | Dated boom catalogue, break and bubble tests, robustness |
| **Q0-P5** | Write-up | Report, 20-year timeline chart, dashboard |

---

## 8. Outputs

* **Boom catalogue:** sector × country, with takeoff year and range, peak, status (boom / spike / none) and current
  lifecycle stage.
* **Timeline chart** of SEA's digital-economy booms.
* **Short report** positioned against e-Conomy SEA.

---

## 9. Known risks

1. **Takeoffs that predate the data** (Project 2's main problem). This is why the audit of Passport start years comes first.
2. **Short series** (about 10 years) give the break and bubble tests low power. They are used only where series are long enough.
3. **e-Conomy SEA figures are modelled estimates** that are revised. Handled by chain-linking and Passport cross-checks.
4. **Thin Tier B data.** Expect a descriptive treatment only.
5. **Data for lending, investment/insurance, remittances and crypto may stay thin** even after P0's search. Regulator
   data often cover only some countries (Indonesia, Thailand, Malaysia, Philippines are likeliest). Where the
   minimum-data rule fails, the result is "not testable", stated openly.
6. **Mixed frequencies** (monthly regulator data, annual Passport/IMF). Takeoff is dated on annual totals so all
   sectors are comparable; monthly data are used for the break and bubble tests.
5. **Licence limits** on what Passport-derived results can be published. Checked before the repo goes public.

---

## 10. Decisions log

| Date | Decision |
|---|---|
| 2026-10-11 | Focus on the digital economy (tech-enabled sectors), not GICS IT or hardware |
| 2026-10-11 | Period: as far back as the data allows |
| 2026-10-11 | Secondary layer kept, descriptive only (superseded) |
| 2026-10-11 | All 11 sectors get the full analysis, same rigour; P0 searches for monthly regulator data for the four weak-data sectors; uniform minimum-data rule ("not testable" where it fails) |
| 2026-10-11 | Blind coding round agreed for P3 |
| 2026-10-11 | One repo for the whole series; private GitHub repo during the build, public after a licence check |

---

## References (to be verified in P0)

* Golder, P. N. & Tellis, G. J. (1997). Will it ever fly? Modeling the takeoff of really new consumer durables. *Marketing Science*, 16(3).
* Golder, P. N. & Tellis, G. J. (2004). Growing, growing, gone. *Marketing Science*, 23(2).
* Tellis, G. J., Stremersch, S. & Yin, E. (2003). The international takeoff of new products. *Marketing Science*, 22(2).
* Stremersch, S. & Tellis, G. J. (2004). Understanding and managing international growth of new products. *IJRM*, 21(4).
* Van Everdingen, Y., Fok, D. & Stremersch, S. (2009). Modeling global spillover of new product takeoff. *Journal of Marketing Research*, 46(5).
* Comin, D. & Mestieri, M. (2018). If technology has arrived everywhere, why has income diverged? *AEJ: Macroeconomics*, 10(3).
* Bai, J. & Perron, P. (1998). Estimating and testing linear models with multiple structural changes. *Econometrica*, 66(1).
* Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*, 56(4).
* Google, Temasek & Bain & Company. *e-Conomy SEA 2025*.
