"""
This example comes from a request in the forums. 
The post can be found here: https://www.quantopian.com/posts/ranking-system-based-on-trading-volume-slash-shares-outstanding
 
The request was: 
 
I am stuck trying to build a stock ranking system with two signals:
1. Trading Volume/Shares Outstanding.
2. Price of current day / Price of 60 days ago.
Then rank Russell 2000 stocks every month, long the top 5%, short the bottom 5%.
 
"""
 
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.filters.morningstar import Q500US, Q1500US, Q3000US
from quantopian.pipeline.data import EquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import PercentChange, RSI, SimpleMovingAverage

def make_pipeline():
    
    universe = Q500US()
    
    price = EquityPricing.close.latest
    close = EquityPricing.close
    
    EMA200 = SimpleMovingAverage(inputs=[close], window_length=200)/price*100
    delta125 = PercentChange(inputs=[close], window_length=125)*100
    EMA50 = SimpleMovingAverage(inputs=[close], window_length=50)/price*100
    delta20 = PercentChange(inputs=[close], window_length=20)*100
    RSI14 = RSI(inputs=[close], window_length=15)
    
    
    SCTR = 0.3*EMA200 + 0.3*delta125 + 0.15*EMA50 + 0.15*delta20 + 0.05*RSI14
    
    classification = morningstar.asset_classification.morningstar_industry_group_code.latest
    
    return Pipeline(
        columns={
            'prev_close':price,
            'Stock Ranking':SCTR,
            'classification':classification,
        },
        screen=universe
    )


 
def initialize(context):
    pipe = make_pipeline()
    pipe = attach_pipeline(pipe, name='stock_screen')
            
    # Scedule my rebalance function
    schedule_function(func=rebalance, 
                      date_rule=date_rules.month_start(days_offset=0), 
                      time_rule=time_rules.market_open(hours=0,minutes=30), 
                      half_days=True)
    
    # set my leverage
    context.long_leverage = 0.50
    context.short_leverage = -0.50
            
def before_trading_start(context, data):
    # Call pipelive_output to get the output
    context.output = pipeline_output('stock_screen')
      
    # Narrow down the securities to only the top 200 & update my universe
    context.long_list = context.output.sort(
        ['Stock Ranking'], 
        ascending=True
    ).iloc[:100]
 
    context.short_list = context.output.sort(
        ['Stock Ranking'], 
        ascending=True
    ).iloc[-100:]  
    
#    update_universe(context.long_list.index.union(context.short_list.index)) 
 
 
def handle_data(context, data):  
    
     # Record and plot the leverage of our portfolio over time. 
    record(leverage=context.account.leverage)
    
    print("Long List")
    log.info("\n" + str(context.long_list.sort(['Stock Ranking'], ascending=True).head(10)))
    
    print("Short List") 
    log.info("\n" + str(context.short_list.sort(['Stock Ranking'], ascending=True).head(10)))
 
# This rebalancing is called according to our schedule_function settings.     
def rebalance(context,data):
    
    long_weight = context.long_leverage / float(len(context.long_list))
    short_weight = context.short_leverage / float(len(context.short_list))
 
    
    for long_stock in context.long_list.index:
        if long_stock in data:
            #log.info("ordering longs")
            #log.info("weight is %s" % (long_weight))
            order_target_percent(long_stock, long_weight)
        
    for short_stock in context.short_list.index:
        if short_stock in data:
            #log.info("ordering shorts")
            #log.info("weight is %s" % (short_weight))
            order_target_percent(short_stock, short_weight)
        
    for stock in context.portfolio.positions:
        if stock not in context.long_list.index and stock not in context.short_list.index:
            order_target(stock, 0)