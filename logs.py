#!/usr/bin/env python3
import subprocess
import argparse
import json
import re
from datetime import datetime

# file_path = "/var/log/boot.log"

# with open("/var/log/boot.log", "r", encoding="utf-8") as log_file:
#     content = log_file.read()
#     print(content)

# try:
#     result = subprocess.run(['sudo', 'tail', '-f', '-n', '5', file_path], capture_output=True, text=True, check=True)
#     file_content = result.stdout
#     print(file_content[:50])
# except subprocess.CalledProcessError as e:
#     print(e.stderr)

# process = subprocess.Popen(['sudo', 'tail', '-f', '-n', '5', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# try:
#     for i, line in enumerate(iter(process.stdout.readline, "")):
#         print(f"Line {i}: {line.strip()}")
# except KeyboardInterrupt:
#     print("\nInterrupted...")
#     process.terminate()

# Solution One
def read_log(file_path):
    with open(file_path, "r", encoding="utf-8") as log_file:
        for i, line in enumerate(log_file, start=1):
            # print(f"Line {i}: {line.rstrip()}")
            parsed = detect_and_parse(line)
            if parsed:
                print(f"Line {i}: [{parsed['level']}] {parsed['timestamp']} — {parsed['message']}")
            else:
                print(f"Line {i}: [UNRECOGNIZED] {line.rstrip()}")


# Solution Two
def detect_and_parse(line: str) -> dict | None:
    line = line.strip()
    if not line:
        return None

    # Try JSON first
    try:
        data = json.loads(line)
        return {
            "timestamp": data.get("timestamp", ""),
            "level":     data.get("level", ""),
            "message":   data.get("message", "")
        }
    except json.JSONDecodeError:
        pass

    # Format 1: "2024-01-15 10:03:22 ERROR message"
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)", line)
    if match:
        return {
            "timestamp": match.group(1),
            "level":     match.group(2),
            "message":   match.group(3)
        }

    # Format 2: syslog "2026-06-06T22:09:01.712376+02:00 hostname PROCESS[pid]: message"
    match = re.match(r"(\S+)\s+\S+\s+(\w+)\[\d+\]:\s+(.*)", line)
    if match:
        return {
            "timestamp": match.group(1),
            "level":     "INFO", #syslog has no level field, default to INFO
            "message":   match.group(3)
        }

    return None  

# SOlution to Three
def count_log_levels(file_path: str):
    errors   = 0
    warnings = 0
    info     = 0

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            parsed = detect_and_parse(line)
            if parsed:
                level = parsed["level"].upper()
                if level == "ERROR":
                    errors += 1
                elif level == "WARNING":
                    warnings += 1
                elif level == "INFO":
                    info += 1

    print(f"Errors:   {errors}")
    print(f"Warnings: {warnings}")
    print(f"Info:     {info}")

# Solution to Four
def most_common_error(file_path: str):
    error_counts = {}

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            parsed = detect_and_parse(line)
            if parsed and parsed["level"].upper() == "ERROR":
                message = parsed["message"]
                if message in error_counts:
                    error_counts[message] += 1
                else:
                    error_counts[message] = 1

    if error_counts:
        top_error = max(error_counts, key=error_counts.get)
        print(f'Most frequent error: "{top_error}" ({error_counts[top_error]} times)')
    else:
        print("No errors found.")

# Solution to 5
def filter_logs(file_path, level_filter, from_time, to_time):
    from_dt = datetime.strptime(from_time, "%Y-%m-%d %H:%M") if from_time else None
    to_dt   = datetime.strptime(to_time,   "%Y-%m-%d %H:%M") if to_time   else None
    with open(file_path, "r", encoding="utf-8") as log_file:
        for i, line in enumerate(log_file, start=1):
            parsed = detect_and_parse(line)
            if not parsed:
                continue

            # Filter by level
            if level_filter and parsed["level"].upper() != level_filter.upper():
                continue

            # Filter by time range
            if from_dt or to_dt:
                try:
                    line_dt = datetime.strptime(parsed["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if from_dt and line_dt < from_dt:
                        continue
                    if to_dt and line_dt > to_dt:
                        continue
                except ValueError:
                    continue  # skip lines with unparseable timestamps

            print(f"Line {i}: [{parsed['level']}] {parsed['timestamp']} — {parsed['message']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a log file line by line")
    parser.add_argument("-file", required=True, help="Path to the log file")
    parser.add_argument("--level", default=None, help="Filter by log level e.g. ERROR")
    parser.add_argument("--from",  dest="from_time", default=None, help='Start time e.g. "2024-01-15 10:00"')
    parser.add_argument("--to",    dest="to_time",   default=None, help='End time e.g. "2024-01-15 12:00"')
    args = parser.parse_args()

    read_log(args.file)
    print()
    count_log_levels(args.file)
    print()
    most_common_error(args.file)
    print()
    filter_logs(args.file, level_filter=args.level, from_time=args.from_time, to_time=args.to_time)
