from aiohttp import ClientSession
import argparse
import csv
import pubchempy as pcp
import asyncio
from tqdm import tqdm


def get_chemical_data(name):
    if "Analyte" in name:
        return {"cid": "xxxxxx", "smiles": "xxxxxx", "inchikey": "xxxxxx"}
    try:
        compounds = pcp.get_compounds(name, "name")
        result = {"cid": "", "smiles": "", "inchikey": ""}

        if compounds:
            compound = compounds[0]
            result["cid"] = compound.cid
            result["smiles"] = compound.isomeric_smiles
            result["inchikey"] = compound.inchikey
        else:
            result = {key: "xxxxxx" for key in result.keys()}

        return result
    except Exception as e:
        return {"cid": "xxxxxx", "smiles": "xxxxxx", "inchikey": "xxxxxx"}


def process_csv_row(chemical_name):
    data = get_chemical_data(chemical_name)
    return [chemical_name, data["cid"], data["smiles"], data["inchikey"]]


def main():
    parser = argparse.ArgumentParser(
        description="Process a CSV file to obtain chemical data."
    )
    parser.add_argument("file_path", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    with open(args.file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        # Assuming each row has one column
        tasks = [row[0] for row in reader]
        results = []
        for name in tqdm(tasks):
            results.append(process_csv_row(name))

    with open(args.output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Writing headers
        writer.writerow(["Name", "CID", "SMILES", "InChIKey"])
        writer.writerows(results)


if __name__ == "__main__":
    main()
