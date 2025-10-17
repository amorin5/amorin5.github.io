import requests
import csv
import sys
import os

# === CONFIGURATION ===
SONAR_HOST = "https://sonar.gaptech.com"
PROJECT_KEY = "com.gap.pricing.price-engine:pnp-order-pricing"
AUTH_TOKEN = ""  # Replace with your token or use env variable

# === VALIDATE CLI ARGUMENT ===
if len(sys.argv) != 2:
    print("Usage: python sonar_script.py <relative_file_path>")
    print("Example: python sonar_script.py root/package/src/File.java")
    sys.exit(1)

file_path = sys.argv[1]

# === API URL AND PARAMS ===
url = f"{SONAR_HOST}/api/issues/search"
params = {
    "componentKeys": PROJECT_KEY,
    "severities": "BLOCKER",
    "statuses": "OPEN,CONFIRMED",
    "resolved": "false",
    "ps": 500,
    "facets": "severities",
    "additionalFields": "_all",
    "types": "BUG,CODE_SMELL,VULNERABILITY",
    "files": file_path
}

headers = {
    "Accept": "application/json"
}
auth = (AUTH_TOKEN, "") if AUTH_TOKEN else None

# === MAKE REQUEST ===
print(f"📡 Fetching BLOCKER issues for file: {file_path}")
response = requests.get(url, headers=headers, params=params, auth=auth)
response.raise_for_status()
data = response.json()

# === WRITE TO CSV ===
output_file = f"sonar_blockers_{os.path.basename(file_path)}.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Type", "Severity", "Message", "Component", "Line", "Rule", "Effort", "Status"])

    for issue in data.get("issues", []):
        writer.writerow([
            issue.get("type"),
            issue.get("severity"),
            issue.get("message"),
            issue.get("component"),
            issue.get("line"),
            issue.get("rule"),
            issue.get("effort"),
            issue.get("status")
        ])

print(f"✅ Exported {len(data.get('issues', []))} BLOCKER issues to {output_file}")
