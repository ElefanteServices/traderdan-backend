from flask import Blueprint, jsonify, request
import requests
import sys
import os

# Add the crypto trading system to the path
sys.path.append('/home/ubuntu/crypto_trading_system/src')

from coingecko_client import CoinGeckoClient
from market_analyzer import MarketAnalyzer

crypto_bp = Blueprint('crypto', __name__)

# Initialize clients
coingecko_client = CoinGeckoClient()
market_analyzer = MarketAnalyzer(coingecko_client)

@crypto_bp.route('/market-overview', methods=['GET'])
def get_market_overview():
    """Get global market overview data"""
    try:
        overview = market_analyzer.get_global_market_overview()
        return jsonify({
            "success": True,
            "data": overview
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@crypto_bp.route('/top-coins', methods=['GET'])
def get_top_coins():
    """Get top cryptocurrencies by market cap"""
    try:
        limit = request.args.get('limit', 15, type=int)
        coins = coingecko_client.get_coins_markets(vs_currency='usd', per_page=limit, page=1)
        
        # Format the data for frontend
        formatted_coins = []
        for coin in coins:
            formatted_coins.append({
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'].upper(),
                'price': coin['current_price'],
                'change24h': coin['price_change_percentage_24h'],
                'marketCap': coin['market_cap'],
                'volume': coin['total_volume'],
                'rank': coin['market_cap_rank']
            })
        
        return jsonify({
            "success": True,
            "data": formatted_coins
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@crypto_bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending cryptocurrencies"""
    try:
        trending = market_analyzer.get_trending_coins()
        return jsonify({
            "success": True,
            "data": trending
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@crypto_bp.route('/volume-anomalies', methods=['GET'])
def get_volume_anomalies():
    """Get volume anomaly signals"""
    try:
        anomalies = market_analyzer.scan_volume_anomalies()
        return jsonify({
            "success": True,
            "data": anomalies
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@crypto_bp.route('/sentiment', methods=['GET'])
def get_market_sentiment():
    """Get market sentiment data (mock for now, will integrate CoinDesk later)"""
    try:
        # Mock sentiment data - will be replaced with CoinDesk API
        sentiment_data = {
            "overall": "NEUTRAL",
            "score": 52,
            "trending": [
                {"topic": "Bitcoin ETF inflows", "sentiment": "POSITIVE"},
                {"topic": "Regulatory concerns", "sentiment": "NEGATIVE"},
                {"topic": "DeFi developments", "sentiment": "POSITIVE"},
                {"topic": "Market volatility", "sentiment": "NEUTRAL"}
            ],
            "history": [
                {"date": "Jun 1", "score": 48},
                {"date": "Jun 2", "score": 52},
                {"date": "Jun 3", "score": 55},
                {"date": "Jun 4", "score": 51},
                {"date": "Jun 5", "score": 49},
                {"date": "Jun 6", "score": 52}
            ]
        }
        
        return jsonify({
            "success": True,
            "data": sentiment_data
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

