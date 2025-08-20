# app.py
from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

def get_exchange_rate(base: str, target: str):
    """
    Fetch the latest exchange rate from Yahoo Finance.
    Example: base='USD', target='EUR'
    """
    base = base.upper()
    target = target.upper()
    symbol = f"{base}{target}=X"

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if data.empty:
            return None
        # Get the last closing price
        rate = data['Close'][-1]
        return rate
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

@app.route('/exchange', methods=['GET'])
def exchange_rate():
    base = request.args.get('base')
    target = request.args.get('target')

    if not base or not target:
        return jsonify({'error': 'Specify both base and target currencies, e.g. ?base=USD&target=EUR'}), 400

    rate = get_exchange_rate(base, target)
    if rate is None:
        return jsonify({'error': 'Rate not found or failed to fetch'}), 404

    return jsonify({
        'base': base.upper(),
        'target': target.upper(),
        'rate': rate
    })

if __name__ == '__main__':
    app.run(debug=True)
