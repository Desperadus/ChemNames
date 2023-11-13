from aiohttp import ClientSession
import argparse
import csv
import pubchempy as pcp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from tqdm.asyncio import tqdm


async def get_chemical_data(name, session, executor):
    if "Analyte" in name:
        return {"cid": "xxxxxx", "smiles": "xxxxxx", "inchikey": "xxxxxx"}

    try:
        loop = asyncio.get_event_loop()
        compounds = await loop.run_in_executor(
            executor, pcp.get_compounds, name, "name"
        )
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


async def process_csv_row(chemical_name, session, executor):
    data = await get_chemical_data(chemical_name, session, executor)
    return [chemical_name, data["cid"], data["smiles"], data["inchikey"]]


async def process_csv_file(file_path, output_file):
    executor = ThreadPoolExecutor()
    async with ClientSession() as session:
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            tasks = [process_csv_row(row[0], session, executor)
                     for row in reader]

            results = []
            async for result in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                results.append(await result)

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "CID", "SMILES", "InChIKey"])
            writer.writerows(results)

    executor.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description="Process a CSV file to obtain chemical data."
    )
    parser.add_argument("file_path", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    asyncio.run(process_csv_file(args.file_path, args.output_file))


if __name__ == "__main__":
    main()
