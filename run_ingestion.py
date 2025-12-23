import os
from pathlib import Path
import subprocess

# Load .env file
env_path = Path(".env")
if not env_path.exists():
    raise FileNotFoundError("Error: .env file not found.")

with open(env_path, "r") as f:
    for line in f:
        if line.strip() and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

# Create the final config file by replacing placeholders
template_path = Path("open-metadata/dbt_local_config.template.yml")
config_path = Path("open-metadata/dbt_local_config.yml")

with open(template_path, "r") as template_file:
    template_content = template_file.read()

# Replace placeholders with actual values
config_content = template_content.replace(
    "${DBT_CATALOG_PATH}", os.environ["DBT_CATALOG_PATH"]
).replace(
    "${DBT_MANIFEST_PATH}", os.environ["DBT_MANIFEST_PATH"]
).replace(
    "${DBT_RUN_RESULTS_PATH}", os.environ["DBT_RUN_RESULTS_PATH"]
).replace(
    "${OM_BOT_JWT_TOKEN}", os.environ["OM_BOT_JWT_TOKEN"]
)

with open(config_path, "w") as config_file:
    config_file.write(config_content)

# Print the generated config for debugging
print("Generated config file:")
print(config_content)

# Run ingestion
subprocess.run(["metadata", "ingest", "-c", str(config_path)], check=True)
