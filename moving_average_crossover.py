from AlgorithmImports import *

class MovingAverageCrossoverAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2021, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)
        self.SetBenchmark("SPY")

        btcusd = self.AddCrypto("BTCUSD", Resolution.Minute).Symbol

        self.fast_ma_period = 200
        self.slow_ma_period = 600

        self.fast_ma = self.SMA("BTCUSD", self.fast_ma_period, Resolution.Minute)
        self.slow_ma = self.SMA("BTCUSD", self.slow_ma_period, Resolution.Minute)
        self.previous_fast_ma = None
        self.previous_slow_ma = None

        self.buying = False
        self.selling = False

        self.atr = self.ATR("BTCUSD", 14, Resolution.Daily)
        self.profit_target = 0
        self.stop_loss = 0

    def OnData(self, data):
        if not (self.fast_ma.IsReady and self.slow_ma.IsReady and self.atr.IsReady):
            return

        atr = self.atr.Current.Value
        self.stop_loss = atr * 3
        self.profit_target = atr * 5
        
        current_fast_ma = self.fast_ma.Current.Value
        current_slow_ma = self.slow_ma.Current.Value
        
        if self.previous_fast_ma and self.previous_slow_ma:
            if self.previous_fast_ma < self.previous_slow_ma and current_fast_ma > current_slow_ma:
                self.buying = True
            elif self.previous_fast_ma > self.previous_slow_ma and current_fast_ma < current_slow_ma:
                self.selling = True
        
        self.previous_fast_ma = current_fast_ma
        self.previous_slow_ma = current_slow_ma
        
        if self.buying:
            self.LimitOrder("BTCUSD", 1, data["BTCUSD"].Close)
            self.buying = False
        
        if self.selling:
            self.LimitOrder("BTCUSD", -1, data["BTCUSD"].Close)
            self.selling = False

        for holding in self.Portfolio:
            symbol = holding.Key
            position = holding.Value
            if position.Invested:
                unrealized_pnl = position.UnrealizedProfitPercent
                if unrealized_pnl >= self.profit_target or unrealized_pnl <= -self.stop_loss:
                    self.Liquidate(symbol)
                

def OnOrderEvent(self, orderEvent):
    order = self.Transactions.GetOrderById(orderEvent.OrderId)
    if order.Status == OrderStatus.Filled:
        if order.Direction == OrderDirection.Buy:
            self.Debug("Bought {0} units of {1} at {2}".format(orderEvent.FillQuantity, orderEvent.Symbol, orderEvent.FillPrice))
        elif order.Direction == OrderDirection.Sell:
            self.Debug("Sold {0} units of {1} at {2}".format(orderEvent.FillQuantity, orderEvent.Symbol, orderEvent.FillPrice))
            
def OnEndOfAlgorithm(self):
    self.Log("Final portfolio value: {0}".format(self.Portfolio.TotalPortfolioValue))
