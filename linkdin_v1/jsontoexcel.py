import json
import pandas as pd

def convert_jsonl_to_excel(jsonl_path, excel_path):
    data = []
    
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON: {e}")
    
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    print(f"✅ Conversion terminée : {excel_path}")

# Exemple d'utilisation
convert_jsonl_to_excel(
    "linkdin/output/people.jsonl",
    "linkdin/output/people.xlsx"
)