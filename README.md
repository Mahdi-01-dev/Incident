## Instructions for Running

### **Pre-requisites**
1. Ensure you have Python 3.7+ installed.

2. The script does not require additional dependencies beyond Python's standard library. Ensure the following imports work in your Python environment:
   - `json`
   - `math`
   - `argparse`
   - `datetime`

---

### **How to Run the Script**

To run the script, use the following command:

```bash
python render-schedule.py \
    --schedule=schedule.json \
    --overrides=overrides.json \
    --from="START_TIME" \
    --until="END_TIME"
```
or

```bash
python3 render-schedule.py \
    --schedule=schedule.json \
    --overrides=overrides.json \
    --from="START_TIME" \
    --until="END_TIME"
```
<br><br>
## **Comments on Code Structure and Approach**

#### **Code Structure**
1. **`ScheduleEntry` Class**:
   - Represents a single entry of the schedule (a user and their assigned time period).
   - Encapsulates logic for converting the entry into a JSON-serialisable format (`to_json`).
   - Keeps the code modular by separating the concept of a schedule entry from the scheduling logic.

2. **Key Functions**:
   - **`parse_time`**:
     - Handles time parsing from ISO 8601 format to Python `datetime` objects.
     - Ensures consistent time handling, particularly with UTC (`Z`) timestamps.
   - **`load_files`**:
     - Responsible for loading and validating the input JSON files (`schedule.json` and `overrides.json`).
     - Sorts the overrides (I assume the given overrides aren't already).
   - **`create_schedule`**:
     - The core logic of the script, which:
       - Generates the schedule based on user rotations and handover intervals, and handles truncation.
       - Uses a sort of 2 pointer technique, with a pointer for the expected user to run and another for the override.
       - Returns a list of ScheduleEntry objects in order of their scheduled time.
       
#### **Approach**
- The script generates the schedule based on user rotations and handover intervals, handling truncation where necessary.
- A two-pointer technique is used:
  - One pointer tracks the expected user in the rotation.
  - Another pointer iterates through the overrides.
- The result is a list of `ScheduleEntry` objects, sorted in chronological order.
