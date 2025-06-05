from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from espn_api.basketball import League
from app.espnCookieExtractor import ESPNCookieExtractor
from app.services import Services
from typing import Optional


router = APIRouter()

# Global variable to store current services instance
current_services = None


class ESPNCredentials(BaseModel):
    league_id: int = Field(..., description="ESPN Fantasy League ID")
    year: int = Field(2025, description="Fantasy season year")
    espn_s2: Optional[str] = Field(None, description="ESPN_S2 cookie (optional for public leagues)")
    swid: Optional[str] = Field(None, description="SWID cookie (optional for public leagues)")
    username: Optional[str] = Field(None, description="ESPN username (alternative to cookies)")
    password: Optional[str] = Field(None, description="ESPN password (alternative to cookies)")


@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}


@router.post("/initialize")
async def initialize_services(credentials: ESPNCredentials):
    """Initialize services with ESPN credentials - supports multiple auth methods"""
    try:
        global current_services
        
        # Try different authentication methods
        league = None
        
        # Method 1: Try with cookies (most reliable for private leagues)
        if credentials.espn_s2 and credentials.swid:
            try:
                league = League(
                    league_id=credentials.league_id,
                    year=credentials.year,
                    espn_s2=credentials.espn_s2,
                    swid=credentials.swid
                )
                print("✓ Successfully authenticated with ESPN cookies")
            except Exception as e:
                print(f"Cookie auth failed: {e}")
        
        # Method 2: Try with username/password (if provided)
        if not league and credentials.username and credentials.password:
            try:
                extractor = ESPNCookieExtractor()
                cookies = extractor.get_cookies(credentials.username, credentials.password)
                if cookies:
                    league = League(
                        league_id=credentials.league_id,
                        year=credentials.year,
                        espn_s2=cookies['espn_s2'],
                        swid=cookies['swid']
                    )
                else:
                    print("Failed to retrieve cookies")
                print("✓ Successfully authenticated with username/password")
            except Exception as e:
                print(f"Username/password auth failed: {e}")
        
        # Method 3: Try as public league (no authentication)
        if not league:
            try:
                league = League(
                    league_id=credentials.league_id,
                    year=credentials.year
                )
                print("✓ Successfully connected to public league")
            except Exception as e:
                print(f"Public league access failed: {e}")
                raise HTTPException(
                    status_code=400, 
                    detail="Failed to access league. Please check your League ID or provide valid credentials for private leagues."
                )
        
        # Initialize services with the league
        current_services = Services(
            league_id=credentials.league_id,
            year=credentials.year,
            espn_s2=credentials.espn_s2,
            swid=credentials.swid,
            league_instance=league  # Pass the league instance directly
        )

        # Verify the services work by checking if we can access team data
        if current_services.team is None:
            raise HTTPException(
                status_code=400, 
                detail="Unable to access your team data. You may need to provide authentication for private leagues."
            )

        return {
            "message": "Services initialized successfully",
            "auth_method": "cookies" if credentials.espn_s2 and credentials.swid else 
                         "username/password" if credentials.username and credentials.password else "public",
            "league_name": getattr(league.settings, 'name', 'Unknown League')
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Initialization failed: {str(e)}")


@router.get("/league/info")
async def get_league_info():
    """Get basic league information to verify connection"""
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        
        league = current_services.league
        return {
            "league_name": getattr(league.settings, 'name', 'Unknown League'),
            "league_id": league.league_id,
            "year": league.year,
            "team_count": len(league.teams),
            "current_week": getattr(league, 'current_week', 'Unknown'),
            "your_team": current_services.team.team_name if current_services.team else "Unknown"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test-connection")
async def test_connection():
    """Test if the current connection is working"""
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        
        # Try to access basic data
        team_name = current_services.team.team_name if current_services.team else "No team found"
        league_name = getattr(current_services.league.settings, 'name', 'Unknown League')
        
        return {
            "status": "connected",
            "your_team": team_name,
            "league": league_name,
            "message": "Connection is working properly"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")


# All your existing endpoints remain the same
@router.get("/team/find-trae")
async def find_trae_young_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        return current_services.find_trae_young()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/weekly-average")
async def get_weekly_average_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        return current_services.get_weekly_average()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/best-week")
async def get_best_week_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        best_week, best_score = current_services.get_best_week()
        return f"Week: {best_week}, Score: {int(best_score)}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/worst-week")
async def get_worst_week_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        worst_week, worst_score = current_services.get_worst_week()
        return f"Week: {worst_week}, Score: {int(worst_score)}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/longest-streak")
async def get_longest_streak_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        wins, loss = current_services.get_longest_streak()
        return f"Longest Win Streak: {wins}, Longest Loss Streak: {loss}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/sleeper")
async def get_sleeper_star_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        name, actual, projected = current_services.get_sleeper_star()
        return f"Name: {name}, Average: {actual}, Projected: {projected}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/bust")
async def get_bust_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        name, actual, projected = current_services.get_bust()
        return f"Name: {name}, Average: {actual}, Projected: {projected}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/clutch")
async def find_clutch_player_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        return current_services.find_clutch_player()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/best-matchup")
async def find_best_team_matchup_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        result = current_services.find_best_team_matchup()
        if isinstance(result, str):
            return result
        team, wins = result
        return f"Team: {team}, Wins: {wins}, Losses: {4 - wins}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/worst-matchup")
async def find_worst_team_matchup_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        result = current_services.find_worst_team_matchup()
        if isinstance(result, str):
            return result
        team, losses = result
        return f"Team: {team}, Wins: {4 - losses}, Losses: {losses}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/biggest-comeback")
async def get_biggest_comeback_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        comeback_deficit, week, opponent = current_services.get_biggest_comeback()
        return f"Week: {week}, Opponent: {opponent.team_name if hasattr(opponent, 'team_name') else opponent}, Deficit: {comeback_deficit}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/bonus-titles")
async def bonus_titles_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        titles = current_services.bonus_title()
        return ", ".join(titles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/missing-points")
async def missing_points_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        missing_points = current_services.missing_points()
        return str(missing_points)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_services():
    """Reset the current services instance"""
    global current_services
    current_services = None
    return {"message": "Services reset successfully"}