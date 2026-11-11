# Cricket Statistics Analysis

A Python-based project that analyses cricket batting and bowling statistics across **ODI, T20I, and Test formats** using ball-by-ball cricket data.

## Features

### Batting Statistics
- Total innings
- Total runs
- Batting average
- Strike rate
- Fours and sixes
- Highest score
- Half-centuries (50s)
- Centuries (100s)

### Bowling Statistics
- Total innings
- Total wickets
- Bowling average
- Bowling strike rate
- Economy rate
- Dot balls
- Three-wicket hauls
- Five-wicket hauls

## Technologies Used
- Python
- Pandas

## Project Structure

```text
Cricket-Statistics-Analysis/
├── project.py
├── README.md
└── data/
    ├── ODI/
    ├── T20I/
    └── Test/
```

The `data` folder contains the ball-by-ball CSV files required to run the project. These datasets are not included in this repository because of their large size.

## Dataset Source

The project uses cricket data from **Cricsheet**.

Dataset download: https://cricsheet.org/downloads/

Download the required ODI, T20I, and Test CSV datasets and place them in their respective folders inside `data`.

## Installation and Execution

Install the required Python library:

```bash
pip install pandas
```

Run the program:

```bash
python project.py
```

## Working

The program loads the ball-by-ball CSV files, combines the data for the selected format, and calculates statistics based on the player's name and selected role (batter or bowler).
