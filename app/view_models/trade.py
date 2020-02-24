
# 礼物或心愿模型转详情页里的交易信息
class TradeInfo:

    def __init__(self, trades):
        self.total = 0
        self.trades = []
        self.__parse(trades)

    def __parse(self, trades):
        self.total = len(trades)
        self.trades = [self.__map_to_trade(trade) for trade in trades]

    def __map_to_trade(self, trade):
        return dict(
            user_name=trade.user.nickname,
            time='暂时没有时间',
            id=trade.id
        )