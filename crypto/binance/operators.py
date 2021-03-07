import pandas as pd
from datetime import datetime, timedelta

from crypto.client.auth import BinanceHook


class BinanceOperator:
    """A set of operation for binance
    """
    ENDPOINTS = {
        'kline': '/api/v3/klines'
    }
    INTERVALS = {
        "1m": 60,
        "5m": 60*5,
        "15m": 60*15,
        "30m": 60*30,
        "1h": 60*(60*1),
        "2h": 60*(60*2),
        "4h": 60*(60*4),
        "6h": 60*(60*6),
        "8h": 60*(60*8),
        "12h": 60*(60*12),
        "1d": 60*(60*24),
        "3d": 60*(60*24*3),
        "1w": 60*(60*24*7),
        "1mo": 60*(60*24*30)
    }

    def __init__(self):
        self.binance = BinanceHook()

    def get_candlestick(
            self,
            symbol: str,
            interval: str,
            start_time: float = None,
            end_time: float = None,
            limit: int = 1000):
        """Return the canddlesticks

        Args:
            symbol (str): Symbol of the pair
            interval (str): Must be an interval defined by Binance
            start_time (float, optional): Timestamp of the start.
            Defaults to None.
            end_time (float, optional): Timestamp of the end. Defaults to None.
            limit (int, optional): Maximum limit size. Defaults to 1000.

        Returns:
            (json): Return a json response of the requested candlestick
        """
        endpoint = self.ENDPOINTS['kline']
        r = self.binance.client.get(
            self.binance.BASIC_URL + endpoint,
            params={
                'symbol': symbol,
                'interval': interval,
                'startTime': start_time,
                'endTime': end_time,
                'limit': limit
            }
        )
        results = pd.DataFrame(r.json(), columns=[
            'open_time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_asset_volume',
            'nb_trades',
            'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume',
            'osef'
        ])
        results['open_time'] = pd.to_datetime(
            results['open_time'],
            unit='ms')
        results['close_time'] = pd.to_datetime(
            results['close_time'],
            unit='ms')
        return results

    def candle_history(
        self,
        symbol: str,
        interval: str,
        start_time: datetime,
        end_time: datetime,
    ):
        dfs = []
        start = start_time
        step = self.INTERVALS[interval]
        while start <= end_time:
            end = start + timedelta(seconds=step * 1000)
            starting_time = datetime.timestamp(start)
            if end >= datetime.now():
                end = datetime.now().replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0) - timedelta(days=1)
            dfs.append(
                self.get_candlestick(
                    symbol,
                    interval,
                    int(starting_time)*1000,
                    int(datetime.timestamp(end))*1000))
            start = end
        df = pd.concat(dfs).drop_duplicates(['open_time'])
        file_name = f"{symbol}_{interval}_{start_time.date()}_{end_time.date()}.csv"
        df[(df.open_time >= start_time) & (df.open_time < end_time)] \
            .to_csv(
                file_name,
                index=False)
