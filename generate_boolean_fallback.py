import pandas as pd
import json
import re

# Load the CSV
csv_file = "milx0724.csv"
df = pd.read_csv(csv_file, quotechar='"', on_bad_lines='skip')

MOS_CODE_COLUMN = "MOC"
ONET_TITLE_COLUMNS = ["ONET1_TITLE", "ONET2_TITLE", "ONET3_TITLE", "ONET4_TITLE"]

# Load stopwords
stopwords_file = "stopwords.txt"

try:
    with open(stopwords_file, "r") as f:
        STOPWORDS = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    STOPWORDS = set([
        "and", "or", "of", "the", "commercial", "inspectors", "copilots", "pilots",
        "airline", "airlines", "flight", "aviation", "with", "without", "other", "not", "miscellaneous"
    ])

fallback_mapping = {}

for _, row in df.iterrows():
    mos_code = str(row[MOS_CODE_COLUMN]).strip()
    titles_combined = " ".join([str(row[col]).strip() for col in ONET_TITLE_COLUMNS if pd.notna(row[col])])
    words = re.sub(r'[^\w\s]', '', titles_combined).split()
    
    keywords = [word.capitalize() for word in words if word.lower() not in STOPWORDS and len(word) > 2]

    if keywords:
        boolean_string = "(" + " OR ".join(sorted(set(keywords))) + ")"
        fallback_mapping[mos_code] = boolean_string
    else:
        fallback_mapping[mos_code] = mos_code

# Minify + save
output_file = "mos_fallback_mapping_boolean.min.json"
with open(output_file, "w") as f:
    json.dump(fallback_mapping, f, separators=(',', ':'))

print("✅ DONE → Generated:", output_file)
