from flask import Blueprint, jsonify, request
import sys
import os
from datetime import datetime

# Add the crypto trading system to the path
sys.path.append('/home/ubuntu/crypto_trading_system/src')

from coingecko_client import CoinGeckoClient

opportunities_bp = Blueprint('opportunities', __name__)

# Initialize components
coingecko_client = CoinGeckoClient()

# Mock swing trading scanner for now
class MockSwingScanner:
    def __init__(self, client):
        self.client = client
    
    def scan_swing_opportunities(self):
        # Return mock opportunities data
        mock_opportunities = [
            type('Opportunity', (), {
                'coin_id': 'polkadot',
                'coin_name': 'Polkadot',
                'symbol': 'DOT',
                'rank': 29,
                'current_price': 3.96,
                'entry_point': 3.85,
                'exit_point': 4.75,
                'price_target': 5.20,
                'entry_confidence': 95,
                'risk_level': 'LOW',
                'time_horizon': '2-3 weeks',
                'description': 'High value score with oversold RSI at 27.1. Down 25.2% from 30-day high with increasing volume trend.',
                'swing_signals': ['Oversold RSI', 'Volume increase', 'Support level'],
                'rsi_14d': 27.1,
                'volume_trend': 'Increasing',
                'momentum': 'Bullish',
                'support_level': 3.80,
                'resistance_level': 4.20,
                'market_cap': 6028918470,
                'volume_24h': 253270247,
                'price_change_24h': -1.2,
                'price_change_7d': -25.2,
                'value_score': 100
            })(),
            type('Opportunity', (), {
                'coin_id': 'solana',
                'coin_name': 'Solana',
                'symbol': 'SOL',
                'rank': 6,
                'current_price': 151.73,
                'entry_point': 148.50,
                'exit_point': 172.00,
                'price_target': 185.00,
                'entry_confidence': 92,
                'risk_level': 'LOW',
                'time_horizon': '3-4 weeks',
                'description': 'Value score of 92/100 with oversold RSI at 25.4. Technical analysis shows strong support.',
                'swing_signals': ['Oversold RSI', 'Strong support', 'Developer activity'],
                'rsi_14d': 25.4,
                'volume_trend': 'Increasing',
                'momentum': 'Bullish',
                'support_level': 145.00,
                'resistance_level': 160.00,
                'market_cap': 65700000000,
                'volume_24h': 3420000000,
                'price_change_24h': -0.2,
                'price_change_7d': -18.5,
                'value_score': 92
            })()
        ]
        return mock_opportunities

swing_scanner = MockSwingScanner(coingecko_client)

