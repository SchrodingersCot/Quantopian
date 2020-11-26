# Uncovering Momentum
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline.filters import QTradableStocksUS
from quantopian.pipeline.data import Fundamentals
from quantopian.pipeline.factors import Returns
from quantopian.pipeline import Pipeline
import quantopian.optimize as opt
import pandas as pd 
# -----------------------------------------------------------------------------------
QTU = QTradableStocksUS(); MOM = 126; N = 20; PCTL_LB = 90; PCTL_UB = 100; LEV = 1.0;
# -----------------------------------------------------------------------------------
def initialize(context):
    schedule_function(rebalance, date_rules.month_end(6), time_rules.market_close(minutes = 30))   
    m = QTU    
    mom = Returns(window_length = MOM + 1, mask = m) 
    w_10 = mom.percentile_between(PCTL_LB, PCTL_UB, mask = m)
    m &= w_10 & mom.isfinite()
    factor = Fundamentals.pb_ratio.latest 
    m &= factor.top(N, mask = m) & factor .isfinite()
    
    attach_pipeline(Pipeline(screen = m), 'pipeline')  

def rebalance(context, data):
    output = pipeline_output('pipeline')    
    stocks = output.index
    stock_weight = 1.0 / len(stocks)
    stock_weights = pd.Series(index = stocks, data = stock_weight)
    
    order_optimal_portfolio(opt.TargetWeights(stock_weights), [opt.MaxGrossExposure(LEV)])
    
def before_trading_start(context, data):
    record(leverage = context.account.leverage)