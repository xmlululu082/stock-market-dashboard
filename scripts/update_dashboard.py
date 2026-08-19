import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data.json"

TICKERS = [
    "AAPL", "AXP", "KO", "BAC", "CVX", "OXY", "GOOGL",
    "CB", "MCO", "KHC",
    "NVDA", "MSFT", "JPM", "CEG",
    "SHOP.TO", "RY.TO", "CCO.TO", "ENB.TO", "BN.TO",
    "MU", "SNDK", "RDDT", "RKLB", "ASTS", "APLD", "NBIS"
]

def fmt_number(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return round(value, 2)
    return value

def stock_snapshot(ticker):
    stock = yf.Ticker(ticker)
    info = stock.get_info()

    return {
        "ticker": ticker,
        "name": info.get("shortName") or info.get("longName") or ticker,
        "price": fmt_number(info.get("currentPrice") or info.get("regularMarketPrice")),
        "changePercent": fmt_number(info.get("regularMarketChangePercent")),
        "marketCap": info.get("marketCap"),
        "pe": fmt_number(info.get("trailingPE") or info.get("forwardPE")),
        "eps": fmt_number(info.get("trailingEps") or info.get("forwardEps")),
        "dividendYield": fmt_number(info.get("dividendYield")),
        "fiftyTwoWeekHigh": fmt_number(info.get("fiftyTwoWeekHigh")),
        "fiftyTwoWeekLow": fmt_number(info.get("fiftyTwoWeekLow"))
    }

stocks = []

for ticker in TICKERS:
    try:
        stocks.append(stock_snapshot(ticker))
    except Exception as error:
        stocks.append({
            "ticker": ticker,
            "error": str(error)
        })

data = {
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "marketPulse": [
        {
            "label": "自动行情",
            "title": "股票基础数据已刷新",
            "detail": "价格、PE、EPS、股息率和52周区间来自 yfinance。"
        }
    ],
    "stocks": stocks,
    "news": [],
    "hotStocks": []
}

DATA_PATH.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Updated {DATA_PATH}")
