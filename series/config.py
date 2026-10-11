"""
Shared settings for the SEA Boom Series: paths, countries, sectors and indicator codes.
Every question (Q0–Q5) imports from here so all studies use the same definitions.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "public" / "raw"
MANUAL = DATA / "public" / "manual"
PROC = DATA / "public" / "processed"
LICENSED = DATA / "licensed"                       # git-ignored: Passport, Orbis (UCL licence)
for _d in (RAW, MANUAL, PROC, LICENSED):
    _d.mkdir(parents=True, exist_ok=True)

USER_AGENT = "sea-boom-series/0.1 (personal research)"

# ---------------------------------------------------------------------------
# Countries: all 11 SEA states. Tier = data richness, not inclusion.
# ---------------------------------------------------------------------------
COUNTRIES = {
    # iso3: (name, iso2, tier)
    "IDN": ("Indonesia", "ID", "A"),
    "MYS": ("Malaysia", "MY", "A"),
    "PHL": ("Philippines", "PH", "A"),
    "SGP": ("Singapore", "SG", "A"),
    "THA": ("Thailand", "TH", "A"),
    "VNM": ("Vietnam", "VN", "A"),
    "BRN": ("Brunei", "BN", "B"),
    "KHM": ("Cambodia", "KH", "B"),
    "LAO": ("Laos", "LA", "B"),
    "MMR": ("Myanmar", "MM", "B"),
    "TLS": ("Timor-Leste", "TL", "B"),
}
NAME = {k: v[0] for k, v in COUNTRIES.items()}
TIER_A = [k for k, v in COUNTRIES.items() if v[2] == "A"]

# ---------------------------------------------------------------------------
# Sectors (design §2.3). GICS sectors verified in P0 against the 2023 GICS revision:
# payment processors moved from IT to Financials; ride-hailing (Uber, Lyft) sits in Industrials.
# ---------------------------------------------------------------------------
SECTORS = {
    "ecommerce":        dict(label="E-commerce",                    gics="Consumer Discretionary", group="established"),
    "ride_hailing":     dict(label="Ride-hailing",                  gics="Industrials",            group="established"),
    "food_delivery":    dict(label="Food delivery",                 gics="Consumer Discretionary", group="established"),
    "online_travel":    dict(label="Online travel",                 gics="Consumer Discretionary", group="established"),
    "online_media":     dict(label="Online media",                  gics="Communication Services", group="established"),
    "digital_payments": dict(label="Digital payments / e-wallets",  gics="Financials",             group="established"),
    "digital_banking":  dict(label="Digital banking",               gics="Financials",             group="established"),
    "digital_lending":  dict(label="Digital lending / BNPL",        gics="Financials",             group="to_build"),
    "remittances":      dict(label="Digital remittances",           gics="Financials",             group="to_build"),
    "invest_insure":    dict(label="Digital investment & insurance", gics="Financials",            group="to_build"),
    "crypto":           dict(label="Crypto",                        gics="Financials",             group="to_build"),
}

# ---------------------------------------------------------------------------
# Indicator codes
# ---------------------------------------------------------------------------
# IMF Financial Access Survey: harmonised digital-finance outcomes
IMF_FAS_INDICATORS = {
    "FA65": "mobile_money_tx_value_pct_gdp",
    "FA66N": "mobile_money_tx_per_1000_adults",
    "FA67N": "mobile_money_accounts_per_1000_adults",
    "FA64": "mobile_money_balances_pct_gdp",
    "FA60": "mobile_internet_banking_tx_value_pct_gdp",
    "FA37N": "mobile_internet_banking_tx_per_1000_adults",
}

# World Bank Global Findex (survey waves 2011, 2014, 2017, 2021, 2024): cross-checks for the to-build sectors
FINDEX_INDICATORS = {
    "dig.acc": "digitally_enabled_account_pct",
    "fh2a": "received_intl_remittances_pct",
    "fh2": "received_domestic_remittances_pct",
    "fin20": "applied_loan_mobile_pct",
    "fin21": "received_loan_mobile_pct",
    "fin22a_1": "borrowed_mobile_money_provider_pct",
    "fin29": "received_domestic_remittances_into_account_pct",
    "fin26b": "bought_online_with_phone_or_internet_pct",
    "g20.made": "made_digital_payment_pct",
    "fin19": "paid_insurance_regularly_pct",
}

# World Bank WDI: denominators and context
WB_INDICATORS = {
    "NY.GDP.PCAP.PP.KD": "gdp_pc_ppp",
    "NY.GDP.MKTP.CN": "gdp_lcu",
    "IT.NET.USER.ZS": "internet_users_pct",
    "SP.POP.TOTL": "population",
    "BX.TRF.PWKR.DT.GD.ZS": "remittance_inflows_pct_gdp",
}

# e-Conomy SEA reports (each edition also reports back-years)
ECONSEA_REPORTS = {y: f"https://services.google.com/fh/files/misc/e_conomy_sea_{y}_report.pdf"
                   for y in range(2021, 2026)}
