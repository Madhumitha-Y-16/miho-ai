import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import hashlib
import json
import re
import urllib.request
import urllib.parse
import urllib.error

from io import BytesIO
from html import escape

from modules.profiler import profile_dataset


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="MIHO AI | Beyond Data",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #EEF0FF !important;
    color: #172554 !important;
}

/* Main content */

[data-testid="stMain"] {
    background: #EEF0FF !important;
}

.block-container {
    max-width: 1600px;
    padding-top: 2rem;
    padding-bottom: 1rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #DFE6FF 0%, #E9EDFF 100%) !important;
    border-right: 1px solid #D2DBFF;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #172554 !important;
}

section[data-testid="stSidebar"] h3 {
    font-size: 20px;
    font-weight: 750;
}

/* Sidebar uploader */

section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.45);
    border: 1px dashed #9BAEFF;
    border-radius: 12px;
    padding: 8px;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background: transparent;
}

/* Upload button styling */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background-color: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background-color: #EEF0FF !important;
    color: #172554 !important;
}

/* Inputs */

.stTextInput input {
    background: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder {
    color: #8996BD !important;
}

/* HERO BANNER */

.miho-hero {
    position: relative;
    overflow: hidden;
    min-height: 250px;
    padding: 34px 38px;
    border-radius: 20px;
    background:
        radial-gradient(circle at 82% 50%, rgba(71, 126, 255, 0.55), transparent 28%),
        radial-gradient(circle at 95% 90%, rgba(139, 92, 246, 0.75), transparent 30%),
        linear-gradient(110deg, #101A48 0%, #172E78 58%, #4937B8 100%);
    box-shadow: 0 12px 30px rgba(55, 65, 160, 0.16);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
}

.miho-hero-content {
    position: relative;
    z-index: 2;
    max-width: 65%;
}

.miho-brand {
    color: #A99BFF;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.miho-hero-title {
    color: #FFFFFF !important;
    font-size: clamp(30px, 3.1vw, 48px);
    line-height: 1.12;
    font-weight: 800;
    margin: 0 0 16px 0;
}

.miho-hero-title span {
    color: #A88BFF !important;
}

.miho-hero-description {
    color: #E3E9FF !important;
    font-size: 16px;
    line-height: 1.65;
    max-width: 570px;
}

.miho-art {
    position: absolute;
    right: 4%;
    top: 18%;
    width: 34%;
    height: 70%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    opacity: 0.95;
}

.art-panel {
    background: rgba(28, 74, 190, 0.38);
    border: 1px solid rgba(126, 180, 255, 0.55);
    border-radius: 12px;
    padding: 13px;
    color: #CDEBFF;
    box-shadow: 0 0 18px rgba(37, 145, 255, 0.2);
    font-size: 22px;
    text-align: center;
}

.art-panel.small {
    transform: translateY(-28px);
}

.art-panel.large {
    font-size: 42px;
    padding: 23px;
    background: rgba(32, 91, 235, 0.45);
    box-shadow: 0 0 35px rgba(0, 183, 255, 0.4);
}

/* ACTION BUTTONS */

div.stButton > button {
    min-height: 58px;
    width: 100%;
    border-radius: 14px;
    border: 1px solid #D0D5FF;
    background: rgba(255,255,255,0.72);
    color: #172554 !important;
    font-size: 15px;
    font-weight: 700;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    border-color: #7664FF;
    background: #FFFFFF;
    color: #5140D8 !important;
    transform: translateY(-2px);
}

div.stButton > button:focus {
    box-shadow: 0 0 0 2px #A99BFF;
}

/* PRIMARY CHAT BUTTON */

div[data-testid="column"]:last-child div.stButton > button {
    background: linear-gradient(110deg, #6245E8, #7952E9);
    color: #FFFFFF !important;
    border: none;
}

div[data-testid="column"]:last-child div.stButton > button:hover {
    background: linear-gradient(110deg, #5134D5, #6840D8);
    color: #FFFFFF !important;
}

/* FEATURES PANEL */

.features-panel {
    background: rgba(255,255,255,0.75);
    border: 1px solid #D9DEFF;
    border-radius: 18px;
    padding: 18px;
    margin-top: 20px;
    box-shadow: 0 5px 18px rgba(68, 76, 160, 0.06);
}

.features-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding: 0 5px;
}

.features-heading h3 {
    color: #172554 !important;
    font-size: 20px;
    font-weight: 800;
    margin: 0;
}

.features-heading p {
    color: #4F5D91 !important;
    font-size: 13px;
    margin: 0;
}

.feature-card {
    background: rgba(239, 241, 255, 0.92);
    border: 1px solid #DCE1FF;
    border-radius: 13px;
    padding: 14px 13px;
    min-height: 76px;
    height: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.feature-icon {
    width: 40px;
    height: 40px;
    min-width: 40px;
    border-radius: 50%;
    background: #E4E5FF;
    color: #624BFF !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    font-weight: 700;
}

.feature-title {
    color: #172554 !important;
    font-size: 14px;
    font-weight: 750;
    margin-bottom: 4px;
}

.feature-description {
    color: #42517F !important;
    font-size: 12px;
    line-height: 1.4;
}

/* RESULT SECTIONS */

.result-panel {
    background: #FFFFFF;
    border: 1px solid #DCE1FF;
    border-radius: 15px;
    padding: 20px;
    margin-top: 22px;
}

.result-title {
    color: #172554 !important;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* METRICS */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE1FF;
    border-radius: 12px;
    padding: 13px;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #172554 !important;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #DCE1FF;
    border-radius: 10px;
}

/* FOOTER */

.miho-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    color: #6255D9 !important;
    font-size: 14px;
    font-weight: 700;
    padding: 22px 0 8px 0;
}

.miho-footer-line {
    height: 1px;
    background: #AAA4FF;
    flex: 1;
}

/* Hide Streamlit footer */

footer {
    visibility: hidden;
}


/* SIDEBAR - LIGHT THEME FIXES */

/* Uploaded file card */
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
    background: #FFFFFF !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 10px !important;
    color: #172554 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] span {
    color: #172554 !important;
}

/* Gemini API key visibility button */
section[data-testid="stSidebar"] [data-testid="stTextInput"] button {
    background: #FFFFFF !important;
    color: #6245E8 !important;
    border: 1px solid #C7D2FE !important;
}

section[data-testid="stSidebar"] [data-testid="stTextInput"] button:hover {
    background: #EEF0FF !important;
    color: #6245E8 !important;
}

/* Dataset success message */
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #E5F5EC !important;
    border: 1px solid #B7E4C7 !important;
    border-radius: 10px !important;
    color: #14532D !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] p,
section[data-testid="stSidebar"] [data-testid="stAlert"] span {
    color: #14532D !important;
}


/* COMPLETE SIDEBAR LIGHT THEME */

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #E5EAFF !important;
    color: #172554 !important;
}

/* All sidebar widget containers */
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] section,
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"],
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #FFFFFF !important;
    color: #172554 !important;
    border-color: #C7D2FE !important;
}

/* All text inputs */
section[data-testid="stSidebar"] input {
    background: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #C7D2FE !important;
}

/* Input visibility and action buttons */
section[data-testid="stSidebar"] button {
    background: #FFFFFF !important;
    color: #5140D8 !important;
    border: 1px solid #C7D2FE !important;
}

/* Uploaded file text */
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] * {
    color: #172554 !important;
}

/* Success message */
section[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #14532D !important;
}

/* Remove dark backgrounds from nested sidebar blocks */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    background-color: transparent;
}