@opportunities_bp.route('/sale-of-the-day', methods=['GET'])
def get_sale_of_the_day():
    """Get top trading opportunities with entry/exit points"""
    try:
        # Get swing trading opportunities
        opportunities = swing_scanner.scan_swing_opportunities()
        
        # Format opportunities for frontend
        formatted_opportunities = []
        for opp in opportunities[:10]:  # Top 10 opportunities
            # Calculate potential returns
            entry_to_exit_return = ((opp.exit_point - opp.entry_point) / opp.entry_point) * 100 if opp.exit_point and opp.entry_point else 0
            entry_to_target_return = ((opp.price_target - opp.entry_point) / opp.entry_point) * 100 if opp.price_target and opp.entry_point else 0
            current_to_target_return = ((opp.price_target - opp.current_price) / opp.current_price) * 100 if opp.price_target else 0
            
            # Calculate stop loss suggestion (5% below entry)
            stop_loss = opp.entry_point * 0.95 if opp.entry_point else opp.current_price * 0.95
            
            formatted_opp = {
                'id': opp.coin_id,
                'name': opp.coin_name,
                'symbol': opp.symbol,
                'rank': opp.rank,
                'current_price': opp.current_price,
                'entry_point': opp.entry_point,
                'exit_point': opp.exit_point,
                'price_target': opp.price_target,
                'stop_loss': stop_loss,
                'confidence': opp.entry_confidence,
                'risk_level': opp.risk_level,
                'time_horizon': opp.time_horizon,
                'reasoning': opp.description,
                'signals': opp.swing_signals,
                'returns': {
                    'entry_to_exit': round(entry_to_exit_return, 2),
                    'entry_to_target': round(entry_to_target_return, 2),
                    'current_to_target': round(current_to_target_return, 2)
                },
                'technical_data': {
                    'rsi_14d': opp.rsi_14d,
                    'volume_trend': opp.volume_trend,
                    'momentum': opp.momentum,
                    'support_level': opp.support_level,
                    'resistance_level': opp.resistance_level
                },
                'market_data': {
                    'market_cap': opp.market_cap,
                    'volume_24h': opp.volume_24h,
                    'price_change_24h': opp.price_change_24h,
                    'price_change_7d': opp.price_change_7d
                },
                'value_score': opp.value_score,
                'timestamp': datetime.now().isoformat()
            }
            
            formatted_opportunities.append(formatted_opp)
        
        # Calculate summary statistics
        risk_distribution = {}
        confidence_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for opp in formatted_opportunities:
            # Risk distribution
            risk_level = opp['risk_level']
            risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + 1
            
            # Confidence distribution
            confidence = opp['confidence']
            if confidence >= 90:
                confidence_distribution['high'] += 1
            elif confidence >= 80:
                confidence_distribution['medium'] += 1
            else:
                confidence_distribution['low'] += 1
        
        summary = {
            'total_opportunities': len(formatted_opportunities),
            'risk_distribution': risk_distribution,
            'confidence_distribution': confidence_distribution,
            'avg_confidence': sum(opp['confidence'] for opp in formatted_opportunities) / len(formatted_opportunities) if formatted_opportunities else 0,
            'avg_potential_return': sum(opp['returns']['current_to_target'] for opp in formatted_opportunities) / len(formatted_opportunities) if formatted_opportunities else 0
        }
        
        return jsonify({
            "success": True,
            "data": {
                "opportunities": formatted_opportunities,
                "summary": summary,
                "last_updated": datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@opportunities_bp.route('/top-picks', methods=['GET'])
def get_top_picks():
    """Get top 5 highest confidence opportunities"""
    try:
        limit = request.args.get('limit', 5, type=int)
        opportunities = swing_scanner.scan_swing_opportunities()
        
        # Sort by confidence and take top picks
        top_picks = sorted(opportunities, key=lambda x: x.entry_confidence, reverse=True)[:limit]
        
        formatted_picks = []
        for opp in top_picks:
            formatted_picks.append({
                'id': opp.coin_id,
                'name': opp.coin_name,
                'symbol': opp.symbol,
                'current_price': opp.current_price,
                'entry_point': opp.entry_point,
                'price_target': opp.price_target,
                'confidence': opp.entry_confidence,
                'risk_level': opp.risk_level,
                'potential_return': ((opp.price_target - opp.current_price) / opp.current_price) * 100 if opp.price_target else 0,
                'key_signal': opp.swing_signals[0] if opp.swing_signals else "High value opportunity"
            })
        
        return jsonify({
            "success": True,
            "data": formatted_picks
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@opportunities_bp.route('/by-risk/<risk_level>', methods=['GET'])
def get_opportunities_by_risk(risk_level):
    """Get opportunities filtered by risk level"""
    try:
        risk_level = risk_level.upper()
        if risk_level not in ['LOW', 'MEDIUM', 'HIGH']:
            return jsonify({
                "success": False,
                "error": "Invalid risk level. Use LOW, MEDIUM, or HIGH"
            }), 400
        
        opportunities = swing_scanner.scan_swing_opportunities()
        filtered_opportunities = [opp for opp in opportunities if opp.risk_level == risk_level]
        
        formatted_opportunities = []
        for opp in filtered_opportunities:
            formatted_opportunities.append({
                'id': opp.coin_id,
                'name': opp.coin_name,
                'symbol': opp.symbol,
                'current_price': opp.current_price,
                'confidence': opp.entry_confidence,
                'potential_return': ((opp.price_target - opp.current_price) / opp.current_price) * 100 if opp.price_target else 0,
                'time_horizon': opp.time_horizon
            })
        
        return jsonify({
            "success": True,
            "data": {
                "risk_level": risk_level,
                "count": len(formatted_opportunities),
                "opportunities": formatted_opportunities
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

