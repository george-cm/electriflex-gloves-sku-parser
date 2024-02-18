# Electriflex Gloves SKU Parser

Python program to parse Electriflex Gloves SKUs and extract their attributes in a CSV file.

Takes a CSV file as input. The file must have a column containing Elctrefix Gloves SKUs.

The default column name is SKU but can be changed with the `--sku-column-name` argument.

## Installation

Install in a virtual environment using:

```sh
python -m pip install "git+https://github.com/george-cm/electriflex-gloves-sku-parser#egg=electriflex-gloves-sku-parser"
```

In case you are new to Python and virtual environments here's an excelent primer from the nice poeple of Real Python: [Python Virtual Environments: A Primer][def].

## Usage

```sh
usage: parse_electriflex_gloves_skus [-h] [--version] [--sku-column-name SKU_COLUMN_NAME] [--output-file OUTPUT_FILE] INPUTFILE

parse_electriflex_gloves_skus v0.1.0

Parse Electriflex gloves SKUs into attributes.
It is specific to Electriflex Gloves SKUs and will not work with other SKUs.
Takes a CSV file as input. The file must have  column containing the SKUs.
The output is a CSV file with the same columns as the input file plus the
attributes parsed from the SKUs (Class, Length, Length UOM, Cuff Style, Color,
Size, RFID, EXTRA).

Example:
    (.venv) $ parse_electriflex_gloves_skus input.csv
    (.venv) $ parse_electriflex_gloves_skus input.csv --sku-column SKU_CODE
    (.venv) $ parse_electriflex_gloves_skus input.csv --sku-column SKU_CODE --output-file parsed_output.csv

Notes:
    - The input file must have a column named "SKU" by default.
      The column name can be specified with the --sku-column option.
      It must be utf-8 encoded.
    - The output file will have the same columns as the input file plus the
      following columns:
        - Class (int): The product voltage class.
        - Length (int): The product length.
        - Length UOM (str): The length unit of measure.
        - Cuff Style (str): The cuff style.
        - Color (str): The product color.
        - Size (str): The product size.
        - RFID (str): Whether the product has RFID.
        - EXSTRA (str): Extra information if present.

positional arguments:
  INPUTFILE             Path to CSV file containing Electriflex glove SKUs

options:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
  --sku-column-name SKU_COLUMN_NAME, -scn SKU_COLUMN_NAME
                        Name of SKU column in the CSV file. Default: SKU
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Name of output file. Default: output.csv
```

## Sourcecode

You can checkout the code on github: [github.com/george-cm/electriflex-gloves-sku-parser][def2]

[def]: https://realpython.com/python-virtual-environments-a-primer/ "Python Virtual Environments: A Primer"
[def2]: https://github.com/george-cm/electriflex-gloves-sku-parser "github.com/george-cm/electriflex-gloves-sku-parser"