</style>
""", unsafe_allow_html=True)



# ==========================================================
# 3. SESSION STATE
# ==========================================================

defaults = {
    "data": None,
    "filename": None,
    "file_signature": None,
    "active_action": None,
    "gemini_api_key": "",
    "chat_history": [],
    "cleaned_data": None,
    "cleaning_log": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# 4. DATA LOADING FUNCTIONS
# ==========================================================

def read_dataset(file_bytes, filename):

    name = filename.lower()

    if name.endswith(".csv"):

        for encoding in ["utf-8", "utf-8-sig", "cp1252", "latin1"]:
            try:
                return pd.read_csv(
                    BytesIO(file_bytes),
                    encoding=encoding
                )
            except UnicodeDecodeError:
                continue

        raise ValueError("Could not identify the CSV encoding.")

    elif name.endswith((".xlsx", ".xls")):

        return pd.read_excel(BytesIO(file_bytes))

    elif name.endswith(".json"):

        return pd.read_json(BytesIO(file_bytes))

    elif name.endswith(".xml"):

        return pd.read_xml(BytesIO(file_bytes))

    else:

        raise ValueError(
            "Unsupported file type. Upload CSV, Excel, JSON or XML."
        )


def load_from_url(url):

    url = url.strip()

    if not url:
        raise ValueError("Please enter a file URL.")

    # Convert Google Drive sharing URL to direct download URL

    drive_match = re.search(
        r"/file/d/([a-zA-Z0-9_-]+)",
        url
    )

    if drive_match:

        file_id = drive_match.group(1)

        url = (
            "https://drive.google.com/uc"
            f"?export=download&id={file_id}"
        )

    elif "drive.google.com" in url and "id=" in url:

        parsed = urllib.parse.urlparse(url)

        file_id = urllib.parse.parse_qs(
            parsed.query
        ).get("id", [None])[0]

        if file_id:
            url = (
                "https://drive.google.com/uc"
                f"?export=download&id={file_id}"
            )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=45) as response:

        file_bytes = response.read()

    if not file_bytes:
        raise ValueError("The URL returned an empty file.")

    path = urllib.parse.urlparse(url).path

    filename = path.split("/")[-1] or "miho_dataset.csv"

    if "." not in filename:
        filename = "miho_dataset.csv"

    df = read_dataset(file_bytes, filename)

    return df, filename, file_bytes


def store_dataset(df, filename, file_bytes):

    signature = hashlib.sha256(file_bytes).hexdigest()

    st.session_state.data = df
    st.session_state.filename = filename
    st.session_state.file_signature = signature
    st.session_state.active_action = None
    st.session_state.chat_history = []
    st.session_state.cleaned_data = None
    st.session_state.cleaning_log = []


# ==========================================================
# 5. GEMINI AI FUNCTION
# ==========================================================


def ask_gemini(prompt):

    api_key = st.session_state.get("gemini_api_key", "").strip()

    if not api_key:
        raise ValueError(
            "Enter your Gemini API key in the left sidebar first."
        )

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.5-flash-lite   :generateContent"
        f"?key={urllib.parse.quote(api_key)}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 8192
        }
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        candidates = result.get("candidates", [])

        if not candidates:
            raise RuntimeError(
                "Gemini did not return a valid response. Please try again."
            )

        candidate = candidates[0]

        finish_reason = candidate.get("finishReason", "UNKNOWN")

        parts = candidate.get("content", {}).get("parts", [])

        answer = "\n".join(
            part["text"]
            for part in parts
            if "text" in part
        ).strip()

        if finish_reason == "MAX_TOKENS":
            raise RuntimeError(
                "MIHO AI's response reached the token limit. "
                "The report may be incomplete. Please try again."
            )

        if not answer:
            raise RuntimeError(
                f"Gemini returned no text. Finish reason: {finish_reason}"
            )

        return answer

    except urllib.error.HTTPError as error:

        details = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Gemini API error ({error.code}): {details[:800]}"
        )

    except urllib.error.URLError as error:

        raise RuntimeError(
            f"Could not connect to Gemini: {error.reason}"
        )





def build_dataset_context(df):

    # --------------------------------------------------
    # 1. BASIC DATASET INFORMATION
    # --------------------------------------------------

    rows, columns = df.shape

    column_info = "\n".join(
        [f"{col}: {dtype}" for col, dtype in df.dtypes.items()]
    )

    # --------------------------------------------------
    # 2. MISSING VALUE ANALYSIS
    # --------------------------------------------------

    missing = df.isna().sum()

    missing_info = "\n".join(
        [
            f"{col}: {count} ({count / rows * 100:.2f}%)"
            for col, count in missing.items()
            if count > 0
        ]
    ) if rows > 0 else "Dataset has no rows."

    if not missing_info:
        missing_info = "No missing values found."

    # --------------------------------------------------
    # 3. NUMERICAL STATISTICAL SUMMARY
    # --------------------------------------------------

    numeric_df = df.select_dtypes(include="number").copy()

    identifier_columns = [
    column for column in numeric_df.columns
    if str(column).strip().lower() in [
        "row id",
        "id",
        "order id",
        "customer id",
        "product id" 
        "postal_code"]]

    numeric_df = numeric_df.drop(
    columns=identifier_columns,
    errors="ignore")

    if not numeric_df.empty:
        statistics = numeric_df.describe().round(2).to_string()
    else:
        statistics = "No numeric columns available."

    # --------------------------------------------------
    # 4. AUTOMATED BUSINESS METRICS
    # --------------------------------------------------

    business_metrics = []

    # Find columns without depending on capitalization
    column_lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    def get_numeric_column(column_name):

        actual_column = column_lookup.get(column_name.lower())

        if actual_column is None:
            return None

        return pd.to_numeric(
            df[actual_column],
            errors="coerce"
        ).dropna()

    def add_metric(label, value):

        business_metrics.append(
            f"{label}: {value}"
        )

    # Sales metrics
    sales = get_numeric_column("Sales")

    if sales is not None and not sales.empty:

        total_sales = sales.sum()

        add_metric(
            "Total Sales",
            f"{total_sales:,.2f}"
        )

        add_metric(
            "Average Sales",
            f"{sales.mean():,.2f}"
        )

        add_metric(
            "Median Sales",
            f"{sales.median():,.2f}"
        )

    else:
        total_sales = None

    # Profit metrics
    profit = get_numeric_column("Profit")

    if profit is not None and not profit.empty:

        total_profit = profit.sum()

        add_metric(
            "Total Profit",
            f"{total_profit:,.2f}"
        )

        add_metric(
            "Average Profit",
            f"{profit.mean():,.2f}"
        )

        add_metric(
            "Negative Profit Records",
            f"{(profit < 0).sum():,}"
        )

        add_metric(
            "Zero Profit Records",
            f"{(profit == 0).sum():,}"
        )

        add_metric(
            "Positive Profit Records",
            f"{(profit > 0).sum():,}"
        )

        # Profit margin
        if total_sales is not None and total_sales != 0:

            profit_margin = (
                total_profit / total_sales
            ) * 100

            add_metric(
                "Overall Profit Margin",
                f"{profit_margin:.2f}%"
            )

    # Quantity metrics
    quantity = get_numeric_column("Quantity")

    if quantity is not None and not quantity.empty:

        add_metric(
            "Total Quantity Sold",
            f"{quantity.sum():,.0f}"
        )

        add_metric(
            "Average Quantity",
            f"{quantity.mean():,.2f}"
        )

    # Discount metrics
    discount = get_numeric_column("Discount")

    if discount is not None and not discount.empty:

        add_metric(
            "Average Discount",
            f"{discount.mean() * 100:.2f}%"
        )

        add_metric(
            "Median Discount",
            f"{discount.median() * 100:.2f}%"
        )

        add_metric(
            "Maximum Discount",
            f"{discount.max() * 100:.2f}%"
        )

    # Shipping cost metrics
    shipping = get_numeric_column("Shipping Cost")

    if shipping is not None and not shipping.empty:

        add_metric(
            "Total Shipping Cost",
            f"{shipping.sum():,.2f}"
        )

        add_metric(
            "Average Shipping Cost",
            f"{shipping.mean():,.2f}"
        )

        add_metric(
            "Maximum Shipping Cost",
            f"{shipping.max():,.2f}"
        )

    if not business_metrics:
        business_metrics.append(
            "No recognized business metric columns found."
        )

    # --------------------------------------------------
    # 5. DUPLICATE RECORD ANALYSIS
    # --------------------------------------------------

    duplicate_count = int(df.duplicated().sum())

    # --------------------------------------------------
    # 6. SMALL DATASET SAMPLE
    # --------------------------------------------------

    sample = df.head(5).to_string(
        index=False,
        max_cols=20
    )

    # --------------------------------------------------
    # 7. FINAL DATASET CONTEXT
    # --------------------------------------------------

    return f"""
DATASET NAME: {st.session_state.filename}

DATASET DIMENSIONS:
Total Rows: {rows:,}
Total Columns: {columns:,}

COLUMN INFORMATION:
{column_info}

MISSING VALUE ANALYSIS:
{missing_info}

DUPLICATE ROWS:
{duplicate_count:,}

