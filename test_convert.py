from pathlib import Path

from convert_eyetrack import convert_file

# def test_convert_file():

raw_bids_path = Path("/home/remi/gin/Nilsonne/ds000201/sourcedata/EyeTrackingLogFiles")

input_file = raw_bids_path.joinpath(
    "9001_1_18730311_EyeTrackingLogFiles/9001_1_18730311_182923_eyedata_Resting.txt"
)
output_file = Path().joinpath("test.tsv")
sidecar_file = Path().joinpath("test.json")

convert_file(input_file, output_file, sidecar_file)
