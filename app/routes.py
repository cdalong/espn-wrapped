from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from espn_api.basketball import League
from app.services import Services


router = APIRouter()

# Global variable to store current services instance
current_services = None


class ESPNCredentials(BaseModel):
    league_id: int
    year: int
    espn_s2: str
    swid: str


@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}


@router.post("/initialize")
async def initialize_services(credentials: ESPNCredentials):
    """Initialize services with ESPN credentials"""
    try:
        global current_services
        current_services = Services(
            league_id=credentials.league_id,
            year=credentials.year,
            espn_s2=credentials.espn_s2,
            swid=credentials.swid
        )

        # Verify the credentials work by accessing the team property
        if current_services.team is None:
            raise HTTPException(status_code=400, detail="Invalid ESPN credentials")

        return {"message": "Services initialized successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Initialization failed: {str(e)}")


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
        team, wins = current_services.find_best_team_matchup()
        return f"Team: {team}, Wins: {wins}, Losses: {4 - wins}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/worst-matchup")
async def find_worst_team_matchup_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        team, losses = current_services.find_worst_team_matchup()
        return f"Team: {team}, Wins: {4- losses}, Losses: {losses}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/biggest-comeback")
async def get_biggest_comeback_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        comeback_deficit, week, opponent = current_services.get_biggest_comeback()
        return f"Week: {week}, Opponent: {opponent}, Deficit: {comeback_deficit}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/bonus-title")
async def bonus_title_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        titles = current_services.bonus_title()
        return f"Titles: {titles}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team/missing-points")
async def missing_points_route():
    try:
        if current_services is None:
            raise HTTPException(status_code=400, detail="Services not initialized. Call /initialize first.")
        missing_points = current_services.missing_points()
        return f"Missed Points: {missing_points}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_services():
    """Reset the current services instance"""
    global current_services
    current_services = None
    return {"message": "Services reset successfully"}