NUMERICAL STATISTICAL SUMMARY:
{statistics}

VERIFIED BUSINESS METRICS:
{chr(10).join(business_metrics)}

SAMPLE DATA (FIRST 5 ROWS):
{sample}

IMPORTANT:
Business metrics above were calculated directly from the
complete dataset using Pandas.

The sample data is provided only for understanding column
values and structure. Do not use it as evidence for
dataset-wide conclusions.
"""

def execute_chat_analysis(df, plan):

    allowed_aggregations = [
        "sum", "mean", "median", "min", "max", "count"
    ]

    group_by = plan.get("group_by", [])
    metric = plan.get("metric")
    aggregation = plan.get("aggregation", "sum")
    limit = plan.get("limit", 10)
    ascending = plan.get("ascending", False)

    # Validate the analysis plan

    if not isinstance(group_by, list):
        raise ValueError("Invalid grouping instructions.")

    if not group_by:
        raise ValueError("At least one grouping column is required.")

    if not all(column in df.columns for column in group_by):
        raise ValueError("One or more grouping columns do not exist.")

    if aggregation not in allowed_aggregations:
        raise ValueError("Unsupported calculation requested.")

    if aggregation != "count":

        if metric not in df.columns:
            raise ValueError("The requested metric column does not exist.")

        if not pd.api.types.is_numeric_dtype(df[metric]):
            raise ValueError("The metric column must contain numeric data.")

    # Perform calculation on the complete dataset

    grouped = df.groupby(
        group_by,
        dropna=False
    )

    if aggregation == "count":

        if metric:
            result = grouped[metric].count()
        else:
            result = grouped.size()

    else:

        result = grouped[metric].agg(aggregation)

    result = result.reset_index(name="Result")

    # Sort and limit results

    result = result.sort_values(
        "Result",
        ascending=ascending
    )

    limit = max(1, min(int(limit), 50))

    result = result.head(limit)

    return result.to_string(
    index=False,
    float_format=lambda value: f"{value:,.2f}")




# ==========================================================
# 6. PDF REPORT FUNCTION
# ==========================================================



def create_pdf_report(df):

    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import (
        getSampleStyleSheet,
        ParagraphStyle
    )
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image,
        PageBreak
    )

    from reportlab.lib.units import inch

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=40,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "MihoTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#252D69"),
        fontSize=21,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "MihoHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#252D69"),
        fontSize=13,
        spaceBefore=14,
        spaceAfter=9
    )

    subheading_style = ParagraphStyle(
        "MihoSubheading",
        parent=styles["Heading3"],
        textColor=colors.HexColor("#454B91"),
        fontSize=10,
        spaceBefore=8,
        spaceAfter=6
    )

    header_style = ParagraphStyle(
        "MihoTableHeader",
        parent=styles["Normal"],
        textColor=colors.white,
        fontSize=7,
        fontName="Helvetica-Bold",
        leading=9
    )

    body_style = ParagraphStyle(
        "MihoTableBody",
        parent=styles["Normal"],
        fontSize=7,
        leading=10
    )

    insight_style = ParagraphStyle(
        "MihoInsight",
        parent=styles["Normal"],
        fontSize=9,
        leading=14,
        spaceAfter=7
    )

    content = []

    # --------------------------------------------------
    # HELPER FUNCTIONS
    # --------------------------------------------------

    def add_heading(text):

        content.append(
            Paragraph(text, heading_style)
        )

    def add_table(rows, widths, numeric_cols=None):

        if numeric_cols is None:
            numeric_cols = []

        formatted_rows = []

        for row_index, row in enumerate(rows):

            formatted_row = []

            for value in row:

                style = (
                    header_style
                    if row_index == 0
                    else body_style
                )

                formatted_row.append(
                    Paragraph(
                        escape(str(value)),
                        style
                    )
                )

            formatted_rows.append(formatted_row)

        table = Table(
            formatted_rows,
            colWidths=widths,
            repeatRows=1,
            hAlign="LEFT"
        )

        table_styles = [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#252D69")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.lightgrey
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#F0F1FF")
                ]
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ]

        for col in numeric_cols:

            table_styles.append(
                (
                    "ALIGN",
                    (col, 1),
                    (col, -1),
                    "RIGHT"
                )
            )

        table.setStyle(
            TableStyle(table_styles)
        )

        content.append(table)
        content.append(Spacer(1, 12))

    def add_chart(figure):

        chart_buffer = BytesIO()

        figure.savefig(
            chart_buffer,
            format="png",
            dpi=160,
            bbox_inches="tight"
        )

        plt.close(figure)

        chart_buffer.seek(0)

        chart = Image(
            chart_buffer,
            width=500,
            height=250,
            kind="proportional"
        )

        content.append(chart)
        content.append(Spacer(1, 15))

    # --------------------------------------------------
    # 1. REPORT TITLE
    # --------------------------------------------------

    content.append(
        Paragraph(
            "MIHO AI - Data Analysis Report",
            title_style
        )
    )

    content.append(
        Paragraph(
            f"Dataset: {escape(str(st.session_state.filename))}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 18))

    rows, columns = df.shape

    # --------------------------------------------------
    # 2. DATASET OVERVIEW
    # --------------------------------------------------

    add_heading("01. Dataset Overview")

    overview = [
        ["Metric", "Value"],
        ["Total Rows", f"{rows:,}"],
        ["Total Columns", f"{columns:,}"],
        [
            "Missing Values",
            f"{int(df.isna().sum().sum()):,}"
        ],
        [
            "Duplicate Rows",
            f"{int(df.duplicated().sum()):,}"
        ]
    ]

    add_table(
        overview,
        [350, 175],
        numeric_cols=[1]
    )

    # --------------------------------------------------
    # 3. COLUMN INFORMATION
    # --------------------------------------------------

    add_heading("02. Column Information")

    column_data = [
        ["Column", "Data Type", "Missing Values"]
    ]

    for column in df.columns:

        column_data.append([
            str(column),
            str(df[column].dtype),
            f"{int(df[column].isna().sum()):,}"
        ])

    add_table(
        column_data,
        [290, 120, 115],
        numeric_cols=[2]
    )

    # --------------------------------------------------
    # 4. MISSING VALUE ANALYSIS
    # --------------------------------------------------

    add_heading("03. Missing Value Analysis")

    missing_data = [
        ["Column", "Missing Values", "Missing %"]
    ]

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        if missing_count > 0:

            percentage = (
                missing_count / rows * 100
                if rows > 0
                else 0
            )

            missing_data.append([
                str(column),
                f"{missing_count:,}",
                f"{percentage:.2f}%"
            ])

    if len(missing_data) > 1:

        add_table(
            missing_data,
            [290, 120, 115],
            numeric_cols=[1, 2]
        )

    else:

        content.append(
            Paragraph(
                "No missing values were detected.",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 12))

    # --------------------------------------------------
    # 5. STATISTICAL SUMMARY
    # --------------------------------------------------

    add_heading("04. Statistical Summary")

    numeric_df = df.select_dtypes(
        include="number"
    ).copy()

    # Exclude identifiers and location codes

    excluded_columns = [
        "id",
        "row id",
        "order id",
        "customer id",
        "product id",
        "postal code"
    ]

    identifier_columns = [
        column
        for column in numeric_df.columns
        if str(column).strip().lower() in excluded_columns
    ]

    numeric_df = numeric_df.drop(
        columns=identifier_columns,
        errors="ignore"
    )

    if not numeric_df.empty:

        statistics_data = [[
            "Column",
            "Mean",
            "Median",
            "Std Dev",
            "Minimum",
            "Maximum"
        ]]

        for column in numeric_df.columns:

            series = pd.to_numeric(
                numeric_df[column],
                errors="coerce"
            ).dropna()

            if series.empty:
                continue

            statistics_data.append([
                str(column),
                f"{series.mean():,.2f}",
                f"{series.median():,.2f}",
                f"{series.std():,.2f}",
                f"{series.min():,.2f}",
                f"{series.max():,.2f}"
            ])

        if len(statistics_data) > 1:

            add_table(
                statistics_data,
                [100, 85, 85, 85, 85, 85],
                numeric_cols=[1, 2, 3, 4, 5]
            )

    else:

        content.append(
            Paragraph(
                "No suitable numerical columns are available.",
                styles["Normal"]
            )
        )

    # --------------------------------------------------
    # 6. OUTLIER ANALYSIS
    # --------------------------------------------------

    add_heading("05. Outlier Analysis (IQR Method)")

    outlier_data = [[
        "Column",
        "Lower Bound",
        "Upper Bound",
        "Outliers",
        "Outlier %"
    ]]

    for column in numeric_df.columns:

        series = pd.to_numeric(
            numeric_df[column],
            errors="coerce"
        ).dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = int(
            (
                (series < lower_bound)
                | (series > upper_bound)
            ).sum()
        )

        outlier_percentage = (
            outlier_count / len(series) * 100
        )

        outlier_data.append([
            str(column),
            f"{lower_bound:,.2f}",
            f"{upper_bound:,.2f}",
            f"{outlier_count:,}",
            f"{outlier_percentage:.2f}%"
        ])

    if len(outlier_data) > 1:

        add_table(
            outlier_data,
            [105, 105, 105, 95, 115],
            numeric_cols=[1, 2, 3, 4]
        )

        content.append(
            Paragraph(
                "<b>Interpretation:</b> Outliers are observations "
                "outside the IQR boundaries. They may represent "
                "unusual but valid records and should be reviewed "
                "before deciding whether to remove or modify them.",
                insight_style
            )
        )

        content.append(Spacer(1, 10))

    else:

        content.append(
            Paragraph(
                "No suitable numerical columns are available "
                "for outlier analysis.",
                styles["Normal"]
            )
        )

    # --------------------------------------------------
    # 7. CATEGORY PERFORMANCE
    # --------------------------------------------------

    add_heading("06. Category Performance")

    category_results = None

    if "Category" in df.columns:

        category_results = {}

        for metric in ["Sales", "Profit"]:

            if metric not in df.columns:
                continue

            metric_values = pd.to_numeric(
                df[metric],
                errors="coerce"
            )

            category_summary = (
                df.assign(_metric=metric_values)
                .groupby(
                    "Category",
                    dropna=False
                )["_metric"]
                .sum()
                .sort_values(ascending=False)
            )

            category_results[metric] = category_summary

            total_metric = metric_values.sum()

            content.append(
                Paragraph(
                    f"Total {metric} by Category",
                    subheading_style
                )
            )

            category_data = [[
                "Category",
                f"Total {metric}",
                "Contribution %"
            ]]

            for category, value in category_summary.items():

                contribution = (
                    value / total_metric * 100
                    if total_metric != 0
                    else 0
                )

                category_data.append([
                    str(category),
                    f"{value:,.2f}",
                    f"{contribution:.2f}%"
                ])

            add_table(
                category_data,
                [190, 170, 165],
                numeric_cols=[1, 2]
            )

    else:

        content.append(
            Paragraph(
                "A Category column was not found in this dataset.",
                styles["Normal"]
            )
        )

    # --------------------------------------------------
    # 8. DATA VISUALIZATIONS
    # --------------------------------------------------

    add_heading("07. Data Visualizations")

    if category_results:

        for metric in ["Sales", "Profit"]:

            if metric not in category_results:
                continue

            chart_data = category_results[metric]

            fig, ax = plt.subplots(figsize=(9, 4.5))

            ax.bar(
                chart_data.index.astype(str),
                chart_data.values
            )

            ax.set_title(
                f"{metric} by Category",
                fontsize=14,
                fontweight="bold"
            )

            ax.set_xlabel("Category")
            ax.set_ylabel(f"Total {metric}")

            ax.tick_params(
                axis="x",
                labelrotation=15
            )

            ax.grid(
                axis="y",
                alpha=0.25
            )

            fig.tight_layout()

            add_chart(fig)

    else:

        content.append(
            Paragraph(
                "Category visualizations are unavailable "
                "for this dataset.",
                styles["Normal"]
            )
        )

    # --------------------------------------------------
    # 9. DATA QUALITY FINDINGS
    # --------------------------------------------------

    add_heading("08. Data Quality Findings")

    findings = []

    total_missing = int(
        df.isna().sum().sum()
    )

    duplicate_count = int(
        df.duplicated().sum()
    )

    total_cells = rows * columns

    if total_cells > 0:

        missing_percentage = (
            total_missing / total_cells * 100
        )

        findings.append(
            f"Missing cells: {total_missing:,} "
            f"({missing_percentage:.2f}% of all dataset cells)."
        )

    findings.append(
        f"Duplicate records detected: {duplicate_count:,}."
    )

    constant_columns = [
        str(column)
        for column in df.columns
        if df[column].nunique(dropna=True) <= 1
    ]

    if constant_columns:

        findings.append(
            "Columns with zero or one distinct non-missing value: "
            + ", ".join(constant_columns[:10])
        )

    for finding in findings:

        content.append(
            Paragraph(
                escape(finding),
                insight_style
            )
        )

    # --------------------------------------------------
    # 10. AI-GENERATED BUSINESS INSIGHTS
    # --------------------------------------------------

    add_heading("09. AI-Generated Business Insights")

    ai_summary = st.session_state.get(
        "ai_summary",
        ""
    )

    if ai_summary and ai_summary.strip():

        content.append(
            Paragraph(
                "The following insights reuse the AI-generated "
                "dataset analysis available in MIHO AI.",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 10))

        for line in ai_summary.splitlines():

            line = line.strip()

            if not line:
                content.append(Spacer(1, 5))
                continue

            # Remove basic Markdown heading markers

            clean_line = line.lstrip("#").strip()

            # Remove basic Markdown bullet markers

            if clean_line.startswith("- "):
                clean_line = "• " + clean_line[2:]

            elif clean_line.startswith("* "):
                clean_line = "• " + clean_line[2:]

            content.append(
                Paragraph(
                    escape(clean_line),
                    insight_style
                )
            )

    else:

        content.append(
            Paragraph(
                "No AI-generated summary is currently available. "
                "Generate an AI Summary in MIHO AI before creating "
                "the report to include business insights here.",
                insight_style
            )
        )

    # --------------------------------------------------
    # 11. REPORT FOOTER
    # --------------------------------------------------

    content.append(Spacer(1, 22))

    content.append(
        Paragraph(
            "MIHO AI | Beyond Data. Into Intelligence.",
            styles["Italic"]
        )
    )

    document.build(content)

    buffer.seek(0)

    return buffer.getvalue()



def create_analysis_plan(df, question):

    columns = list(df.columns)

    prompt = f"""
