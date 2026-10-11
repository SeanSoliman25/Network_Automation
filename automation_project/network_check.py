import json
from datetime import datetime
from pathlib import Path

inv_path = Path(__file__).parent / "inventory.json"

with open(inv_path, "r", encoding="utf-8") as inv:
    data = json.load(inv)

for entry in data:
    print(entry["name"])
    print(f"\tIP Address: {entry['address']}")
    print(f"\tDevice: {entry['model']}")
    print(f"\tLocation: {entry['location']}")
    print(f"\tStatus: {'UP' if entry['status'] else 'DOWN'}")

out_path = Path(__file__).parent / "output.json"

try:
    with open(out_path, "r", encoding="utf-8") as out:
        out_json = json.load(out)
    out_json.append({"id":len(out_json)+1, "time":f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "data":data})
except:
    out_json = [{"id":1, "time":f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "data":data}]

with open(out_path, "w", encoding="utf-8") as out:
    json.dump(out_json, out, indent=4, ensure_ascii=False)