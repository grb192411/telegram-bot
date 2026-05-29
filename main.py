import requests
import time
import os

BOT_TOKEN = "8983766299:AAFhbL3GlF7J4ueeMQ3GfORZMDRzBmldqwo"
CHANNEL_ID = "@pythonggrb"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def send_image(image_path, caption=""):
    if not os.path.exists(image_path):
        send_message(CHANNEL_ID, f"❌ Missing image: {image_path}")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        requests.post(
            url,
            data={"chat_id": CHANNEL_ID, "caption": caption},
            files={"photo": photo}
        )

# ✅ SAFE get_updates (NO CRASH)
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}

    try:
        response = requests.get(url, params=params).json()
        print("API RESPONSE:", response)  # 🔍 debug

        if response.get("ok"):
            return response.get("result", [])
        else:
            print("❌ API ERROR:", response)
            return []

    except Exception as e:
        print("❌ ERROR:", e)
        return []

print("⏳ Waiting for teacher to start exam...")

last_update_id = None

while True:
    updates = get_updates(last_update_id)

    for update in updates:
        last_update_id = update["update_id"] + 1

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            print("Received:", text)  # 🔍 debug

            # ✅ TRIGGER (FIXED)
            if "start_test_123" in text:

                send_message(CHANNEL_ID, "📢 TEST RULES\n- Duration: 30 min\n- Each set: 3 min")
                time.sleep(2)

                send_message(CHANNEL_ID, "🚀 EXAM STARTED")
                time.sleep(2)

                start_time = time.time()
                duration = 30 * 60
                interval = 3 * 60
                set_no = 1

                while time.time() - start_time < duration:

                    send_image(f"images/SET-{set_no}.png", f"📚 SET {set_no}")

                    time.sleep(interval)

                    send_message(CHANNEL_ID, f"⏳ SET {set_no} TIME OVER")

                    set_no += 1

                send_message(CHANNEL_ID, "⛔ EXAM ENDED")