You are the question-understanding engine for MIHO AI.

Convert the user's data analysis question into a JSON analysis plan.

Available dataset columns:
{json.dumps(columns)}

User question:
{question}

Return ONLY valid JSON in this format:

{{
    "group_by": ["column_name"],
    "metric": "numeric_column_name",
    "aggregation": "sum",
    "limit": 10,
    "ascending": false
}}

Rules:
1. Use only columns that exist in the dataset.
2. For highest total sales, use Product Name as group_by,
   Sales as metric, and sum as aggregation.
3. For highest profit, use Profit as metric and sum as aggregation.
4. For quantity sold, use Quantity as metric.
5. For average questions, use mean.
6. For lowest questions, set ascending to true.
7. For counting records, use count.
8. Use exact column names.
9. Set limit between 1 and 50.
10. Return unsupported_question if the question cannot
    be represented by this calculation format.
11. Do not include explanations or Markdown.
"""

    # 1. Get Gemini response

    response = ask_gemini(prompt).strip()

    # 2. Extract JSON if Gemini adds Markdown

    if response.startswith("```"):

        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0].strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end < start:

        raise ValueError(
            "MIHO AI received an invalid analysis plan. Please try again."
        )

    response = response[start:end + 1]

    # 3. Parse JSON safely

    try:

        plan = json.loads(response)

    except json.JSONDecodeError:

        raise ValueError(
            "MIHO AI could not understand the analysis instructions. "
            "Please try asking your question differently."
        )

    if not isinstance(plan, dict):

        raise ValueError("Invalid analysis plan format.")

    if "error" in plan:

        raise ValueError(
            "This question is not supported by the current analysis engine."
        )

    # 4. Validate required fields

    required_fields = [
        "group_by",
        "metric",
        "aggregation",
        "limit",
        "ascending"
    ]

    if not all(field in plan for field in required_fields):

        raise ValueError("The analysis plan is missing required fields.")

    group_by = plan["group_by"]
    metric = plan["metric"]
    aggregation = plan["aggregation"]
    limit = plan["limit"]
    ascending = plan["ascending"]

    # 5. Validate grouping columns

    if (
        not isinstance(group_by, list)
        or not group_by
        or not all(isinstance(col, str) for col in group_by)
    ):

        raise ValueError("Invalid grouping columns.")

    if len(group_by) != len(set(group_by)):

        raise ValueError("Duplicate grouping columns are not allowed.")

    if not all(col in columns for col in group_by):

        raise ValueError("The requested grouping column does not exist.")

    # 6. Validate aggregation

    allowed_aggregations = [
        "sum", "mean", "median", "min", "max", "count"
    ]

    if aggregation not in allowed_aggregations:

        raise ValueError("Unsupported aggregation method.")

    # 7. Validate metric

    if aggregation == "count":

        if metric is not None:

            if not isinstance(metric, str) or metric not in columns:

                raise ValueError("Invalid counting column.")

    else:

        if not isinstance(metric, str) or metric not in columns:

            raise ValueError("The requested metric column does not exist.")

        if not pd.api.types.is_numeric_dtype(df[metric]):

            raise ValueError("The selected metric must be numeric.")

    # 8. Validate result limit

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 50
    ):

        raise ValueError("Result limit must be between 1 and 50.")

    # 9. Validate sorting direction

    if not isinstance(ascending, bool):

        raise ValueError("Invalid sorting direction.")

    return plan

# ==========================================================
# 7. LEFT SIDEBAR - UPLOAD AND API SETTINGS
# ==========================================================

with st.sidebar:

    st.markdown("### Upload your File")

    st.caption("Choose a file")

    uploaded_file = st.file_uploader(
        "Drag and drop your file here",
        type=["csv", "xlsx", "xls", "json", "xml"],
        help="Supported formats: CSV, XLSX, XLS, JSON and XML.",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        uploaded_bytes = uploaded_file.getvalue()

        uploaded_signature = hashlib.sha256(
            uploaded_bytes
        ).hexdigest()

        if uploaded_signature != st.session_state.file_signature:

            try:

                loaded_df = read_dataset(
                    uploaded_bytes,
                    uploaded_file.name
                )

                store_dataset(
                    loaded_df,
                    uploaded_file.name,
                    uploaded_bytes
                )

                st.success("Dataset loaded successfully.")

            except Exception as error:

                st.error(f"Upload error: {error}")

    st.write("")

    st.markdown("**Enter Google Drive File URL**")

    drive_url = st.text_input(
        "Google Drive URL",
        placeholder="https://drive.google.com/...",
        label_visibility="collapsed",
        key="drive_url"
    )

    if st.button(
        "Load from URL",
        use_container_width=True,
        key="load_url"
    ):

        try:

            with st.spinner("Loading your dataset..."):

                url_df, url_filename, url_bytes = load_from_url(
                    drive_url
                )

                store_dataset(
                    url_df,
                    url_filename,
                    url_bytes
                )

            st.success("Dataset loaded successfully.")

        except Exception as error:

            st.error(f"URL loading error: {error}")

    st.write("")

    st.markdown("**Enter Gemini API Key**")

    st.text_input(
        "Gemini API Key",
        placeholder="Enter your API key...",
        type="password",
        label_visibility="collapsed",
        key="gemini_api_key"
    )

    st.caption(
        "Your API key is kept in the current app session."
    )

    st.write("")

    if st.session_state.data is not None:

        st.divider()

        st.markdown("**Current Dataset**")

        st.write(st.session_state.filename)

        st.caption(
            f"{st.session_state.data.shape[0]:,} rows · "
            f"{st.session_state.data.shape[1]:,} columns"
        )


# ==========================================================
# 8. MAIN HERO BANNER
# ==========================================================

hero_html = """
<div class="miho-hero">

    <div class="miho-hero-content">

        <div class="miho-brand">
            MIHO AI ─────
        </div>

        <div class="miho-hero-title">
            Beyond Data.<br>
            Into <span>Intelligence.</span>
        </div>

        <div class="miho-hero-description">
            Transform raw data into meaningful insights.<br>
            Discover deeper patterns with the power of AI.
        </div>

    </div>

    <div class="miho-art">

        <div class="art-panel small">
            📈<br>
            <small>ANALYTICS</small>
        </div>

        <div class="art-panel large">
            ✨<br>
            <small>AI</small>
        </div>

        <div class="art-panel small">
            ▥<br>
            <small>INSIGHTS</small>
        </div>

    </div>

