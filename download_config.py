BASE_URL = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"

EXTRACT_FIELDS = ["SC_CODE", "SC_NAME", "OPEN", "HIGH", "LOW", "CLOSE"]

FIELD_MAP = {
    "SC_NAME": "NAME",
    "SC_CODE": "CODE",
}

OUTPUT_FIELDS = ["CODE", "NAME", "HIGH", "LOW", "OPEN", "CLOSE", "GAIN"]

SORT_KEY = "GAIN"