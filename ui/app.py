import streamlit as st
import pandas as pd
import joblib

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield · Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #04070f !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,200,150,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,120,255,0.07) 0%, transparent 60%),
        #04070f !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }

html, body, * { font-family: 'Syne', sans-serif !important; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,200,150,0.12);
    border: 1px solid rgba(0,200,150,0.3);
    color: #00c896;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    color: #f0f4ff;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin: 0 0 0.6rem;
}
.hero-title span {
    background: linear-gradient(135deg, #00c896 0%, #00a2ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #5a6880;
    font-size: 0.95rem;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.04em;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(0,200,150,0.22); }
.card-title {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00c896;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-title::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    background: #00c896;
    border-radius: 50%;
}

/* Input overrides */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8edf5 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(0,200,150,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,200,150,0.08) !important;
}
label, .stSelectbox label, .stNumberInput label {
    color: #8899aa !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em !important;
    font-weight: 600 !important;
}
[data-testid="stSelectbox"] svg { color: #5a6880 !important; }
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.06) !important;
    border: none !important;
    color: #8899aa !important;
    border-radius: 6px !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(0,200,150,0.15) !important;
    color: #00c896 !important;
}

/* Predict button */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #00c896 0%, #00a2ff 100%) !important;
    color: #04070f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(0,200,150,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(0,200,150,0.35) !important;
}

/* Result banners */
.result-fraud {
    background: linear-gradient(135deg, rgba(255,60,80,0.12), rgba(255,60,80,0.05));
    border: 1px solid rgba(255,60,80,0.4);
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    animation: slideIn 0.35s ease;
}
.result-legit {
    background: linear-gradient(135deg, rgba(0,200,150,0.12), rgba(0,200,150,0.05));
    border: 1px solid rgba(0,200,150,0.4);
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    animation: slideIn 0.35s ease;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-icon  { font-size: 2rem; line-height: 1; flex-shrink: 0; }
.result-label {
    font-size: 0.65rem;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.result-fraud .result-label { color: rgba(255,80,100,0.8); }
.result-legit .result-label { color: rgba(0,200,150,0.8); }
.result-verdict { font-size: 1.3rem; font-weight: 700; color: #f0f4ff; line-height: 1.2; }
.result-prob {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem;
    margin-top: 0.35rem;
}
.result-fraud .result-prob { color: rgba(255,120,130,0.9); }
.result-legit .result-prob { color: rgba(0,200,150,0.9); }
.prob-bar-wrap {
    margin-top: 0.9rem;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 5px;
    overflow: hidden;
}
.prob-bar-fill-fraud {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff3c50, #ff8c96);
}
.prob-bar-fill-legit {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #00c896, #00e6b0);
}

/* Stat chips */
.chips-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin: 0.4rem 0 2rem;
    justify-content: center;
}
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 0.28rem 0.85rem;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem;
    color: #5a6880;
    letter-spacing: 0.06em;
}
.chip b { color: #8899aa; }

/* Derived signals */
.derived-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.9rem; }
.derived-chip {
    flex: 1;
    min-width: 130px;
    background: rgba(0,200,150,0.05);
    border: 1px solid rgba(0,200,150,0.14);
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
}
.dc-label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem;
    color: #4a5e70;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.dc-value {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem;
    color: #00c896;
    font-weight: 700;
}

