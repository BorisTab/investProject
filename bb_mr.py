from AlgorithmImports import *
from QuantConnect import *
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
 
class BollingerBandsMeanReversion(QCAlgorithm):
 
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)
        self.crypto = self.AddCrypto("BTCUSD", Resolution.Hour, Market.GDAX)
 
        self.bollingerPeriod = 20
        self.bollingerUpperThreshold = 10
        self.bollingerLowerThreshold = 1
        self.meanReversionPeriod = 16
 
        self.SetBenchmark("SPY")
 
 
    def OnData(self, data):
        if not self.Securities[self.crypto.Symbol].HasData:
            return
 
        if self.priceSeries and self.priceSeries.IsReady:
            self.priceSeries.AddPoint(self.Time, self.crypto.Price)
 
        history = self.History([self.crypto.Symbol], self.bollingerPeriod + self.meanReversionPeriod, Resolution.Hour)
        prices = history.loc[self.crypto.Symbol].close
 
        self.bollingerUpperBand = prices.rolling(self.bollingerPeriod).mean() + self.bollingerUpperThreshold * prices.rolling(self.bollingerPeriod).std()
        self.bollingerLowerBand = prices.rolling(self.bollingerPeriod).mean() + self.bollingerLowerThreshold * prices.rolling(self.bollingerPeriod).std()
 
        self.meanReversion = (prices - prices.rolling(self.meanReversionPeriod).mean()) / prices.rolling(self.meanReversionPeriod).std()
 
        if  self.meanReversion[-1] < self.bollingerLowerBand[-1]:
            self.SetHoldings(self.crypto.Symbol, 1)
        elif self.meanReversion[-1] > self.bollingerUpperBand[-1]:
            self.SetHoldings(self.crypto.Symbol, -1)
        else:
            pass
 