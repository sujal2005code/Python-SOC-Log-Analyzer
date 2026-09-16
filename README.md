# 🔐 Python SOC Log Analyzer

A modular Python-based Security Operations Center (SOC) log analyzer
that parses structured OpenSSH authentication logs, normalizes
authentication events, detects repeated failed login activity, and
generates security reports.

> **Current status:** Milestone 1 --- Real SSH Log Analysis ✅\
> Future milestones are planned for multi-log support, expanded
> detection rules, JSON output, testing, and a SOC dashboard.

------------------------------------------------------------------------

## 🎯 Project Overview

Security teams work with large volumes of authentication logs. Manually
identifying repeated failed login attempts can be slow and error-prone.

This project automates the first stage of that workflow:

``` text
Raw OpenSSH Logs
       │
       ▼
┌──────────────────┐
│   Log Parser     │
│ parser.py        │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────┐
│ Normalized Authentication  │
│ user / IP / status         │
└────────────┬───────────────┘
             │
             ▼
┌──────────────────┐
│ Detection Engine │
│ detector.py      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Security Report  │
│ report.py        │
└──────────────────┘
```

------------------------------------------------------------------------

## ✨ Current Features

-   📄 Parse structured OpenSSH authentication logs
-   🔎 Extract usernames and source IP addresses
-   ✅ Detect successful SSH authentication
-   ❌ Detect failed authentication
-   🚨 Detect repeated failed login attempts
-   ⚙️ Configure brute-force threshold from the CLI
-   🖥️ Run analysis from the command line
-   📝 Generate a human-readable security report
-   💾 Save reports automatically
-   🧩 Separate parsing, detection, reporting, and CLI responsibilities

------------------------------------------------------------------------

## 🏗️ Architecture

``` mermaid
flowchart TD
    A[OpenSSH Structured CSV] --> B[main.py]
    B --> C[parser.py]
    C --> D[Normalized Events]
    D --> E[detector.py]
    E --> F[Failed Login Detection]
    E --> G[Brute-Force Detection]
    F --> H[report.py]
    G --> H
    H --> I[security_report.txt]

    J[CLI Arguments] --> B
    J --> K[Log File]
    J --> L[Detection Threshold]
    J --> M[Report Output]
```

### Separation of Responsibilities

  Component        Responsibility
  ---------------- ----------------------------------------------
  `main.py`        CLI, application flow, orchestration
  `parser.py`      Read logs and normalize OpenSSH events
  `detector.py`    Identify failed logins and repeated failures
  `report.py`      Build and save security reports
  `tests/`         Automated testing
  `sample_logs/`   Example authentication datasets
  `reports/`       Generated security reports

------------------------------------------------------------------------

## 🔄 Processing Pipeline

``` mermaid
sequenceDiagram
    participant U as User
    participant M as main.py
    participant P as parser.py
    participant D as detector.py
    participant R as report.py

    U->>M: Provide log file + threshold
    M->>P: Load log file
    P->>P: Parse OpenSSH messages
    P-->>M: Normalized events
    M->>D: Analyze events
    D-->>M: Failed logins + alerts
    M->>R: Generate report
    R-->>U: Display + save security report
```

------------------------------------------------------------------------

## 🧠 Event Normalization

Different raw SSH messages are converted into a common internal
structure.

### Failed authentication

``` text
Failed password for invalid user webmaster from 173.234.31.186
```

becomes:

``` json
{
  "user": "webmaster",
  "ip_address": "173.234.31.186",
  "status": "FAILED"
}
```

### Successful authentication

``` text
Accepted password for fztu from 119.137.62.142
```

becomes:

``` json
{
  "user": "fztu",
  "ip_address": "119.137.62.142",
  "status": "SUCCESS"
}
```

This normalization keeps the detection logic independent from the
original log message format.

------------------------------------------------------------------------

## 🚨 Brute-Force Detection

The current detection rule groups failed authentication attempts by:

``` text
username + source IP
```

A configurable threshold determines when an alert is generated.

### Example

With:

``` text
threshold = 5
```

    Attempts Result
  ---------- ----------
           1 No alert
           4 No alert
           5 🚨 Alert
          20 🚨 Alert
         276 🚨 Alert

The threshold can be changed without modifying the source code.

------------------------------------------------------------------------

## 📊 Milestone 1 Results

The analyzer was tested against the OpenSSH structured dataset included
in `sample_logs/`.

### Parsed Authentication Events

``` mermaid
pie title Authentication Event Distribution
    "Failed" : 635
    "Successful" : 1
```

### Security Alerts

``` mermaid
pie title Detection Result
    "Brute-force alerts" : 13
    "No alert" : 623
```

### Observed Results

  Metric                         Result
  -------------------- ----------------
  Parsed events                 **636**
  Successful logins               **1**
  Failed logins                 **635**
  Brute-force alerts             **13**
  Default threshold      **5 attempts**

One detected source/user combination contained **276 failed attempts**,
demonstrating why automated repeated-failure detection is useful.

> These values represent the current test run against the included
> dataset and are not intended to represent a general real-world attack
> rate.

------------------------------------------------------------------------

## 🖥️ CLI Usage

### Run with the default threshold

``` bash
python src/main.py --log sample_logs/OpenSSH_2k.log_structured.csv
```

### Change the detection threshold

``` bash
python src/main.py --log sample_logs/OpenSSH_2k.log_structured.csv --threshold 10
```

### Specify a custom report path

``` bash
python src/main.py --log sample_logs/OpenSSH_2k.log_structured.csv --threshold 10 --output reports/custom_report.txt
```

------------------------------------------------------------------------

