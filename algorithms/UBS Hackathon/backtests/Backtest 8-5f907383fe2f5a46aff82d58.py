from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.filters.morningstar import Q500US, Q1500US, Q3000US
from quantopian.pipeline.data import EquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import PercentChange, RSI, SimpleMovingAverage, SimpleBeta
from quantopian.pipeline.factors import CustomFactor
from quantopian.pipeline.data.quandl import cboe_vix as vixData

class getVix(CustomFactor):  
    def compute(self, today, assets, out, vix):   
        out[:] = vix[-1]

def make_pipeline():
    
    universe = Q500US()
    
    price = EquityPricing.close.latest
    close = EquityPricing.close
    
    EMA200 = SimpleMovingAverage(inputs=[close], window_length=200)/price*100
    delta125 = PercentChange(inputs=[close], window_length=125)*100
    EMA50 = SimpleMovingAverage(inputs=[close], window_length=50)/price*100
    delta20 = PercentChange(inputs=[close], window_length=20)*100
    RSI14 = RSI(inputs=[close], window_length=15)
    
    #StockCharts Technical Rank (SCTR)
    SCTR = 0.3*EMA200 + 0.3*delta125 + 0.15*EMA50 + 0.15*delta20 + 0.05*RSI14
    
    beta = SimpleBeta(symbol('SPY') , regression_length = 252)
    
    vix  = getVix(inputs  = [vixData.vix_close],window_length = 1)
    
    classification = morningstar.asset_classification.morningstar_industry_group_code.latest
    
    return Pipeline(
        columns={
            'prev_close':price,
            'Stock Ranking':SCTR,
            'classification':classification,
            'beta':beta,
            'vix': vix
        },
        screen=universe
    )
 
def initialize(context):
    pipe = make_pipeline()
    pipe = attach_pipeline(pipe, name='stock_screen')
    
    set_commission(commission.PerShare(cost=0.001, min_trade_cost=1))
    set_benchmark(symbol('RSP'))
            
    # Scedule my rebalance function  
    schedule_function(rebalance, date_rules.month_start(),time_rules.market_close(minutes = 120))
            
def before_trading_start(context, data):
    # Call pipeline_output to get the output
    context.output = pipeline_output('stock_screen')
    #long top 50 stocks
    context.long_list = context.output.sort_values(by = ['Stock Ranking'], ascending=False).iloc[:50]
    
    context.bear_list = context.output.sort_values(by = ['beta'],ascending = True).iloc[:50]
#rebalance quarterly
def rebalance(context, data):  
    this_month = get_datetime('US/Eastern').month  
    if this_month not in [3, 6, 9, 12]:  
        log.info("skipping this month")  
        return  
    else:  
        log.info("trading this month")  
        trade(context, data) 
    
# This rebalancing is called according to our schedule_function settings.     
def trade(context,data):
    if context.output.vix[0] <23:
        long_weight = 1 / float(len(context.long_list))


        for long_stock in context.long_list.index:
            order_target_percent(long_stock, long_weight)

            for stock in context.portfolio.positions:
                if stock not in context.long_list.index:
                    order_target(stock, 0)
    else:
        bear_weight = 1 / float(len(context.bear_list))


        for bear_stock in context.bear_list.index:
            order_target_percent(bear_stock, bear_weight)

            for stock in context.portfolio.positions:
                if stock not in context.bear_list.index:
                    order_target(stock, 0)