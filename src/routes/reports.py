from flask import Blueprint, jsonify, request
import sys
import os
from datetime import datetime

# Add the crypto trading system to the path
sys.path.append('/home/ubuntu/crypto_trading_system/src')

from market_analyzer import MarketAnalyzer
from coingecko_client import CoinGeckoClient

reports_bp = Blueprint('reports', __name__)

# Initialize components
coingecko_client = CoinGeckoClient()
market_analyzer = MarketAnalyzer(coingecko_client)

@reports_bp.route('/daily', methods=['GET'])
def generate_daily_report():
    """Generate comprehensive daily trading report"""
    try:
        # Get global market overview
        global_overview = market_analyzer.get_global_market_overview()
        
        # Get trending analysis
        trending = market_analyzer.get_trending_coins()
        
        # Get volume anomalies
        volume_anomalies = market_analyzer.scan_volume_anomalies()
        
        # Get momentum signals
        momentum_signals = market_analyzer.scan_momentum_signals()
        
        # Get category performance
        category_performance = market_analyzer.analyze_category_performance()
        
        # Compile report data
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "global_overview": global_overview,
            "trending_analysis": trending,
            "volume_anomalies": volume_anomalies,
            "momentum_signals": momentum_signals,
            "category_performance": category_performance,
            "summary": {
                "total_market_cap": global_overview.get('total_market_cap', 0),
                "total_volume_24h": global_overview.get('total_volume_24h', 0),
                "btc_dominance": global_overview.get('btc_dominance', 0),
                "market_sentiment": global_overview.get('market_sentiment', 'NEUTRAL'),
                "anomalies_count": len(volume_anomalies),
                "momentum_signals_count": len(momentum_signals),
                "trending_count": len(trending)
            }
        }
        
        return jsonify({
            "success": True,
            "data": report_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@reports_bp.route('/technical-analysis', methods=['GET'])
def get_technical_analysis():
    """Get technical analysis for major cryptocurrencies"""
    try:
        # Get top coins for technical analysis
        top_coins = ['bitcoin', 'ethereum', 'solana', 'polkadot', 'cardano']
        technical_data = []
        
        for coin_id in top_coins:
            try:
                # Get historical data for technical analysis
                historical_data = coingecko_client.get_coin_market_chart(
                    coin_id, vs_currency='usd', days=30
                )
                
                if historical_data and 'prices' in historical_data:
                    prices = [price[1] for price in historical_data['prices']]
                    current_price = prices[-1] if prices else 0
                    
                    # Calculate basic technical indicators
                    if len(prices) >= 14:
                        # Simple RSI calculation
                        gains = []
                        losses = []
                        for i in range(1, len(prices)):
                            change = prices[i] - prices[i-1]
                            if change > 0:
                                gains.append(change)
                                losses.append(0)
                            else:
                                gains.append(0)
                                losses.append(abs(change))
                        
                        avg_gain = sum(gains[-14:]) / 14
                        avg_loss = sum(losses[-14:]) / 14
                        rs = avg_gain / avg_loss if avg_loss != 0 else 0
                        rsi = 100 - (100 / (1 + rs))
                        
                        # Support and resistance levels
                        recent_prices = prices[-30:]
                        support_level = min(recent_prices) * 1.02
                        resistance_level = max(recent_prices) * 0.98
                        
                        technical_data.append({
                            'coin_id': coin_id,
                            'current_price': current_price,
                            'rsi_14d': rsi,
                            'support_level': support_level,
                            'resistance_level': resistance_level,
                            'price_change_30d': ((current_price - prices[0]) / prices[0]) * 100 if prices[0] != 0 else 0
                        })
                        
            except Exception as coin_error:
                print(f"Error analyzing {coin_id}: {coin_error}")
                continue
        
        return jsonify({
            "success": True,
            "data": technical_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@reports_bp.route('/market-summary', methods=['GET'])
def get_market_summary():
    """Get condensed market summary"""
    try:
        global_overview = market_analyzer.get_global_market_overview()
        volume_anomalies = market_analyzer.scan_volume_anomalies()
        
        summary = {
            "market_cap": global_overview.get('total_market_cap', 0),
            "volume_24h": global_overview.get('total_volume_24h', 0),
            "btc_dominance": global_overview.get('btc_dominance', 0),
            "sentiment": global_overview.get('market_sentiment', 'NEUTRAL'),
            "anomalies_detected": len(volume_anomalies),
            "last_updated": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "data": summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

