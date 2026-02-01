"""
FinTrack SA – Personal Finance Tracker & Budget Planner (ZAR)
Improved interactive version – Feb 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import warnings

warnings.filterwarnings("ignore")

# ───────────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="FinTrack SA",
    page_icon="🇿🇦💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ───────────────────────────────────────────────
# CUSTOM CSS
# ───────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #007749, #FFB81C, #007749);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.1rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #004d38;
        font-size: 1.7rem;
        font-weight: 700;
        border-bottom: 3px solid #FFB81C;
        padding-bottom: 0.4rem;
        margin: 1.8rem 0 1.2rem;
    }
    .card {
        background: white;
        padding: 1.4rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #007749;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #009A44;
    }
    .delete-btn>button {
        background-color: #c0392b;
    }
    .delete-btn>button:hover {
        background-color: #a93226;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ───────────────────────────────────────────────
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["Date", "Type", "Category", "Description", "Amount", "Account"]
    )

if "budgets" not in st.session_state:
    st.session_state.budgets = {
        "Groceries & Food": 4500,
        "Transport & Fuel": 3000,
        "Rent / Bond": 9500,
        "Electricity & Water": 1800,
        "Airtime & Data": 600,
        "Entertainment & Dining": 1800,
        "Clothing & Personal": 1200,
        "Medical & Insurance": 2500,
        "Savings / Investments": 6000,
        "Debt Repayments": 2000,
        "Miscellaneous": 1500,
    }

if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "FNB Cheque": 18400,
        "Standard Bank Savings": 32000,
        "Capitec Savings": 12500,
        "Credit Card": -7800,
    }

if "goals" not in st.session_state:
    st.session_state.goals = [
        {"name": "Emergency Fund (3–6 months)", "target": 90000, "current": 22000},
        {"name": "December Holiday / Christmas", "target": 25000, "current": 8400},
        {"name": "New Laptop / PC", "target": 18000, "current": 3000},
    ]

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Manchidi",
        "monthly_income": 42000,
        "savings_rate_target": 20
    }

# Make sure Date column is datetime
if not st.session_state.transactions.empty:
    st.session_state.transactions["Date"] = pd.to_datetime(st.session_state.transactions["Date"])

# ───────────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────────
def fmt_zar(amount: float) -> str:
    if pd.isna(amount):
        return "—"
    return f"R{amount:,.2f}" if amount >= 0 else f"-R{abs(amount):,.2f}"

def calculate_net_worth() -> float:
    return sum(st.session_state.accounts.values())

def monthly_expenses() -> float:
    if st.session_state.transactions.empty:
        return 0.0
    return abs(st.session_state.transactions[
        st.session_state.transactions["Type"] == "Expense"
    ]["Amount"].sum())

def savings_score() -> int:
    income = st.session_state.profile["monthly_income"]
    if income <= 0:
        return 0
    expenses = monthly_expenses()
    score = 100 - int((expenses / income) * 100)
    return max(0, min(100, score))

# ───────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────
with st.sidebar:
    st.title("🇿🇦 FinTrack SA")
    page = st.radio(
        "Menu",
        ["🏠 Dashboard", "➕ Add Transaction", "📋 Transactions", "💸 Budgets", 
         "🏦 Accounts", "🎯 Goals", "⚙️ Settings"],
        index=0
    )
    st.divider()
    st.metric("Net Worth", fmt_zar(calculate_net_worth()))
    st.metric("Savings Score", f"{savings_score()}/100")
    st.caption("Personal finance • ZAR only")

# ───────────────────────────────────────────────
# HEADER
# ───────────────────────────────────────────────
st.markdown('<div class="main-header">FinTrack South Africa</div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
# PAGES
# ───────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown('<div class="sub-header">Financial Snapshot</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    c1.metric("Net Worth", fmt_zar(calculate_net_worth()), help="Total of all accounts")
    c2.metric("Monthly Income", fmt_zar(st.session_state.profile["monthly_income"]))
    c3.metric("This Month Spent", fmt_zar(monthly_expenses()))
    c4.metric("Savings Score", f"{savings_score()}/100")

    score = savings_score()
    if score < 40:
        st.error("🚨 **High spending alert** – you're spending significantly more than planned.")
    elif score < 65:
        st.warning("⚠️ Moderate spending – room to improve savings rate.")
    else:
        st.success("✅ **Strong financial discipline** – well done!")

    if not st.session_state.transactions.empty:
        df = st.session_state.transactions.copy()
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        col1, col2 = st.columns(2)

        with col1:
            exp = df[df["Type"] == "Expense"]
            if not exp.empty:
                fig_pie = px.pie(
                    exp, 
                    names="Category", 
                    values="Amount",
                    title="Expenses by Category (all time)",
                    hole=0.38,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            trend = df.groupby(["Month", "Type"])["Amount"].sum().reset_index()
            fig_trend = px.line(
                trend,
                x="Month",
                y="Amount",
                color="Type",
                title="Monthly Income vs Expenses Trend",
                markers=True
            )
            fig_trend.update_traces(line=dict(width=2.4))
            st.plotly_chart(fig_trend, use_container_width=True)


elif page == "➕ Add Transaction":
    st.markdown('<div class="sub-header">Record New Transaction</div>', unsafe_allow_html=True)

    with st.form("add_transaction", clear_on_submit=True):
        col1, col2 = st.columns([1, 1.6])

        with col1:
            t_type = st.selectbox("Type", ["Expense", "Income"], index=0)
            t_date = st.date_input("Date", value=date.today())

        with col2:
            category = st.selectbox("Category", list(st.session_state.budgets.keys()))
            description = st.text_input("Description", placeholder="e.g. Woolworths groceries, Salary Oct")

        colA, colB, colC = st.columns([1.2, 1.2, 1.4])
        with colA:
            amount = st.number_input("Amount (ZAR)", min_value=0.01, step=10.0, format="%.2f")
        with colB:
            account = st.selectbox("Account", list(st.session_state.accounts.keys()))
        with colC:
            st.write("")  # spacer
            st.write("")

        submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                signed_amount = -amount if t_type == "Expense" else amount
                new_row = {
                    "Date": pd.Timestamp(t_date),
                    "Type": t_type,
                    "Category": category,
                    "Description": description.strip() or "(no description)",
                    "Amount": signed_amount,
                    "Account": account
                }
                st.session_state.transactions = pd.concat([
                    st.session_state.transactions,
                    pd.DataFrame([new_row])
                ], ignore_index=True)

                # Update account balance
                st.session_state.accounts[account] += signed_amount

                st.success(f"Transaction saved • {t_type} of {fmt_zar(signed_amount)}")
                st.balloons()


elif page == "📋 Transactions":
    st.markdown('<div class="sub-header">All Transactions</div>', unsafe_allow_html=True)

    if st.session_state.transactions.empty:
        st.info("No transactions recorded yet. Add your first one!")
    else:
        df = st.session_state.transactions.sort_values("Date", ascending=False).copy()
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        # Quick filters
        c1, c2, c3 = st.columns([2, 1.4, 1])
        with c1:
            search = st.text_input("🔍 Search description or category", "")
        with c2:
            type_filter = st.selectbox("Type", ["All", "Income", "Expense"])
        with c3:
            if st.button("Clear Filters"):
                st.rerun()

        filtered = df.copy()
        if search:
            filtered = filtered[filtered.astype(str).apply(lambda row: row.str.contains(search, case=False)).any(axis=1)]
        if type_filter != "All":
            filtered = filtered[filtered["Type"] == type_filter]

        st.dataframe(
            filtered.style.format({
                "Amount": lambda x: fmt_zar(x)
            }),
            use_container_width=True,
            hide_index=True
        )

        # Delete functionality
        st.subheader("Delete Transaction")
        idx_to_delete = st.number_input("Row index to delete", min_value=0, max_value=len(df)-1, step=1)
        if st.button("🗑️ Delete selected row", type="primary"):
            if 0 <= idx_to_delete < len(st.session_state.transactions):
                row = st.session_state.transactions.iloc[idx_to_delete]
                st.session_state.accounts[row["Account"]] -= row["Amount"]  # reverse the effect
                st.session_state.transactions.drop(idx_to_delete, inplace=True)
                st.success("Transaction deleted")
                st.rerun()
            else:
                st.error("Invalid row index")


elif page == "💸 Budgets":
    st.markdown('<div class="sub-header">Budget vs Actual Spending</div>', unsafe_allow_html=True)

    if st.session_state.transactions.empty:
        st.info("No expenses recorded yet → budget bars will appear once you add transactions.")
    else:
        budget_data = []
        for cat, limit in st.session_state.budgets.items():
            spent = abs(st.session_state.transactions[
                (st.session_state.transactions["Category"] == cat) &
                (st.session_state.transactions["Type"] == "Expense")
            ]["Amount"].sum())

            pct = spent / limit if limit > 0 else 0
            status = "🔴 Over" if pct > 1.05 else "🟠 Near" if pct > 0.9 else "🟢 Good"

            budget_data.append({
                "Category": cat,
                "Budget": limit,
                "Spent": spent,
                "% Used": round(pct * 100, 1),
                "Status": status
            })

        bd = pd.DataFrame(budget_data).sort_values("% Used", ascending=False)

        st.dataframe(
            bd.style
               .format({"Budget": fmt_zar, "Spent": fmt_zar})
               .background_gradient(subset=["% Used"], cmap="YlOrRd", vmin=0, vmax=150)
               .highlight_between(subset=["% Used"], left=90, right=150, color="#fff3cd")
               .highlight_between(subset=["% Used"], left=150, color="#f8d7da"),
            use_container_width=True,
            hide_index=True
        )


elif page == "🏦 Accounts":
    st.markdown('<div class="sub-header">Your Accounts</div>', unsafe_allow_html=True)

    acc_df = pd.DataFrame.from_dict(
        st.session_state.accounts, orient="index", columns=["Balance"]
    ).reset_index().rename(columns={"index": "Account"})

    st.dataframe(
        acc_df.style.format({"Balance": fmt_zar}),
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Add / Edit Account", expanded=False):
        with st.form("account_form"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Account Name", placeholder="e.g. Nedbank Savings")
            balance = col2.number_input("Current Balance", value=0.0, step=100.0)
            if st.form_submit_button("Add / Update Account"):
                if name.strip():
                    st.session_state.accounts[name.strip()] = balance
                    st.success(f"Account '{name}' updated / added")
                    st.rerun()


elif page == "🎯 Goals":
    st.markdown('<div class="sub-header">Savings Goals Progress</div>', unsafe_allow_html=True)

    monthly_savings_capacity = (
        st.session_state.profile["monthly_income"] *
        (st.session_state.profile["savings_rate_target"] / 100)
    )

    for i, goal in enumerate(st.session_state.goals):
        with st.container():
            st.write(f"**{goal['name']}**")
            prog = min(100, goal["current"] / goal["target"] * 100) if goal["target"] > 0 else 0
            st.progress(prog / 100)

            remaining = max(0, goal["target"] - goal["current"])
            eta_months = int(remaining / monthly_savings_capacity) if monthly_savings_capacity > 0 else "—"
            eta_text = f"≈ {eta_months} months" if eta_months != "—" else "∞"

            st.caption(f"{fmt_zar(goal['current'])} / {fmt_zar(goal['target'])}  •  {eta_text}")

            colA, colB, colC = st.columns([1.4, 1, 1])
            with colA:
                add_amount = st.number_input("Contribute (R)", min_value=0, step=100, key=f"add_amt_{i}")
            with colB:
                if st.button("➕ Contribute", key=f"btn_add_{i}"):
                    if add_amount > 0:
                        goal["current"] += add_amount
                        st.success(f"Added R{add_amount:,} to {goal['name']}")
                        st.rerun()
            with colC:
                if st.button("Reset", key=f"reset_{i}"):
                    goal["current"] = 0
                    st.rerun()

            st.markdown("---")


elif page == "⚙️ Settings":
    st.markdown('<div class="sub-header">Profile & Preferences</div>', unsafe_allow_html=True)

    with st.form("profile_settings"):
        name = st.text_input("Your Name", value=st.session_state.profile["name"])
        income = st.number_input("Monthly Take-home Income (ZAR)", value=float(st.session_state.profile["monthly_income"]), step=500.0)
        savings_rate = st.slider("Target Savings Rate (%)", 0, 60, st.session_state.profile["savings_rate_target"])

        if st.form_submit_button("Save Settings"):
            st.session_state.profile.update({
                "name": name.strip() or "User",
                "monthly_income": max(0, income),
                "savings_rate_target": savings_rate
            })
            st.success("Profile updated successfully!")
            st.rerun()

st.caption("FinTrack SA  •  Personal finance dashboard for South Africans  •  v0.2 improved")
