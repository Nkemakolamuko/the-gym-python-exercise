#!/usr/bin/env python3
import subprocess
import argparse

file_path = "/var/log/boot.log"

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

def read_log(file_path: str):
    with open(file_path, "r", encoding="utf-8") as log_file:
        for i, line in enumerate(log_file, start=1):
            print(f"Line {i}: {line.rstrip()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a log file line by line")
    parser.add_argument("-file", required=True, help="Path to the log file")
    args = parser.parse_args()

    read_log(args.file)
