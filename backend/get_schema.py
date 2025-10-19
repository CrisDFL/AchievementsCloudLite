import requests, json

API_KEY = "3D6B5AA52BE9B69C62F179D2FA1BB800"  # reemplázala por tu key de https://steamcommunity.com/dev/apikey
APP_ID = 367520

r = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={API_KEY}&appid={APP_ID}")
schema = r.json()

ach_map = {}
for a in schema["game"]["availableGameStats"]["achievements"]:
    ach_map[a["name"]] = {
        "displayName": a["displayName"],
        "description": a.get("description", "")
    }

with open("steam_schema.json", "w", encoding="utf-8") as f:
    json.dump(ach_map, f, indent=2)
print("Archivo steam_schema.json creado con", len(ach_map), "logros.")
