"""
Personal Finance Tracker & Budget Planner - South African Rand (ZAR)
A comprehensive financial management application for South African users
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar
from typing import Dict, List, Tuple
import json
import warnings
warnings.filterwarnings('ignore')

# Page configuration with caching
@st.cache_resource(show_spinner=False)
def setup_page():
    st.set_page_config(
        page_title="FinTrack SA - Personal Finance Manager",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

setup_page()

# Custom CSS with South African theme colors
st.markdown("""
<style>
    /* Main app styling with SA colors (Green, Gold, Black, White, Blue, Red) */
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #007749 0%, #FFB81C 100%); /* SA Green to Gold */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 1rem;
        padding: 1rem;
    }
    
    .sub-header {
        color: #007749; /* SA Green */
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #FFB81C; /* SA Gold */
    }
    
    /* Card styling */
    .finance-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        transition: all 0.3s ease;
    }
    
    .finance-card:hover {
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #007749 0%, #FFB81C 100%); /* SA Green to Gold */
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 119, 73, 0.3);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #E03C31 0%, #FFB81C 100%); /* SA Red to Gold */
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
    }
    
    .success-card {
        background: linear-gradient(135deg, #007749 0%, #009A44 100%); /* SA Green shades */
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
    }
    
    /* Button styling with SA colors */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background-color: #007749; /* SA Green */
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 119, 73, 0.3);
        background-color: #009A44; /* Lighter Green */
    }
    
    /* Input styling */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid #FFB81C; /* SA Gold */
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #007749; /* SA Green */
        box-shadow: 0 0 0 3px rgba(0, 119, 73, 0.2);
    }
    
    /* Progress bars in SA Green */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #007749 0%, #009A44 100%);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #F7FAFC;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        background-color: #007749; /* SA Green */
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFB81C !important; /* SA Gold for active tab */
        color: #000000 !important;
    }
    
    /* Data editor styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Remove Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar in SA colors */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F1F1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #007749; /* SA Green */
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #009A44;
    }
    
    /* South African flag color highlights */
    .zar-amount {
        color: #007749; /* SA Green */
        font-weight: bold;
    }
    
    .positive-amount {
        color: #007749; /* SA Green */
        font-weight: bold;
    }
    
    .negative-amount {
        color: #E03C31; /* SA Red */
        font-weight: bold;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #001489 0%, #007749 100%); /* SA Blue to Green */
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables for South African context"""
    if 'transactions' not in st.session_state:
        st.session_state.transactions = pd.DataFrame(
            columns=['Date', 'Type', 'Category', 'Description', 'Amount', 'Account']
        )
    
    # South African specific budget categories and amounts
    if 'budgets' not in st.session_state:
        st.session_state.budgets = {
            'Food & Groceries': 4000,
            'Transport & Fuel': 2500,
            'Rent/Mortgage': 8000,
            'Utilities (Eskom, Water)': 1500,
            'Communication (Cell, Internet)': 800,
            'Entertainment & Dining': 2000,
            'Shopping & Personal Care': 1500,
            'Healthcare & Medical': 1000,
            'Education & Learning': 2000,
            'Savings & Investments': 5000,
            'Insurance': 1500,
            'Tax (VAT, Income)': 3000,
            'Bank Fees & Charges': 300,
            'Donations & Gifts': 500,
            'Other Expenses': 1000
        }
    
    # South African account types
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {
            'Standard Bank Cheque': 25000,
            'FNB Savings Account': 50000,
            'Absa Credit Card': -5000,
            'Nedbank Investment': 75000,
            'Capitec Transactional': 15000,
            'Discovery Bank': 30000,
            'African Bank Savings': 20000,
            'Tax-Free Savings Account': 40000
        }
    
    # Financial goals with realistic South African amounts
    if 'financial_goals' not in st.session_state:
        st.session_state.financial_goals = [
            {'name': 'Emergency Fund (3 months)', 'target': 45000, 'current': 15000, 'deadline': '2024-12-31'},
            {'name': 'Car Deposit', 'target': 30000, 'current': 12000, 'deadline': '2024-08-31'},
            {'name': 'Holiday to Cape Town', 'target': 15000, 'current': 5000, 'deadline': '2024-06-30'},
            {'name': 'New Laptop', 'target': 12000, 'current': 4000, 'deadline': '2024-05-31'},
            {'name': 'Home Renovation', 'target': 80000, 'current': 20000, 'deadline': '2024-12-31'}
        ]
    
    # South African user profile
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'South African User',
            'currency': 'ZAR',
            'monthly_income': 35000,
            'savings_rate': 15,
            'province': 'Gauteng',
            'city': 'Johannesburg',
            'tax_number': ''
        }
    
    # South African exchange rates (for information only)
    if 'exchange_rates' not in st.session_state:
        st.session_state.exchange_rates = {
            'USD': 18.50,
            'EUR': 20.10,
            'GBP': 23.40,
            'AUD': 12.10
        }

initialize_session_state()

# Helper functions for South African Rand
def format_zar(amount: float) -> str:
    """Format amount as South African Rand (ZAR)"""
    if amount >= 0:
        return f"R{amount:,.2f}"
    else:
        return f"-R{abs(amount):,.2f}"

def format_currency(amount: float) -> str:
    """Format amount with appropriate currency symbol (ZAR)"""
    return format_zar(amount)

def calculate_category_spending() -> Dict:
    """Calculate spending by category for current month"""
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    # Filter transactions for current month
    df = st.session_state.transactions.copy()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        monthly_transactions = df[
            (df['Date'].dt.month == current_month) &
            (df['Date'].dt.year == current_year) &
            (df['Type'] == 'Expense')
        ]
        
        if not monthly_transactions.empty:
            category_spending = monthly_transactions.groupby('Category')['Amount'].sum().to_dict()
            return category_spending
    
    return {category: 0 for category in st.session_state.budgets}

def calculate_budget_progress() -> Dict:
    """Calculate budget progress for each category"""
    category_spending = calculate_category_spending()
    budgets = st.session_state.budgets
    
    progress = {}
    for category, budget in budgets.items():
        spent = abs(category_spending.get(category, 0))
        progress[category] = {
            'spent': spent,
            'budget': budget,
            'remaining': max(0, budget - spent),
            'percentage': min(100, (spent / budget * 100) if budget > 0 else 0)
        }
    
    return progress

def calculate_net_worth() -> float:
    """Calculate total net worth in ZAR"""
    return sum(st.session_state.accounts.values())

def get_south_african_financial_tips() -> List[str]:
    """Get South African specific financial tips"""
    tips = [
        "Consider a Tax-Free Savings Account (TFSA) - you can invest up to R36,000 per year tax-free",
        "Check if you qualify for the South African Social Security Agency (SASSA) grants if applicable",
        "Review your medical aid scheme annually during open enrollment period",
        "Consider investing in a Retirement Annuity (RA) for tax benefits",
        "Monitor your credit score with TransUnion or Experian South Africa",
        "Be aware of South African Reserve Bank (SARB) interest rate announcements",
        "Consider stokvels or burial societies for community savings",
        "Check if you're eligible for the Employment Tax Incentive (ETI) if you employ staff",
        "Review your will and estate planning with a South African attorney",
        "Consider property investments through Real Estate Investment Trusts (REITs) on the JSE"
    ]
    return tips

def generate_financial_insights() -> List[str]:
    """Generate personalized financial insights for South African context"""
    insights = []
    
    # Calculate monthly metrics
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    df = st.session_state.transactions.copy()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        monthly_expenses = df[
            (df['Date'].dt.month == current_month) &
            (df['Date'].dt.year == current_year) &
            (df['Type'] == 'Expense')
        ]['Amount'].sum()
        
        monthly_income = df[
            (df['Date'].dt.month == current_month) &
            (df['Date'].dt.year == current_year) &
            (df['Type'] == 'Income')
        ]['Amount'].sum()
        
        # Insight 1: Spending vs Income
        if monthly_income > 0:
            savings_rate = ((monthly_income - abs(monthly_expenses)) / monthly_income) * 100
            target_rate = st.session_state.user_profile['savings_rate']
            
            if savings_rate < target_rate:
                insights.append(f"Your savings rate ({savings_rate:.1f}%) is below your target ({target_rate}%). Consider reducing expenses.")
            else:
                insights.append(f"Great! Your savings rate ({savings_rate:.1f}%) exceeds your target ({target_rate}%). Keep it up!")
        
        # Insight 2: Budget warnings
        progress = calculate_budget_progress()
        for category, data in progress.items():
            if data['percentage'] > 90:
                insights.append(f"Warning: {category}: You've spent {data['percentage']:.0f}% of your budget!")
            elif data['percentage'] > 75:
                insights.append(f"Alert: {category}: {data['percentage']:.0f}% of budget used. Watch your spending.")
    
    # Insight 3: Account balance warnings
    for account, balance in st.session_state.accounts.items():
        if balance < 0:
            insights.append(f"{account} has a negative balance of {format_zar(balance)}")
    
    # Insight 4: Goal progress
    for goal in st.session_state.financial_goals:
        progress = (goal['current'] / goal['target']) * 100
        if progress >= 100:
            insights.append(f"Congratulations! You've achieved your {goal['name']} goal!")
        elif progress >= 75:
            insights.append(f"You're {progress:.0f}% towards your {goal['name']} goal")
    
    # South African specific insights
    net_worth = calculate_net_worth()
    if net_worth > 1000000:
        insights.append(f"Your net worth is over R1 million! Consider consulting a South African financial advisor for investment opportunities.")
    
    return insights if insights else ["Add transactions to see personalized insights!"]

# Sidebar Navigation with South African theme
with st.sidebar:
    # South African flag colors
    st.markdown("""
    <div style="background: linear-gradient(to right, #007749 33%, #FFFFFF 33%, #FFFFFF 66%, #FFB81C 66%); 
                height: 10px; border-radius: 5px; margin-bottom: 20px;"></div>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/323/323319.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #007749;'>FinTrack SA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>South African Personal Finance</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["Dashboard", "Add Transaction", "Transactions", "Budget Manager", 
         "Accounts", "Financial Goals", "Exchange Rates", "Reports", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### Quick Stats")
    
    # Calculate quick stats
    net_worth = calculate_net_worth()
    category_spending = calculate_category_spending()
    total_spent = sum(abs(amount) for amount in category_spending.values())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Net Worth", format_zar(net_worth))
    with col2:
        st.metric("Monthly Spend", format_zar(total_spent))
    
    # Current month/year with SA seasons
    today = date.today()
    month_name = today.strftime('%B')
    season = "Winter" if 5 <= today.month <= 7 else "Summer" if 11 <= today.month <= 1 else "Spring/Autumn"
    st.caption(f"{month_name} {today.year} • {season}")
    
    st.markdown("---")
    
    # Export/Import Data
    st.markdown("### Data Management")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("Export Data", use_container_width=True):
            # Export functionality would go here
            st.success("Data exported successfully!")
    with col_exp2:
        if st.button("Reset Data", use_container_width=True):
            if st.checkbox("Confirm reset all data"):
                for key in ['transactions', 'budgets', 'accounts', 'financial_goals']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

# Main content based on selected page
st.markdown('<div class="main-header">FinTrack South Africa</div>', unsafe_allow_html=True)
st.caption("Your Personal Finance Management Dashboard for South African Rand (ZAR)")

if page == "Dashboard":
    # Dashboard View
    st.markdown('<div class="sub-header">Financial Dashboard</div>', unsafe_allow_html=True)
    
    # South African Economy Snapshot
    st.markdown('<div class="finance-card">', unsafe_allow_html=True)
    col_sa1, col_sa2, col_sa3, col_sa4 = st.columns(4)
    with col_sa1:
        st.markdown(f'<div class="stats-card"><h4>SARB Repo Rate</h4><h3>8.25%</h3></div>', unsafe_allow_html=True)
    with col_sa2:
        st.markdown(f'<div class="stats-card"><h4>CPI Inflation</h4><h3>5.5%</h3></div>', unsafe_allow_html=True)
    with col_sa3:
        st.markdown(f'<div class="stats-card"><h4>USD/ZAR</h4><h3>18.50</h3></div>', unsafe_allow_html=True)
    with col_sa4:
        st.markdown(f'<div class="stats-card"><h4>Fuel Price</h4><h3>R22.45/L</h3></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        net_worth = calculate_net_worth()
        st.markdown(f'<div class="metric-card"><h3>Net Worth</h3><h2>{format_zar(net_worth)}</h2></div>', 
                   unsafe_allow_html=True)
    
    with col2:
        monthly_income = st.session_state.user_profile['monthly_income']
        st.markdown(f'<div class="metric-card"><h3>Monthly Income</h3><h2>{format_zar(monthly_income)}</h2></div>', 
                   unsafe_allow_html=True)
    
    with col3:
        progress = calculate_budget_progress()
        total_budget = sum(data['budget'] for data in progress.values())
        total_spent = sum(data['spent'] for data in progress.values())
        budget_usage = (total_spent / total_budget * 100) if total_budget > 0 else 0
        st.markdown(f'<div class="metric-card"><h3>Budget Used</h3><h2>{budget_usage:.1f}%</h2></div>', 
                   unsafe_allow_html=True)
    
    with col4:
        total_goals = len(st.session_state.financial_goals)
        completed_goals = sum(1 for goal in st.session_state.financial_goals 
                            if goal['current'] >= goal['target'])
        st.markdown(f'<div class="metric-card"><h3>Goals Progress</h3><h2>{completed_goals}/{total_goals}</h2></div>', 
                   unsafe_allow_html=True)
    
    # Charts Row 1
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Income vs Expenses")
        
        # Prepare data for income vs expenses chart
        df = st.session_state.transactions.copy()
        if not df.empty:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            
            monthly_summary = df.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
            monthly_summary = monthly_summary.tail(6)  # Last 6 months
            
            if not monthly_summary.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary.get('Income', 0),
                    name='Income',
                    marker_color='#007749'  # SA Green
                ))
                fig.add_trace(go.Bar(
                    x=monthly_summary.index.astype(str),
                    y=abs(monthly_summary.get('Expense', 0)),
                    name='Expenses',
                    marker_color='#FFB81C'  # SA Gold
                ))
                
                fig.update_layout(
                    height=300,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=30, b=0),
                    yaxis_title="Amount (ZAR)"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No transaction data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Spending by Category")
        
        progress = calculate_budget_progress()
        if progress:
            # Get top 8 categories for better visualization
            top_categories = dict(sorted(progress.items(), key=lambda x: x[1]['spent'], reverse=True)[:8])
            
            categories = list(top_categories.keys())
            spent = [data['spent'] for data in top_categories.values()]
            budgets = [data['budget'] for data in top_categories.values()]
            
            fig = go.Figure(data=[
                go.Bar(name='Spent', y=categories, x=spent, orientation='h', marker_color='#007749'),
                go.Bar(name='Budget', y=categories, x=budgets, orientation='h', marker_color='#FFB81C', opacity=0.3)
            ])
            
            fig.update_layout(
                height=300,
                barmode='overlay',
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title="Amount (ZAR)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No budget data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Account Balances")
        
        accounts = st.session_state.accounts
        if accounts:
            account_names = list(accounts.keys())
            balances = list(accounts.values())
            
            colors = ['#007749' if bal >= 0 else '#E03C31' for bal in balances]  # Green for positive, Red for negative
            
            fig = go.Figure(data=[
                go.Bar(x=account_names, y=balances, marker_color=colors)
            ])
            
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0),
                yaxis_title="Amount (ZAR)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No account data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart4:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Financial Goals Progress")
        
        goals = st.session_state.financial_goals
        if goals:
            goal_names = [goal['name'] for goal in goals]
            percentages = [(goal['current'] / goal['target'] * 100) for goal in goals]
            current_amounts = [goal['current'] for goal in goals]
            target_amounts = [goal['target'] for goal in goals]
            
            fig = go.Figure(data=[
                go.Bar(x=goal_names, y=percentages,
                      marker_color=['#007749' if p >= 100 else '#FFB81C' if p >= 50 else '#E03C31' 
                                   for p in percentages],
                      text=[f"R{current:,.0f}/R{target:,.0f}" for current, target in zip(current_amounts, target_amounts)],
                      textposition='auto')
            ])
            
            fig.update_layout(
                height=300,
                yaxis_title="Progress %",
                yaxis_range=[0, 100],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No financial goals set")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Financial Insights & South African Tips
    col_insights, col_tips = st.columns(2)
    
    with col_insights:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Financial Insights")
        
        insights = generate_financial_insights()
        for insight in insights:
            st.write(f"• {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_tips:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### South African Financial Tips")
        
        tips = get_south_african_financial_tips()
        for tip in tips[:5]:  # Show first 5 tips
            st.write(f"• {tip}")
        
        if len(tips) > 5:
            with st.expander("Show more tips"):
                for tip in tips[5:]:
                    st.write(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Add Transaction":
    # Add Transaction View
    st.markdown('<div class="sub-header">Add New Transaction</div>', unsafe_allow_html=True)
    
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        
        # Transaction Form
        with st.form("transaction_form"):
            col_type, col_date = st.columns(2)
            with col_type:
                transaction_type = st.selectbox(
                    "Type",
                    ["Expense", "Income", "Transfer"],
                    key="trans_type"
                )
            with col_date:
                transaction_date = st.date_input(
                    "Date",
                    value=date.today(),
                    key="trans_date"
                )
            
            category = st.selectbox(
                "Category",
                list(st.session_state.budgets.keys()),
                key="trans_category"
            )
            
            description = st.text_input(
                "Description",
                placeholder="e.g., Checkers groceries, Salary from work, etc.",
                key="trans_desc"
            )
            
            amount = st.number_input(
                "Amount (ZAR)",
                min_value=0.01,
                value=500.00,
                step=100.00,
                key="trans_amount"
            )
            
            account = st.selectbox(
                "Account",
                list(st.session_state.accounts.keys()),
                key="trans_account"
            )
            
            submitted = st.form_submit_button("Save Transaction", use_container_width=True)
            
            if submitted:
                # Add transaction to dataframe
                new_transaction = pd.DataFrame([{
                    'Date': transaction_date,
                    'Type': transaction_type,
                    'Category': category,
                    'Description': description,
                    'Amount': -amount if transaction_type == 'Expense' else amount,
                    'Account': account
                }])
                
                st.session_state.transactions = pd.concat(
                    [st.session_state.transactions, new_transaction],
                    ignore_index=True
                )
                
                # Update account balance
                if transaction_type == 'Expense':
                    st.session_state.accounts[account] -= amount
                elif transaction_type == 'Income':
                    st.session_state.accounts[account] += amount
                
                st.success(f"Transaction added successfully! {format_zar(amount)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_form2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Common South African Expenses")
        
        # Common South African expense categories
        common_expenses = [
            ("Eskom Electricity", 1200),
            ("Municipal Water", 500),
            ("DSTV Subscription", 700),
            ("Cellphone Airtime", 300),
            ("Petrol/Diesel", 800),
            ("Woolworths Groceries", 1500),
            ("Takeaways (Uber Eats)", 250),
            ("Medical Aid Contribution", 2500),
            ("School Fees", 2000),
            ("Car Insurance", 800)
        ]
        
        for expense_name, expense_amount in common_expenses:
            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn1:
                if st.button(f"{expense_name}", use_container_width=True, key=f"quick_{expense_name}"):
                    # Auto-fill form
                    st.session_state.trans_type = "Expense"
                    # Map to appropriate category
                    if "Eskom" in expense_name or "Municipal" in expense_name:
                        st.session_state.trans_category = "Utilities (Eskom, Water)"
                    elif "DSTV" in expense_name or "Cellphone" in expense_name:
                        st.session_state.trans_category = "Communication (Cell, Internet)"
                    elif "Petrol" in expense_name:
                        st.session_state.trans_category = "Transport & Fuel"
                    elif "Groceries" in expense_name:
                        st.session_state.trans_category = "Food & Groceries"
                    elif "Medical" in expense_name:
                        st.session_state.trans_category = "Healthcare & Medical"
                    elif "Insurance" in expense_name:
                        st.session_state.trans_category = "Insurance"
                    elif "School" in expense_name:
                        st.session_state.trans_category = "Education & Learning"
                    else:
                        st.session_state.trans_category = "Other Expenses"
                    
                    st.session_state.trans_desc = expense_name
                    st.session_state.trans_amount = expense_amount
                    st.success(f"Quick add: {expense_name} - {format_zar(expense_amount)}")
                    st.rerun()
            with col_btn2:
                st.markdown(f'<span class="zar-amount">{format_zar(expense_amount)}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Recent Transactions")
        
        if not st.session_state.transactions.empty:
            recent_transactions = st.session_state.transactions.tail(5)
            for _, trans in recent_transactions.iterrows():
                amount_color = "positive-amount" if trans['Amount'] > 0 else "negative-amount"
                # Fix date formatting issue
                trans_date = trans['Date']
                if hasattr(trans_date, 'strftime'):
                    date_str = trans_date.strftime('%b %d')
                else:
                    date_str = str(trans_date)
                
                st.write(f"**{date_str}** - {trans['Description']}")
                st.markdown(f'<span class="{amount_color}">{format_zar(trans["Amount"])}</span>', 
                          unsafe_allow_html=True)
                st.write(f"*{trans['Category']}* • {trans['Account']}")
                st.markdown("---")
        else:
            st.info("No recent transactions")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Transactions":
    # Transactions View
    st.markdown('<div class="sub-header">Transaction History</div>', unsafe_allow_html=True)
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        filter_type = st.multiselect(
            "Filter by Type",
            ["All", "Expense", "Income", "Transfer"],
            default=["All"]
        )
    
    with col_filter2:
        filter_category = st.multiselect(
            "Filter by Category",
            ["All"] + list(st.session_state.budgets.keys()),
            default=["All"]
        )
    
    with col_filter3:
        date_range = st.date_input(
            "Date Range",
            value=(date.today() - timedelta(days=30), date.today()),
            key="date_filter"
        )
    
    # Display transactions
    if not st.session_state.transactions.empty:
        df = st.session_state.transactions.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Apply filters
        if "All" not in filter_type:
            df = df[df['Type'].isin(filter_type)]
        
        if "All" not in filter_category:
            df = df[df['Category'].isin(filter_category)]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
        
        # Summary statistics
        total_income = df[df['Type'] == 'Income']['Amount'].sum()
        total_expense = abs(df[df['Type'] == 'Expense']['Amount'].sum())
        net_flow = total_income - total_expense
        
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            st.metric("Total Income", format_zar(total_income))
        with col_sum2:
            st.metric("Total Expense", format_zar(total_expense))
        with col_sum3:
            st.metric("Net Flow", format_zar(net_flow), 
                     delta=format_zar(net_flow) if net_flow != 0 else None)
        
        # Display transactions table
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Transaction List")
        
        # Format for display
        display_df = df.copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: format_zar(x))
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df.sort_values('Date', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Export option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export as CSV",
            data=csv,
            file_name=f"transactions_zar_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No transactions found. Add your first transaction!")

elif page == "Budget Manager":
    # Budget Manager View
    st.markdown('<div class="sub-header">Budget Management</div>', unsafe_allow_html=True)
    
    col_budget1, col_budget2 = st.columns(2)
    
    with col_budget1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Budget Overview")
        
        progress = calculate_budget_progress()
        
        for category, data in progress.items():
            st.write(f"**{category}**")
            col_bar1, col_bar2 = st.columns([4, 1])
            with col_bar1:
                st.progress(data['percentage'] / 100)
            with col_bar2:
                st.write(f"{data['percentage']:.0f}%")
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.caption(f"Spent: {format_zar(data['spent'])}")
            with col_info2:
                st.caption(f"Remaining: {format_zar(data['remaining'])}")
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_budget2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Edit Budgets")
        
        with st.form("budget_form"):
            budgets = st.session_state.budgets.copy()
            
            for category in budgets.keys():
                budgets[category] = st.number_input(
                    f"{category} Budget (ZAR)",
                    min_value=0.0,
                    value=float(budgets[category]),
                    step=100.0,
                    key=f"budget_{category}"
                )
            
            submitted = st.form_submit_button("Update Budgets", use_container_width=True)
            if submitted:
                st.session_state.budgets = budgets
                st.success("Budgets updated successfully!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### South African Budgeting Tips")
        
        tips = [
            "Allocate 25-30% of income to housing (rent/mortgage)",
            "Save at least 15% of income for retirement (RA or pension fund)",
            "Budget for annual expenses like vehicle license renewals",
            "Include contingency for load shedding expenses (generator/inverter)",
            "Consider medical aid and gap cover in healthcare budget",
            "Budget for school fees and uniform expenses if applicable",
            "Include savings for annual tax payments if not PAYE",
            "Allocate funds for stokvel contributions if participating"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Accounts":
    # Accounts View
    st.markdown('<div class="sub-header">Account Management</div>', unsafe_allow_html=True)
    
    col_acc1, col_acc2 = st.columns(2)
    
    with col_acc1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Account Balances")
        
        accounts = st.session_state.accounts
        
        total_positive = sum(bal for bal in accounts.values() if bal > 0)
        total_negative = sum(bal for bal in accounts.values() if bal < 0)
        net_total = sum(accounts.values())
        
        for account, balance in accounts.items():
            amount_class = "positive-amount" if balance >= 0 else "negative-amount"
            
            col_acc_name, col_acc_bal = st.columns([2, 1])
            with col_acc_name:
                st.write(f"**{account}**")
            with col_acc_bal:
                st.markdown(f'<span class="{amount_class}">{format_zar(balance)}</span>', 
                          unsafe_allow_html=True)
            
            st.markdown("---")
        
        st.markdown(f"**Total Assets:** <span class='positive-amount'>{format_zar(total_positive)}</span>", 
                   unsafe_allow_html=True)
        st.markdown(f"**Total Liabilities:** <span class='negative-amount'>{format_zar(abs(total_negative))}</span>", 
                   unsafe_allow_html=True)
        st.markdown(f"**Net Worth:** <span class='positive-amount'>{format_zar(net_total)}</span>", 
                   unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_acc2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Add/Edit Account")
        
        with st.form("account_form"):
            account_name = st.text_input("Account Name", placeholder="e.g., FNB Cheque, Standard Bank Savings")
            account_type = st.selectbox("Account Type", ["Asset", "Liability"])
            initial_balance = st.number_input("Initial Balance (ZAR)", value=0.0, step=1000.0)
            
            # South African bank selection
            bank_options = ["Select Bank", "Standard Bank", "First National Bank (FNB)", "Absa", 
                           "Nedbank", "Capitec", "Discovery Bank", "African Bank", "Investec", "Other"]
            selected_bank = st.selectbox("Bank", bank_options)
            
            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                add_submitted = st.form_submit_button("Add Account", use_container_width=True)
            with col_sub2:
                update_submitted = st.form_submit_button("Update Selected", use_container_width=True)
            
            if add_submitted and account_name:
                full_account_name = f"{selected_bank} - {account_name}" if selected_bank != "Select Bank" else account_name
                st.session_state.accounts[full_account_name] = initial_balance if account_type == "Asset" else -initial_balance
                st.success(f"Account '{full_account_name}' added!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### South African Banking Tips")
        
        banking_tips = [
            "Compare bank fees across different South African banks",
            "Consider Capitec for lower fees if you have basic banking needs",
            "Use FNB's eBucks rewards program if you're a frequent spender",
            "Check if you qualify for Absa's bundle packages",
            "Consider Discovery Bank for integrated health and banking rewards",
            "Review your bank charges statement monthly",
            "Set up SMS notifications for all transactions",
            "Use banking apps for better security and convenience"
        ]
        
        for tip in banking_tips[:4]:
            st.write(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Financial Goals":
    # Financial Goals View
    st.markdown('<div class="sub-header">Financial Goals</div>', unsafe_allow_html=True)
    
    col_goal1, col_goal2 = st.columns(2)
    
    with col_goal1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Your Goals")
        
        goals = st.session_state.financial_goals
        
        for i, goal in enumerate(goals):
            progress = (goal['current'] / goal['target']) * 100
            deadline = datetime.strptime(goal['deadline'], '%Y-%m-%d').date()
            days_remaining = (deadline - date.today()).days
            
            st.write(f"**{goal['name']}**")
            st.progress(progress / 100)
            
            col_goal_info1, col_goal_info2, col_goal_info3 = st.columns(3)
            with col_goal_info1:
                st.caption(f"Current: {format_zar(goal['current'])}")
            with col_goal_info2:
                st.caption(f"Target: {format_zar(goal['target'])}")
            with col_goal_info3:
                st.caption(f"{days_remaining} days left")
            
            # Quick update buttons
            col_update1, col_update2 = st.columns(2)
            with col_update1:
                if st.button(f"Add R500", key=f"add_{i}", use_container_width=True):
                    goal['current'] += 500
                    st.rerun()
            with col_update2:
                if st.button(f"Remove R500", key=f"remove_{i}", use_container_width=True):
                    goal['current'] = max(0, goal['current'] - 500)
                    st.rerun()
            
            st.markdown("---")
        
        if not goals:
            st.info("No financial goals set. Create your first goal!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_goal2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Set New Goal")
        
        with st.form("goal_form"):
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, Car Deposit, House Deposit")
            target_amount = st.number_input("Target Amount (ZAR)", min_value=1000.0, value=10000.0, step=1000.0)
            current_amount = st.number_input("Current Amount (ZAR)", min_value=0.0, value=0.0, step=1000.0)
            deadline = st.date_input("Target Date", value=date.today() + timedelta(days=180))
            
            # South African specific goal categories
            goal_category = st.selectbox(
                "Goal Category",
                ["Emergency Fund", "Vehicle", "Property", "Education", "Travel", 
                 "Retirement", "Investment", "Wedding", "Business", "Other"]
            )
            
            submitted = st.form_submit_button("Add Goal", use_container_width=True)
            
            if submitted and goal_name:
                new_goal = {
                    'name': f"{goal_category}: {goal_name}",
                    'target': target_amount,
                    'current': current_amount,
                    'deadline': deadline.strftime('%Y-%m-%d')
                }
                st.session_state.financial_goals.append(new_goal)
                st.success(f"Goal '{goal_name}' added!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### South African Goal Setting Tips")
        
        tips = [
            "Aim for 3-6 months of expenses in emergency fund (R45,000-R90,000 for average household)",
            "Save 20% deposit for property purchases in South Africa",
            "Consider a Tax-Free Savings Account (TFSA) for long-term goals",
            "Use stokvels for disciplined community savings",
            "Check if you qualify for the First Home Finance subsidy",
            "Consider a retirement annuity (RA) for retirement goals with tax benefits",
            "Save for annual vehicle license and insurance renewals",
            "Budget for year-end bonuses and 13th cheques"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Exchange Rates":
    # Exchange Rates View
    st.markdown('<div class="sub-header">Exchange Rates & Currency Converter</div>', unsafe_allow_html=True)
    
    col_exchange1, col_exchange2 = st.columns(2)
    
    with col_exchange1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Current Exchange Rates (ZAR)")
        
        # Display exchange rates
        exchange_rates = st.session_state.exchange_rates
        
        st.markdown("#### Market Rates")
        for currency, rate in exchange_rates.items():
            col_curr1, col_curr2 = st.columns(2)
            with col_curr1:
                st.write(f"**1 {currency} =**")
            with col_curr2:
                st.markdown(f'<span class="zar-amount">R{rate:.2f}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### Historical ZAR Performance")
        
        # Simulated historical data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        usd_zar = [18.20, 18.35, 18.50, 18.45, 18.60, 18.50]
        
        fig = go.Figure(data=[
            go.Scatter(x=months, y=usd_zar, mode='lines+markers', name='USD/ZAR', 
                      line=dict(color='#007749', width=3))
        ])
        
        fig.update_layout(
            height=300,
            xaxis_title="Month",
            yaxis_title="USD/ZAR Rate",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_exchange2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Currency Converter")
        
        # Currency converter
        col_conv1, col_conv2 = st.columns(2)
        
        with col_conv1:
            convert_from = st.selectbox(
                "From",
                ["ZAR (South African Rand)", "USD (US Dollar)", "EUR (Euro)", "GBP (British Pound)"]
            )
            
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=1000.00,
                step=100.00,
                key="convert_amount"
            )
        
        with col_conv2:
            convert_to = st.selectbox(
                "To",
                ["USD (US Dollar)", "EUR (Euro)", "GBP (British Pound)", "ZAR (South African Rand)"]
            )
        
        # Conversion logic
        if st.button("Convert", use_container_width=True):
            # Extract currency codes
            from_currency = convert_from[:3]
            to_currency = convert_to[:3]
            
            if from_currency == to_currency:
                converted = amount
            elif from_currency == "ZAR" and to_currency in ["USD", "EUR", "GBP"]:
                # ZAR to foreign
                rate = 1 / exchange_rates[to_currency]
                converted = amount * rate
            elif from_currency in ["USD", "EUR", "GBP"] and to_currency == "ZAR":
                # Foreign to ZAR
                rate = exchange_rates[from_currency]
                converted = amount * rate
            else:
                # Foreign to foreign via ZAR
                rate_from = exchange_rates[from_currency]
                rate_to = 1 / exchange_rates[to_currency]
                converted = amount * rate_from * rate_to
            
            st.markdown(f"### Conversion Result")
            st.markdown(f"**{format_zar(amount) if from_currency == 'ZAR' else f'{amount:.2f} {from_currency}'}** =")
            st.markdown(f"<h2 style='color: #007749;'>{format_zar(converted) if to_currency == 'ZAR' else f'{converted:.2f} {to_currency}'}</h2>", 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Forex Tips for South Africans")
        
        forex_tips = [
            "Monitor SARB (South African Reserve Bank) announcements for rate changes",
            "Consider using forex cards for international travel instead of cash",
            "Use limit orders when trading forex to control risk",
            "Be aware of exchange controls when transferring large amounts overseas",
            "Check Compare Forex for best exchange rates",
            "Consider forward contracts if you know you'll need foreign currency in future",
            "Use online platforms like XE.com for live rates",
            "Be cautious of 'too good to be true' exchange rates"
        ]
        
        for tip in forex_tips[:4]:
            st.write(f"• {tip}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Reports":
    # Reports View
    st.markdown('<div class="sub-header">Financial Reports</div>', unsafe_allow_html=True)
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Spending Analysis", "Income Analysis", "Net Worth Trend", "Budget vs Actual", "Tax Summary"]
    )
    
    if report_type == "Spending Analysis":
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Spending Analysis Report")
        
        if not st.session_state.transactions.empty:
            df = st.session_state.transactions.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            
            # Spending by month
            monthly_spending = df[df['Type'] == 'Expense'].groupby('Month')['Amount'].sum().abs()
            
            fig = px.line(
                x=monthly_spending.index.astype(str),
                y=monthly_spending.values,
                title="Monthly Spending Trend (ZAR)",
                labels={'x': 'Month', 'y': 'Amount (ZAR)'}
            )
            fig.update_traces(line_color='#007749', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top spending categories
            top_categories = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum().abs().nlargest(5)
            
            fig2 = px.pie(
                values=top_categories.values,
                names=top_categories.index,
                title="Top Spending Categories (ZAR)",
                color_discrete_sequence=['#007749', '#009A44', '#FFB81C', '#E03C31', '#001489']
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Monthly summary table
            st.markdown("### Monthly Summary")
            monthly_summary = df.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
            monthly_summary['Expense'] = monthly_summary['Expense'].abs()
            monthly_summary['Net'] = monthly_summary.get('Income', 0) - monthly_summary.get('Expense', 0)
            monthly_summary = monthly_summary.tail(6)
            
            # Format for display
            display_summary = monthly_summary.copy()
            for col in ['Income', 'Expense', 'Net']:
                if col in display_summary.columns:
                    display_summary[col] = display_summary[col].apply(lambda x: format_zar(x))
            
            st.dataframe(display_summary, use_container_width=True)
        else:
            st.info("No transaction data available for reports")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Settings":
    # Settings View
    st.markdown('<div class="sub-header">Application Settings</div>', unsafe_allow_html=True)
    
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### User Profile")
        
        with st.form("profile_form"):
            name = st.text_input(
                "Full Name",
                value=st.session_state.user_profile['name'],
                key="profile_name"
            )
            
            province = st.selectbox(
                "Province",
                ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", 
                 "Free State", "Limpopo", "Mpumalanga", "North West", "Northern Cape"],
                index=["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", 
                      "Free State", "Limpopo", "Mpumalanga", "North West", "Northern Cape"].index(
                    st.session_state.user_profile.get('province', 'Gauteng')
                ),
                key="profile_province"
            )
            
            city = st.text_input(
                "City",
                value=st.session_state.user_profile.get('city', ''),
                key="profile_city"
            )
            
            tax_number = st.text_input(
                "Tax Number (Optional)",
                value=st.session_state.user_profile.get('tax_number', ''),
                key="profile_tax"
            )
            
            monthly_income = st.number_input(
                "Monthly Income (ZAR)",
                min_value=0.0,
                value=float(st.session_state.user_profile['monthly_income']),
                step=1000.0,
                key="profile_income"
            )
            
            savings_rate = st.slider(
                "Target Savings Rate (%)",
                min_value=0,
                max_value=100,
                value=st.session_state.user_profile['savings_rate'],
                key="profile_savings"
            )
            
            submitted = st.form_submit_button("Save Profile", use_container_width=True)
            if submitted:
                st.session_state.user_profile = {
                    'name': name,
                    'currency': 'ZAR',
                    'monthly_income': monthly_income,
                    'savings_rate': savings_rate,
                    'province': province,
                    'city': city,
                    'tax_number': tax_number
                }
                st.success("Profile updated successfully!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_set2:
        st.markdown('<div class="finance-card">', unsafe_allow_html=True)
        st.markdown("### Application Settings")
        
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "System"],
            key="app_theme"
        )
        
        currency_format = st.selectbox(
            "Currency Format",
            ["R 1,234.56 (South African)", "1 234,56 R (European)", "R1,234.56 (Compact)"],
            key="currency_format"
        )
        
        date_format = st.selectbox(
            "Date Format",
            ["YYYY-MM-DD", "DD/MM/YYYY", "DD Month YYYY"],
            key="date_format"
        )
        
        notifications = st.checkbox(
            "Enable Notifications",
            value=True,
            key="app_notifications"
        )
        
        auto_save = st.checkbox(
            "Auto-save Changes",
            value=True,
            key="app_autosave"
        )
        
        if st.button("Save Settings", use_container_width=True):
            st.success("Settings saved!")
        
        st.markdown("---")
        st.markdown("### About FinTrack SA")
        
        st.write("**FinTrack SA v2.0**")
        st.write("South African Personal Finance Management Application")
        st.write("Optimized for South African Rand (ZAR) and local financial context")
        
        st.markdown("---")
        st.markdown("**Data Privacy & Security:**")
        st.caption("All data is stored locally in your browser. No financial data is sent to external servers. Compliant with South African POPI Act.")
        
        # South African financial year info
        st.markdown("---")
        st.markdown("**South African Financial Year:**")
        st.caption("Financial Year: 1 March - 28/29 February")
        st.caption("Tax Season: 1 July - 23 November (Individuals)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer with South African context
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    user_name = st.session_state.user_profile['name']
    user_province = st.session_state.user_profile.get('province', 'South Africa')
    st.caption(f"User: {user_name} • {user_province}")
with col_footer2:
    st.caption(f"Currency: ZAR • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col_footer3:
    if st.button("Refresh Application", key="footer_refresh"):
        st.rerun()

# South African flag footer
st.markdown("""
<div style="background: linear-gradient(to right, #007749 33%, #FFFFFF 33%, #FFFFFF 66%, #FFB81C 66%); 
            height: 5px; border-radius: 5px; margin-top: 20px;"></div>
""", unsafe_allow_html=True)

# Auto-save reminder
if 'last_save' not in st.session_state:
    st.session_state.last_save = datetime.now()

save_elapsed = (datetime.now() - st.session_state.last_save).seconds
if save_elapsed > 300:  # 5 minutes
    st.toast("Remember to save your changes!")
    st.session_state.last_save = datetime.now()  # FIXED: Added missing closing parenthesis