</div>
"""

st.html(hero_html)


# ==========================================================
# 9. FOUR MAIN ACTION BUTTONS
# ==========================================================

button1, button2, button3, button4 = st.columns(4)

with button1:

    if st.button(
        "▷  Perform EDA",
        use_container_width=True
    ):

        st.session_state.active_action = "eda"

with button2:

    if st.button(
        "▤  Summary Using AI",
        use_container_width=True
    ):

        st.session_state.active_action = "summary"

with button3:

    if st.button(
        "▥  Generate Report",
        use_container_width=True
    ):

        st.session_state.active_action = "report"

with button4:

    if st.button(
        "☁  Chat with data",
        use_container_width=True
    ):

        st.session_state.active_action = "chat"


# ==========================================================
# 10. MIHO FEATURES - APPROVED LAYOUT
# ==========================================================

features = [
    (
        "▤",
        "Module",
        "Complete data analysis platform"
    ),
    (
        "☆",
        "Features",
        "Powerful and easy-to-use tools"
    ),
    (
        "▤",
        "Data ingestion",
        "CSV, Excel, JSON, XML, URL loading"
    ),
    (
        "✦",
        "Data cleaning",
        "Approval-based missing values, duplicates, whitespace and types"
    ),
    (
        "▥",
        "Automated EDA",
        "Overview, quality, statistics, outliers and insights"
    ),
    (
        "⌁",
        "Visualization",
        "Histograms, bar charts, boxplots and correlation heatmaps"
    ),
    (
        "✧",
        "AI analytics",
        "Gemini-generated insights"
    ),
    (
        "☏",
        "Chat with data",
        "Natural-language questions"
    ),
    (
        "▦",
        "Dashboard",
        "KPIs, filters, interactive charts"
    ),
    (
        "▤",
        "Reporting",
        "PDF and downloadable reports"
    ),
    (
        "⬡",
        "Security",
        "API key protection, input validation"
    ),
    (
        "➤",
        "Deployment",
        "GitHub and Streamlit Cloud"
    )
]

st.html("""
<div class="features-panel">

    <div class="features-heading">
        <h3>✦ MIHO Features</h3>
        <p>Unlock the full potential of your data</p>
    </div>

