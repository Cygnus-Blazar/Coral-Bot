import json, os, time

COOLDOWN_FILE = os.path.join("src", "data", "cooldowns.json")

def load_cooldowns():
    if not os.path.exists(COOLDOWN_FILE):
        return {}
    with open(COOLDOWN_FILE, "r") as f:
        return json.load(f)

def save_cooldowns(data):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(data, f, indent=2)

cooldowns = load_cooldowns()

def is_on_cooldown(user_id, command, duration):
    now = time.time()
    user_cd = cooldowns.get(user_id, {}).get(command, 0)
    return now - user_cd < duration, max(0, int(duration - (now - user_cd)))

def set_cooldown(user_id, command):
    now = time.time()
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    cooldowns[user_id][command] = now
    save_cooldowns(cooldowns)