## 📄 Example Report

``` text
========== SECURITY SUMMARY ==========
Total Events       : 636
Successful Logins  : 1
Failed Logins      : 635
Security Alerts    : 13
======================================

========== HIGH-RISK ALERTS ==========

Alert #1
User               : root
IP Address         : 112.95.230.3
Failed Attempts    : 24
Risk Level         : HIGH
```

Reports are written to:

``` text
reports/security_report.txt
```

------------------------------------------------------------------------

## 📁 Project Structure

``` text
python-soc-log-analyzer/
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── sample_logs/
│   ├── authentication_logs.csv
│   └── OpenSSH_2k.log_structured.csv
│
├── reports/
│   └── security_report.txt
│
├── src/
│   ├── detector.py
│   ├── main.py
│   ├── parser.py
│   └── report.py
│
├── tests/
│   └── test_detector.py
│
├── .gitignore
├── README.md
├── LICENSE
├── SECURITY.md
└── CHANGELOG.md
```

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   **Python**
-   Python `csv`
-   Python `re`
-   Python `argparse`
-   Python `pathlib`
-   Git & GitHub
-   GitHub Actions
-   OpenSSH authentication logs

------------------------------------------------------------------------

## 🧪 Testing

The project includes automated tests for the detection logic.

Run:

``` bash
pytest
```

The project also uses GitHub Actions for automated test execution.

------------------------------------------------------------------------

## 🔐 Security Considerations

This project is intended for defensive security analysis and learning.

When using real logs:

-   Do not commit passwords or secrets.
-   Do not upload private authentication logs.
-   Remove sensitive usernames or IP information when necessary.
-   Keep credentials and API keys outside the repository.
-   Review datasets before publishing them publicly.

The included OpenSSH dataset is used as a sample security-analysis
dataset.

------------------------------------------------------------------------

## 🎓 What I Learned

Building this project helped me understand several practical concepts
beyond writing individual Python scripts.

### 1. Log Parsing

I learned how raw security logs can be converted into structured data
using:

-   CSV parsing
-   Regular expressions
-   Pattern matching
-   Field extraction

### 2. Event Normalization

Different SSH messages have different structures. I learned to convert
them into a common event model:

``` text
user
ip_address
status
```

This makes the detection layer easier to maintain.

### 3. Detection Logic

I implemented detection for:

-   Failed authentication
-   Successful authentication
-   Repeated failed attempts
-   Brute-force-style activity

I also learned how a configurable threshold changes detection
sensitivity.

### 4. Modular Software Design

Instead of putting everything into one Python file, the project
separates:

``` text
Parsing
   ↓
Detection
   ↓
Reporting
   ↓
CLI orchestration
```

This makes individual components easier to understand, test, and extend.

### 5. CLI Application Development

I learned how to make a Python security tool configurable from the
command line using `argparse`.

For example:

``` bash
--log
--threshold
--output
```

### 6. Debugging

I worked through issues involving:

-   File paths
-   CLI arguments
-   parser assumptions
-   function parameter changes
-   integration between modules
-   Git repository configuration

### 7. Git & GitHub

I practiced:

``` text
git init
git add
git commit
git remote
git push
```

and learned how to manage changes without uploading unnecessary files
such as virtual environments or caches.

### 8. Security Mindset

The project helped me think about logs from a SOC analyst perspective:

``` text
What happened?
      ↓
Who was targeted?
      ↓
Which IP generated the activity?
      ↓
How frequently did it happen?
      ↓
Does it cross a detection threshold?
      ↓
Should an alert be generated?
```

------------------------------------------------------------------------

## 🚀 Future Roadmap

### Milestone 2 --- Multi-Log Architecture

-   Apache/web-server parser
-   Generic authentication CSV parser
-   Automatic log-type detection
-   Common normalized event schema
-   Separate parser modules

### Milestone 3 --- Expanded Detection Engine

-   More authentication rules
-   Suspicious HTTP activity
-   IP-based behavioral detection
-   Additional configurable detection rules

### Milestone 4 --- Structured JSON Output

Generate machine-readable reports:

``` text
security_report.json
```

This will allow the output to be consumed by:

``` text
Dashboard
   ↓
API
   ↓
SIEM
   ↓
Other security tools
```

### Milestone 5 --- Testing & Code Quality

-   More parser tests
-   CLI tests
-   Edge-case tests
-   Coverage
-   CI improvements

### Milestone 6 --- SOC Dashboard

``` mermaid
flowchart LR
    A[SSH Logs] --> P[Parser Layer]
    B[Apache Logs] --> P
    C[Other Logs] --> P

    P --> N[Normalized Events]
    N --> D[Detection Engine]
    D --> J[JSON / Database]
    J --> S[SOC Dashboard]
    S --> A1[Alerts]
    S --> A2[Analytics]
    S --> A3[Investigation View]
```

------------------------------------------------------------------------

## 💡 Key Takeaway

This project started as a simple authentication-log analyzer and evolved
into a modular security-analysis pipeline.

The main engineering principle is:

> **Parse raw security data → normalize events → apply detection rules →
> produce actionable output.**

The architecture is intentionally designed so that additional log
sources and detection capabilities can be added later without rewriting
the entire application.

------------------------------------------------------------------------

## 👤 Author

**Sujal Maity**\
B.Tech Computer Science & Engineering

Focus areas:

-   Cybersecurity
-   SOC / Security Operations
-   Cloud Security
-   DevOps
-   Python Automation

------------------------------------------------------------------------

## ⭐ Project Status

**Milestone 1 --- Completed ✅**

**Milestone 2--6 --- Planned 🚧**
