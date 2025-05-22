# ESPN Fantasy Basketball Wrapped API

A FastAPI-based REST API that provides detailed statistics and insights for your ESPN Fantasy Basketball season. Get your personal "wrapped" report with fun stats like your best/worst weeks, sleeper picks, busts, and more!

## Features

- **Season Statistics**: Weekly averages, best/worst performing weeks
- **Player Analysis**: Identify sleeper stars, busts, and clutch performers
- **Matchup Insights**: Find your best and worst team matchups
- **Fun Stats**: Includes unique analytics like "Find Trae Young" insights
- **Easy Setup**: No authentication required - just initialize with your ESPN credentials

## Prerequisites

- Python 3.7+
- ESPN Fantasy Basketball league access
- ESPN cookies (espn_s2 and SWID)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd espn-wrapped
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Getting Your ESPN Credentials

To use this API, you need to get your ESPN Fantasy credentials:

### 1. League ID
- Go to your ESPN Fantasy Basketball league
- Look at the URL: `https://fantasy.espn.com/basketball/league?leagueId=123456`
- The number after `leagueId=` is your League ID

### 2. ESPN Cookies (espn_s2 and SWID)
- Open your browser's Developer Tools (F12)
- Go to your ESPN Fantasy league page
- Navigate to **Application** > **Storage** > **Cookies** > `https://fantasy.espn.com`
- Find and copy the values for:
  - `espn_s2` (long string)
  - `SWID` (format: `{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}`)

## Running the API

1. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **The API will be available at:**
   - Local: `http://127.0.0.1:8000`
   - Docs: `http://127.0.0.1:8000/docs`

## Usage

### 1. Initialize the API

Before using any endpoints, you must initialize the API with your ESPN credentials:

**POST** `/initialize`

```json
{
  "league_id": 123456,
  "year": 2024,
  "espn_s2": "your_espn_s2_cookie_value",
  "swid": "your_swid_cookie_value"
}
```

**Example with curl:**
```bash
curl -X POST "http://127.0.0.1:8000/initialize" \
-H "Content-Type: application/json" \
-d '{
  "league_id": 123456,
  "year": 2024,
  "espn_s2": "AEBxxxxxx...",
  "swid": "{12345678-1234-1234-1234-123456789012}"
}'
```

### 2. Available Endpoints

Once initialized, you can call any of these endpoints:

#### Basic Info
- **GET** `/` - Welcome message

#### Team Performance
- **GET** `/team/weekly-average` - Get your team's weekly scoring average
- **GET** `/team/best-week` - Find your highest scoring week
- **GET** `/team/worst-week` - Find your lowest scoring week
- **GET** `/team/longest-streak` - Get your longest winning/losing streak

#### Player Analysis
- **GET** `/team/sleeper` - Identify your sleeper star of the season
- **GET** `/team/bust` - Find your biggest disappointment
- **GET** `/team/clutch` - Discover your most clutch performer

#### Matchup Insights
- **GET** `/team/best-matchup` - Find your easiest opponent
- **GET** `/team/worst-matchup` - Find your toughest opponent

#### Fun Stats
- **GET** `/team/find-trae` - Special Trae Young related insights

#### Utility
- **POST** `/reset` - Reset the current session

### Example API Calls

```bash
# Get weekly average
curl -X GET "http://127.0.0.1:8000/team/weekly-average"

# Find your sleeper pick
curl -X GET "http://127.0.0.1:8000/team/sleeper"

# Get best week performance
curl -X GET "http://127.0.0.1:8000/team/best-week"
```

## Project Structure

```
espn-wrapped/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application setup
│   ├── routes.py        # API endpoints
│   └── services.py      # Business logic and ESPN API integration
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── venv/               # Virtual environment
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations
- **espn-api**: ESPN Fantasy Sports API wrapper

## API Documentation

Once the server is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation powered by Swagger UI.

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid credentials or services not initialized
- **500 Internal Server Error**: Issues with ESPN API or data processing

Always check the error message for specific details about what went wrong.

## Development

### Adding New Endpoints

1. Add your method to the `Services` class in `app/services.py`
2. Create a new route in `app/routes.py`
3. The route should check if `current_services` is initialized
4. Handle exceptions appropriately

### Example:
```python
@router.get("/team/new-stat")
async def get_new_stat_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        return current_services.get_new_stat()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **"Services not initialized" error**
   - Make sure to call `/initialize` first with valid ESPN credentials

2. **"Invalid ESPN credentials" error**
   - Double-check your league_id, espn_s2, and swid values
   - Ensure your ESPN cookies haven't expired

3. **"Unresolved reference 'Services'" error**
   - Make sure `app/services.py` exists and contains the Services class
   - Check that `app/__init__.py` exists (can be empty)

4. **Import errors**
   - Ensure you're running from the project root directory
   - Verify your virtual environment is activated
   - Check that all dependencies are installed

### Getting Help

If you encounter issues:

1. Check the error message in the API response
2. Look at the server logs in your terminal
3. Verify your ESPN credentials are correct and current
4. Make sure you're calling `/initialize` before other endpoints

## Disclaimer

This project is not affiliated with ESPN. It uses publicly available ESPN Fantasy API endpoints for personal use only.