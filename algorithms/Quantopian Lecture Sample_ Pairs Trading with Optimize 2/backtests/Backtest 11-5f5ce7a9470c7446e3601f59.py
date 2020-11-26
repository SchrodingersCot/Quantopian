import numpy as np
import statsmodels.api as sm
import pandas as pd

import quantopian.optimize as opt
import quantopian.algorithm as algo

def initialize(context):
    # Quantopian backtester specific variables
    set_slippage(slippage.FixedSlippage(spread=0))
    set_commission(commission.PerTrade(cost=0.00))
    set_symbol_lookup_date('2020-09-01')
    
    context.stock_pairs = [(symbol('SPY'), symbol('IVV')),
(symbol('SPY'), symbol('IWB')),
(symbol('SPY'), symbol('FEZ')),
(symbol('SPY'), symbol('VOO')),
(symbol('MDY'), symbol('IJH')),
(symbol('MDY'), symbol('VEA')),
(symbol('MDY'), symbol('SCHF')),
(symbol('EWJ'), symbol('XLE')),
(symbol('EWW'), symbol('AMLP')),
(symbol('XLU'), symbol('SHV')),
(symbol('QQQ'), symbol('FEZ')),
(symbol('QQQ'), symbol('XLC')),
(symbol('IJH'), symbol('VEA')),
(symbol('IJR'), symbol('KRE')),
(symbol('IVV'), symbol('FEZ')),
(symbol('IVV'), symbol('VOO')),
(symbol('IVW'), symbol('FEZ')),
(symbol('IWB'), symbol('FEZ')),
(symbol('IWD'), symbol('VTV')),
(symbol('IWF'), symbol('VUG')),
(symbol('IWF'), symbol('FEZ')),
(symbol('EWT'), symbol('TQQQ')),
(symbol('IYR'), symbol('SHV')),
(symbol('EZU'), symbol('QLD')),
(symbol('EZU'), symbol('TQQQ')),
(symbol('EZU'), symbol('IEFA')),
(symbol('VTI'), symbol('ITOT')),
(symbol('VTI'), symbol('FEZ')),
(symbol('EFA'), symbol('VGK')),
(symbol('EFA'), symbol('TQQQ')),
(symbol('IEF'), symbol('SHY')),
(symbol('IEF'), symbol('SHV')),
(symbol('SHY'), symbol('IEI')),
(symbol('SHY'), symbol('SHV')),
(symbol('SHY'), symbol('DGAZ')),
(symbol('AGG'), symbol('SHV')),
(symbol('AGG'), symbol('BND')),
(symbol('ITOT'), symbol('FEZ')),
(symbol('VUG'), symbol('FEZ')),
(symbol('FEZ'), symbol('SH')),
(symbol('FEZ'), symbol('SSO')),
(symbol('FEZ'), symbol('QLD')),
(symbol('FEZ'), symbol('SDS')),
(symbol('FEZ'), symbol('HYG')),
(symbol('FEZ'), symbol('ACWI')),
(symbol('FEZ'), symbol('VT')),
(symbol('FEZ'), symbol('SPXS')),
(symbol('FEZ'), symbol('SPXL')),
(symbol('FEZ'), symbol('SPXU')),
(symbol('FEZ'), symbol('UPRO'))]
    
    context.stocks = symbols('SPY',
'MDY',
'EWJ',
'EWW',
'XLE',
'XLU',
'QQQ',
'IJH',
'IJR',
'IVV',
'IVW',
'IWB',
'IWD',
'IWF',
'EWT',
'IYR',
'EZU',
'VTI',
'EFA',
'IEF',
'SHY',
'AGG',
'ITOT',
'VTV',
'VUG',
'FEZ',
'VGK',
'SH',
'SSO',
'QLD',
'KRE',
'SDS',
'IEI',
'SHV',
'BND',
'HYG',
'VEA',
'ACWI',
'VT',
'SPXS',
'SPXL',
'SPXU',
'UPRO',
'SCHF',
'TQQQ',
'AMLP',
'VOO',
'DGAZ',
'IEFA',
'XLC')
    
    context.num_pairs = len(context.stock_pairs)
    # strategy specific variables
    context.lookback = 20 # used for regression
    context.z_window = 20 # used for zscore calculation, must be <= lookback
    
    context.target_weights = pd.Series(index=context.stocks, data=0)
    
    context.spread = np.ndarray((context.num_pairs, 0))
    context.inLong = [False] * context.num_pairs
    context.inShort = [False] * context.num_pairs
    
    # Only do work 30 minutes before close
    schedule_function(func=check_pair_status, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=90))
    
# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    # Our work is now scheduled in check_pair_status
    pass

def check_pair_status(context, data):
    
    prices = data.history(context.stocks, 'price', 35, '1d').iloc[-context.lookback::]
    
    new_spreads = np.ndarray((context.num_pairs, 1))
    
    for i in range(context.num_pairs):

        (stock_y, stock_x) = context.stock_pairs[i]

        Y = prices[stock_y]
        X = prices[stock_x]
        
        # Comment explaining try block
        try:
            hedge = hedge_ratio(Y, X, add_const=True)      
        except ValueError as e:
            log.debug(e)
            return

        context.target_weights = get_current_portfolio_weights(context, data)
        
        new_spreads[i, :] = Y[-1] - hedge * X[-1]

        if context.spread.shape[1] > context.z_window:
            # Keep only the z-score lookback period
            spreads = context.spread[i, -context.z_window:]

            zscore = (spreads[-1] - spreads.mean()) / spreads.std()

            if context.inShort[i] and zscore < 0.0:
                context.target_weights[stock_y] = 0
                context.target_weights[stock_x] = 0
                
                context.inShort[i] = False
                context.inLong[i] = False
                
                record(X_pct=0, Y_pct=0)
                allocate(context, data)
                return

            if context.inLong[i] and zscore > 0.0:
                context.target_weights[stock_y] = 0
                context.target_weights[stock_x] = 0
                
                
                context.inShort[i] = False
                context.inLong[i] = False
                
                record(X_pct=0, Y_pct=0)
                allocate(context, data)
                return

            if zscore < -1.0 and (not context.inLong[i]):
                # Only trade if NOT already in a trade 
                y_target_shares = 1
                X_target_shares = -hedge
                context.inLong[i] = True
                context.inShort[i] = False

                (y_target_pct, x_target_pct) = computeHoldingsPct(y_target_shares,X_target_shares, Y[-1], X[-1])
                
                context.target_weights[stock_y] = y_target_pct * (10000/context.num_pairs)
                context.target_weights[stock_x] = x_target_pct * (10000/context.num_pairs)
                
                record(Y_pct=y_target_pct, X_pct=x_target_pct)
                allocate(context, data)
                return
                

            if zscore > 1.0 and (not context.inShort[i]):
                # Only trade if NOT already in a trade
                y_target_shares = -1
                X_target_shares = hedge
                context.inShort[i] = True
                context.inLong[i] = False

                (y_target_pct, x_target_pct) = computeHoldingsPct( y_target_shares, X_target_shares, Y[-1], X[-1] )
                
                context.target_weights[stock_y] = y_target_pct * (1.0/context.num_pairs)
                context.target_weights[stock_x] = x_target_pct * (1.0/context.num_pairs)
                
                record(Y_pct=y_target_pct, X_pct=x_target_pct)
                allocate(context, data)
                return
        
    context.spread = np.hstack([context.spread, new_spreads])

def hedge_ratio(Y, X, add_const=True):
    if add_const:
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        return model.params[1]
    model = sm.OLS(Y, X).fit()
    return model.params.values
   
def computeHoldingsPct(yShares, xShares, yPrice, xPrice):
    yDol = yShares * yPrice
    xDol = xShares * xPrice
    notionalDol =  abs(yDol) + abs(xDol)
    y_target_pct = yDol / notionalDol
    x_target_pct = xDol / notionalDol
    return (y_target_pct, x_target_pct)

def get_current_portfolio_weights(context, data):  
    positions = context.portfolio.positions  
    positions_index = pd.Index(positions)  
    share_counts = pd.Series(  
        index=positions_index,  
        data=[positions[asset].amount for asset in positions]  
    )

    current_prices = data.current(positions_index, 'price')  
    current_weights = share_counts * current_prices / context.portfolio.portfolio_value  
    return current_weights.reindex(positions_index.union(context.stocks), fill_value=0.0)  

def allocate(context, data):    
    # Set objective to match target weights as closely as possible, given constraints
    objective = opt.TargetWeights(context.target_weights)
    
    # Define constraints
    constraints = []
    constraints.append(opt.MaxGrossExposure(1.0))
    
    
    algo.order_optimal_portfolio(
        objective=objective,
        constraints=constraints,
    )