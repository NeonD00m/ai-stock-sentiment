# transformers, SOURCE: https://huggingface.co/ProsusAI/finbert
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, AutoModelForTokenClassification

# stock prices
import yfinance # SOURCE: https://aroussi.com/post/python-yahoo-finance

# graphing
import plotly.graph_objects as go

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
sentiment_analysis = pipeline("sentiment-analysis", model = model, tokenizer=tokenizer)

# used to change float and label into a single float value
multipliers = {'neutral': 0, 'negative': -1, 'positive': 1}

# Get sentiments
# def get_sentiments(input_dict, variable_text):
#     for item_ in input_dict:
#         sentiment = sentiment_analysis(item_[variable_text])
#         (calculate score)

#     return input_dict

sent = sentiment_analysis("Shake shack price falls due to impacted quality")  # "Shake shack goes sky high due to a rise market sentiment.")
print(sent)
print(sent[0]['label'] + " - " + str(sent[0]['score']))
print(str(sent[0]['score'] * multipliers[sent[0]['label']]))

def program_input():
    callsign = input("Callsign of the stock you want to predict: ")
    size = int(input("Days per window (integer, recommended: 7): "))
    windows = int(input("# of windows (integer, recommended: 5): "))

    industry = input("Industry of the company: ")
    name = input("Name of the company: ")

    return {
        'callsign': callsign,
        'size': size,
        'windows': windows,
        'industry': industry,
        'name': name,
    }

from datetime import *; from dateutil.relativedelta import *
import calendar


# maybe return a list of dictionaries with the sentiments over time
# input: dictionary returned from program_input()
def get_windows(input):
    results = []
    TODAY = datetime.today()
    stock = yfinance.Ticker(input.callsign)
    #        |           |            |            |
    dates = [TODAY]
    prices = [] #list of prices correlating by index to the dates above, TODO: get TODAY's stock price
    for i in range(input.windows):
        dates.append(TODAY+relativedelta(days=-input.size))
        # add price on this day ^ to the end of prices list
        net_sentiment = 0

        # FIGURE OUT NEWSCATCHERAPI
        # convert datetime data into newscatcher format

        results.append({
            'start_date': dates[len(dates) - 2],
            'end_date': dates[len(dates) - 1],
            'score': net_sentiment,
        })

    return results

# main program
while True:
    info = program_input()
    dataByWindow = get_windows(info)


    response = input("Run program again (Y/N): ")
    if response[0] != "y" and response[0] != "Y":
        break
