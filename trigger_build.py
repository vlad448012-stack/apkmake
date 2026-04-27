import requests
import base64

GITHUB_TOKEN = "github_pat_твой_токен"
REPO_OWNER = "vlad448012-sta"
REPO_NAME = "apkmake"

with open("my_app.py", "r") as f:
    python_code = f.read()

encoded = base64.b64encode(python_code.encode()).decode()

resp = requests.post(
    f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/build-apk.yml/dispatches",
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"},
    json={"ref": "main", "inputs": {"python_code": encoded}}
)

print("✅ Сборка запущена!" if resp.status_code == 204 else f"❌ Ошибка: {resp.status_code}")
