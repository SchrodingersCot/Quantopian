import numpy as np
import statsmodels.api as sm
import pandas as pd

import quantopian.optimize as opt
import quantopian.algorithm as algo

def initialize(context):
    # Quantopian backtester specific variables
    set_slippage(slippage.FixedSlippage(spread=0))
    set_commission(commission.PerTrade(cost=1))
    set_symbol_lookup_date('2020-09-01')
    
    context.stock_pairs = [(symbol('AEP'), symbol('XEL')),
(symbol('AEP'), symbol('AWK')),
(symbol('ATO'), symbol('CMS')),
(symbol('DTE'), symbol('AEE')),
(symbol('DUK'), symbol('OGE')),
(symbol('ED'), symbol('NEE')),
(symbol('ED'), symbol('ES')),
(symbol('ED'), symbol('WEC')),
(symbol('ED'), symbol('XEL')),
(symbol('ED'), symbol('AWK')),
(symbol('ETR'), symbol('NEE')),
(symbol('ETR'), symbol('SO')),
(symbol('NEE'), symbol('WTRG')),
(symbol('NEE'), symbol('SO')),
(symbol('NI'), symbol('OGE')),
(symbol('NI'), symbol('AEE')),
(symbol('OGE'), symbol('AEE')),
(symbol('WEC'), symbol('AWK')),
(symbol('XEL'), symbol('AWK')),
(symbol('AJG'), symbol('AON')),
(symbol('FNB'), symbol('VLY')),
(symbol('FNB'), symbol('PNFP')),
(symbol('FULT'), symbol('VLY')),
(symbol('FULT'), symbol('PNFP')),
(symbol('FULT'), symbol('FHN')),
(symbol('FULT'), symbol('BKU')),
(symbol('VLY'), symbol('PNFP')),
(symbol('VLY'), symbol('FHN')),
(symbol('WTFC'), symbol('UMPQ')),
(symbol('FITB'), symbol('MS')),
(symbol('FITB'), symbol('GS')),
(symbol('FITB'), symbol('CFG')),
(symbol('KEY'), symbol('NTRS')),
(symbol('MTB'), symbol('MS')),
(symbol('MTB'), symbol('GS')),
(symbol('MS'), symbol('CFG')),
(symbol('GS'), symbol('RF')),
(symbol('GS'), symbol('CFG')),
(symbol('WAL'), symbol('RF')),
(symbol('BKH'), symbol('SR')),
(symbol('SR'), symbol('NWE')),
(symbol('ALE'), symbol('NWE')),
(symbol('DRE'), symbol('ELS')),
(symbol('DRE'), symbol('SUI')),
(symbol('DRE'), symbol('MAA')),
(symbol('DRE'), symbol('DEI')),
(symbol('DRE'), symbol('HTA')),
(symbol('FRT'), symbol('NNN')),
(symbol('FRT'), symbol('UDR')),
(symbol('FRT'), symbol('EQR')),
(symbol('FRT'), symbol('AIV')),
(symbol('FRT'), symbol('O')),
(symbol('FRT'), symbol('AVB')),
(symbol('FRT'), symbol('ACC')),
(symbol('FRT'), symbol('STOR')),
(symbol('NNN'), symbol('REG')),
(symbol('NNN'), symbol('AIV')),
(symbol('UDR'), symbol('REG')),
(symbol('UDR'), symbol('AIV')),
(symbol('UDR'), symbol('O')),
(symbol('UDR'), symbol('AVB')),
(symbol('UDR'), symbol('HTA')),
(symbol('ELS'), symbol('ARE')),
(symbol('ELS'), symbol('PLD')),
(symbol('ELS'), symbol('HTA')),
(symbol('CPT'), symbol('EQR')),
(symbol('CPT'), symbol('VER')),
(symbol('CPT'), symbol('STOR')),
(symbol('EQR'), symbol('VER')),
(symbol('EQR'), symbol('HTA')),
(symbol('EQR'), symbol('STOR')),
(symbol('REG'), symbol('ESS')),
(symbol('REG'), symbol('AIV')),
(symbol('REG'), symbol('O')),
(symbol('REG'), symbol('AVB')),
(symbol('REG'), symbol('WPC')),
(symbol('REG'), symbol('ACC')),
(symbol('REG'), symbol('STOR')),
(symbol('SUI'), symbol('MAA')),
(symbol('SUI'), symbol('PLD')),
(symbol('SUI'), symbol('HTA')),
(symbol('MAA'), symbol('HTA')),
(symbol('ESS'), symbol('WPC')),
(symbol('AIV'), symbol('O')),
(symbol('AIV'), symbol('HTA')),
(symbol('AIV'), symbol('STOR')),
(symbol('O'), symbol('HTA')),
(symbol('KRC'), symbol('DEI')),
(symbol('ARE'), symbol('PLD')),
(symbol('ARE'), symbol('DEI')),
(symbol('BXP'), symbol('HTA')),
(symbol('AVB'), symbol('HTA')),
(symbol('AVB'), symbol('STOR')),
(symbol('PLD'), symbol('DEI')),
(symbol('PLD'), symbol('INVH')),
(symbol('PSA'), symbol('CUBE')),
(symbol('DEI'), symbol('AMH')),
(symbol('DEI'), symbol('INVH')),
(symbol('VER'), symbol('HTA')),
(symbol('HTA'), symbol('STOR')),
(symbol('EGP'), symbol('EQC')),
(symbol('EGP'), symbol('HR')),
(symbol('EQC'), symbol('HR')),
(symbol('EQC'), symbol('ESRT')),
(symbol('NHI'), symbol('ESRT')),
(symbol('PSB'), symbol('HR')),
(symbol('HR'), symbol('ADC')),
(symbol('HR'), symbol('ESRT')),
(symbol('ADC'), symbol('ESRT')),
(symbol('TRNO'), symbol('REXR')),
(symbol('KO'), symbol('PG')),
(symbol('RWT'), symbol('CIM')),
(symbol('RWT'), symbol('ARI')),
(symbol('NLY'), symbol('AGNC')),
(symbol('SHO'), symbol('RLJ'))]
    
    context.stocks = symbols('AEP',
'AJG',
'AON',
'ATO',
'BKH',
'CMS',
'DRE',
'DTE',
'DUK',
'ED',
'EGP',
'ETR',
'FNB',
'FITB',
'NEE',
'FRT',
'FULT',
'EQC',
'KEY',
'KO',
'SR',
'MTB',
'NHI',
'NI',
'NNN',
'NTRS',
'ES',
'OGE',
'PG',
'PSB',
'WTRG',
'SO',
'UDR',
'VLY',
'WEC',
'ELS',
'HR',
'CPT',
'EQR',
'REG',
'SUI',
'MAA',
'ADC',
'ESS',
'AIV',
'O',
'RWT',
'KRC',
'WTFC',
'ARE',
'BXP',
'MS',
'NLY',
'UMPQ',
'AVB',
'GS',
'PACW',
'WPC',
'XEL',
'ALE',
'PNFP',
'AEE',
'PLD',
'PSA',
'FHN',
'ACC',
'SHO',
'CUBE',
'NWE',
'WAL',
'DEI',
'RF',
'CIM',
'AWK',
'AGNC',
'ARI',
'TRNO',
'BKU',
'RLJ',
'VER',
'HTA',
'REXR',
'AMH',
'ESRT',
'CFG',
'STOR',
'INVH')
    
    context.num_pairs = len(context.stock_pairs)
    # strategy specific variables
    context.lookback = 20 # used for regression
    context.z_window = 20 # used for zscore calculation, must be <= lookback
    
    context.target_weights = pd.Series(index=context.stocks, data=0.25)
    
    context.spread = np.ndarray((context.num_pairs, 0))
    context.inLong = [False] * context.num_pairs
    context.inShort = [False] * context.num_pairs
    
    # Only do work 30 minutes before close
    schedule_function(func=check_pair_status, date_rule=date_rules.every_day(), time_rule=time_rules.market_close(minutes=30))
    
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
                
                context.target_weights[stock_y] = y_target_pct * (1.0/context.num_pairs)
                context.target_weights[stock_x] = x_target_pct * (1.0/context.num_pairs)
                
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