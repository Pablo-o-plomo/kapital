import re
from datetime import date
from app.services.report_types import REPORT_TYPES

SUBJECT_PATTERN = re.compile(r"\[(?P<restaurant_code>[A-Z0-9_]+)\]\s+(?P<report_code>R\d{2})?.*?(?P<d1>\d{4}-\d{2}-\d{2})(?:_(?P<d2>\d{4}-\d{2}-\d{2}))?", re.I)


def detect_report_code(subject: str, filename: str | None = None) -> str | None:
    target = f"{subject} {filename or ''}".upper()
    m = re.search(r"R\d{2}", target)
    if m and m.group(0) in REPORT_TYPES:
        return m.group(0)
    for code, meta in REPORT_TYPES.items():
        if meta['name_ru'].upper().split('/')[0].strip() in target:
            return code
    return None


def parse_subject(subject: str, filename: str | None = None):
    m = SUBJECT_PATTERN.search(subject.upper().strip())
    if not m:
        return None
    report_code = detect_report_code(subject, filename)
    d1 = date.fromisoformat(m.group('d1'))
    d2 = date.fromisoformat(m.group('d2')) if m.group('d2') else d1
    return {'restaurant_code': m.group('restaurant_code'), 'report_code': report_code or 'UNKNOWN', 'report_date_start': d1, 'report_date_end': d2}
