"""
Diferencia entre precio actual y máximo histórico (ATH)
Índices: S&P 500, NASDAQ 100, FTSE 100, FTSE 250

Requiere:
    pip install yfinance
"""

import yfinance as yf
from datetime import datetime

INDICES = {
    "S&P 500":    "^GSPC",
    "NASDAQ 100": "^NDX",
    "FTSE 100":   "^FTSE",
    "FTSE 250":   "^FTMC",
}

def get_data(ticker_symbol: str) -> dict:
    ticker = yf.Ticker(ticker_symbol)

    # Precio actual (último cierre disponible)
    hist_recent = ticker.history(period="5d")
    if hist_recent.empty:
        raise ValueError(f"No se obtuvieron datos para {ticker_symbol}")
    current_price = hist_recent["Close"].iloc[-1]

    # Máximo histórico: descarga todo el historial disponible
    hist_all = ticker.history(period="max")
    all_time_high = hist_all["High"].max()
    ath_date = hist_all["High"].idxmax().date()

    diff_abs = current_price - all_time_high
    diff_pct = (diff_abs / all_time_high) * 100

    return {
        "current":   current_price,
        "ath":       all_time_high,
        "ath_date":  ath_date,
        "diff_abs":  diff_abs,
        "diff_pct":  diff_pct,
    }

def main():
    width = 70
    print("=" * width)
    print(f"{'PRECIO ACTUAL vs MÁXIMO HISTÓRICO (ATH)':^{width}}")
    print(f"{'Fecha de consulta: ' + datetime.now().strftime('%d/%m/%Y %H:%M'):^{width}}")
    print("=" * width)

    for name, symbol in INDICES.items():
        print(f"\n📊  {name}  ({symbol})")
        print("-" * width)
        try:
            d = get_data(symbol)

            status = "🔴 Por debajo del ATH" if d["diff_pct"] < -0.1 else "🟢 En máximos históricos"

            print(f"  Precio actual :  {d['current']:>12,.2f}")
            print(f"  Máximo hist.  :  {d['ath']:>12,.2f}  (alcanzado el {d['ath_date']})")
            print(f"  Diferencia    :  {d['diff_abs']:>+12,.2f}  ({d['diff_pct']:>+.2f}%)")
            print(f"  Estado        :  {status}")

        except Exception as e:
            print(f"  ⚠️  Error al obtener datos: {e}")

    print("\n" + "=" * width)
    print("Fuente de datos: Yahoo Finance (yfinance)")
    print("=" * width)

if __name__ == "__main__":
    main()
