## 🚆 Train Reminder Script – VBB Journey Notifier

This script helps a commuter avoid missing their train by setting a reminder **10 minutes before departure**.  
It uses the **VBB (BVG) transport API** to fetch upcoming journeys from a given origin to a destination station.

### 🏙️ Assumptions About the Commute

In my hypothesis:

- The colleague **starts at station A**, which is the nearest urban station to the colleague's office.  
  He prefers to walk a bit more, so instead of taking the Kochstr. U-Bahn, he walks to **U Stadtmitte** station.

- The colleague **lives in Potsdam**, so his destination is set as **S Potsdam Hauptbahnhof**.

```python
stationA = {"id": "900100011", "name": "U Stadtmitte"}
stationB = {"id": "900230999", "name": "S Potsdam Hauptbahnhof"}
```

---

### ✅ How It Works

1. The user is asked to input the desired train departure time (e.g., `17:30`).
2. The script calculates a reminder time (10 minutes earlier).
3. At that reminder time, a macOS dialog pops up reminding the user to leave.
4. It displays the next available **train line** and **departure station**.
5. The full journey, with all relevant legs, is printed in the terminal.

---

### 🧪 Testing Mode

For testing purposes, the script **simulates the reminder time as now**, so the final dialog appears immediately—even if the actual departure time is later.

---

### ⚠️ Platform Note

This version uses **AppleScript via `osascript`**, which only works on **macOS**.  
If you're using **Windows** or **Linux**, replace `show_dialog` with a cross-platform library such as:

- [`tkinter`](https://docs.python.org/3/library/tkinter.html)
- [`plyer`](https://plyer.readthedocs.io/en/latest/)
