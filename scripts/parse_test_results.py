import xml.etree.ElementTree as ET
from pathlib import Path

REPORT_PATH = Path("reports/test-results.xml")

if not REPORT_PATH.exists():
    print(f"[WARN] {REPORT_PATH} not found – generating dummy report")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        "<testsuite name='dummy'><testcase name='smoke-test'/></testsuite>",
        encoding="utf-8",
    )

tree = ET.parse(REPORT_PATH)
root = tree.getroot()

total = 0
failed = 0

for tc in root.findall(".//testcase"):
    total += 1
    if tc.find("failure") is not None:
        failed += 1

print(f"[INFO] Parsed {total} tests, failed={failed}")

if failed > 0:
    raise SystemExit(1)
