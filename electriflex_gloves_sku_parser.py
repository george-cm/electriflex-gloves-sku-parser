"""Parse Electriflex gloves SKUs into attributes.
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
"""
import argparse
import csv
import logging
import re
from pathlib import Path
from typing import Dict, List, Match, Pattern, Union

__version__ = "0.1.0"
logger: logging.Logger = logging.getLogger(__name__)


def get_attributes_from_sku(sku: str) -> Dict[str, Union[str, int]]:
    """Parses a SKU string into a dictionary of product attributes.

    Args:
        sku (str): The product SKU string to parse.

    Returns:
        dict[str, Union[str, int]]: Dictionary containing the parsed attributes:

        - Class (int): The product voltage class.
        - Length (int): The product length.
        - Length UOM (str): The length unit of measure.
        - Cuff Style (str): The cuff style.
        - Color (str): The product color.
        - Size (str): The product size.
        - RFID (str): Whether the product has RFID.
        - EXTRA (str): Any extra attributes.

    Notes:
        - Only works for a very specific type of SKU nomenclature.
            For example: NG216YB/9, NG216BCRB/10H, NG418CRB/12/CLIF, NG216BCBYB/10/RF.
        - If the SKU is invalid, returns an empty dictionary.

    """
    pattern: Pattern[str] = re.compile(
        r"NG(?P<Class>\d)(?P<Length>\d{1,2})(?=[A-Z]+)(?P<CuffStyle>(?:BC)?|C?|(?:CBC)?)(?=B|RB|YB)"
        r"(?P<Color>B|RB|YB|BYB)(?:\/|-)(?P<Size>[0-9H]+)\/?(?P<RFID>(?:RF)?)(?P<EXTRA>.*)"  # noqa: E501 pylint: disable=C0301:line-too-long
    )
    match: Match[str] | None = pattern.match(sku)
    if not match:
        logger.warning("Invalid SKU: %s. Match: %s", sku, match)
        return {
            "Class": "",
            "Length": "",
            "Length UOM": "",
            "Cuff Style": "",
            "Color": "",
            "Size": "",
            "RFID": "",
            "EXTRA": "",
        }
        # raise ValueError(f"Invalid SKU: {sku}")
    props: Dict[str, str] = match.groupdict()
    cuff_styles: Dict[str, str] = {
        "": "Straight Cuff",
        "BC": "Bell Cuff",
        "C": "Contour Cuff",
        "CBC": "Contour Bell Cuff",
    }
    colors: Dict[str, str] = {
        "B": "Black",
        "RB": "Red/Black",
        "YB": "Yellow/Black",
        "BYB": "Black/Yellow/Black",
        "BL": "Blue",
        "BLO": "Blue/Orange",
    }
    attributes: Dict[str, Union[str, int]] = {
        "Class": int(props["Class"]),
        "Length": int(props["Length"]),
        "Length UOM": "inch",
        "Cuff Style": cuff_styles.get(props["CuffStyle"], "Unknown"),
        "Color": colors.get(props["Color"], "Unknown"),
        "Size": props["Size"],
        "RFID": "Yes" if props["RFID"] == "RF" else "No",
        "EXTRA": props["EXTRA"],
    }
    return attributes


def parse_skus(inputfile: Path, outputfile: Path, sku_column: str) -> None:
    """Parses SKUs from input CSV to output CSV with attributes.

    Args:
        inputfile (Path): Path to input CSV file containing SKUs.
        outputfile (Path): Path to output CSV file to write parsed attributes.
        sku_column (str): Name of SKU column in input CSV.

    Returns:
        None: Output CSV file written to disk.

    Notes:
        - Input CSV opened as utf-8 text.
        - Output CSV opened as utf-8 text with newline=''.
        - Writes electriflex_gloves.log to current working directory.
        - Calls get_attributes_from_sku() to parse each SKU.
        - Merges parsed attributes with original row from input CSV.
        - Writes output CSV header from input header plus new columns.

    See also:
        get_attributes_from_sku: Parses a single SKU into attribute dict.
    """
    logger.info("Parsing SKUs from file %s", inputfile.as_posix())
    with inputfile.open("r", encoding="utf-8") as f, outputfile.open(
        "w", encoding="utf-8", newline=""
    ) as of:
        reader = csv.DictReader(f, dialect="excel")
        header: List[str] = []
        # header: list[str] = ["Item no.", "SKU"]
        if reader.fieldnames:
            header = list(reader.fieldnames)
        output_header_written: bool = False
        for row in reader:
            sku = row[sku_column]
            # logger.info("Parsing SKU: %s", sku)
            attributes: dict[str, Union[str, int]] = get_attributes_from_sku(sku)
            if not output_header_written:
                header.extend(attributes.keys())
                writer = csv.DictWriter(of, fieldnames=header, dialect="excel")
                writer.writeheader()
                output_header_written = True
            out_row: dict[str, Union[str, int]] = {**row, **attributes}
            writer.writerow(out_row)  # type: ignore


def argument_parser() -> argparse.ArgumentParser:
    """Parses command-line arguments for electriflex_gloves.py.

    Creates an ArgumentParser to parse the command line arguments for the
    electriflex_gloves.py program.

    Returns:
        argparse.ArgumentParser: Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="parse_electriflex_gloves_skus",
        description=f"%(prog)s v{__version__} \n \n{__doc__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", "-V", action="version", version=f"{__version__}")
    parser.add_argument(
        "inputfile",
        metavar="INPUTFILE",
        help="Path to CSV file containing Electriflex glove SKUs",
    )
    parser.add_argument(
        "--sku-column-name",
        "-scn",
        dest="sku_column_name",
        default="SKU",
        help="Name of SKU column in the CSV file. Default: SKU",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        default="output.csv",
        help="Name of output file. Default: output.csv",
    )
    return parser


def main() -> None:
    """Main entry point.

    Parses command-line arguments, sets up logging, calls parse_skus()
    to convert SKUs, and handles errors.

    Args:
        None.

    Raises:
        SystemExit: Called when main() has completed execution.

    """
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("electriflex_gloves.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # parser = argparse.ArgumentParser(
    #     prog="electriflex_gloves", description="Convert SKU to attributes"
    # )

    # parser.add_argument("inputfile", help="CSV file containing SKUs")
    # parser.add_argument("--version", "-V", action="version", version=__version__)
    # parser.add_argument(
    #     "--sku-column-name",
    #     "-scn",
    #     dest="sku_column_name",
    #     default="SKU",
    #     help="Name of SKU column in the CSV file. Default: SKU",
    # )
    # parser.add_argument(
    #     "--output-file",
    #     "-o",
    #     default="output.csv",
    #     help="Name of output file. Default: output.csv",
    # )

    args: argparse.Namespace = argument_parser().parse_args()

    inputfile = Path(args.inputfile)
    if not inputfile.exists():
        logger.error("Input file not found: %s", inputfile.as_posix())
        raise FileNotFoundError(f"Input file not found: {inputfile.as_posix()}")
    if inputfile.is_dir():
        logger.error("Input file is a directory: %s", inputfile.as_posix())
        raise IsADirectoryError(f"Input file is a directory: {inputfile.as_posix()}")
    outputfile = Path(args.output_file)
    if not outputfile.parent.exists():
        logger.error("Output directory not found: %s", outputfile.parent.as_posix())
        raise FileNotFoundError(
            f"Output directory not found: {outputfile.parent.as_posix()}"
        )

    logger.info("Starting...")
    parse_skus(inputfile, outputfile, args.sku_column_name)

    logger.info("Finished.")
    raise SystemExit


if __name__ == "__main__":
    main()
