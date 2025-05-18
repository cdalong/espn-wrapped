from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import Services
from espn_api.basketball import League

router = APIRouter()
services = Services(league_id=332773775, year=2025, espn_s2='AEB%2FraVAzJUuPQQx%2FZbZyHlQBgCLq%2FRJZeRW%2FD2PS9L1c89tj7UCmG7Y8jGvoYKhToVRtrWmOV8wHyGr8PkOlQJ%2Bc6WyPrTJHE8s2fgroHPV2Z3vA3Hp1QbO0ZlHFu0YvNBT1OMvExX1l7vPZPi5Is4Fmqx8AJDu8aGb5sdXtY5G1oEJ5imB9sjcwj3QUnA0lBdCWbQ%2BUcs%2FDnBNkWDd%2Fe191amCJFp7S0%2BnH1ut5HMOPlo%2B6gh3FhScoJQNIhqkGL2gQr0Bv0WIrSA%2F7Cg8ywpJPBwCDr9tpfwAmfqFWYzABQ%3D%3D', swid='{1A576FEF-EB0A-4EAC-A122-54A7CB7DD0FF}')

@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}

class ServiceParams(BaseModel):
    league_id: int
    year: int
    espn_s2: str
    swid: str

@router.get("/team/find-trae")
def find_trae_young_route(params: ServiceParams):  
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.find_trae_young()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team/week-average")
def get_weekly_average_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_weekly_average()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/best-week")
def get_best_week_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_best_week()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/worst-week")
def get_worst_week_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_worst_week()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/longest-streak")
def get_longest_streak_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_longest_streak()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    

@router.get("/team/sleeper")
def get_sleeper_star_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_sleeper_star()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/bust")
def get_bust_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.get_bust()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/clutch")
def find_clutch_player_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.find_clutch_player()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/best-matchup")
def find_best_team_matchup_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.find_best_team_matchup()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    

@router.get("/team/worst-matchup")
def find_worst_team_matchup_route(params: ServiceParams):
    services = Services(
        league_id = params.league_id,
        year = params.year,
        espn_s2 = params.espn_s2,
        swid = params.swid
    )
    try:
        return services.find_worst_team_matchup()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    

