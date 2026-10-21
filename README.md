# 🛡️ CyberShield

A simple cybersecurity dashboard built with **Python**, **Streamlit** and **Pandas**.
CyberShield shows login activity at a glance, flags IP addresses with many failed logins, and explains why each one was flagged.

> All data in this project is **fictional**. CyberShield does not connect to any real system, and it does not use machine learning.

## Features

- **Dark, modern dashboard** with a title, short description and four number cards:
  Total Logins, Successful Logins, Failed Logins and Suspicious Activities.
- **Generate Sample Data** button that creates 20 fictional login records
  (time, username, IP address and result).
- **Simple detection rule:** an IP address with 5 or more failed logins is marked as suspicious.
- **Security Alerts** table showing the suspicious IP, usernames tried, number of failed attempts,
  a colour-coded risk level (Low, Medium or High) and the reason for the alert.
- **Two charts:**
  - Successful vs Failed Logins
  - Failed Login Attempts by IP Address
- **Two dropdown filters:** filter alerts by risk level, and filter login records by result.
- **Reminder note:** a suspicious login pattern does not automatically prove a cyberattack.

## Technologies

| Technology | Used for |
|---|---|
| Python 3.9+ | Main language |
| Streamlit | Web page, button, dropdowns and layout |
| Pandas | Storing, counting and filtering the login records |

## Getting Started

1. **Install Python** 3.9 or newer.
2. **Install Streamlit** (Pandas is installed with it):

   ```bash
   pip install streamlit
   ```

3. **Open a terminal in the folder that contains `app.py`**, then run:

   ```bash
   streamlit run app.py
   ```

   If the `streamlit` command is not recognised, use:

   ```bash
   python -m streamlit run app.py
   ```

4. Open `http://localhost:8501` in your browser if it does not open automatically.
5. Click **Generate Sample Data** to load the records.

## How It Works

The whole project is one file, `app.py`.

| Part of the code | What it does |
|---|---|
| `make_sample_data()` | Creates the 20 fictional login records |
| `find_suspicious_ips()` | Applies the detection rule and returns the flagged IP addresses |
| `get_risk_level()` | Turns a failed-attempt count into Low, Medium or High |
| `build_alerts_table()` | Builds the Security Alerts table |
| `build_bar_chart()` | Draws a simple bar chart |
| `show_card()` | Draws one number card |

### The detection rule

1. Go through every login record and count the **failed** logins for each IP address.
2. If an IP address has **5 or more** failed logins, mark it as suspicious.

The number on the **Suspicious Activities** card is the number of flagged IP addresses, and it updates automatically.

### Risk levels

| Failed attempts | Risk level |
|---|---|
| 5 | Low (green) |
| 6 to 9 | Medium (orange) |
| 10 or more | High (red) |

## Settings You Can Change

These values are near the top of `app.py`:

```python
FAILED_LIMIT = 5         # failed logins needed to flag an IP address
MEDIUM_RISK_LIMIT = 6    # failed logins for a Medium risk label
HIGH_RISK_LIMIT = 10     # failed logins for a High risk label
```

For example, set `HIGH_RISK_LIMIT = 6` to see the sample alert turn High.

## Sample Data

The 20 sample records include normal logins, a few harmless typos, and six failed attempts from one IP address (`203.0.113.45`) trying the usernames `admin`, `root`, `guest` and `test`.
The IP addresses come from ranges reserved for documentation, so they do not belong to real devices.

With the sample data you should see:

| Total | Successful | Failed | Suspicious |
|---|---|---|---|
| 20 | 12 | 8 | 1 |

## Screenshots

_Add screenshots of the dashboard here._

## Limitations

- Uses small, fictional sample data only.
- The rule counts failed logins only. It does not look at timing, location or successful logins that follow failures.
- Many people can share one IP address, so a flagged IP is a reason to look closer, not proof of an attack.

## Ideas for the Future

- Load login records from a CSV or log file.
- Add time-based rules, such as five failures within one minute.
- Highlight flagged IP addresses in the login records table.
- Add a chart of failed logins over time and an option to export alerts.

## License

_Add your license here._
