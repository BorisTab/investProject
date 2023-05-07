from QuantConnect import *
from AlgorithmImports import *

class MeanReversionAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        symbols = ["BTCUSD"]
        self.symbols = [self.AddCrypto ("BTCUSD", Resolution.Hour, Market.GDAX).Symbol for symbol in symbols]

        self.SetBenchmark("SPY")

        self.lookback = 200
        self.threshold = 0.5
        self.entry_zscore = 1
        self.exit_zscore = 1.8
        self.stop_loss = 0.6

    def OnData(self, data):
        for symbol in self.symbols:
            if not self.Portfolio[symbol].Invested:
                if self.IsMeanReversionBuySignal(symbol):
                    self.SetHoldings(symbol, 1)
                    self.Debug(f"Bought {symbol} at {self.Securities[symbol].Price}")
            else:
                if self.IsMeanReversionSellSignal(symbol):
                    self.Liquidate(symbol)
                    self.Debug(f"Sold {symbol} at {self.Securities[symbol].Price}")

    def IsMeanReversionBuySignal(self, symbol):
        history = self.History(symbol, self.lookback, Resolution.Minute)
        if "close" not in history.columns or history["close"].isnull().sum() > 0:
            return False

        returns = history["close"].pct_change().dropna()
        zscore = (returns[-1] - returns.mean()) / returns.std()

        return zscore < -self.entry_zscore

    def IsMeanReversionSellSignal(self, symbol):
        history = self.History(symbol, self.lookback, Resolution.Minute)
        if "close" not in history.columns or history["close"].isnull().sum() > 0:
            return False

        returns = history["close"].pct_change().dropna()
        zscore = (returns[-1] - returns.mean()) / returns.std()

        return zscore > -self.exit_zscore or self.Portfolio[symbol].UnrealizedProfitPercent < -self.stop_loss\
