import re
from pathlib import Path
from pprint import pprint

LOG_START_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+"
    r"(?P<level>[A-Z]+)\s+\[(?P<class>[^\]]+)\]\s+(?P<message>.*)"
)

def parse_log_lines(lines):
    entries = []
    current_entry = []

    for line in lines:
        print("line", line)
        if LOG_START_PATTERN.match(line):
            print("current_entry", current_entry)
            if current_entry:
                entries.append(current_entry)
            current_entry = [line.rstrip()]
        else:
            if current_entry:
                current_entry.append(line.rstrip())

    if current_entry:
        entries.append(current_entry)

    return entries

def parse_log_entry(lines):
    header_match = LOG_START_PATTERN.match(lines[0])  #MATCH
    if not header_match:
        return {}

    data = header_match.groupdict()  #dict
    stack_trace = []
    for line in lines[1:]:
        if line.startswith("    ") or line.startswith("Caused by:") or line.startswith("at ") or line.startswith("..."):
            stack_trace.append(line.strip())

    if stack_trace:
        data["stack_trace"] = stack_trace
    return data

def parse_log_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    raw_entries = parse_log_lines(lines)
    print("-------raw_entries--------")
    pprint(raw_entries)
    print("-------raw_entries--------")
    parsed_entries = [parse_log_entry(entry) for entry in raw_entries]
    print("-------parsed_entries--------")
    pprint(parsed_entries)
    print("-------parsed_entries--------")
    return parsed_entries

# Example usage
if __name__ == "__main__":
    log_path = Path("app_java.log")
    logs = parse_log_file(log_path)

    for log in logs:
        pprint(log)
