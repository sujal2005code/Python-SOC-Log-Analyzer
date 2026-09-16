"""
parser.py

Responsible for loading and parsing authentication log files.
"""

import csv
import re


def load_log_file(file_path):
    """
    Load authentication logs from a CSV file.

    Supports structured OpenSSH log datasets.
    """

    events = []

    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            content = row.get("Content", "")

            # Successful password authentication
            success_password = re.search(
                r"Accepted password for (?:invalid user )?(\S+) from ([\d.]+)",
                content,
                re.IGNORECASE,
            )

            # Successful public-key authentication
            success_key = re.search(
                r"Accepted publickey for (?:invalid user )?(\S+) from ([\d.]+)",
                content,
                re.IGNORECASE,
            )

            # Failed password authentication
            failed_password = re.search(
                r"Failed password for (?:invalid user )?(\S+) from ([\d.]+)",
                content,
                re.IGNORECASE,
            )

            # Invalid SSH username
            invalid_user = re.search(
                r"Invalid user (\S+) from ([\d.]+)",
                content,
                re.IGNORECASE,
            )

            if success_password:
                events.append(
                    {
                        "user": success_password.group(1),
                        "ip_address": success_password.group(2),
                        "status": "SUCCESS",
                    }
                )

            elif success_key:
                events.append(
                    {
                        "user": success_key.group(1),
                        "ip_address": success_key.group(2),
                        "status": "SUCCESS",
                    }
                )

            elif failed_password:
                events.append(
                    {
                        "user": failed_password.group(1),
                        "ip_address": failed_password.group(2),
                        "status": "FAILED",
                    }
                )

            elif invalid_user:
                events.append(
                    {
                        "user": invalid_user.group(1),
                        "ip_address": invalid_user.group(2),
                        "status": "FAILED",
                    }
                )

    return events