"""
Read our raw database to be used.
"""
import pandas as pd
from pathlib import Path

from opensignals.data.yahoo import Yahoo
from opensignals.data.provider import SIGNALS_UNIVERSE


class DataBaseReader:
    def __init__(self, db_dir: Path):
        self.db_dir = db_dir
        self.yahoo = Yahoo()
        self._ticker_universe = None

    def get_data(self):          
        """
        Load the data from the database, stored as parquet files.
        """
        ticker_data = self.yahoo.get_ticker_data(self.db_dir)

        print(f'Ticker data loaded:     {len(ticker_data): 10}, cols: {ticker_data.shape[1]}')
        print(f'Ticker universe loaded: {len(self.ticker_universe): 10}, cols: {self.ticker_universe.shape[1]}')

        # Keep only tickers in the numerai universe
        tickers_idx = ticker_data.bloomberg_ticker.isin(self.ticker_universe['bloomberg_ticker'])
        ticker_data = ticker_data[tickers_idx]
        print(f'Ticker data useful:     {len(ticker_data): 10}, cols: {ticker_data.shape[1]}')

        return ticker_data

    @property
    def ticker_universe(self):
        if self._ticker_universe is None:
            self._ticker_universe = pd.read_csv(SIGNALS_UNIVERSE)

        return self._ticker_universe
