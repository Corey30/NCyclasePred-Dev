# NCyclasePred-Dev

NCyclasePred-Dev is a tool for predicting N-cyclase enzymes using sequence data and machine learning techniques.

## Features

- Predicts N-cyclase enzymes based on user-input protein sequences.
- User-friendly interface for batch and single predictions.
- Clear results and classification output.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/Corey30/NCyclasePred-Dev.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your protein sequence data in FASTA format.
2. Run the prediction script:

    ```bash
    python main.py --input your_sequences.fasta --output results.csv
    ```

3. Check the results in `results.csv`.

## Requirements

- Python 3.7 or above
- See `requirements.txt` for all dependencies

## Project Structure

- `main.py` - Main entry point for running predictions.
- `models/` - Pre-trained model files.
- `utils/` - Utility scripts for data processing.
- `examples/` - Example input files.

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, please open an issue in this repository.
