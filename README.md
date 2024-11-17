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
