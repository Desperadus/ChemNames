import pandas as pd
import requests
from tqdm import tqdm
import re
import json


def get_kegg_id(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for CID {cid}")
        return None

    try:
        json_string = json.dumps(response.json())
        # Use regex to find the KEGG ID
        match = re.search(r"kegg.jp/entry/(\w+)", json_string)
        if match:
            return match.group(1)
    except ValueError:
        print("Invalid JSON response")

    return None


def main():
    df = pd.read_csv("output.csv")

    df["kegg"] = None

    for index, row in tqdm(df.iterrows()):
        cid = row["CID"]
        if cid != "xxxxxx":
            kegg_id = get_kegg_id(cid)
            if kegg_id is not None:
                df.at[index, "kegg"] = kegg_id
            else:
                df.at[index, "kegg"] = "xxxxxx"
        else:
            df.at[index, "kegg"] = "xxxxxx"

    df.to_csv("updated_file.csv", index=False)


if __name__ == "__main__":
    main()
    # print(get_kegg_id(280))
