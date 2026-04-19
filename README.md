# Auto MT5 Data Downloader

A simple, automated tool to connect to MetaTrader 5, download OHLC and tick volume data across multiple symbols and timeframes, and save them as structured CSV files. Designed to be extremely easy to use, even for non-coders.

## Features

- **One-Click Run:** No command line needed. Just double-click `run.bat`.
- **Multiple Symbols & Timeframes:** Download multiple pairs (e.g., EURUSD, XAUUSD) and timeframes (M1, H1, D1) all at once.
- **Secure Credentials:** Store your login safely in a `.env` file.
- **Data Reporting:** Shows how many bars were requested, how many are available in MT5, and how many were downloaded.
- **Organized Storage:** Automatically saves data into `data/<symbol>/<timeframe>/` folders.

## Prerequisites

1. **Python:** You must have Python installed. [Download Python here](https://www.python.org/downloads/).
   - _Important:_ When installing Python, make sure to check the box that says **"Add Python to PATH"**.
2. **MetaTrader 5 (MT5):** You must have the MT5 Desktop Terminal installed on your computer.

## Setup Instructions

### 1. Configure the MT5 Path and Login (Optional but Recommended)

Open the `.env` file (if you don't see it, double click `run.bat` once to generate it from `.env.example`, or rename `.env.example` to `.env`).
Open it in Notepad and fill in your details:

```env
MT5_LOGIN=12345678
MT5_PASSWORD=your_secure_password
MT5_SERVER=Your-Broker-Server

# IMPORTANT: If MT5 doesn't connect automatically, you must provide the path to your MT5 terminal.
MT5_PATH=C:\Program Files\MetaTrader 5\terminal64.exe
```

_Note: If your MT5 is installed elsewhere (like on a different drive), change the `MT5_PATH` to point to the correct `terminal64.exe`._

### 2. Choose Symbols and Timeframes

Open `config.json` in Notepad.

```json
{
  "symbols": ["EURUSD", "XAUUSD"],
  "timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"],
  "max_bars": 99000 //Limit on the number of bars to download. You can change it. e.g. 50000, 100000, etc.
}
```

- Add or remove any symbols to the `"symbols"` list.
- Add or remove timeframes. Valid timeframes include: `M1`, `M5`, `M15`, `M30`, `H1`, `H4`, `D1`, `W1`, `MN1`.
- Set `"max_bars"` to the maximum number of bars you want to pull (e.g., `5000`, `10000`, up to `99000`).
  - **Important Note on Max Bars:** You can request up to `99000` bars. However, **you will not get 99,000 bars for every timeframe.** Timeframes like `H4`, `D1`, `W1`, or `MN1` represent huge amounts of time per bar. Your broker simply does not have 99,000 days of historical data (that would be 270+ years!). The script will automatically download exactly as many bars as actually exist in your MT5 terminal for those higher timeframes.

## How to Run

### Method 1: Using the Terminal (Recommended for VS Code)
If you are using a code editor like VS Code or prefer the command line:
1. Open your terminal.
2. Install the required libraries (only needed the first time):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Python script:
   ```bash
   python mt5_downloader.py
   ```

### Method 2: Using the Batch File (For Non-Coders)
Simply double-click the **`run.bat`** file from your file explorer!

The script will automatically:

1. Create a Python environment.
2. Install necessary libraries (`MetaTrader5`, `pandas`, `python-dotenv`).
3. Connect to your MT5 terminal.
4. Download the requested data.
5. Save everything in the `data/` folder.
6. Display a summary of the downloaded bars vs. the maximum available bars for each symbol/timeframe.
