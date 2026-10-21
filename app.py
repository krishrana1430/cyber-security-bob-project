# CyberShield - a simple cybersecurity dashboard built with Streamlit
# Run it with:  streamlit run app.py

import pandas as pd
import streamlit as st

# ---------- Page settings ----------
st.set_page_config(page_title="CyberShield", page_icon="🛡️", layout="wide")

# ---------- Dark theme styling (CSS) ----------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #0b1220;
        color: #e5e7eb;
    }

    /* Hide default Streamlit menu and footer */
    #MainMenu, footer, header {visibility: hidden;}

    /* Title and description */
    .title {
        font-size: 3rem;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 0;
    }
    .description {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    /* Number cards */
    .card {
        background-color: #111a2e;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
    }
    .card-label {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    .card-number {
        font-size: 2.6rem;
        font-weight: 700;
    }

    /* Section heading and empty message */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e5e7eb;
        margin: 2rem 0 0.5rem 0;
    }
    .empty-message {
        background-color: #111a2e;
        border: 1px dashed #334155;
        border-radius: 10px;
        padding: 20px;
        color: #94a3b8;
    }

    /* Warning box for suspicious IPs */
    .warning-box {
        background-color: #2a1215;
        border: 1px solid #ef4444;
        border-left: 6px solid #ef4444;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 1.5rem;
        color: #fecaca;
    }
    .ok-box {
        background-color: #10261a;
        border: 1px solid #22c55e;
        border-left: 6px solid #22c55e;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 1.5rem;
        color: #bbf7d0;
    }

    /* Risk level labels */
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
        color: #0b1220;
    }
    .risk-high { background-color: #ef4444; }    /* red */
    .risk-medium { background-color: #f59e0b; }  /* orange */
    .risk-low { background-color: #22c55e; }     /* green */

    /* Friendly note under the alerts */
    .note-box {
        background-color: #0f1b33;
        border: 1px solid #1e3a5f;
        border-left: 6px solid #38bdf8;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 1rem;
        color: #cbd5e1;
    }

    /* Simple bar charts */
    .chart-card {
        background-color: #111a2e;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 20px 24px;
    }
    .chart-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 14px;
    }
    .bar-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }
    .bar-label {
        width: 130px;
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    .bar-track {
        flex: 1;
        background-color: #1e293b;
        border-radius: 6px;
        height: 22px;
    }
    .bar-fill {
        height: 100%;
        border-radius: 6px;
    }
    .bar-value {
        width: 30px;
        font-weight: 700;
        color: #e5e7eb;
    }
    .chart-caption {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 12px;
    }

    /* Filter labels and small helper text */
    .filter-label {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0.5rem 0 0.2rem 0;
    }
    .count-text {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0.5rem 0;
    }

    /* Login records table */
    .log-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #111a2e;
        color: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
    }
    .log-table th {
        background-color: #1e293b;
        color: #38bdf8;
        text-align: left;
        padding: 10px 14px;
    }
    .log-table td {
        padding: 9px 14px;
        border-top: 1px solid #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Fake login records (all fictional) ----------
# Each record is: (time, username, IP address, result)
# The IP addresses come from ranges reserved for examples,
# so they do not belong to any real device.
def make_sample_data():
    records = [
        ("2026-10-21 09:02:15", "alice", "192.0.2.10", "Success"),
        ("2026-10-21 09:05:41", "bob", "192.0.2.22", "Success"),
        ("2026-10-21 09:11:08", "carol", "198.51.100.7", "Success"),
        ("2026-10-21 09:14:30", "dave", "192.0.2.35", "Failed"),   # typo in password
        ("2026-10-21 09:15:02", "dave", "192.0.2.35", "Success"),  # tried again
        # --- Several failed attempts from ONE IP address (suspicious) ---
        ("2026-10-21 09:20:47", "admin", "203.0.113.45", "Failed"),
        ("2026-10-21 09:20:55", "root", "203.0.113.45", "Failed"),
        ("2026-10-21 09:21:03", "guest", "203.0.113.45", "Failed"),
        ("2026-10-21 09:21:10", "admin", "203.0.113.45", "Failed"),
        ("2026-10-21 09:21:18", "test", "203.0.113.45", "Failed"),
        ("2026-10-21 09:21:26", "admin", "203.0.113.45", "Failed"),
        # --- Back to normal activity ---
        ("2026-10-21 09:30:12", "eve", "198.51.100.14", "Success"),
        ("2026-10-21 09:42:55", "frank", "192.0.2.50", "Success"),
        ("2026-10-21 09:48:19", "grace", "198.51.100.21", "Failed"),
        ("2026-10-21 09:48:40", "grace", "198.51.100.21", "Success"),
        ("2026-10-21 10:03:27", "heidi", "192.0.2.61", "Success"),
        ("2026-10-21 10:10:05", "ivan", "198.51.100.33", "Success"),
        ("2026-10-21 10:17:44", "judy", "192.0.2.72", "Success"),
        ("2026-10-21 10:25:09", "alice", "192.0.2.10", "Success"),
        ("2026-10-21 10:31:50", "bob", "192.0.2.22", "Success"),
    ]
    return pd.DataFrame(records, columns=["Time", "Username", "IP Address", "Result"])


# ---------- The security rule ----------
# RULE: if the same IP address has 5 or more FAILED logins,
#       mark that IP address as suspicious.
# This is a plain counting rule. There is no machine learning here,
# and nothing connects to a real system.
FAILED_LIMIT = 5


def find_suspicious_ips(logins):
    failed_counts = {}    # IP address -> how many times it failed
    usernames_tried = {}  # IP address -> list of usernames it tried

    # Step 1: go through every record and count the failed logins per IP
    for index, row in logins.iterrows():
        if row["Result"] == "Failed":
            ip = row["IP Address"]
            username = row["Username"]

            # First time we see this IP? Start its counter at 0.
            if ip not in failed_counts:
                failed_counts[ip] = 0
                usernames_tried[ip] = []

            failed_counts[ip] = failed_counts[ip] + 1

            # Remember each username only once
            if username not in usernames_tried[ip]:
                usernames_tried[ip].append(username)

    # Step 2: apply the rule - which IPs reached the limit?
    suspicious = []
    for ip in failed_counts:
        if failed_counts[ip] >= FAILED_LIMIT:
            suspicious.append(
                {
                    "ip": ip,
                    "failed": failed_counts[ip],
                    "usernames": usernames_tried[ip],
                }
            )

    return suspicious


# ---------- Risk levels ----------
# The more failed attempts an IP address has, the higher its risk label:
#   5 failed attempts      -> Low
#   6 to 9 failed attempts -> Medium
#   10 or more             -> High
MEDIUM_RISK_LIMIT = 6
HIGH_RISK_LIMIT = 10


def get_risk_level(failed):
    if failed >= HIGH_RISK_LIMIT:
        return "High"
    elif failed >= MEDIUM_RISK_LIMIT:
        return "Medium"
    else:
        return "Low"


# Builds the HTML table for the Security Alerts section
def build_alerts_table(suspicious_ips):
    rows = ""

    for item in suspicious_ips:
        ip = item["ip"]
        failed = item["failed"]
        names = ", ".join(item["usernames"])
        how_many_names = len(item["usernames"])

        risk = get_risk_level(failed)
        badge_class = "risk-" + risk.lower()  # risk-high, risk-medium or risk-low

        reason = (
            f"{failed} failed logins from this IP (limit is {FAILED_LIMIT}), "
            f"trying {how_many_names} different username(s)."
        )

        rows = rows + (
            "<tr>"
            f"<td>{ip}</td>"
            f"<td>{names}</td>"
            f"<td>{failed}</td>"
            f'<td><span class="badge {badge_class}">{risk}</span></td>'
            f"<td>{reason}</td>"
            "</tr>"
        )

    return (
        '<table class="log-table">'
        "<tr><th>Suspicious IP</th><th>Username(s)</th>"
        "<th>Failed Attempts</th><th>Risk Level</th><th>Reason</th></tr>"
        + rows
        + "</table>"
    )


# ---------- Simple bar chart ----------
# items is a list of (label, number, color).
# The biggest number gets a full-width bar; the others are drawn
# relative to it (for example, half the number = half the width).
def build_bar_chart(items):
    biggest = 1
    for label, number, color in items:
        if number > biggest:
            biggest = number

    html = ""
    for label, number, color in items:
        width = number / biggest * 100  # bar width as a percentage
        html = html + (
            '<div class="bar-row">'
            f'<div class="bar-label">{label}</div>'
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width: {width}%; background-color: {color};"></div>'
            "</div>"
            f'<div class="bar-value">{number}</div>'
            "</div>"
        )
    return html


# ---------- Title and description ----------
st.markdown('<p class="title">🛡️ CyberShield</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="description">A simple security dashboard that keeps an eye on '
    "login activity and highlights anything suspicious.</p>",
    unsafe_allow_html=True,
)

# ---------- Button: Generate Sample Data ----------
# st.session_state remembers the data between button clicks.
if "logins" not in st.session_state:
    st.session_state["logins"] = None  # no data yet

if st.button("Generate Sample Data"):
    st.session_state["logins"] = make_sample_data()

logins = st.session_state["logins"]

# ---------- Work out the numbers for the cards ----------
if logins is None:
    total_logins = 0
    successful_logins = 0
    failed_logins = 0
    suspicious_ips = []
else:
    total_logins = len(logins)
    successful_logins = int((logins["Result"] == "Success").sum())
    failed_logins = int((logins["Result"] == "Failed").sum())
    suspicious_ips = find_suspicious_ips(logins)  # apply the rule

# Each flagged IP address counts as one suspicious activity
suspicious_activities = len(suspicious_ips)


# ---------- Helper function to draw one card ----------
def show_card(label, number, color):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">{label}</div>
            <div class="card-number" style="color: {color};">{number}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Four number cards in one row ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    show_card("Total Logins", total_logins, "#38bdf8")  # blue
with col2:
    show_card("Successful Logins", successful_logins, "#22c55e")  # green
with col3:
    show_card("Failed Logins", failed_logins, "#f59e0b")  # orange
with col4:
    show_card("Suspicious Activities", suspicious_activities, "#ef4444")  # red

# ---------- Charts ----------
st.markdown('<p class="section-title">Charts</p>', unsafe_allow_html=True)

if logins is None:
    st.markdown(
        '<div class="empty-message">No charts yet. '
        "Click <b>Generate Sample Data</b> to see them.</div>",
        unsafe_allow_html=True,
    )
else:
    chart_left, chart_right = st.columns(2)

    # Chart 1: successful logins compared with failed logins
    with chart_left:
        chart_1 = build_bar_chart(
            [
                ("Successful", successful_logins, "#22c55e"),  # green
                ("Failed", failed_logins, "#f59e0b"),  # orange
            ]
        )
        st.markdown(
            '<div class="chart-card">'
            '<div class="chart-title">Successful vs Failed Logins</div>'
            + chart_1
            + '<div class="chart-caption">Shows how much of our login traffic '
            "fails. A sudden jump in failed logins is worth a closer look.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    # Chart 2: failed login attempts for each IP address
    with chart_right:
        # Pandas: keep only the failed rows, then count them per IP address
        failed_rows = logins[logins["Result"] == "Failed"]
        failed_per_ip = failed_rows["IP Address"].value_counts()

        flagged_ips = [item["ip"] for item in suspicious_ips]

        ip_items = []
        for ip_address, count in failed_per_ip.items():
            if ip_address in flagged_ips:
                color = "#ef4444"  # red = flagged as suspicious
            else:
                color = "#f59e0b"  # orange = normal failures
            ip_items.append((ip_address, int(count), color))

        chart_2 = build_bar_chart(ip_items)
        st.markdown(
            '<div class="chart-card">'
            '<div class="chart-title">Failed Login Attempts by IP Address</div>'
            + chart_2
            + '<div class="chart-caption">Red bars are IP addresses flagged by our '
            "rule. One IP standing far above the rest is the pattern to watch.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

# ---------- Warnings for suspicious IP addresses ----------
if logins is not None:
    if len(suspicious_ips) > 0:
        for item in suspicious_ips:
            ip = item["ip"]
            failed = item["failed"]
            names = ", ".join(item["usernames"])

            st.markdown(
                f"""
                <div class="warning-box">
                    <b>⚠️ Suspicious IP address flagged: {ip}</b><br>
                    <b>Why:</b> this IP had {failed} failed login attempts,
                    which is at or above our limit of {FAILED_LIMIT}.<br>
                    <b>Usernames it tried:</b> {names}<br>
                    Many failed logins from one address can mean someone is
                    guessing passwords.
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="ok-box">✅ No suspicious IP addresses found.</div>',
            unsafe_allow_html=True,
        )

# ---------- Security Alerts section ----------
st.markdown('<p class="section-title">Security Alerts</p>', unsafe_allow_html=True)

if logins is None:
    st.markdown(
        '<div class="empty-message">No alerts yet. '
        "Click <b>Generate Sample Data</b> to check the login records.</div>",
        unsafe_allow_html=True,
    )
elif len(suspicious_ips) == 0:
    st.markdown(
        '<div class="ok-box">✅ No security alerts. Nothing needs attention.</div>',
        unsafe_allow_html=True,
    )
else:
    # Dropdown filter: choose which risk level to show
    filter_col, space_col = st.columns([1, 3])
    with filter_col:
        st.markdown('<div class="filter-label">Filter alerts by risk level</div>', unsafe_allow_html=True)
        risk_filter = st.selectbox(
            "Risk level",
            ["All", "High", "Medium", "Low"],
            key="risk_filter",
            label_visibility="collapsed",
        )

    # Keep only the alerts that match the chosen risk level
    shown_alerts = []
    for item in suspicious_ips:
        if risk_filter == "All" or get_risk_level(item["failed"]) == risk_filter:
            shown_alerts.append(item)

    if len(shown_alerts) > 0:
        st.markdown(build_alerts_table(shown_alerts), unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="empty-message">No alerts with {risk_filter} risk level.</div>',
            unsafe_allow_html=True,
        )

# A reminder that alerts are clues, not proof
st.markdown(
    """
    <div class="note-box">
        <b>ℹ️ Please note:</b> a suspicious login pattern does not automatically
        prove a cyberattack. There can be harmless explanations, such as someone
        forgetting their password, a misconfigured app, or many people sharing
        one network address. Treat an alert as a reason to take a closer look,
        not as proof that something bad happened.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Login records table ----------
st.markdown('<p class="section-title">Recent Login Records</p>', unsafe_allow_html=True)

if logins is None:
    st.markdown(
        '<div class="empty-message">No data yet. '
        "Click <b>Generate Sample Data</b> to load 20 fake login records.</div>",
        unsafe_allow_html=True,
    )
else:
    # Dropdown filter: choose which login results to show
    result_col, space_col2 = st.columns([1, 3])
    with result_col:
        st.markdown('<div class="filter-label">Filter by login result</div>', unsafe_allow_html=True)
        result_filter = st.selectbox(
            "Login result",
            ["All", "Success", "Failed"],
            key="result_filter",
            label_visibility="collapsed",
        )

    # Pandas: keep only the rows that match the chosen result
    if result_filter == "All":
        shown_logins = logins
    else:
        shown_logins = logins[logins["Result"] == result_filter]

    st.markdown(
        f'<div class="count-text">Showing {len(shown_logins)} of {len(logins)} records</div>',
        unsafe_allow_html=True,
    )
    st.markdown(shown_logins.to_html(index=False, classes="log-table"), unsafe_allow_html=True)
