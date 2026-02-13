# ChemNames

A CLI utility to retrieve chemical data (SMILES, InChI, Full Names) from PubChem and map Compound names to their corresponding identifiers.

## Installation

This package is managed with standard Python tools and can be installed via `pip`.

run:
```bash
pip install chemnames
```

Or you can get the newest release by installing it from here by running:
```bash
pip install git+https://github.com/Desperadus/ChemNames
```

For manual editable install follow these steps:

1. Clone the repository.
2. Install the package in editable mode (or normal mode):

```bash
pip install . -e
```

Or using `uv` to manage the environment:

```bash
uv pip install . -e
```

After installation, the CLI tool `addchemnames` will be available in your path.

## Usage

### 1. Retrieve Chemical Data

The main utility reads a CSV file containing a `Compound` column, queries PubChem, and outputs a new CSV with added `SMILES`, `InChI`, and `Full Name` columns.

**Input CSV Format:**
The input file **MUST** contain a column named `Compound`.

Example `input.csv`:
```csv
Compound,ID
Aspirin,1
Caffeine,2
```

**Run the command:**

```bash
addchemnames input.csv output.csv
```

**Output:**
The tool will generate `output.csv` with the enriched data. If a compound is not found, "xxxxxx" will be used as the placeholder.

### 2. Add KEGG IDs

If you have a CSV file that already contains PubChem CIDs (e.g., from a previous step or source), you can use `add_keggs.py` (located in the root of the repository) to append KEGG IDs.

**Run the command:**

```bash
python add_keggs.py input_with_cids.csv output_with_keggs.csv
```

## Notes

- **Network Requests**: This tool makes network requests to PubChem. Large files may take some time to process.
- **Rate Limiting**: The tool uses threading to speed up requests, but be mindful of PubChem's usage policies.
- **Data Accuracy**: Data is fetched "as is" from PubChem.

## License

MIT