/* Awaiting placeholder */
.awaiting {
    border: 1px dashed rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    color: #2a3a4e;
}
.awaiting-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.awaiting-text {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #04070f; }
::-webkit-scrollbar-thumb { background: #1a2535; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m = joblib.load("models/lightgbm_fraud_model.pkl")
    f = joblib.load("models/model_features.pkl")
    return m, f

model, features = load_model()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ &nbsp; Powered by LightGBM</div>
    <h1 class="hero-title">Fraud<span>Shield</span></h1>
    <p class="hero-sub">Real-time transaction risk analysis</p>
</div>
<div class="chips-row">
    <div class="chip">Model <b>LightGBM</b></div>
    <div class="chip">Dataset <b>PaySim</b></div>
    <div class="chip">ROC-AUC <b>0.976</b></div>
    <div class="chip">Features <b>15</b></div>
</div>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    # Transaction Info
    st.markdown('<div class="card"><div class="card-title">Transaction Info</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        step   = st.number_input("Step (time index)", min_value=1, value=1)
        amount = st.number_input("Transaction Amount", min_value=0.0, value=0.0, format="%.2f")
    with c2:
        transaction_type = st.selectbox(
            "Transaction Type",
            ["CASH_IN", "CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"]
        )
        isFlaggedFraud = st.selectbox(
            "System Flagged Fraud", [0, 1],
            format_func=lambda x: "Yes ⚠️" if x == 1 else "No ✓"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Origin Account
    st.markdown('<div class="card"><div class="card-title">Origin Account</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        oldbalanceOrg  = st.number_input("Old Balance (Origin)",  min_value=0.0, value=0.0, format="%.2f")
    with c4:
        newbalanceOrig = st.number_input("New Balance (Origin)",  min_value=0.0, value=0.0, format="%.2f")
    st.markdown('</div>', unsafe_allow_html=True)

    # Destination Account
    st.markdown('<div class="card"><div class="card-title">Destination Account</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        oldbalanceDest = st.number_input("Old Balance (Destination)", min_value=0.0, value=0.0, format="%.2f")
    with c6:
        newbalanceDest = st.number_input("New Balance (Destination)", min_value=0.0, value=0.0, format="%.2f")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    # Derived signals (live-updating)
    balance_diff_orig         = oldbalanceOrg  - newbalanceOrig
    balance_diff_dest         = oldbalanceDest - newbalanceDest
    amount_balance_ratio_orig = amount / (balance_diff_orig + 1)
    balance_error             = (oldbalanceOrg - amount) - newbalanceOrig

    st.markdown('<div class="card"><div class="card-title">Derived Signals (Live)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="derived-row">
        <div class="derived-chip">
            <div class="dc-label">Orig Δ Balance</div>
            <div class="dc-value">{balance_diff_orig:,.2f}</div>
        </div>
        <div class="derived-chip">
            <div class="dc-label">Dest Δ Balance</div>
            <div class="dc-value">{balance_diff_dest:,.2f}</div>
        </div>
    </div>
    <div class="derived-row">
        <div class="derived-chip">
            <div class="dc-label">Amt / Balance Ratio</div>
            <div class="dc-value">{amount_balance_ratio_orig:,.4f}</div>
        </div>
        <div class="derived-chip">
            <div class="dc-label">Balance Error</div>
            <div class="dc-value">{balance_error:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # Predict button
    predict_clicked = st.button("⚡  Analyze Transaction", use_container_width=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # Result
    if predict_clicked:
        type_CASH_OUT = 1 if transaction_type == "CASH_OUT" else 0
        type_TRANSFER = 1 if transaction_type == "TRANSFER" else 0
        type_PAYMENT  = 1 if transaction_type == "PAYMENT"  else 0
        type_DEBIT    = 1 if transaction_type == "DEBIT"    else 0

        transaction = {
            "step":                      step,
            "amount":                    amount,
            "oldbalanceOrg":             oldbalanceOrg,
            "newbalanceOrig":            newbalanceOrig,
            "oldbalanceDest":            oldbalanceDest,
            "newbalanceDest":            newbalanceDest,
            "isFlaggedFraud":            isFlaggedFraud,
            "balance_diff_orig":         balance_diff_orig,
            "balance_diff_dest":         balance_diff_dest,
            "amount_balance_ratio_orig": amount_balance_ratio_orig,
            "balance_error":             balance_error,
            "type_CASH_OUT":             type_CASH_OUT,
            "type_TRANSFER":             type_TRANSFER,
            "type_PAYMENT":              type_PAYMENT,
            "type_DEBIT":                type_DEBIT,
        }

        df   = pd.DataFrame([transaction])[features]
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]
        pct  = prob * 100

        if pred == 1:
            st.markdown(f"""
            <div class="result-fraud">
                <div class="result-icon">🚨</div>
                <div style="width:100%">
                    <div class="result-label">Verdict</div>
                    <div class="result-verdict">Fraud Detected</div>
                    <div class="result-prob">Risk score: {pct:.2f}%</div>
                    <div class="prob-bar-wrap">
                        <div class="prob-bar-fill-fraud" style="width:{pct:.1f}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-legit">
                <div class="result-icon">✅</div>
                <div style="width:100%">
                    <div class="result-label">Verdict</div>
                    <div class="result-verdict">Legitimate Transaction</div>
                    <div class="result-prob">Risk score: {pct:.2f}%</div>
                    <div class="prob-bar-wrap">
                        <div class="prob-bar-fill-legit" style="width:{max(pct, 2):.1f}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="awaiting">
            <div class="awaiting-icon">🛡️</div>
            <div class="awaiting-text">AWAITING ANALYSIS</div>
        </div>
        """, unsafe_allow_html=True)