</div>
""")

feature_columns = st.columns(3)

for index, (icon, title, description) in enumerate(features):

    with feature_columns[index % 3]:

        st.html(
            f"""
            <div class="feature-card">

                <div class="feature-icon">
                    {escape(icon)}
                </div>

                <div>
                    <div class="feature-title">
                        {escape(title)}
                    </div>

                    <div class="feature-description">
                        {escape(description)}
                    </div>
                </div>

            </div>
            """,
        )


# ==========================================================
# 11. DATASET STATUS
# ==========================================================

original_df = st.session_state.data
df = (
    st.session_state.cleaned_data.copy()
    if st.session_state.cleaned_data is not None
    else original_df
)

if df is None:

    st.info(
        "Please upload a dataset or load a file from a URL "
        "to start using MIHO AI."
    )

else:

    active_version = "cleaned working copy" if st.session_state.cleaned_data is not None else "original dataset"
    st.success(
        f"Dataset ready: {st.session_state.filename} "
        f"({df.shape[0]:,} rows × {df.shape[1]:,} columns) · Using {active_version}"
    )


# ==========================================================
# 12. MIHO AUTOMATED EDA + APPROVAL-BASED DATA CLEANING
# ==========================================================

if st.session_state.active_action == "eda":

    st.html(
        '<div class="result-panel">'
        '<div class="result-title">MIHO Automated EDA</div>'
        '</div>'
    )

    if df is None:
        st.warning("Upload a dataset first.")
    else:
        tabs = st.tabs([
            "Dataset Overview",
            "Missing Values",
            "Duplicates",
            "Statistical Summary",
            "Outliers",
            "Visualizations",
            "Key Insights",
            "Data Cleaning"
        ])

        # 1. DATASET OVERVIEW
        with tabs[0]:
            st.subheader("Dataset Overview")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Rows", f"{df.shape[0]:,}")
            m2.metric("Total Columns", f"{df.shape[1]:,}")
            m3.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
            m4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
            st.markdown("**Column names and data types**")
            # Keep the profiler's four-value return contract consistent.
            summary, column_report, numeric_report, whitespace_report = profile_dataset(df)
            column_report = column_report.drop(columns=["Constant Column"],errors="ignore")
            st.dataframe(column_report, use_container_width=True, hide_index=True)
            st.markdown("**Dataset preview**")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)

        # 2. MISSING VALUE ANALYSIS
        with tabs[1]:
            st.subheader("Missing Value Analysis")
            missing = pd.DataFrame({
                "Column": [str(c) for c in df.columns],
                "Missing Values": [int(df[c].isna().sum()) for c in df.columns],
                "Missing Percentage": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns]
            })
            missing = missing.sort_values("Missing Values", ascending=False)
            st.metric("Total Missing Cells", f"{int(df.isna().sum().sum()):,}")
            st.dataframe(missing, use_container_width=True, hide_index=True)
            if int(df.isna().sum().sum()) == 0:
                st.success("No missing values were detected.")

        # 3. DUPLICATE DETECTION
        with tabs[2]:
            st.subheader("Duplicate Detection")
            duplicate_count = int(df.duplicated().sum())
            d1, d2 = st.columns(2)
            d1.metric("Duplicate Rows", f"{duplicate_count:,}")
            d2.metric("Unique Rows", f"{len(df) - duplicate_count:,}")
            if duplicate_count:
                st.write("Preview of duplicate records:")
                st.dataframe(df.loc[df.duplicated(keep=False)].head(20), use_container_width=True)
                st.caption("No rows are removed here. Use the Data Cleaning tab to review and approve removal.")
            else:
                st.success("No duplicate rows were detected.")

        # 4. STATISTICAL SUMMARY
        with tabs[3]:
            st.subheader("Statistical Summary")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                stat_rows = []
                for column in numeric_cols:
                    values = pd.to_numeric(df[column], errors="coerce").dropna()
                    modes = values.mode()
                    stat_rows.append({
                        "Column": str(column),
                        "Mean": values.mean() if not values.empty else np.nan,
                        "Median": values.median() if not values.empty else np.nan,
                        "Mode": modes.iloc[0] if not modes.empty else np.nan,
                        "Minimum": values.min() if not values.empty else np.nan,
                        "Maximum": values.max() if not values.empty else np.nan,
                        "Standard Deviation": values.std() if len(values) > 1 else np.nan
                    })
                st.dataframe(pd.DataFrame(stat_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No numerical columns are available for numeric statistics.")
            categorical_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
            
        # 5. IQR OUTLIER DETECTION
        with tabs[4]:
            st.subheader("Outlier Detection - IQR Method")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            outlier_rows = []
            for column in numeric_cols:
                values = pd.to_numeric(df[column], errors="coerce").dropna()
                if len(values) < 4:
                    continue
                q1 = values.quantile(0.25)
                q3 = values.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                count = int(((values < lower) | (values > upper)).sum())
                outlier_rows.append({
                    "Column": str(column), "Q1": q1, "Q3": q3,
                    "IQR": iqr, "Lower Bound": lower,
                    "Upper Bound": upper, "Potential Outliers": count
                })
            if outlier_rows:
                outlier_table = pd.DataFrame(outlier_rows)
                st.dataframe(outlier_table, use_container_width=True, hide_index=True)
                st.caption("Outliers are flagged for review only. MIHO AI does not remove or change them automatically.")
            else:
                st.info("No eligible numeric columns were found for IQR outlier analysis.")

        # 6. DATA VISUALIZATION
        with tabs[5]:
            st.subheader("Data Visualization")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()

            if numeric_cols:
                selected_numeric = st.selectbox("Select a numerical column", numeric_cols, key="eda_numeric_v1")
                left, right = st.columns(2)
                with left:
                    hist = px.histogram(df, x=selected_numeric, title=f"Histogram - {selected_numeric}", template="plotly_white")
                    st.plotly_chart(hist, use_container_width=True)
                with right:
                    box = px.box(df, y=selected_numeric, title=f"Boxplot - {selected_numeric}", template="plotly_white")
                    st.plotly_chart(box, use_container_width=True)
            else:
                st.info("No numerical columns are available for histograms or boxplots.")

            if categorical_cols:
                selected_category = st.selectbox("Select a categorical column", categorical_cols, key="eda_category_v1")
                counts = (
                    df[selected_category].astype("string").fillna("(Missing)")
                    .value_counts().head(20).rename_axis("Category").reset_index(name="Count")
                )
                bar = px.bar(counts, x="Category", y="Count", title=f"Category counts - {selected_category}", template="plotly_white")
                st.plotly_chart(bar, use_container_width=True)
            else:
                st.info("No categorical columns are available for a bar chart.")

            if len(numeric_cols) >= 2:
                correlation = df[numeric_cols].corr(numeric_only=True)
                heatmap = px.imshow(
                    correlation, text_auto=".2f", aspect="auto",
                    color_continuous_scale="Purples", title="Correlation Heatmap"
                )
                st.plotly_chart(heatmap, use_container_width=True)
            else:
                st.info("At least two numerical columns are required for a correlation heatmap.")

        # 7. KEY INSIGHTS — COMPUTED FIRST, OPTIONAL GEMINI EXPLANATION
        with tabs[6]:
            st.subheader("Key Insights")
            insights = []
            rows, columns = df.shape
            insights.append(f"The dataset contains {rows:,} rows and {columns:,} columns.")
            missing_total = int(df.isna().sum().sum())
            missing_pct = (missing_total / (rows * columns) * 100) if rows and columns else 0
            insights.append(f"There are {missing_total:,} missing cells ({missing_pct:.2f}% of all cells).")
            duplicates = int(df.duplicated().sum())
            insights.append(f"The dataset contains {duplicates:,} duplicate rows.")
            if columns and rows:
                missing_by_col = df.isna().sum()
                if int(missing_by_col.max()) > 0:
                    top_missing_col = missing_by_col.idxmax()
                    insights.append(f"'{top_missing_col}' has the most missing values ({int(missing_by_col.max()):,}).")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            for column in numeric_cols:
                values = pd.to_numeric(df[column], errors="coerce").dropna()
                if len(values) >= 4:
                    q1, q3 = values.quantile(.25), values.quantile(.75)
                    iqr = q3 - q1
                    count = int(((values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)).sum()) if iqr != 0 else 0
                    if count:
                        insights.append(f"'{column}' has {count:,} potential IQR outlier(s).")
            categorical_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
            for column in categorical_cols[:3]:
                modes = df[column].mode(dropna=True)
                if not modes.empty:
                    count = int((df[column] == modes.iloc[0]).sum())
                    insights.append(f"The most common value in '{column}' is '{modes.iloc[0]}' ({count:,} rows).")
            if len(numeric_cols) >= 2:
                corr = df[numeric_cols].corr(numeric_only=True).abs()
                corr = corr.copy()
                corr_values = corr.to_numpy(copy=True)
                np.fill_diagonal(corr_values, np.nan)
                corr = pd.DataFrame(
                    corr_values,
                    index=corr.index,
                    columns=corr.columns
                )
                if corr.notna().any().any():
                    strongest = corr.stack().idxmax()
                    strength = float(corr.loc[strongest[0], strongest[1]])
                    insights.append(f"The strongest absolute numeric correlation is between '{strongest[0]}' and '{strongest[1]}' ({strength:.2f}). This is association, not proof of causation.")
            for item in insights:
                st.markdown(f"- {item}")

            if st.session_state.get("gemini_api_key", "").strip():
                if st.button("Explain these findings with Gemini", key="explain_eda_insights"):
                    try:
                        prompt = (
                            "You are MIHO AI, a careful data analyst. Explain the following computed findings "
                            "in plain English and identify practical implications. Do not invent facts.\n\n"
                            + "\n".join(f"- {item}" for item in insights)
                        )
                        with st.spinner("Gemini is explaining the computed findings..."):
                            explanation = ask_gemini(prompt)
                        st.markdown("### AI Explanation")
                        st.markdown(explanation)
                    except Exception as error:
                        st.error(f"Gemini explanation failed: {error}")
            else:
                st.caption("Add your Gemini API key in the sidebar to receive an AI explanation of these computed findings.")

        # 8. DATA CLEANING — ALL ACTIONS REQUIRE USER APPROVAL
        with tabs[7]:
            st.subheader("Approval-Based Data Cleaning")
            st.warning("MIHO AI never changes your uploaded original automatically. Review each preview and click the matching approval button to apply a change to the working copy.")
            st.caption("The original uploaded dataset remains available until you replace the file.")

            clean_df = df.copy()
            if st.session_state.cleaned_data is not None:
                st.info("You are editing the cleaned working copy.")
            else:
                st.info("You are editing a separate working copy. The uploaded original is unchanged.")

            # Missing-value treatment
            st.markdown("#### 1. Handle Missing Values")
            missing_columns = [c for c in clean_df.columns if clean_df[c].isna().any()]
            if missing_columns:
                miss_col = st.selectbox("Column", missing_columns, key="clean_missing_col")
                miss_method = st.selectbox(
                    "Treatment", ["Drop rows missing this column", "Fill with mean", "Fill with median", "Fill with mode", "Fill with fixed value"],
                    key="clean_missing_method"
                )
                fixed_value = st.text_input("Fixed value (used only for fixed-value treatment)", key="clean_fixed_value")
                preview_df = clean_df.copy()
                preview_error = None
                try:
                    if miss_method == "Drop rows missing this column":
                        preview_df = preview_df.dropna(subset=[miss_col])
                    elif miss_method == "Fill with mean":
                        if not pd.api.types.is_numeric_dtype(clean_df[miss_col]):
                            raise ValueError("Mean fill is available only for numeric columns.")
                        preview_df[miss_col] = preview_df[miss_col].fillna(clean_df[miss_col].mean())
                    elif miss_method == "Fill with median":
                        if not pd.api.types.is_numeric_dtype(clean_df[miss_col]):
                            raise ValueError("Median fill is available only for numeric columns.")
                        preview_df[miss_col] = preview_df[miss_col].fillna(clean_df[miss_col].median())
                    elif miss_method == "Fill with mode":
                        modes = clean_df[miss_col].mode(dropna=True)
                        if modes.empty:
                            raise ValueError("No non-missing mode is available for this column.")
                        preview_df[miss_col] = preview_df[miss_col].fillna(modes.iloc[0])
                    else:
                        fill_value = fixed_value
                        if pd.api.types.is_numeric_dtype(clean_df[miss_col]):
                            fill_value = pd.to_numeric(fixed_value, errors="raise")
                        preview_df[miss_col] = preview_df[miss_col].fillna(fill_value)
                    st.write(f"Missing values in **{miss_col}**: {int(clean_df[miss_col].isna().sum()):,} → {int(preview_df[miss_col].isna().sum()):,}")
                    st.write(f"Rows: {len(clean_df):,} → {len(preview_df):,}")
                    if st.button("Approve and apply missing-value treatment", key="approve_missing"):
                        st.session_state.cleaned_data = preview_df.copy()
                        st.session_state.cleaning_log.append(f"{miss_method} in column '{miss_col}'")
                        st.rerun()
                except Exception as error:
                    preview_error = str(error)
                if preview_error:
                    st.warning(preview_error)
            else:
                st.success("No missing values detected.")

            # Duplicate removal
            st.markdown("#### 2. Remove Duplicate Rows")
            duplicate_count = int(clean_df.duplicated().sum())
            st.write(f"Duplicate rows detected: **{duplicate_count:,}**")
            if duplicate_count:
                st.dataframe(clean_df.loc[clean_df.duplicated(keep=False)].head(10), use_container_width=True)
                st.caption(f"Preview: {len(clean_df):,} rows would become {len(clean_df.drop_duplicates()):,} rows.")
                if st.button("Approve and remove duplicate rows", key="approve_duplicates"):
                    st.session_state.cleaned_data = clean_df.drop_duplicates().copy()
                    st.session_state.cleaning_log.append(f"Removed {duplicate_count:,} duplicate rows")
                    st.rerun()
            else:
                st.success("No duplicate rows detected.")

            # Whitespace trimming
            st.markdown("#### 3. Trim Leading and Trailing Whitespace")
            string_columns = clean_df.select_dtypes(include=["object", "string"]).columns.tolist()
            if string_columns:
                trim_columns = st.multiselect("Text columns to trim", string_columns, default=string_columns, key="trim_columns")
                trim_preview = clean_df.copy()
                trim_counts = {}
                for column in trim_columns:
                    original_values = trim_preview[column].astype("string")
                    trimmed_values = original_values.str.strip()
                    trim_counts[column] = int((original_values != trimmed_values).sum())
                    trim_preview[column] = trimmed_values
                st.write(f"Values that would be trimmed: **{sum(trim_counts.values()):,}**")
                if trim_columns and st.button("Approve and trim whitespace", key="approve_trim"):
                    st.session_state.cleaned_data = trim_preview.copy()
                    st.session_state.cleaning_log.append(f"Trimmed whitespace in {len(trim_columns)} column(s)")
                    st.rerun()
            else:
                st.info("No text columns are available for whitespace trimming.")

            # Column-name standardization
            st.markdown("#### 4. Standardize Column Names")
            def standard_column_name(value):
                name = re.sub(r"[^0-9a-zA-Z]+", "_", str(value).strip().lower()).strip("_")
                return name or "column"
            proposed_names = []
            used_names = set()
            for column in clean_df.columns:
                base = standard_column_name(column)
                candidate = base
                suffix = 2
                while candidate in used_names:
                    candidate = f"{base}_{suffix}"
                    suffix += 1
                used_names.add(candidate)
                proposed_names.append(candidate)
            rename_preview = pd.DataFrame({"Current name": [str(c) for c in clean_df.columns], "Proposed name": proposed_names})
            st.dataframe(rename_preview, use_container_width=True, hide_index=True)
            if list(clean_df.columns) != proposed_names and st.button("Approve and standardize column names", key="approve_names"):
                renamed = clean_df.copy()
                renamed.columns = proposed_names
                st.session_state.cleaned_data = renamed
                st.session_state.cleaning_log.append("Standardized column names")
                st.rerun()
            elif list(clean_df.columns) == proposed_names:
                st.caption("Column names are already standardized.")

            # Type conversion
            st.markdown("#### 5. Convert Data Types")
            if len(clean_df.columns):
                type_column = st.selectbox("Column to convert", list(clean_df.columns), key="clean_type_column")
                type_target = st.selectbox("Convert to", ["string", "integer", "float", "datetime", "category"], key="clean_type_target")
                type_preview = None
                type_error = None
                try:
                    if type_target == "string":
                        type_preview = clean_df[type_column].astype("string")
                    elif type_target == "integer":
                        type_preview = pd.to_numeric(clean_df[type_column], errors="raise").astype("Int64")
                    elif type_target == "float":
                        type_preview = pd.to_numeric(clean_df[type_column], errors="raise").astype("float64")
                    elif type_target == "datetime":
                        type_preview = pd.to_datetime(clean_df[type_column], errors="raise")
                    else:
                        type_preview = clean_df[type_column].astype("category")
                    st.dataframe(pd.DataFrame({"Before": clean_df[type_column].astype("string").head(10), "After": type_preview.astype("string").head(10)}), use_container_width=True)
                    if st.button("Approve and convert data type", key="approve_dtype"):
                        converted = clean_df.copy()
                        converted[type_column] = type_preview
                        st.session_state.cleaned_data = converted
                        st.session_state.cleaning_log.append(f"Converted '{type_column}' to {type_target}")
                        st.rerun()
                except Exception as error:
                    type_error = str(error)
                if type_error:
                    st.warning(f"Type conversion preview failed: {type_error}")

            # Optional outlier treatment
            st.markdown("#### 6. Review and Handle Outliers")
            numeric_clean_cols = clean_df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_clean_cols:
                outlier_col = st.selectbox("Numeric column", numeric_clean_cols, key="clean_outlier_column")
                outlier_values = pd.to_numeric(clean_df[outlier_col], errors="coerce")
                valid = outlier_values.dropna()
                if len(valid) >= 4:
                    q1, q3 = valid.quantile(.25), valid.quantile(.75)
                    iqr = q3 - q1
                    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                    mask = (outlier_values < lower) | (outlier_values > upper)
                    outlier_n = int(mask.sum())
                    st.write(f"IQR bounds: **{lower:,.4f} to {upper:,.4f}** · Potential outliers: **{outlier_n:,}**")
                    outlier_method = st.selectbox("Treatment", ["Cap values to IQR bounds", "Remove rows containing these outliers"], key="clean_outlier_method")
                    if outlier_method == "Cap values to IQR bounds":
                        outlier_preview = clean_df.copy()
                        outlier_preview[outlier_col] = outlier_values.clip(lower, upper)
                    else:
                        outlier_preview = clean_df.loc[~mask].copy()
                    st.write(f"Rows: {len(clean_df):,} → {len(outlier_preview):,}")
                    if outlier_n and st.button("Approve and apply outlier treatment", key="approve_outliers"):
                        st.session_state.cleaned_data = outlier_preview.copy()
                        st.session_state.cleaning_log.append(f"{outlier_method} for '{outlier_col}' ({outlier_n:,} outliers)")
                        st.rerun()
                else:
                    st.info("At least four non-missing numeric values are needed for IQR treatment.")
            else:
                st.info("No numeric columns are available for outlier treatment.")

            # Current cleaning history, reset and export
            st.markdown("#### Cleaning History")
            if st.session_state.cleaning_log:
                for entry in st.session_state.cleaning_log:
                    st.markdown(f"- {entry}")
            else:
                st.caption("No cleaning operations have been applied yet.")

            reset_col, export_col = st.columns(2)
            with reset_col:
                if st.button("Reset working copy to original", key="reset_cleaning"):
                    st.session_state.cleaned_data = None
                    st.session_state.cleaning_log = []
                    st.rerun()
            with export_col:
                st.download_button(
                    "Download cleaned CSV",
                    data=clean_df.to_csv(index=False).encode("utf-8-sig"),
                    file_name="MIHO_AI_cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )


# ==========================================================
# 13. AI SUMMARY
# ==========================================================

elif st.session_state.active_action == "summary":

    st.markdown("## MIHO AI - Intelligent Dataset Summary")

    if df is None:

        st.warning("Upload a dataset first.")

    else:

        if st.button(
            "Generate AI Summary",
            key="generate_ai_summary"
        ):

            try:

                with st.spinner(
                    "MIHO AI is analyzing your dataset..."
                ):

                    context = build_dataset_context(df)

                    prompt = f"""
