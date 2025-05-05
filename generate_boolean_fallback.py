import pandas as pd
import json
import re

# Load the existing MOS to ONET titles CSV
csv_file = "milx0724.csv"  # Local CSV file
df = pd.read_csv(csv_file, quotechar='"', on_bad_lines='skip')

# Columns to use
MOS_CODE_COLUMN = "MOC"
ONET_TITLE_COLUMNS = ["ONET1_TITLE", "ONET2_TITLE", "ONET3_TITLE", "ONET4_TITLE"]

# Stopwords to remove from keywords
STOPWORDS = set([
    "and", "or", "of", "the", "commercial", "inspectors", "copilots", "pilots", 
    "airline", "airlines", "flight", "aviation", "with", "without", "other", "not", "miscellaneous"
])

# Build fallback mapping with boolean strings
fallback_mapping = {}

for _, row in df.iterrows():
    mos_code = str(row[MOS_CODE_COLUMN]).strip()

    # Combine ONET titles
    titles_combined = " ".join([str(row[col]).strip() for col in ONET_TITLE_COLUMNS if pd.notna(row[col])])

    # Generate keywords
    words = re.sub(r'[^\w\s]', '', titles_combined).split()
    keywords = [word.capitalize() for word in words if word.lower() not in STOPWORDS and len(word) > 2]

    # Create boolean string
    if keywords:
        boolean_string = "(" + " OR ".join(sorted(set(keywords))) + ")"
        fallback_mapping[mos_code] = boolean_string
    else:
        fallback_mapping[mos_code] = mos_code  # Fallback to MOS code itself

# Minify and save
minified_file = "mos_fallback_mapping_boolean.min.json"
with open(minified_file, "w") as f:
    json.dump(fallback_mapping, f, separators=(',', ':'))

print("✅ Boolean fallback mapping generated: mos_fallback_mapping_boolean.min.json")

