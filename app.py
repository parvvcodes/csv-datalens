import io
import base64
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, Image,
)


st.set_page_config(page_title="CSV DataLens", layout="wide")


st.markdown("""
<style>
    body { 
            background-color: #020817; 
        }

    .box {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #111827, #020617);
        border: 1px solid #1e293b;
        box-shadow: 0 0 20px rgba(34,197,94,0.15);
        margin-bottom: 25px;
    }
            
    .box h1 { 
            color: #22c55e; 
            font-size: 42px; 
            margin-bottom: 5px; 
        }
            
    .box p {
             color: #94a3b8; 
            font-size: 15px; 
        }

    .card {
        background: #07111f;
        padding: 24px;
        border-radius: 20px;
        text-align: left;
        border: 1px solid #1f2937;
        position: relative;
        box-shadow: 0 0 12px rgba(0,0,0,0.35);
    }
            
    .card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 4px;
        border-radius: 20px 20px 0 0;
        background: var(--topcolor);
    }
            
    .card-title {
        color: #64748b;
        font-size: 13px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
            
    .card-value { 
            color: #ffffff; 
            font-size: 42px; 
            font-weight: 700; 
        }

    .table-container {
        background: #07111f;
        padding: 16px;
        border-radius: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 0 12px rgba(0,0,0,0.35);
        overflow-x: auto;
        margin-top: 20px;
    }
            
    .data-table { 
            border-collapse: collapse; 
            color: white; 
            min-width: 900px; 
        }
            
    .data-table th {
        text-align: left;
        padding: 14px;
        color: #94a3b8;
        border-bottom: 1px solid #7490b8;
        font-size: 14px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
            
    .data-table td { 
            padding: 14px; 
            border-bottom: 1px solid #1f2937; 
            transition: all 0.3s ease; 
        }
            
    .data-table tr:hover { 
            background-color: #0f172a; 
            transform: scale(1.01); 
        }

    div[data-testid="stButton"] button {
        width: 100%;
        background: #07111f;
        color: #cbd5e1;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 14px 10px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    div[data-testid="stButton"] button::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: #22c55e;
        border-radius: 10px 0 0 10px;
        transition: width 0.25s ease;
    }
    div[data-testid="stButton"] button:hover {
        background: #0c1f35;
        border-color: #22c55e;
        color: #22c55e;
        box-shadow: 0 0 18px rgba(34,197,94,0.15);
        transform: translateY(-1px);
    }
            
    div[data-testid="stButton"] button:hover::before { 
            width: 100%; 
            opacity: 0.06; 
    }
    
    div[data-testid="stButton"] button:active { 
            transform: translateY(0px); 
            box-shadow: none; 
    }

    .clean-stat-row { 
            display: flex; 
            gap: 16px; 
            margin-bottom: 24px; 
        }
            
    .clean-stat {
        flex: 1;
        background: #07111f;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
    }
            
    .clean-stat::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0;
        width: 100%; height: 2px;
        background: var(--accent);
    }

    .clean-stat-label {
             color: #64748b; 
            font-size: 11px; 
            letter-spacing: 2px; 
            text-transform: uppercase; 
            margin-bottom: 10px; 
        }
            
    .clean-stat-value { 
            color: #ffffff; 
            font-size: 32px; 
            font-weight: 700; 
            line-height: 1; 
        }

    div.stDownloadButton > button 
        {
        background: linear-gradient(135deg, #16a34a, #166534);
        color: white;
        border: none;
        padding: 13px 22px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        width: 100%;
        letter-spacing: 0.4px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 16px rgba(34,197,94,0.35);
    }
    
    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(34,197,94,0.55);
        cursor: pointer;
    }
        
    div.stDownloadButton > button:active  { 
            transform: scale(0.98); 
        }

    div.stDownloadButton > button:focus   { 
            outline: none; 
            border: none; 
        }
            
    div.stButton > button {
        background: linear-gradient(135deg, #16a34a, #166534);
        color: white;
        border: none;
        padding: 13px 22px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        width: 100%;
        letter-spacing: 0.4px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 16px rgba(34,197,94,0.35);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(34,197,94,0.55);
        cursor: pointer;
    }
            
    div.stButton > button:active { 
            transform: scale(0.98); 
        }
    
    div.stButton > button:focus  { 
            outline: none; 
            border: none; 
        }
</style>
""", unsafe_allow_html=True)



