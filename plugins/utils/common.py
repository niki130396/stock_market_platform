def parse_numeric_string(s: str) -> (int, float):
    if "," in s:
        s = s.replace(",", "")
    if "." in s:
        return float(s)
    return int(s)
