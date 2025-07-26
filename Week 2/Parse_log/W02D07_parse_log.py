import os
import re

module_path = os.path.dirname(os.path.realpath(__file__))
filename = 'app.log'
file_path = os.path.join(module_path, ".." , "Simulating_log", filename)
print(file_path)

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{2,3})\s+"
    r"(?P<level>[A-Z]+)\s+\[(?P<service>.*?)\]\s+"
    r"(?P<message>.*)$"
)

def parse_complex_log(log_line):
    """Parses a complex log line using regex."""
    match = LOG_PATTERN.search(log_line)
    if match:
        return match.groupdict()
    return {"raw_line": log_line.strip(), "parse_error": "No match"}

parsed_data = []

with open(file_path) as f:
    for line in f.readlines():
        match_regex = parse_complex_log(line)
        parsed_data.append(match_regex)

print(parsed_data[:5])