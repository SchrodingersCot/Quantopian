"""
For this example, we're going to write a simple momentum script.  
When the stock goes up quickly, we're going to buy; 
when it goes down we're going to sell.  
Hopefully we'll ride the waves.

To run an algorithm in Quantopian, you need to define two functions: 
initialize and handle_data.

Note: AAPL had a 7:1 split in June 2014, which is reflected in the 
recorded variables plot.
"""

"""
The initialize function sets any data or variables that 
you'll use in your algorithm. 
It's only called once at the beginning of your algorithm.
"""
def initialize(context):
    # In our example, we're looking at Apple.  If you re-type 
    # this line you'll see the auto-complete popup after `sid(`.
    context.security = sid(24)

    # Specify that we want the 'rebalance' method to run once a day
    schedule_function(rebalance, date_rule=date_rules.every_day())

"""
Rebalance function scheduled to run once per day (at market open).
"""
def rebalance(context, data):
    # To make market decisions, we're calculating the stock's 
    # moving average for the last 5 days.

    # We get the price history for the last 5 days. 
    price_history = data.history(
        context.security,
        fields='price',
        bar_count=5,
        frequency='1d'
    )

    # Then we take an average of those 5 days.
    average_price = price_history.mean()
    
    # We also get the stock's current price. 
    current_price = data.current(context.security, 'price') 
    
    # If our stock is currently listed on a major exchange
    if data.can_trade(context.security):
        # If the current price is 1% above the 5-day average price, 
        # we open a long position. If the current price is below the 
        # average price, then we want to close our position to 0 shares.
        if current_price > (1.01 * average_price):
            # Place the buy order (positive means buy, negative means sell)
            order_target_percent(context.security, 1)
            log.info("Buying %s" % (context.security.symbol))
        elif current_price < average_price:
            # Sell all of our shares by setting the target position to zero
            order_target_percent(context.security, 0)
            log.info("Selling %s" % (context.security.symbol))
    
    # Use the record() method to track up to five custom signals. 
    # Record Apple's current price and the average price over the last 
    # five days.
    record(current_price=current_price, average_price=average_price)
