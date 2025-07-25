import subprocess
from pyparsing import line
import requests
from datetime import datetime, timedelta

def ask_input(prompt, title="Input Required"):
    script = f'''
    set userInput to text returned of (display dialog "{prompt}" with title "{title}" default answer "")
    return userInput
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()

def show_dialog(message, title="Reminder"):
    safe_message = message.replace('"', '\\"')
    script = f'display dialog "{safe_message}" with title "{title}" buttons {{"OK"}} default button "OK"'
    subprocess.run(["osascript", "-e", script])

colleagueName = "Jörg"
stationA = {"id": "900100011", "name": "U Stadtmitte"}
stationB = {"id": "900230999", "name": "S Potsdam Hauptbahnhof"}

def fetch_journeys(from_id, to_id, departure_time_iso, results=5):
    url = "https://v6.bvg.transport.rest/journeys"
    params = {
        "from": from_id,
        "to": to_id,
        "departure": departure_time_iso,
        "results": results,
        "language": "en",
        "stopovers": False
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def main():
    user_time_str = ask_input("At what time do you need to catch the train? (HH:MM, 24h format)")
    try:
        user_time = datetime.strptime(user_time_str, "%H:%M")
    except ValueError:
        show_dialog("Invalid time format. Please enter HH:MM (e.g. 17:30).", title="Error")
        return

    now = datetime.now().astimezone()
    user_time = user_time.replace(year=now.year, month=now.month, day=now.day, tzinfo=now.tzinfo)
    reminder_time = user_time - timedelta(minutes=10)
    reminder_str = reminder_time.strftime("%H:%M")

    show_dialog(f"Perfect, I will remind you at {reminder_str} to catch your train.", title="Reminder Set")

    journeys_data = fetch_journeys(
        from_id=stationA["id"],
        to_id=stationB["id"],
        departure_time_iso=reminder_time.isoformat()
    )

    journeys = journeys_data.get("journeys", [])
    if not journeys:
        show_dialog("No journeys found after your reminder time.", title="No Journeys")
        return

    legs = journeys[0]["legs"]
    first_leg = legs[0]

    dep_time = datetime.fromisoformat(first_leg["departure"]).strftime("%H:%M")
    dep_station = first_leg["origin"]["name"]
    line = first_leg.get("line", {}).get("name", "unknown")

    message = (
    f"Hey {colleagueName}, It's time to go, it's already {reminder_str}!\n"
    f"Next available journey:\n"
    f"Line {line}\n"
    f"Departure: {dep_station} at {dep_time}\n"
    f"For full trip details, check the terminal logs."
)
    show_dialog(message, title="Train Reminder")
    print("\n--- FULL JOURNEY ---")
    for i, leg in enumerate(journeys[0]["legs"], start=1):
        origin = leg["origin"]["name"]
        destination = leg["destination"]["name"]
        dep = datetime.fromisoformat(leg["departure"]).strftime("%H:%M")
        arr = datetime.fromisoformat(leg["arrival"]).strftime("%H:%M")
        line = leg.get("line", {}).get("name")

        if not line or origin == destination:
            continue

        print(f"\nLeg {i}:")
        print(f"  Line: {line}")
        print(f"  From: {origin} at {dep}")
        print(f"  To:   {destination} at {arr}")

if __name__ == "__main__":
    main()
