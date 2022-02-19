def parse_numeric_string(s: str) -> (int, float):
    if not s[-1].isdigit():
        return s
    if "," in s:
        s = s.replace(",", "")
    if "." in s:
        return float(s)
    return int(s)