You are MIHO AI, an expert data analyst.

Do not include author names, prepared-by lines, job titles,
or professional designations in the report.

Your task is to prepare an accurate, evidence-based business
analysis report using the supplied dataset context.

IMPORTANT ANALYSIS RULES:

1. Use only information explicitly available in the dataset context.
2. Never invent numbers, statistics, trends, correlations, or findings.
3. Clearly distinguish:
   - Verified findings: directly supported by supplied statistics.
   - Potential explanations: reasonable hypotheses that require further analysis.
4. Do not make dataset-wide conclusions from the five sample rows.
5. Use numerical statistics only when they are explicitly provided.
6. If a requested analysis cannot be performed with the available
   information, clearly state that it requires further analysis.
7. Do not assume correlation means causation.
8. Do not recommend specific thresholds or policies without
   sufficient supporting evidence.
9. Use clear, professional, business-friendly language.
10. Avoid repeating the same finding in multiple sections.
11. Refer to individual dataset rows as records or transactions.
    Do not call them unique orders unless distinct Order IDs
    have been calculated.
12. Never assume that two financial metrics represent
    separate accounting expenses or revenues.
13. Do not interpret Shipping Cost as an additional deduction
    from Profit unless the dataset's accounting definitions
    establish this relationship.
14. Do not assume a currency symbol or currency denomination
    unless it is explicitly established by the dataset.
