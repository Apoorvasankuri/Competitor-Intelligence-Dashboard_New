import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="KEC Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS with KEC branding colors (Orange & Blue)
st.markdown("""
<style>
    /* KEC Brand Colors */
    :root {
        --color-primary: #FF8C00;        /* Orange */
        --color-primary-hover: #E67E00;
        --color-secondary: #1E3A8A;      /* Dark Blue */
        --color-accent: #0066cc;
        --color-bg: #f5f5f5;
        --color-text: #333;
        --color-border: #ddd;
        --color-card-bg: #fff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background-color: var(--color-bg);
    }
    
    /* Header with KEC branding */
    .kec-header {
        background: linear-gradient(90deg, var(--color-secondary) 0%, #1e3a8a 50%, #2563eb 100%);
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: -80px -80px 30px -80px;
        border-radius: 0;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .header-title {
        color: white;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        margin: 4px 0 0 0;
        font-size: 14px;
        font-weight: 400;
    }
    
    .header-logo {
        width: 50px;
        height: 50px;
        background: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: var(--color-primary);
        font-size: 20px;
    }
    
    /* Tab Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: white;
        border-bottom: 2px solid var(--color-border);
        display: flex;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 16px 32px;
        background-color: white;
        color: var(--color-text);
        border-bottom: 3px solid transparent;
        font-weight: 500;
        font-size: 14px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: var(--color-primary);
        border-bottom-color: var(--color-primary);
    }
    
    .stTabs [aria-selected="false"]:hover {
        background-color: #f9f9f9;
    }
    
    /* Main Content Area */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* KPI/Summary Cards */
    .summary-card {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .summary-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .summary-card h4 {
        margin: 0 0 8px 0;
        color: var(--color-secondary);
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .summary-card .value {
        font-size: 32px;
        font-weight: 800;
        color: var(--color-primary);
        margin: 8px 0;
    }
    
    .summary-card .subtext {
        font-size: 12px;
        color: #666;
    }
    
    /* Article Card in Executive Summary */
    .article-summary-card {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    
    .article-summary-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: var(--color-primary);
    }
    
    .article-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--color-text);
        margin: 0 0 12px 0;
    }
    
    .article-summary {
        font-size: 13px;
        color: #666;
        line-height: 1.6;
        margin: 0 0 16px 0;
    }
    
    .article-meta {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        font-size: 12px;
    }
    
    .article-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #e8f4f8;
        color: var(--color-accent);
        border-radius: 12px;
        font-weight: 500;
    }
    
    .article-badge.competitor {
        background-color: rgba(255, 140, 0, 0.1);
        color: var(--color-primary);
    }
    
    .article-badge.category {
        background-color: rgba(30, 58, 138, 0.1);
        color: var(--color-secondary);
    }
    
    .article-badge.sbu {
        background-color: rgba(0, 102, 204, 0.1);
        color: var(--color-accent);
    }
    
    .article-source {
        font-size: 12px;
        color: #999;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #f0f0f0;
    }
    
    /* Sub-tabs styling */
    .subtab-container {
        display: flex;
        gap: 8px;
        margin-top: 24px;
        border-bottom: 1px solid var(--color-border);
    }
    
    .subtab-button {
        padding: 12px 16px;
        background: white;
        border: none;
        border-bottom: 3px solid transparent;
        cursor: pointer;
        font-weight: 500;
        font-size: 13px;
        color: var(--color-text);
        transition: all 0.2s ease;
    }
    
    .subtab-button:hover {
        background-color: #f9f9f9;
    }
    
    .subtab-button.active {
        color: var(--color-primary);
        border-bottom-color: var(--color-primary);
    }
    
    /* Two-column layout for BU */
    .two-column-layout {
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 20px;
    }
    
    .sidebar {
        background-color: var(--color-card-bg);
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 0;
        height: fit-content;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .sidebar-section {
        border-bottom: 1px solid var(--color-border);
    }
    
    .sidebar-title {
        padding: 12px;
        font-weight: 600;
        background-color: #f9f9f9;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-item {
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sidebar-item:hover {
        background-color: #f9f9f9;
    }
    
    .sidebar-item.active {
        background-color: rgba(255, 140, 0, 0.1);
        color: var(--color-primary);
        font-weight: 600;
    }
    
    .sidebar-count {
        font-size: 11px;
        color: #999;
        background-color: #f0f0f0;
        padding: 2px 8px;
        border-radius: 10px;
    }
    
    /* Main content card */
    .main-content {
        background-color: var(--color-card-bg);
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Grid for competitor/BU cards */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 20px;
    }
    
    .grid-card {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .grid-card:hover {
        border-color: var(--color-primary);
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.2);
        transform: translateY(-2px);
    }
    
    .grid-card h4 {
        margin: 0 0 12px 0;
        font-size: 14px;
        font-weight: 600;
        color: var(--color-text);
    }
    
    .grid-card .badge {
        display: inline-block;
        background: var(--color-primary);
        color: white;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Articles table */
    .articles-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-size: 13px;
    }
    
    .articles-table thead {
        background-color: #f9f9f9;
    }
    
    .articles-table th {
        padding: 12px;
        text-align: left;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid var(--color-border);
    }
    
    .articles-table td {
        padding: 12px;
        border-bottom: 1px solid var(--color-border);
    }
    
    .articles-table tr:hover {
        background-color: #f9f9f9;
    }
    
    .article-link {
        color: var(--color-accent);
        text-decoration: none;
        font-weight: 500;
    }
    
    .article-link:hover {
        text-decoration: underline;
    }
    
    /* Filter section */
    .filter-container {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--color-primary);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: var(--color-primary-hover);
        transform: translateY(-2px);
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .two-column-layout {
            grid-template-columns: 1fr;
        }
        
        .sidebar {
            max-height: none;
        }
    }
    
    @media (max-width: 768px) {
        .card-grid {
            grid-template-columns: 1fr;
        }
        
        .kec-header {
            flex-direction: column;
            text-align: center;
        }
        
        .header-left {
            width: 100%;
            justify-content: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Executive Summary"

# ═════════════════════════════════════════════════════════════════
# HEADER WITH KEC LOGO AND BRANDING
# ═════════════════════════════════════════════════════════════════
st.markdown("""
<div class="kec-header">
    <div class="header-left">
        <div class="header-logo">K</div>
        <div>
            <h1 class="header-title">KEC Competitor Intelligence Dashboard</h1>
            <p class="header-caption">Competition & Industry Updates</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# LOAD DEFAULT EXCEL FILE
# ═════════════════════════════════════════════════════════════════
def load_default_data():
    """Load data from default Excel file stored in project"""
    excel_file_path = "competitor_data.xlsx"
    
    if os.path.exists(excel_file_path):
        try:
            df = pd.read_excel(excel_file_path)
            
            # Process data
            processed_data = []
            for _, row in df.iterrows():
                sbu_list = str(row.get('SBU', '')).split(',') if pd.notna(row.get('SBU')) else []
                sbu_list = [s.strip() for s in sbu_list if s.strip()]
                
                comp_list = str(row.get('Competitor', '')).split(',') if pd.notna(row.get('Competitor')) else []
                comp_list = [c.strip() for c in comp_list if c.strip()]
                
                processed_data.append({
                    'keyword': str(row.get('keyword', '')).strip(),
                    'newstitle': str(row.get('newstitle', 'No title'))[:200],
                    'summary': str(row.get('summary', 'No summary available'))[:300],
                    'sbu_list': sbu_list,
                    'competitor_list': comp_list,
                    'publishedate': pd.to_datetime(row.get('publishedate', datetime.now())),
                    'source': str(row.get('source', 'Unknown')).strip(),
                    'category': str(row.get('category', 'Other')).strip()
                })
            
            return pd.DataFrame(processed_data)
        except Exception as e:
            st.warning(f"Could not load default file: {str(e)}")
            return None
    return None

# Load default data
if st.session_state.raw_data is None:
    default_data = load_default_data()
    if default_data is not None:
        st.session_state.raw_data = default_data
        st.session_state.filtered_data = default_data.copy()

# ═════════════════════════════════════════════════════════════════
# MAIN TABS
# ═════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Competitors", "BU Specific", "Industry Updates"])

# ═════════════════════════════════════════════════════════════════
# EXECUTIVE SUMMARY TAB
# ═════════════════════════════════════════════════════════════════
with tab1:
    if st.session_state.raw_data is not None:
        df = st.session_state.raw_data
        
        # Major moves - top 6-7 articles
        st.markdown("### 📊 Major Moves")
        
        # Get top articles sorted by date
        top_articles = df.sort_values('publishedate', ascending=False).head(7)
        
        # Sub-tabs for filtering within Executive Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            unique_competitors = set()
            for comp_list in df['competitor_list']:
                unique_competitors.update(comp_list)
            competitor_filter = st.selectbox("Filter by Competitor", 
                                            ["All"] + sorted(list(unique_competitors)),
                                            key="exec_comp")
        
        with col2:
            unique_categories = df['category'].unique()
            category_filter = st.selectbox("Filter by News Type", 
                                          ["All"] + sorted(list(unique_categories)),
                                          key="exec_cat")
        
        with col3:
            unique_sbus = set()
            for sbu_list in df['sbu_list']:
                unique_sbus.update(sbu_list)
            sbu_filter = st.selectbox("Filter by BU", 
                                     ["All"] + sorted(list(unique_sbus)),
                                     key="exec_sbu")
        
        # Apply filters to top articles
        filtered_top = top_articles.copy()
        
        if competitor_filter != "All":
            filtered_top = filtered_top[filtered_top['competitor_list'].apply(lambda x: competitor_filter in x)]
        
        if category_filter != "All":
            filtered_top = filtered_top[filtered_top['category'] == category_filter]
        
        if sbu_filter != "All":
            filtered_top = filtered_top[filtered_top['sbu_list'].apply(lambda x: sbu_filter in x)]
        
        # Display article cards
        st.markdown("<br>", unsafe_allow_html=True)
        
        for idx, (_, article) in enumerate(filtered_top.iterrows()):
            competitor = article['competitor_list'][0] if article['competitor_list'] else "N/A"
            category = article['category']
            sbu = article['sbu_list'][0] if article['sbu_list'] else "N/A"
            
            st.markdown(f"""
            <div class="article-summary-card">
                <h4 class="article-title">{article['newstitle']}</h4>
                <p class="article-summary">{article['summary']}</p>
                <div class="article-meta">
                    <span class="article-badge competitor">{competitor}</span>
                    <span class="article-badge category">{category}</span>
                    <span class="article-badge sbu">{sbu}</span>
                </div>
                <div class="article-source">
                    <strong>{article['source']}</strong> • {article['publishedate'].strftime('%d %b %Y')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(filtered_top) == 0:
            st.info("No articles match your filters")
    else:
        st.info("Upload an Excel file to get started")

# ═════════════════════════════════════════════════════════════════
# COMPETITORS TAB
# ═════════════════════════════════════════════════════════════════
with tab2:
    if st.session_state.raw_data is not None:
        df = st.session_state.raw_data
        
        # Get unique competitors
        unique_competitors = set()
        for comp_list in df['competitor_list']:
            unique_competitors.update(comp_list)
        
        st.markdown("### 🏢 Competitors")
        
        # Create filter
        selected_competitor = st.selectbox("Select Competitor", 
                                          sorted(list(unique_competitors)),
                                          key="comp_select")
        
        # Filter articles for selected competitor
        comp_articles = df[df['competitor_list'].apply(lambda x: selected_competitor in x)]
        
        # Show summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card">
                <h4>Total Articles</h4>
                <div class="value">{len(comp_articles)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            unique_cats = comp_articles['category'].nunique()
            st.markdown(f"""
            <div class="summary-card">
                <h4>News Categories</h4>
                <div class="value">{unique_cats}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unique_sbus = set()
            for sbu_list in comp_articles['sbu_list']:
                unique_sbus.update(sbu_list)
            st.markdown(f"""
            <div class="summary-card">
                <h4>Business Units</h4>
                <div class="value">{len(unique_sbus)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            unique_sources = comp_articles['source'].nunique()
            st.markdown(f"""
            <div class="summary-card">
                <h4>News Sources</h4>
                <div class="value">{unique_sources}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show articles table
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"### 📰 Recent Articles - {selected_competitor}")
        
        if len(comp_articles) > 0:
            display_df = comp_articles[['newstitle', 'category', 'source', 'publishedate']].copy()
            display_df.columns = ['Title', 'Category', 'Source', 'Date']
            display_df['Date'] = display_df['Date'].dt.strftime('%d %b %Y')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No articles found for this competitor")
    else:
        st.info("Upload an Excel file to get started")

# ═════════════════════════════════════════════════════════════════
# BU SPECIFIC TAB
# ═════════════════════════════════════════════════════════════════
with tab3:
    if st.session_state.raw_data is not None:
        df = st.session_state.raw_data
        
        # Get unique SBUs
        unique_sbus = set()
        for sbu_list in df['sbu_list']:
            unique_sbus.update(sbu_list)
        
        st.markdown("### 🏭 Business Units")
        
        # Create filter
        selected_sbu = st.selectbox("Select Business Unit", 
                                   sorted(list(unique_sbus)),
                                   key="sbu_select")
        
        # Filter articles for selected SBU
        sbu_articles = df[df['sbu_list'].apply(lambda x: selected_sbu in x)]
        
        # Show summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card">
                <h4>Total Articles</h4>
                <div class="value">{len(sbu_articles)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            unique_competitors = set()
            for comp_list in sbu_articles['competitor_list']:
                unique_competitors.update(comp_list)
            st.markdown(f"""
            <div class="summary-card">
                <h4>Competitors Mentioned</h4>
                <div class="value">{len(unique_competitors)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unique_cats = sbu_articles['category'].nunique()
            st.markdown(f"""
            <div class="summary-card">
                <h4>News Categories</h4>
                <div class="value">{unique_cats}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            unique_sources = sbu_articles['source'].nunique()
            st.markdown(f"""
            <div class="summary-card">
                <h4>News Sources</h4>
                <div class="value">{unique_sources}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show articles table
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"### 📰 Recent Articles - {selected_sbu}")
        
        if len(sbu_articles) > 0:
            display_df = sbu_articles[['newstitle', 'category', 'competitor_list', 'source', 'publishedate']].copy()
            display_df['Competitors'] = display_df['competitor_list'].apply(lambda x: ', '.join(x) if x else 'N/A')
            display_df = display_df[['newstitle', 'category', 'Competitors', 'source', 'publishedate']]
            display_df.columns = ['Title', 'Category', 'Competitors', 'Source', 'Date']
            display_df['Date'] = display_df['Date'].dt.strftime('%d %b %Y')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No articles found for this BU")
    else:
        st.info("Upload an Excel file to get started")

# ═════════════════════════════════════════════════════════════════
# INDUSTRY UPDATES TAB
# ═════════════════════════════════════════════════════════════════
with tab4:
    if st.session_state.raw_data is not None:
        df = st.session_state.raw_data
        
        st.markdown("### 📰 All Industry Updates")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            unique_competitors = set()
            for comp_list in df['competitor_list']:
                unique_competitors.update(comp_list)
            competitor_filter = st.selectbox("Competitor", 
                                            ["All"] + sorted(list(unique_competitors)),
                                            key="ind_comp")
        
        with col2:
            unique_categories = df['category'].unique()
            category_filter = st.selectbox("News Type", 
                                          ["All"] + sorted(list(unique_categories)),
                                          key="ind_cat")
        
        with col3:
            unique_sbus = set()
            for sbu_list in df['sbu_list']:
                unique_sbus.update(sbu_list)
            sbu_filter = st.selectbox("Business Unit", 
                                     ["All"] + sorted(list(unique_sbus)),
                                     key="ind_sbu")
        
        # Apply filters
        filtered_df = df.copy()
        
        if competitor_filter != "All":
            filtered_df = filtered_df[filtered_df['competitor_list'].apply(lambda x: competitor_filter in x)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        if sbu_filter != "All":
            filtered_df = filtered_df[filtered_df['sbu_list'].apply(lambda x: sbu_filter in x)]
        
        # Sort by date
        filtered_df = filtered_df.sort_values('publishedate', ascending=False)
        
        # Show articles
        st.markdown("<br>", unsafe_allow_html=True)
        
        if len(filtered_df) > 0:
            display_df = filtered_df[['newstitle', 'category', 'competitor_list', 'source', 'publishedate']].copy()
            display_df['Competitors'] = display_df['competitor_list'].apply(lambda x: ', '.join(x) if x else 'N/A')
            display_df = display_df[['newstitle', 'category', 'Competitors', 'source', 'publishedate']]
            display_df.columns = ['Title', 'Category', 'Competitors', 'Source', 'Date']
            display_df['Date'] = display_df['Date'].dt.strftime('%d %b %Y')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No articles match your filters")
    else:
        st.info("Upload an Excel file to get started")

# ═════════════════════════════════════════════════════════════════
# FILE UPLOADER (Always at bottom)
# ═════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("Browse for files", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Process data
        processed_data = []
        for _, row in df.iterrows():
            sbu_list = str(row.get('SBU', '')).split(',') if pd.notna(row.get('SBU')) else []
            sbu_list = [s.strip() for s in sbu_list if s.strip()]
            
            comp_list = str(row.get('Competitor', '')).split(',') if pd.notna(row.get('Competitor')) else []
            comp_list = [c.strip() for c in comp_list if c.strip()]
            
            processed_data.append({
                'keyword': str(row.get('keyword', '')).strip(),
                'newstitle': str(row.get('newstitle', 'No title'))[:200],
                'summary': str(row.get('summary', 'No summary available'))[:300],
                'sbu_list': sbu_list,
                'competitor_list': comp_list,
                'publishedate': pd.to_datetime(row.get('publishedate', datetime.now())),
                'source': str(row.get('source', 'Unknown')).strip(),
                'category': str(row.get('category', 'Other')).strip()
            })
        
        st.session_state.raw_data = pd.DataFrame(processed_data)
        st.session_state.filtered_data = st.session_state.raw_data.copy()
        
        st.success(f"✅ File uploaded successfully! {len(processed_data)} articles loaded.")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

if st.session_state.raw_data is not None:
    total_articles = len(st.session_state.raw_data)
    st.markdown(f"<div style='color: #666; font-size: 12px; margin-top: 16px;'>✓ Data Synced • {total_articles} articles loaded</div>", unsafe_allow_html=True)
