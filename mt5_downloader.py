import os
import json
import logging
import datetime
from pathlib import Path
import MetaTrader5 as mt5
import pandas as pd
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_configuration():
    # Load environment variables
    load_dotenv()
    
    # Load config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found! Please create one based on the instructions.")
        exit(1)
        
    return {
        "login": int(os.getenv("MT5_LOGIN", 0)) if os.getenv("MT5_LOGIN") else None,
        "password": os.getenv("MT5_PASSWORD", ""),
        "server": os.getenv("MT5_SERVER", ""),
        "path": os.getenv("MT5_PATH", ""),
        "symbols": config.get("symbols", []),
        "timeframes": config.get("timeframes", []),
        "max_bars": config.get("max_bars", 5000)
    }

def get_mt5_timeframe(tf_string):
    tf_map = {
        "M1": mt5.TIMEFRAME_M1, "M2": mt5.TIMEFRAME_M2, "M3": mt5.TIMEFRAME_M3,
        "M4": mt5.TIMEFRAME_M4, "M5": mt5.TIMEFRAME_M5, "M6": mt5.TIMEFRAME_M6,
        "M10": mt5.TIMEFRAME_M10, "M12": mt5.TIMEFRAME_M12, "M15": mt5.TIMEFRAME_M15,
        "M20": mt5.TIMEFRAME_M20, "M30": mt5.TIMEFRAME_M30, "H1": mt5.TIMEFRAME_H1,
        "H2": mt5.TIMEFRAME_H2, "H3": mt5.TIMEFRAME_H3, "H4": mt5.TIMEFRAME_H4,
        "H6": mt5.TIMEFRAME_H6, "H8": mt5.TIMEFRAME_H8, "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1, "W1": mt5.TIMEFRAME_W1, "MN1": mt5.TIMEFRAME_MN1
    }
    return tf_map.get(tf_string.upper())

def main():
    cfg = load_configuration()
    
    # Check MT5 setup
    logging.info("Initializing MT5...")
    
    init_args = {}
    if cfg["path"]:
        init_args["path"] = cfg["path"]
        
    if cfg["login"] and cfg["password"] and cfg["server"]:
        init_args["login"] = cfg["login"]
        init_args["password"] = cfg["password"]
        init_args["server"] = cfg["server"]
        
    # Attempt connection
    if not mt5.initialize(**init_args):
        logging.error(f"MT5 initialization failed. Error: {mt5.last_error()}")
        logging.error("Ensure MetaTrader 5 is installed. If it is, check the MT5_PATH in your .env file.")
        input("Press Enter to exit...")
        exit(1)
        
    # Ensure login if credentials were provided
    if cfg["login"]:
        authorized = mt5.login(cfg["login"], cfg["password"], cfg["server"])
        if not authorized:
            logging.error(f"MT5 login failed. Error: {mt5.last_error()}")
            mt5.shutdown()
            input("Press Enter to exit...")
            exit(1)
            
    logging.info("Successfully connected to MetaTrader 5!")
    
    for symbol in cfg["symbols"]:
        # Ensure symbol is available
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logging.warning(f"{symbol} not found. Skipping...")
            continue
            
        if not symbol_info.visible:
            logging.info(f"{symbol} is not visible, trying to select it...")
            if not mt5.symbol_select(symbol, True):
                logging.warning(f"Failed to select {symbol}. Skipping...")
                continue
                
        for tf_str in cfg["timeframes"]:
            tf = get_mt5_timeframe(tf_str)
            if tf is None:
                logging.warning(f"Invalid timeframe: {tf_str}. Skipping...")
                continue
                
            logging.info(f"Downloading data for {symbol} on {tf_str}...")
            
            try:
                requested_bars = int(cfg.get("max_bars", 99000))
            except ValueError:
                requested_bars = 99000
                
            # Download bars
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, requested_bars)
            
            if rates is None or len(rates) == 0:
                logging.error(f"Failed to download data for {symbol} {tf_str}. Error: {mt5.last_error()}")
                continue
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            
            retrieved_bars = len(df)
            logging.info("==================================================")
            logging.info(f"Report for {symbol} {tf_str}:")
            logging.info(f"  - Requested Bars (max_bars setting): {requested_bars}")
            logging.info(f"  - Max bars terminal could provide at once: {retrieved_bars}")
            logging.info(f"  - Successfully Downloaded: {retrieved_bars} bars")
            logging.info("==================================================")
            
            # Save to file
            timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_path = Path(f"data/{symbol}/{tf_str}")
            folder_path.mkdir(parents=True, exist_ok=True)
            
            filename = f"{symbol}_{tf_str}_{timestamp_str}.csv"
            filepath = folder_path / filename
            
            df.to_csv(filepath, index=False)
            logging.info(f"Saved to {filepath}")
            logging.info("")  # Empty line for spacing
            
    mt5.shutdown()
    logging.info("Done! All requested data has been downloaded.")

if __name__ == '__main__':
    main()