def data_completeness_score(df: pd.DataFrame) -> float:
    """
    Returns a normalized quality score (0–100)
    based on equal contribution of 4 factors.
    """

    total_cells = df.size
    missing_ratio = df.isnull().sum().sum() / total_cells if total_cells else 0

    dup_ratio = df.duplicated().sum() / len(df) if len(df) else 0

    completeness = df.notnull().mean().mean()

    numeric_ratio = df.select_dtypes(include=["int64", "float64"]).shape[1] / max(len(df.columns), 1)

    # convert all to "goodness" score
    score = (
        (1 - missing_ratio) +
        (1 - dup_ratio) +
        completeness +
        numeric_ratio
    ) / 4

    return round(score * 100, 2)



st.markdown("""
<div class="box">
    <h1>CSV DataLens</h1>
    <p>Analyze, visualize, and explore your CSV data through an interactive dashboard.</p>
</div>
""", unsafe_allow_html=True)



csv_file = st.file_uploader("Upload your CSV file", type=["csv"])

if csv_file is not None:
    df = pd.read_csv(csv_file)

    # ── SIDEBAR NAV ──────────────────────────
    with st.sidebar:
        selected = option_menu(
            menu_title="Dashboard Menu",
            options=[
                "Preview", "Summary", "Search",
                "Clean Data", "Visualization",
                "Data Completeness score", "CSV Report",
            ],
            icons=[
                "table", "bar-chart-line", "search",
                "brush", "clipboard-data",
                "shield-check", "file-earmark-text",
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "nav-link":          {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#22c55e", "color": "#1e293b"},
            },
        )


    if selected == "Preview":
        st.markdown("<center><h3 style='margin-top:25px;'>Dataset Preview</h3></center>", unsafe_allow_html=True)

        header_html = "<tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"

        rows_html = ""
        for row in df.values:
            rows_html += "<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"

        st.markdown(f"""
        <div class="table-container">
            <table class="data-table">
                <thead>{header_html}</thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

    
    elif selected == "Summary":
        st.markdown("<center><h3 style='margin-top:25px;'>Data Summary</h3></center>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='card' style="--topcolor:#38bdf8;">
                <div class='card-title'>Rows</div>
                <div class='card-value'>{df.shape[0]}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='card' style="--topcolor:#6366f1;">
                <div class='card-title'>Columns</div>
                <div class='card-value'>{df.shape[1]}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='card' style="--topcolor:#f59e0b;">
                <div class='card-title'>Missing</div>
                <div class='card-value'>{df.isnull().sum().sum()}</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class='card' style="--topcolor:#ec4899;">
                <div class='card-title'>Duplicates</div>
                <div class='card-value'>{df.duplicated().sum()}</div>
            </div><br>""", unsafe_allow_html=True)

        memory         = df.memory_usage(deep=True).sum() / 1024
        numeric_cols   = df.select_dtypes(include="number").shape[1]
        categorical_cols = df.select_dtypes(include="object").shape[1]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="card" style="--topcolor:#22c55e;">
                <div class="card-title">Memory Usage</div>
                <div class="card-value">{memory:.2f} KB</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card" style="--topcolor:#14b8a6;">
                <div class="card-title">Numeric Columns</div>
                <div class="card-value">{numeric_cols}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card" style="--topcolor:#f97316;">
                <div class="card-title">Categorical Columns</div>
                <div class="card-value">{categorical_cols}</div>
            </div><br>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<center><h3 style='margin-top:25px;'>Data Type Summary</h3></center>", unsafe_allow_html=True)

        dtype_rows = "".join(
            f"<tr><td>{col}</td><td>{df[col].dtype}</td></tr>"
            for col in df.columns
        )
        st.markdown(f"""
        <div class="table-container">
            <table class="data-table">
                <tr><th>Column Name</th><th>Data Type</th></tr>
                {dtype_rows}
            </table>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<center><h3 style='margin-top:25px;'>Statistical Summary</h3></center>", unsafe_allow_html=True)

        numeric_df = df.select_dtypes(include="number")

        if len(numeric_df.columns) > 0:
            manual_describe = pd.DataFrame({
                "Count":   numeric_df.count(),
                "Mean":    numeric_df.mean().round(2),
                "Std Dev": numeric_df.std().round(2),
                "Minimum": numeric_df.min(),
                "25%":     numeric_df.quantile(0.25).round(2),
                "Median":  numeric_df.median().round(2),
                "75%":     numeric_df.quantile(0.75).round(2),
                "Maximum": numeric_df.max(),
            })

            header_html = "<tr><th>Statistic</th>" + "".join(f"<th>{c}</th>" for c in manual_describe.columns) + "</tr>"
            rows_html   = ""
            for stat, row in manual_describe.iterrows():
                rows_html += f"<tr><td>{stat}</td>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"

            st.markdown(f"""
            <div class="table-container">
                <table class="data-table">
                    {header_html}{rows_html}
                </table>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:15px;border-radius:12px;
                        background:#2b0000;border:1px solid #ff4d4d;
                        color:#ff4d4d;font-size:16px;font-weight:600;margin-top:20px;">
                No numeric columns available for statistical summary.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

    elif selected == "Search":
        st.markdown("""
        <style>
            div[data-baseweb="input"] {
                background: #020c1b;
                border: 1px solid #1f2937;
                border-radius: 22px;
                box-shadow: 0 0 10px rgba(0,0,0,0.25);
                overflow: hidden;
            }
            div[data-baseweb="input"] input {
                background: transparent;
                color: white;
                font-size: 18px;
                padding: 14px 48px 14px 14px;
            }
            div[data-baseweb="input"] input::placeholder { color: #94a3b8; }
        </style>""", unsafe_allow_html=True)

        st.markdown("<center><h3 style='margin-top:25px;'>Search Dataset</h3></center>", unsafe_allow_html=True)

        search_value = st.text_input("", placeholder="Search any row value...")
        flag = 0

        if search_value:
            mask   = df.astype(str).apply(lambda col: col.str.lower().str.contains(search_value.lower(), na=False)).any(axis=1)
            result = df[mask]
            if len(result) > 0:
                flag = 1
        else:
            result = df
            flag   = 1

        if search_value and flag == 1:
            st.markdown(f"""
            <div style="color:#94a3b8;margin-top:10px;margin-bottom:14px;font-size:14px;letter-spacing:1px;">
                Total Results Found:
                <span style="color:#22c55e;font-weight:700;">{len(result)}</span>
            </div>""", unsafe_allow_html=True)

        if flag == 1:
            table_html = """
            <div class="table-container">
                <table class="data-table">
                    <thead><tr>"""
            for col in result.columns:
                table_html += f"<th>{col}</th>"
            table_html += "</tr></thead><tbody>"

            for i in range(len(result)):
                table_html += "<tr>"
                for value in result.iloc[i]:
                    cell = str(value)
                    if search_value:
                        lower_cell   = cell.lower()
                        lower_search = search_value.lower()
                        if lower_search in lower_cell:
                            idx   = lower_cell.find(lower_search)
                            end   = idx + len(search_value)
                            match = cell[idx:end]
                            cell  = (
                                cell[:idx]
                                + f'<span style="background-color:#22c55e;color:#020617;'
                                  f'padding:2px 6px;border-radius:6px;font-weight:700;">{match}</span>'
                                + cell[end:]
                            )
                    table_html += f"<td>{cell}</td>"
                table_html += "</tr>"

            table_html += "</tbody></table></div>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#3b0a0a;color:#ff4d4d;padding:14px;
                        border-radius:10px;text-align:center;font-size:16px;font-weight:600;">
                No Result Found
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

    elif selected == "Clean Data":
        st.markdown("<center><h3 style='margin-top:25px;'>Data Cleaning</h3></center>", unsafe_allow_html=True)

        if "clean_df" not in st.session_state:
            st.session_state.clean_df = df.copy()
        if "actions" not in st.session_state:
            st.session_state.actions = []

        def log(msg):
            st.session_state.actions.append(msg)

        st.markdown("<center><h2 style='font-size:16px;margin:18px 0 10px;'>How do you want to clean the data?</h2></center>",
                    unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c4, c5, _  = st.columns(3)

        with c1:
            if st.button("Drop All Null Rows"):
                before = len(st.session_state.clean_df)
                st.session_state.clean_df = st.session_state.clean_df.dropna().reset_index(drop=True)
                log(f"Drop All Null Rows: removed {before - len(st.session_state.clean_df)} rows")

        with c2:
            if st.button("Smart Numeric Clean"):
                data = st.session_state.clean_df.copy()
                dropped_cols, filled_cols = [], []
                for col in data.select_dtypes(include=["int64", "float64"]).columns:
                    pct = data[col].isna().sum() * 100 / len(data)
                    if pct > 60:
                        data = data.drop(columns=col)
                        dropped_cols.append(col)
                    elif 0 < pct <= 60:
                        data[col] = data[col].fillna(data[col].median())
                        filled_cols.append(col)
                st.session_state.clean_df = data.reset_index(drop=True)
                log(f"Smart Numeric Clean: dropped {dropped_cols or 'none'}, filled {filled_cols or 'none'}")

        with c3:
            if st.button("Remove Duplicates"):
                before = len(st.session_state.clean_df)
                st.session_state.clean_df = st.session_state.clean_df.drop_duplicates().reset_index(drop=True)
                log(f"Remove Duplicates: removed {before - len(st.session_state.clean_df)} rows")

        with c4:
            if st.button("Clean Text Rows"):
                obj_cols = st.session_state.clean_df.select_dtypes(include="object").columns.tolist()
                if obj_cols:
                    before = len(st.session_state.clean_df)
                    st.session_state.clean_df = st.session_state.clean_df.dropna(subset=obj_cols).reset_index(drop=True)
                    log(f"Clean Text Rows: removed {before - len(st.session_state.clean_df)} rows")
                else:
                    log("Clean Text Rows: no text/object columns found")

        with c5:
            if st.button("Remove Outliers (IQR)"):
                data   = st.session_state.clean_df.copy()
                before = len(data)
                for col in data.select_dtypes(include=["int64", "float64"]).columns:
                    Q1, Q3 = data[col].quantile(0.25), data[col].quantile(0.75)
                    IQR    = Q3 - Q1
                    data   = data[(data[col] >= Q1 - 1.5 * IQR) & (data[col] <= Q3 + 1.5 * IQR)]
                st.session_state.clean_df = data.reset_index(drop=True)
                log(f"Remove Outliers (IQR): removed {before - len(st.session_state.clean_df)} rows")

        st.markdown("---")

        cur_r, cur_c = st.session_state.clean_df.shape
        st.markdown(f"""
        <div class="clean-stat-row">
            <div class="clean-stat" style="--accent:#38bdf8;">
                <div class="clean-stat-label">Total Rows</div>
                <div class="clean-stat-value">{cur_r}</div>
            </div>
            <div class="clean-stat" style="--accent:#6366f1;">
                <div class="clean-stat-label">Total Columns</div>
                <div class="clean-stat-value">{cur_c}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        if st.session_state.actions:
            st.markdown("**Applied Actions:**")
            for a in st.session_state.actions:
                st.markdown(f"""
                <div style="background:#071a0f;border-left:3px solid #22c55e;
                            padding:8px 14px;border-radius:6px;
                            color:#94a3b8;font-size:14px;margin-bottom:6px;">
                    {a}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#64748b;font-size:14px;margin-top:10px;'>No cleaning actions applied yet.</div>",
                        unsafe_allow_html=True)

        st.markdown("---")
        st.download_button(
            label="Download Cleaned Data",
            data=st.session_state.clean_df.to_csv(index=False).encode("utf-8"),
            file_name=csv_file.name.replace(".csv", "_cleaned_data.csv"),
            mime="text/csv",
        )
        st.markdown("---")

    elif selected == "Visualization":
        st.markdown("<center><h3 style='margin-top:25px;'>Data Visualization</h3></center>", unsafe_allow_html=True)
        st.markdown("---")

        numeric_cols     = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

        def chart_header(title):
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #22c55e;color:#22c55e;
                        padding:12px;border-radius:10px;text-align:center;
                        font-size:18px;font-weight:600;margin-bottom:20px;">
                {title}
            </div>""", unsafe_allow_html=True)

        def error_box(msg):
            st.markdown(f"""
            <div style="background:#3b0a0a;color:#ff4d4d;padding:14px;
                        border-radius:10px;text-align:center;font-size:16px;font-weight:600;">
                {msg}
            </div>""", unsafe_allow_html=True)

        # Line Chart
        chart_header("Line Chart")
        if len(numeric_cols) < 2:
            error_box("Numeric data is insufficient to generate a Line Chart.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("Select X Axis", numeric_cols, key="line_x")
            with col2:
                y_axis = st.selectbox("Select Y Axis", [c for c in numeric_cols if c != x_axis], key="line_y")
            fig = px.line(df, x=x_axis, y=y_axis, template="plotly_dark")
            fig.update_layout(height=500, title=f"{y_axis} vs {x_axis}", title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Scatter Plot
        chart_header("Scatter Plot")
        if len(numeric_cols) < 2:
            error_box("Numeric data is insufficient to generate a Scatter Plot.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                scatter_x = st.selectbox("Select X Axis", numeric_cols, key="scatter_x")
            with col2:
                scatter_y = st.selectbox("Select Y Axis", [c for c in numeric_cols if c != scatter_x], key="scatter_y")
            fig = px.scatter(df, x=scatter_x, y=scatter_y, template="plotly_dark")
            fig.update_layout(height=500, title=f"{scatter_y} vs {scatter_x}", title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Bar Chart
        chart_header("Bar Chart")
        if not categorical_cols or not numeric_cols:
            error_box("Suitable columns are unavailable for generating a Bar Chart.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                bar_x = st.selectbox("Select X Axis", categorical_cols, key="bar_x")
            with col2:
                bar_y = st.selectbox("Select Y Axis", numeric_cols, key="bar_y")
            chart_data = df.groupby(bar_x)[bar_y].sum().reset_index()
            fig = px.bar(chart_data, x=bar_x, y=bar_y, template="plotly_dark")
            fig.update_layout(height=500, title=f"{bar_y} by {bar_x}", title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Histogram
        chart_header("Histogram")
        if not numeric_cols:
            error_box("No numeric columns available for Histogram.")
        else:
            hist_col = st.selectbox("Select Column", numeric_cols, key="histogram")
            fig = px.histogram(df, x=hist_col, template="plotly_dark")
            fig.update_layout(height=500, title=f"Distribution of {hist_col}", title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Pie Chart
        chart_header("Pie Chart")
        if not categorical_cols:
            error_box("No categorical columns available for Pie Chart.")
        else:
            pie_col  = st.selectbox("Select Column", categorical_cols, key="pie")
            pie_data = df[pie_col].value_counts().reset_index()
            pie_data.columns = [pie_col, "Count"]
            fig = px.pie(pie_data, names=pie_col, values="Count", template="plotly_dark")
            fig.update_layout(height=500, title=f"{pie_col} Distribution", title_x=0.35)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Heatmap
        chart_header("Heatmap")
        if len(numeric_cols) < 2:
            error_box("At least 2 numeric columns are required for Heatmap.")
        else:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", template="plotly_dark")
            fig.update_layout(height=600, title="Correlation Heatmap", title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")


    elif selected == "Data Completeness score":
        st.markdown("<h3 style='text-align:center;margin-top:20px;'>Data Completeness Score</h3>",
                    unsafe_allow_html=True)

        st.markdown("""
        <style>
            div.stButton > button {
                background: linear-gradient(135deg, #16a34a, #166534) !important;
                color: white !important;
                border: none !important;
                padding: 13px 22px !important;
                border-radius: 12px !important;
                font-size: 15px !important;
                font-weight: 600 !important;
                width: 100% !important;
                letter-spacing: 0.4px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 6px 16px rgba(34,197,94,0.35) !important;
            }
            div.stButton > button:hover {
                background: linear-gradient(135deg, #22c55e, #15803d) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 0 12px rgba(34,197,94,0.65), 0 0 24px rgba(34,197,94,0.45) !important;
                cursor: pointer !important;
            }
            div.stButton > button:active { transform: scale(0.98) !important; }
            div.stButton > button:focus  { outline: none !important; border: none !important; }
        </style>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            calculate = st.button("Calculate Completeness Score")

        if calculate:
            # ── Uses the single shared function ──
            score = data_completeness_score(df)

            st.metric("Score", f"{score} / 100")
            st.progress(int(score))

            if score >= 80:
                st.markdown("""
                <div style="background:#0f172a;border:1px solid #22c55e;color:#22c55e;
                            padding:12px;border-radius:10px;text-align:center;
                            font-size:18px;font-weight:600;margin-bottom:20px;">
                    Excellent Score
                </div>""", unsafe_allow_html=True)
            elif score >= 50:
                st.markdown("""
                <div style="background:#0f172a;border:1px solid yellow;color:#f59e0b;
                            padding:12px;border-radius:10px;text-align:center;
                            font-size:18px;font-weight:600;margin-bottom:20px;">
                    Moderate Score
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#3b0a0a;color:#ff4d4d;padding:14px;
                            border-radius:10px;text-align:center;
                            font-size:16px;font-weight:600;">
                    Poor Score: Needs Cleaning
                </div>""", unsafe_allow_html=True)

            st.markdown("---")

    
    elif selected == "CSV Report":
        st.markdown("<center><h3 style='margin-top:25px;'>CSV Report</h3></center><br>",
                    unsafe_allow_html=True)

        if st.button("Generate CSV Report"):
            buf_pdf   = io.BytesIO()
            file_name = csv_file.name
            doc       = SimpleDocTemplate(buf_pdf, pagesize=A4)
            styles    = getSampleStyleSheet()
            story     = []

            centered_style = ParagraphStyle(
                name="centered_heading",
                parent=styles["Heading2"],
                alignment=TA_CENTER,
            )

            def add_page_number(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica", 9)
                canvas.drawCentredString(A4[0] / 2, 0.5 * inch, f"Page {canvas.getPageNumber()}")
                canvas.restoreState()

            # Title
            story.append(Paragraph("<b>CSV DATALENS REPORT</b>", styles["Title"]))
            story.append(Spacer(1, 20))

            # Dataset overview
            rows_count       = df.shape[0]
            cols_count       = df.shape[1]
            columns_list     = ", ".join(df.columns)
            missing_values   = df.isnull().sum().sum()
            duplicate_values = df.duplicated().sum()
            memory_usage     = df.memory_usage(deep=True).sum() / 1024
            numeric_cols     = len(df.select_dtypes(include=["int64", "float64"]).columns)
            categorical_cols = len(df.select_dtypes(include=["object"]).columns)

            info = (
                f"&bull; There are total {rows_count} rows and {cols_count} columns in this dataset. "
                f"The column names are: {columns_list}. "
                f"There are {missing_values} missing values and {duplicate_values} duplicate rows. "
                f"The total memory usage is {memory_usage:.2f} KB. "
                f"There are {numeric_cols} Numeric columns and {categorical_cols} Categorical columns."
            )
            story.append(Paragraph(info, styles["Normal"]))
            story.append(Spacer(1, 10))

            # Data Type Summary table
            story.append(Paragraph("Data Type Summary", centered_style))
            dtype_data = [["Column Name", "Data Type"]] + [[col, str(dtype)] for col, dtype in df.dtypes.items()]
            dtype_table = Table(dtype_data, colWidths=[300, 150])
            dtype_table.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.black),
                ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0),  12),
                ("BACKGROUND",    (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR",     (0, 1), (-1, -1), colors.black),
                ("GRID",          (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOTTOMPADDING", (0, 0), (-1, 0),  10),
                ("TOPPADDING",    (0, 0), (-1, 0),  10),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("TOPPADDING",    (0, 1), (-1, -1), 8),
            ]))
            story.append(dtype_table)

            # Statistical Summary table
            describe_df = df.describe().round(2)
            stat_data   = [["Statistic"] + describe_df.columns.tolist()]
            for idx, row in describe_df.iterrows():
                stat_data.append([idx] + row.tolist())

            stat_table = Table(stat_data)
            stat_table.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.black),
                ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("BACKGROUND",    (0, 1), (-1, -1), colors.white),
                ("GRID",          (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOTTOMPADDING", (0, 0), (-1, 0),  10),
                ("TOPPADDING",    (0, 0), (-1, 0),  10),
            ]))
            story.append(PageBreak())
            story.append(Paragraph("Statistical Summary", centered_style))
            story.append(Spacer(1, 10))
            story.append(stat_table)

            # Auto-cleaning for report
            temp = df.dropna().drop_duplicates().reset_index(drop=True)
            obj_cols = temp.select_dtypes(include="object").columns.tolist()
            if obj_cols:
                temp = temp.dropna(subset=obj_cols).reset_index(drop=True)

            for col in temp.select_dtypes(include=["int64", "float64"]).columns:
                pct = temp[col].isna().sum() * 100 / len(temp)
                if pct > 60:
                    temp = temp.drop(columns=col)
                elif 0 < pct <= 60:
                    temp[col] = temp[col].fillna(temp[col].median())

            temp = temp.reset_index(drop=True)
            obj_cols = temp.select_dtypes(include="object").columns.tolist()
            if obj_cols:
                temp = temp.dropna(subset=obj_cols).reset_index(drop=True)

            rows_after, cols_after = temp.shape

            story.append(Paragraph("After Cleaning", centered_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(
                f"&bull; After Cleaning, there are total {rows_after} rows.<br/>"
                f"&bull; After Cleaning, there are {cols_after} columns.",
                styles["Normal"],
            ))
            story.append(Spacer(1, 10))

            # Correlation Heatmap
            num_cols = temp.select_dtypes(include=["int64", "float64"]).columns.tolist()
            if len(num_cols) >= 2:
                corr    = temp[num_cols].corr()
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax)
                ax.set_title("Correlation Heatmap")
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight")
                buf.seek(0)
                plt.close(fig)
                story.append(PageBreak())
                story.append(Paragraph("Correlation Heatmap", centered_style))
                story.append(Spacer(1, 10))
                story.append(Image(buf, width=480, height=340))
            else:
                story.append(Paragraph(
                    "Correlation Heatmap could not be generated: fewer than 2 numeric columns.",
                    styles["Normal"],
                ))

            # ── Data Completeness Score ──────────────
            # Uses the SAME function as the "Data Completeness score" tab
            score = data_completeness_score(df)

            story.append(Paragraph("Data Completeness Score", centered_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(
                f"&bull; The data completeness score of this dataset is {score} / 100. "
                f"This score is calculated using a weighted formula that accounts for "
                f"missing values, duplicate rows, overall non-null ratio, and numeric column proportion.",
                styles["Normal"],
            ))

            # Build PDF
            doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
            buf_pdf.seek(0)
            st.session_state.pdf_data = buf_pdf.getvalue()
            st.success("Report generated successfully!")

        # Preview & Download
        if "pdf_data" in st.session_state:
            b64 = base64.b64encode(st.session_state.pdf_data).decode("utf-8")
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="900" type="application/pdf"></iframe>',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="Download PDF Report",
                data=st.session_state.pdf_data,
                file_name=f"{csv_file.name}_report.pdf",
                mime="application/pdf",
            )