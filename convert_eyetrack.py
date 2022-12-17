import json
from pathlib import Path

import pandas as pd
from bids import BIDSLayout
from rich import print

raw_bids_path = Path("/home/remi/gin/Nilsonne/ds000201/")

output_dir = raw_bids_path.joinpath("..", "raw")


def create_tsv_from_file(input_file):

    with open(input_file) as f:
        lines = f.readlines()

    header = None
    ScreenSize = None
    ViewingDistance = None

    for i, i_line in enumerate(lines):

        line_content = i_line.split("\t")

        if line_content[0] == "5":
            header = line_content[1:]
            print(f"header: {header}")
            first_line = i
        elif line_content[0] == "3" and line_content[1] == "ScreenSize":
            ScreenSize = [x.replace("\n", "") for x in line_content[2:]]
            print(f"ScreenSize: {ScreenSize}")
        elif line_content[0] == "3" and line_content[1] == "ViewingDistance":
            ViewingDistance = [x.replace("\n", "") for x in line_content[2:]]
            print(f"ViewingDistance: {ViewingDistance}")

        if (
            (ViewingDistance is not None)
            and (ScreenSize is not None)
            and (header is not None)
        ):
            json_content = {
                "ScreenSize": ScreenSize,
                "ViewingDistance": ViewingDistance,
            }
            with open("tmp.json", "w") as json_file:
                json.dump(json_content, fp=json_file, indent=4)
            break

    with open("tmp.tsv", "w") as new:
        new.writelines(lines[first_line:])


def convert_file(input_file, output_file, sidecar_file):

    create_tsv_from_file(input_file)

    eye_data = pd.read_csv("tmp.tsv", sep="\t")

    eye_data.rename(
        columns={
            "TotalTime": "eye_timestamp",
            "X_Gaze": "eye1_x_coordinate",
            "Y_Gaze": "eye1_y_coordinate",
            "PupilWidth": "eye1_pupil_width",
            "PupilHeight": "eye1_pupil_height",
            "Marker\n": "Marker",
        },
        inplace=True,
    )

    # grab start and end time and remove the rows
    index = eye_data.index.values
    start_row = index[eye_data["5"] == 16]
    StartTime = eye_data["eye_timestamp"][start_row].values[0]
    eye_data.drop(index=start_row, inplace=True)

    index = eye_data.index.values
    end_row = index[eye_data["5"] == 12]
    EndTime = eye_data["eye_timestamp"][end_row].values[0]
    eye_data.drop(index=end_row, inplace=True)

    index = eye_data.index.values
    eye_data.drop(index=index[eye_data["5"] == 7], inplace=True)

    # make sure we only got data rows
    assert len(eye_data["5"].unique()) == 1

    eye_data.drop(["5", "DeltaTime"], axis=1, inplace=True)

    cols = [
        "eye_timestamp",
        "eye1_x_coordinate",
        "eye1_y_coordinate",
        "eye1_pupil_width",
        "eye1_pupil_height",
        "Region",
        "Quality",
        "Fixation",
        "Count",
        "Marker",
    ]
    eye_data = eye_data[cols]

    eye_data.to_csv(output_file, sep="\t", index=False)

    with open("tmp.json") as json_file:
        json_content = json.load(json_file)
    json_content["StartTime"] = StartTime
    json_content["EndTime"] = EndTime
    with open(sidecar_file, "w") as json_file:
        json.dump(json_content, fp=json_file, indent=4)


def main():

    eyetracking_sourcedata = raw_bids_path.joinpath("sourcedata", "EyeTrackingLogFiles")

    database_path = raw_bids_path.parent.joinpath("pybids_db")
    if database_path.exists():
        print("Database already exists, loading layout from there.")
        layout = BIDSLayout(database_path=database_path)
    else:
        layout = BIDSLayout(raw_bids_path)
        layout.save(database_path)

    print(layout)

    subjects = layout.get_subjects()
    sessions = layout.get_sessions()
    tasks = {"Resting": "rest", "Sleepiness": "sleepiness"}

    for i_subject in subjects:

        print(f"\nSubject {i_subject}")

        for i_session in sessions:

            print(f" Session {i_session}")

            for key in tasks:
                files = eyetracking_sourcedata.glob(
                    f"**/{i_subject}_{i_session}*{key}.txt"
                )

                for i_file in files:

                    print(i_file)

                    output_path = output_dir.joinpath(
                        f"sub-{i_subject}", f"ses-{i_session}", "func"
                    )
                    output_path.mkdir(parents=True, exist_ok=True)

                    output_file = f"sub-{i_subject}_ses-{i_session}_task-{tasks[key]}_eyetrack.tsv"
                    sidecar = f"sub-{i_subject}_ses-{i_session}_task-{tasks[key]}_eyetrack.json"

                    convert_file(
                        i_file,
                        output_path.joinpath(output_file),
                        output_path.joinpath(sidecar),
                    )


if __name__ == "__main__":
    main()
