
# Waveform Generator Script

This Python script generates and formats waveform outputs for digital signals, including signals like `clk`, `data`, `start`, `tx_done`, etc. The script reads a signal description file, processes the signals, and generates both terminal-friendly text outputs and Markdown-formatted waveform outputs. The output is color-coded for terminal use and ready for Markdown-based documentation.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Assumptions](#assumptions)
- [How the Script Works](#how-the-script-works)
- [Example](#example)
- [License](#license)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repo-url>
   ```

2. **Install required dependencies**:
   You only need Python 3.x to run this script. There are no external dependencies in the current version.
   
   Make sure you have Python installed by running:
   ```bash
   python3 --version
   ```

## Usage

1. Place your signal description file (a `.txt` file) in the same directory as the script.

2. Run the script using the command:
   ```bash
   python3 waveform_gen.py <input_file.txt>
   ```

3. The script will process the input file, generate the waveform, and produce two outputs:
   - **Terminal output** (with colors): This is saved in a text file with the suffix `_output.txt`.
   - **Markdown output**: This is saved in a Markdown file with the suffix `_output.md`.

   For example, if your input file is `signals.txt`, the generated files will be:
   - `signals_output.txt` (for terminal output)
   - `signals_output.md` (for Markdown)

## Assumptions

- The **input file format** should consist of signal names (e.g., `clk`, `data`, `start`, etc.) and their corresponding bit values, which are space-separated on each line. A sample input file could look like this:
  ```
  clk    101010
  data   110010
  start  111111
  tx_done 101101
  ```

- **Each signal line** follows the format: `signal_name signal_values`.
  
- **Signals must be of the same length**: The script automatically pads shorter signals and `clk_signal` to ensure alignment and prevent index errors. This ensures all signals have matching lengths during waveform generation.

- **Signal names** are color-coded based on a hash of their names to make it easier to distinguish between them in the terminal output.

## How the Script Works

1. **Input Processing**:
   The script reads the input file line by line, collecting signals and their respective bit values.

2. **Waveform Generation**:
   For each signal, the script generates a visual representation of the waveform. It checks the state of the `clk` signal (high or low) and aligns the other signals accordingly.

3. **Color Coding**:
   In the terminal output, each signal is color-coded using ANSI escape codes to make it easier to differentiate between signals visually.

4. **Output Files**:
   The script generates two output files:
   - **Text output for terminal**: The waveform is formatted with color coding (if the terminal supports it).
   - **Markdown output**: The waveform is formatted in a way suitable for documentation and can be embedded in GitLab, GitHub, or any other Markdown viewer.

## Example

### Example Input (`signals.txt`):
```plaintext
clk    101010
data   110010
start  111111
tx_done 101101
```

### Example Terminal Output (`signals_output.txt`):
```
clk    |_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾
data   |‾|‾|_|‾|‾|_|‾|‾|_|‾|_|‾|_|_|‾|_|_|‾|‾|‾
start  |‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|_|_
tx_done|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|‾
```

### Example Markdown Output (`signals_output.md`):
```markdown
**clk**
```
```
|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|
```
**data**
```
```
|‾|‾|_|‾|‾|_|‾|‾|_|‾|_|‾|_|_|‾|_|_|‾|‾|‾|
```
**start**
```
```
|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|‾|_|_
```
**tx_done**
```
```
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|‾|
```

## License

This script is released under the MIT License. Feel free to use, modify, and distribute it as needed.