
def extract_log_sections(log_text):
    """
    Split log file into chunks based on lines containing INFO, ERROR, WARN.
    """
    lines = log_text.splitlines()
    chunks, current = [], []

    for line in lines:
        if any(tag in line for tag in ['INFO', 'WARN', 'ERROR']):
            if current:
                chunks.append("\n".join(current))
                current = []
        current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks
