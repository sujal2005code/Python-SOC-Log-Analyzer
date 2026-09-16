"""
python-soc-log-analyzer

Main application entry point.
"""

import argparse
from pathlib import Path

from detector import detect_brute_force, detect_failed_logins
from parser import load_log_file
from report import generate_summary, save_report


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_FILE = BASE_DIR / "sample_logs" / "authentication_logs.csv"
DEFAULT_REPORT_FILE = BASE_DIR / "reports" / "security_report.txt"


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """

    parser = argparse.ArgumentParser(
        description="Analyze authentication logs for suspicious activity."
    )

    parser.add_argument(
        "--log",
        type=Path,
        default=DEFAULT_LOG_FILE,
        help="Path to the authentication log CSV file.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Failed login threshold for brute-force detection.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPORT_FILE,
        help="Path where the security report will be saved.",
    )

    args = parser.parse_args()

    if args.threshold < 1:
        parser.error("--threshold must be at least 1.")

    return args


def main():
    """
    Run the SOC Log Analyzer.
    """

    args = parse_arguments()

    events = load_log_file(args.log)

    failed_logins = detect_failed_logins(events)
    alerts = detect_brute_force(
        events,
        threshold=args.threshold,
    )

    total_events = len(events)

    successful_logins = sum(
        1
        for event in events
        if event["status"].strip().upper() == "SUCCESS"
    )

    generate_summary(
        total_events,
        successful_logins,
        failed_logins,
        alerts,
    )

    save_report(
        total_events,
        successful_logins,
        failed_logins,
        alerts,
        args.output,
    )

    print(f"\nReport saved to: {args.output}")

if __name__ == "__main__":
    main()