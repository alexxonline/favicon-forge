import json
import pathlib
import urllib.request

payload = {"prompt": "A minimalist comet with a star-shaped tail"}

request = urllib.request.Request(
    "http://localhost:8000/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request) as response:
    data = json.loads(response.read().decode("utf-8"))

output_path = pathlib.Path(__file__).with_name("output.svg")
output_path.write_text(data.get("svg", ""), encoding="utf-8")
print(f"Saved SVG to {output_path}")
