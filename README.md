# Chess-clubs
_A Python package for creating a database of a chess club, its players, and their games._

[![GitHub](https://img.shields.io/github/followers/philhanna?label=Follow&style=social)](https://github.com/philhanna)


## Overview

`chess-clubs` is a Python package that extracts information about a chess club
from the USCF website and creates an SQLite3 database.  The information includes:
- The chess club name
- A list of the active players
- The history of all games played between those players over the last two years
- A summary of the head-to-head matchups between each pair of players

## Installation

To install the package, run
```bash
git clone https://github.com/philhanna/chess-clubs.git
cd chess-clubs
pip install -e .
```

### Usage
To run the program, find out the USCF id of the club, then run:
```bash
PYTHONPATH=src python -m chess_clubs <uscfid>
```

## Running tests
To run tests with pytest, use:
```bash
pytest
```
If you're using the `src/` layout, ensure it's installed in **editable mode**:
```bash
pip install -e .
pytest
```

## Contributing
Contributions are welcome! If you'd like to contribute:

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes.
- Commit your changes (`git commit -m "Add new feature"`).
- Push to your fork (`git push origin feature-branch`).
- Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE] file for details.

## Author
[Phil Hanna](https://github.com/philhanna)

## Links
- [Github repository](https://github.com/philhanna/chess-clubs)
- [USCF (United States Chess Federation)](https://www.uschess.org/msa/Index.php)

[License]: https://github.com/philhanna/chess-clubs/blob/main/LICENSE