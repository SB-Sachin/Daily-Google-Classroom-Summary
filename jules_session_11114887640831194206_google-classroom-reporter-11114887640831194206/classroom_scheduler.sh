#!/bin/bash
# classroom_scheduler.sh

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Run the reporter and output to a daily report file
REPORT_FILE="reports/report_$(date +%Y-%m-%d).txt"
mkdir -p reports
python3 classroom_reporter.py > "$REPORT_FILE" 2>&1

echo "Report generated at $REPORT_FILE"