15. Ratios between financial metrics must be presented as
    mathematical comparisons, not automatically as evidence
    of business impact.
16. Do not claim that a particular factor causes losses
    without supporting calculations.
17. Use Markdown tables for numerical comparisons where
    appropriate.


REPORT STRUCTURE:

## 1. Dataset Overview
- Dataset name, number of rows and columns.
- Business domain and what the dataset represents.
- Important column groups.

## 2. Important Patterns
- Highlight patterns supported by the supplied statistics.
- Explain unusual values and distributions.
- Do not claim trends unless time-based evidence is available.

## 3. Data Quality Observations
- Missing values and their percentages.
- Data type concerns.
- Potential data quality issues.
- Clearly distinguish confirmed issues from possible issues.

## 4. Interesting Numerical Findings
- Explain important numerical statistics.
- Include mean, median, minimum, maximum and standard deviation
  where available.
- Explain what these numbers mean for the business.

## 5. Business Insights
For every insight:
- State the finding.
- Provide its supporting evidence.
- Explain its possible business impact.
- Label unsupported explanations as hypotheses.

## 6. Recommended Next Steps
- Recommend practical business analysis tasks.
- Connect every recommendation to an observed finding.
- Identify what additional calculations or data are needed.
- Do not present unverified assumptions as facts.

FINAL QUALITY CHECK:

Before producing the report, verify that:
- Every numerical claim comes from the supplied context.
- No sample observation is presented as a dataset-wide pattern.
- Facts and hypotheses are clearly separated.
- All six sections are included.
- Recommendations are relevant and actionable.

Do not invent facts. Use only the supplied dataset information.
Explain findings in clear language.

DATASET CONTEXT:

{context}
"""

                    answer = ask_gemini(prompt)

                st.session_state.ai_summary = answer

            except Exception as error:

                st.error(str(error))

        if st.session_state.get("ai_summary"):

            st.markdown("### AI-Generated Insights")

            st.markdown(
                st.session_state.ai_summary
            )


# ==========================================================
# 14. GENERATE REPORT
# ==========================================================

elif st.session_state.active_action == "report":

    st.markdown("## MIHO AI - Report Generation")

    if df is None:

        st.warning("Upload a dataset first.")

    else:

        st.write(
            "Generate a downloadable PDF report containing "
            "dataset information and column-level details."
        )

        if st.button(
            "Create PDF Report",
            key="create_pdf"
        ):

            try:

                with st.spinner("Creating your report..."):

                    pdf_data = create_pdf_report(df)

                st.download_button(
                    "Download MIHO AI Report",
                    data=pdf_data,
                    file_name="MIHO_AI_Data_Report.pdf",
                    mime="application/pdf"
                )

                st.success("Your PDF report is ready.")

            except Exception as error:

                st.error(f"Report generation error: {error}")


# ==========================================================
# 15. CHAT WITH DATA
# ==========================================================


elif st.session_state.active_action == "chat":

    st.markdown("## MIHO AI - Chat with your Data")

    if df is None:

        st.warning("Upload a dataset first.")

    else:

        st.write(
            "Ask questions about your dataset in natural language."
        )

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        question = st.chat_input(
            "Ask MIHO anything about your dataset..."
        )

        if question:

            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):

                st.markdown(question)

            try:

                with st.chat_message("assistant"):

                    with st.spinner(
                        "MIHO AI is analyzing your dataset..."
                    ):

                        # 1. Understand the question

                        plan = create_analysis_plan(
                            df,
                            question
                        )

                        # 2. Calculate using the full dataset

                        results = execute_chat_analysis(
                            df,
                            plan
                        )

                        # 3. Ask Gemini to explain verified results

                        prompt = f"""
You are MIHO AI, an intelligent data analyst.

Answer the user's question using ONLY the calculated
results provided below.

USER QUESTION:
{question}

CALCULATION PLAN:
{json.dumps(plan)}

VERIFIED RESULTS:
{results}

RULES:
- The results were calculated using the complete dataset.
- Do not invent or modify any numbers.
- Clearly state the answer.
- Explain the business meaning of the result.
- Use a table when comparing multiple results.
- If the result contains only a limited number of rows,
  do not claim it represents every possible group.
- Do not make unsupported business recommendations.
- Do not claim correlation or causation.
- Keep the answer clear and professional.
"""

                        answer = ask_gemini(prompt)

                    st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    f"MIHO AI could not process this question: {error}"
                )



# ==========================================================
# 16. FOOTER
# ==========================================================

st.html("""
<div class="miho-footer">
    <div class="miho-footer-line"></div>
    <div>MIHO AI | Beyond Data. Into Intelligence.</div>
    <div class="miho-footer-line"></div>
</div>
""")