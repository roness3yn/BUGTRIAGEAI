import zipfile

# Compress the large CSV into a zip file
with zipfile.ZipFile("data/processed/normalized_dataset_bugs.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("data/processed/normalized_dataset_bugs.csv", arcname="normalized_dataset_bugs.csv")

print("File compressed successfully!")