# Chemical Data Retrieval Script

Script designed to map compound names to their corresponding PubChem CIDs, SMILES, and InChIKeys.

## Installation

Ensure you have python 3.x installed on your system.

### Dependencies

The script requires the following Python libraries:
- `aiohttp`
- `pubchempy`
- `tqdm`
- `pandas`

You can install these dependencies via pip. Run the following command:

```bash
pip install aiohttp pubchempy tqdm pandas
```

## Usage

To use the script, you will need a CSV file containing chemical names (one name per line, without a header). The script will process this file and create a new CSV file with the chemical names and their corresponding CID, SMILES, and InChIKey.

### Running the Script

Navigate to the script's directory in your terminal and run the following command:

```bash
python3 main.py input_file.csv output_file.csv
```
If you wish to add kegg ids to the file, that already contains CIDs, run the following command:
```bash
python3 add_kegg.py input_file.csv output_file.csv
```

Replace `input_file.csv` with the path to your input CSV file, and `output_file.csv` with the desired path for the output file.

## Notes

- If a chemical name cannot be found in the PubChem database, the corresponding fields in the output file will be filled with 'xxxxxx'.

## License

MIT
