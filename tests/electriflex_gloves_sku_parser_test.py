"""Tests for electriflex_gloves.py"""
import pytest

from electriflex_gloves_sku_parser import get_attributes_from_sku, main


@pytest.mark.parametrize(
    "sku, expected",
    (
        (
            "NG216YB/9",
            {
                "Class": 2,
                "Length": 16,
                "Length UOM": "inch",
                "Cuff Style": "Straight Cuff",
                "Color": "Yellow/Black",
                "Size": "9",
                "RFID": "No",
                "EXTRA": "",
            },
        ),
        (
            "NG216BCRB/10H",
            {
                "Class": 2,
                "Length": 16,
                "Length UOM": "inch",
                "Cuff Style": "Bell Cuff",
                "Color": "Red/Black",
                "Size": "10H",
                "RFID": "No",
                "EXTRA": "",
            },
        ),
        (
            "NG418CRB/12",
            {
                "Class": 4,
                "Length": 18,
                "Length UOM": "inch",
                "Cuff Style": "Contour Cuff",
                "Color": "Red/Black",
                "Size": "12",
                "RFID": "No",
                "EXTRA": "",
            },
        ),
        (
            "NG216BCBYB/10",
            {
                "Class": 2,
                "Length": 16,
                "Length UOM": "inch",
                "Cuff Style": "Bell Cuff",
                "Color": "Black/Yellow/Black",
                "Size": "10",
                "RFID": "No",
                "EXTRA": "",
            },
        ),
        (
            "NG218CBCRB/11/CLIF",
            {
                "Class": 2,
                "Length": 18,
                "Length UOM": "inch",
                "Cuff Style": "Contour Bell Cuff",
                "Color": "Red/Black",
                "Size": "11",
                "RFID": "No",
                "EXTRA": "CLIF",
            },
        ),
        (
            "NG418CRB/12/RF",
            {
                "Class": 4,
                "Length": 18,
                "Length UOM": "inch",
                "Cuff Style": "Contour Cuff",
                "Color": "Red/Black",
                "Size": "12",
                "RFID": "Yes",
                "EXTRA": "",
            },
        ),
    ),
)
def test_get_attributes_from_sku(sku, expected):
    """Test get_attributes_from_sku"""
    attributes = get_attributes_from_sku(sku)
    assert attributes == expected


def test_argument_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test argument parsing"""
    # Test required arguments
    with pytest.raises(SystemExit):
        monkeypatch.setattr("sys.argv", [])
        main()

    # Test input file
    with pytest.raises(FileNotFoundError):
        monkeypatch.setattr("sys.argv", ["prog", "invalid.csv"])
        main()


def test_main_flow(tmpdir, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main flow"""
    input_file = tmpdir.join("input.csv")
    output_file = tmpdir.join("output.csv")

    monkeypatch.setattr(
        "sys.argv", ["prog", input_file.strpath, "--output-file", output_file.strpath]
    )

    # Test input is directory error
    input_dir = tmpdir.mkdir("input")
    monkeypatch.setattr(
        "sys.argv", ["prog", input_dir.strpath, "--output-file", output_file.strpath]
    )
    with pytest.raises(IsADirectoryError):
        main()

    # Test output directory doesn't exist error
    monkeypatch.setattr(
        "sys.argv",
        ["prog", input_file.strpath, "--output-file", "/invalid/path/output.csv"],
    )
    with pytest.raises(FileNotFoundError):
        main()
