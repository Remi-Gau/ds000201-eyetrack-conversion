# README

Code to convert the eyetracking sourcedata from the ds000201 dataset
into a format compatible with BEP020.

dataset: https://openneuro.org/datasets/ds000201/versions/1.0.3

BEP020: https://bids-specification--1128.org.readthedocs.build/en/1128/modality-specific-files/eye-tracking.html

current output: https://gin.g-node.org/RemiGau/ds000201-eyetrack

## Requires

python >= 3.8

See requirements.txt for the full list of dependencies.

## Usage

Change the lines at the top of `convert_eyetrack.py`
to point to the location of the dataset and the output directory.

```python
raw_bids_path = Path("/home/remi/gin/Nilsonne/ds000201/")

output_dir = raw_bids_path.joinpath("..", "raw")
```

Run the script `convert_eyetrack.py`.

### Errors

See log.txt to see the errors encountered during conversion.

### TODO

- eye_timestamp are meant to be integer and not time values
- the data set has pupil width and height and not eye1_pupil_size
- missing REQUIRED metadata
    - SamplingFrequency
    - SampleCoordinateUnit
    - SampleCoordinateSystem
    - EnvironmentCoordinates
