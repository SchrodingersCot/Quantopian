"""
This sample algorithm will give you a brief overview on using the
Twitter and StockTwits Trader Mood (All Fields, with Retweets) PsychSignal
dataset.

This dataset measures the mood of traders posting messages on both 
StockTwits and Twitter.

Key metrics:

bull_scored_messages - total count of bullish sentiment messages
                       scored by PsychSignal's algorithm
bear_scored_messages - total count of bearish sentiment messages
                       scored by PsychSignal's algorithm
bullish_intensity - score for each message's language for the stength
                    of the bullishness present in the messages on a 0-4
                    scale. 0 indicates no bullish sentiment measured, 4
                    indicates strongest bullish sentiment measured. 4 is rare
bearish_intensity - score for each message's language for the stength
                    of the bearish present in the messages on a 0-4 scale.
                    0 indicates no bearish sentiment measured, 4 indicates
                    strongest bearish sentiment measured. 4 is rare
total_scanned_messages - number of messages coming through PsuchSignal's
                         feeds and attributable to a symbol regardless of
                         whether the PsychSignal sentiment engine can score
                         them for bullish or bearish intensity

This algorithm adds a few of the key metrics above to the pipeline and
uses the `bull_minus_bear` metric to rank each security in `before_trading_start`.
"""

import pandas as pd
import numpy as np

from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline

# This is the Twitter & StockTwits (All Fields) with Retweets dataset
# Full information can be found at
# https://www.quantopian.com/data/psychsignal/aggregated_twitter_withretweets_stocktwits
# from quantopian.pipeline.data.psychsignal import aggregated_twitter_withretweets_stocktwits as psychsignal

# Using the free sample in your pipeline algo
# Free dataset availability is 24 Aug 2009 - 31 Dec 2015
from quantopian.pipeline.data.psychsignal import aggregated_twitter_withretweets_stocktwits_free as psychsignal
        
# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
  
    # Adding our factors, see above for full details on metrics
    # This is the bullish minus bearish intensity score. We'll use this on
    # a daily basis as our main ranking methodology.
    pipe_columns = {
        'bullish_intensity':psychsignal.bullish_intensity.latest,
        'bearish_intensity':psychsignal.bearish_intensity.latest,
        'bull_minus_bear':psychsignal.bull_minus_bear.latest
    }

    # Attaching our pipeline
    pipe = Pipeline(columns = pipe_columns)
    pipe = attach_pipeline(pipe, name='psychsignal')

    # Scheduling a function to run everyday 30 minutes after market open to log
    # our sentiment scores.
    schedule_function(func=log_scores,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_open(minutes=30))
    
def before_trading_start(context, data):
    # Grabbing the results of our pipeline and removing any NaNs we may find
    context.results = pipeline_output('psychsignal').dropna()[:5]

def log_scores(context, data):
    log.info(context.results)
