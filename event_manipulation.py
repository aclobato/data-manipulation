import sys

import requests
from pandas.io.json import json_normalize
import pandas as pd
from constants import Constants, JsonFields
import json


class EventManipulation:

    def __init__(self, data):
        self.data = json_normalize(data[JsonFields.EVENTS])
        self.data = self.split_custom_data_into_columns()

    def split_custom_data_into_columns(self):
        self.data[JsonFields.CUSTOM_DATA] = self.data.apply(separate_key_value, axis=1)
        new_columns = json_normalize(self.data[JsonFields.CUSTOM_DATA])
        return pd.DataFrame.join(self.data.drop(columns=JsonFields.CUSTOM_DATA), new_columns)

    def transform_to_timeline(self):
        filtered_data = self.data.loc[self.data[JsonFields.EVENT] == Constants.EVENT_TYPE_BUY]
        filtered_data = filtered_data.filter([JsonFields.TIMESTAMP, JsonFields.REVENUE,
                                              JsonFields.TRANSACTION_ID, JsonFields.STORE_NAME])

        products = self.data.loc[self.data[JsonFields.EVENT] == Constants.EVENT_TYPE_PRODUCT_BUY]
        filtered_products = products.filter([JsonFields.TRANSACTION_ID, JsonFields.PRODUCT_NAME,
                                             JsonFields.PRODUCT_PRICE])
        filtered_products = filtered_products.rename(columns=
                                                     {JsonFields.PRODUCT_NAME: JsonFields.NAME,
                                                      JsonFields.PRODUCT_PRICE: JsonFields.PRICE})

        def get_products(row):
            products_transaction = filtered_products.loc[filtered_products[JsonFields.TRANSACTION_ID]
                                                         == row[JsonFields.TRANSACTION_ID]]
            products_transaction = products_transaction.filter([JsonFields.NAME, JsonFields.PRICE])
            new_row = products_transaction
            return new_row

        filtered_data[JsonFields.PRODUCTS] = filtered_data.apply(get_products, axis=1)
        filtered_data = filtered_data.sort_values(by=JsonFields.TIMESTAMP, ascending=False)

        result = dict()
        result[JsonFields.TIMELINE] = filtered_data.to_dict(orient='records')
        result_json = pd.DataFrame.from_dict(result).to_json(orient='records')
        return result_json


def separate_key_value(row):
    new_row = {}
    for key_value in row[JsonFields.CUSTOM_DATA]:
        new_row[key_value[JsonFields.KEY]] = key_value[JsonFields.VALUE]
    return new_row


def get_data(url):
    response = requests.get(url)
    return response.json()


def main():
    url = Constants.DEFAULT_URL;
    if len(sys.argv) > 1:
        url = sys.argv[1]
    data = get_data(url)
    event_manipulation = EventManipulation(data)
    result = event_manipulation.transform_to_timeline()
    print(result)


if __name__ == '__main__':
    main()
