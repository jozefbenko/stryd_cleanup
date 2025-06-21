import pandas as pd
import re

def clean_csv():
    input_path = input("Enter path to Stryd CSV file: ").strip()
    output_path = re.sub(r'\.csv$', '', input_path) + '_cleaned.csv'

    with open(input_path, 'r') as f:
        raw = f.read().strip()

    all_items = raw.split(',')

    # Find where the actual headers start (skip "Timestamp" if present)
    try:
        start_idx = all_items.index("Power (w/kg)")
    except ValueError:
        raise ValueError("Header 'Power (w/kg)' not found — is this a valid Stryd CSV?")

    headers = all_items[start_idx:start_idx+19]
    headers[-1] = re.sub(r'\d{10}$', '', headers[-1].strip())

    assert len(headers) == 19, f"Expected 19 headers, got {len(headers)}"

    data_values = all_items[start_idx+19:]

    numeric_values = []
    for val in data_values:
        try:
            numeric_values.append(float(val))
        except ValueError:
            continue

    num_rows = len(numeric_values) // 19
    data_matrix = [numeric_values[i * 19:(i + 1) * 19] for i in range(num_rows)]

    df = pd.DataFrame(data_matrix, columns=headers)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned CSV saved as: {output_path}")

if __name__ == "__main__":
    clean_csv()