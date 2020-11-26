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
    
    set_commission(commission.PerShare(cost=0.001, min_trade_cost=30))
    
    context.counter = 0
            
    # Scedule my rebalance function
    schedule_function(func=rebalance, 
                      date_rule=date_rules.month_start(days_offset=0), 
                      time_rule=time_rules.market_open(hours=0,minutes=30), 
                      half_days=True)
    
    schedule_function(rebalance, date_rules.month_end(),time_rules.market_close(minutes = 120))
            
def before_trading_start(context, data):
    # Call pipeline_output to get the output
    context.output = pipeline_output('stock_screen')
    #long top 50 stocks
    context.long_list = context.output.sort_values(by = 
        ['Stock Ranking'], 
        ascending=False
    ).iloc[:50]

#rebalance quarterly
def rebalance(context, data):  
    freq_month = 3  
    context.counter += 1  
    if context.counter == freq_month:  
        trade(context, data)  
        context.counter = 0 
    
# This rebalancing is called according to our schedule_function settings.     
def trade(context,data):
    
    long_weight = 1 / float(len(context.long_list))
 
    
    for long_stock in context.long_list.index:
        order_target_percent(long_stock, long_weight)
        
    for stock in context.portfolio.positions:
        if stock not in context.long_list.index:
            order_target(stock, 0)