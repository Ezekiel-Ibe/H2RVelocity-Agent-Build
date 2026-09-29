"""Temporary probe: inspect the a01-workspace response identity and annotations."""
import json
import urllib.request

from azure.identity import DefaultAzureCredential

BASE = "https://velocity-h2r-proj-resource.services.ai.azure.com/api/projects/velocity-h2r-proj"
SCOPE = "https://ai.azure.com/.default"
VER = "2025-05-15-preview"

tok = DefaultAzureCredential(exclude_managed_identity_credential=True).get_token(SCOPE).token
payload = {
    "agent": {"name": "a01-workspace", "type": "agent_reference"},
    "input": "Give me one open payroll case as a small markdown table.",
}
req = urllib.request.Request(
    f"{BASE}/openai/responses?api-version={VER}",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

for item in data.get("output", []):
    if item.get("type") != "message":
        continue
    print("AGENT:", json.dumps(item.get("created_by", {}).get("agent", {})))
    for part in item.get("content", []):
        if part.get("type") == "output_text":
            print("TEXT:", part.get("text", "")[:400])
            print("ANNOTATIONS:", json.dumps(part.get("annotations", []), indent=2)[:1500])
