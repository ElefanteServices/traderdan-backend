# TraderDan.xyz Backend API

Professional crypto trading analysis backend for @thecryptoadvisor

## Overview

This Flask-based API powers the TraderDan.xyz crypto trading dashboard, providing real-time market data, trading signals, and performance analytics for professional cryptocurrency trading.

## Features

- **Real-time Market Data**: Integration with CoinGecko API for live cryptocurrency prices
- **Trading Signals**: Daily "Picks of the Day" with entry/exit points
- **Performance Tracking**: Comprehensive analytics and leaderboard system
- **Market Sentiment**: News analysis and sentiment scoring via CoinDesk API
- **Technical Analysis**: RSI, support/resistance levels, and momentum indicators

## API Endpoints

### Crypto Data
- `GET /api/crypto/market-overview` - Global market statistics
- `GET /api/crypto/top-coins` - Top 15 cryptocurrencies by market cap
- `GET /api/crypto/trending` - Trending cryptocurrencies
- `GET /api/crypto/sentiment` - Market sentiment analysis

### Reports
- `GET /api/reports/daily` - Complete daily trading report
- `GET /api/reports/technical-analysis` - Technical analysis for major coins
- `GET /api/reports/market-summary` - Condensed market summary

### Trading Opportunities
- `GET /api/opportunities/sale-of-the-day` - Daily trading picks
- `GET /api/opportunities/top-picks` - Top 5 highest confidence picks
- `GET /api/opportunities/by-risk/{level}` - Filter opportunities by risk level

## Configuration

### Environment Variables
```bash
COINGECKO_API_KEY=your_coingecko_api_key
COINDESK_API_KEY=your_coindesk_api_key
FLASK_ENV=production
```

### API Keys Required
- **CoinGecko API**: For cryptocurrency market data
- **CoinDesk API**: For news and sentiment analysis
- **Arkham API**: For DeFi Dashboard (optional)
- **ETH API**: For gas fees management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traderdan-backend.git
cd traderdan-backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application:
```bash
python src/main.py
```

## Deployment

The API is designed to be deployed on cloud platforms like Heroku, AWS, or DigitalOcean.

### Docker Support
```bash
docker build -t traderdan-api .
docker run -p 5000:5000 traderdan-api
```

## Architecture

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Requests**: HTTP client for external APIs
- **Pandas**: Data analysis and manipulation
- **NumPy**: Numerical computing
- **Matplotlib**: Data visualization

## Trading Strategy

The backend implements professional trading strategies including:

- **Swing Trading**: 2-6 week position holds
- **Technical Analysis**: RSI, support/resistance, volume analysis
- **Risk Management**: Stop-loss and take-profit levels
- **Performance Tracking**: Win rate, average returns, streak tracking

## About @thecryptoadvisor

Professional cryptocurrency analyst Alexandre Azeredo brings Wall Street-grade analysis to the crypto markets. With a background in macroeconomics and international relations, specialized in crypto markets with traditional finance experience.

**Connect:**
- LinkedIn: [Alexandre Azeredo](https://www.linkedin.com/in/alexandre-azeredo/)
- Twitter: [@alexandreazered] TheCryptoAdvisor

## License

This project is an ope source project created by @thecryptoadvisor. Use as you wish. 

## Support

For technical support or trading inquiries, contact: thelord

---

**Disclaimer**: This software is for educational and informational purposes only. Cryptocurrency trading involves substantial risk of loss. Past performance does not guarantee future results.

