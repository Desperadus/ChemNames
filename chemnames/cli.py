import csv
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional
import typer
import pubchempy as pcp
from tqdm import tqdm
import time
import random


def get_chemical_data_sync(name: str, debug: bool = False) -> Dict[str, str]:
    if "Analyte" in name:
         return {
            "SMILES": "xxxxxx",
            "InChI": "xxxxxx",
            "Full Name": "xxxxxx"
        }
    
    max_retries = 5
    base_wait = 2.0

    for attempt in range(max_retries):
        try:
            compounds = pcp.get_compounds(name, "name")
            if compounds:
                compound = compounds[0]
                # Try to get IUPAC name, fallback to first synonym, or empty string
                full_name = getattr(compound, "iupac_name", "") or (compound.synonyms[0] if compound.synonyms else "")
                
                return {
                    "SMILES": getattr(compound, "smiles", "") or getattr(compound, "isomeric_smiles", "") or "",
                    "InChI": getattr(compound, "inchi", "") or "",
                    "Full Name": full_name or ""
                }
            elif debug:
                 tqdm.write(f"No compounds found for '{name}'")
            # If no compounds found, we don't retry
            break
            
        except Exception as e:
            # Check for 503 Server Busy
            error_str = str(e)
            if "503" in error_str and "ServerBusy" in error_str:
                if attempt < max_retries - 1:
                    wait_time = base_wait * (2 ** attempt) + random.uniform(0, 1)
                    if debug:
                        tqdm.write(f"Server busy for '{name}', retrying in {wait_time:.1f}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
            
            if debug:
                tqdm.write(f"Failed to fetch '{name}': {e}")
            break
        
    return {
        "SMILES": "xxxxxx",
        "InChI": "xxxxxx",
        "Full Name": "xxxxxx"
    }

async def process_row(row: Dict[str, str], executor: ThreadPoolExecutor, debug: bool) -> Dict[str, str]:
    compound_name = row.get("Compound")
    if not compound_name:
        return row
    
    loop = asyncio.get_running_loop()
    # Run the blocking pubchem call in a thread
    data = await loop.run_in_executor(executor, get_chemical_data_sync, compound_name, debug)
    
    # Merge existing row data with new data
    return {**row, **data}

async def process_csv_async(input_path: Path, output_path: Path, debug: bool):
    if not input_path.exists():
        typer.secho(f"Error: Input file '{input_path}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Read input CSV
    rows = []
    fieldnames = []
    try:
        with open(input_path, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                 typer.secho("Error: CSV file is empty or missing headers.", fg=typer.colors.RED)
                 raise typer.Exit(code=1)
            
            if "Compound" not in reader.fieldnames:
                typer.secho("Error: Input CSV must contain a 'Compound' column.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
                
            fieldnames = list(reader.fieldnames)
            rows = list(reader)
    except Exception as e:
        typer.secho(f"Error reading input file: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Add new columns to fieldnames
    new_columns = ["SMILES", "InChI", "Full Name"]
    for col in new_columns:
        if col not in fieldnames:
            fieldnames.append(col)

    typer.echo(f"Processing {len(rows)} compounds...")
    
    updated_rows = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [process_row(row, executor, debug) for row in rows]
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            updated_rows.append(await task)

    # Write output CSV
    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        typer.secho(f"Successfully processed data to '{output_path}'.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error writing output file: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

def main(
    input_file: Path = typer.Argument(..., help="Path to the input CSV file. Must contain a 'Compound' column."),
    output_file: Path = typer.Argument(..., help="Path to the output CSV file."),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging to see fetch errors.")
):
    """
    Reads a CSV file, looks up chemical data (SMILES, InChI, Full Name) for entries in the 'Compound' column using PubChem,
    and writes the result to a new CSV file.
    """
    asyncio.run(process_csv_async(input_file, output_file, debug))

def entry_point():
    typer.run(main)

if __name__ == "__main__":
    entry_point()
