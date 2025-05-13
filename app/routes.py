from fastapi import APIRouter, Depends, HTTPException
from app import services
from espn_api.basketball import League

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}


#lowkey chagpted like all of this
@router.get("/team/{team_name}/find-trae")
def find_trae_young_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.find_trae_young(team)

@router.get("/team/{team_name}/points")
def get_team_points_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.get_total_points(team)

@router.get("/team/{team_name}/week-average")
def get_weekly_average_route(league: League = Depends(services.get_league), team_name: str = ""):
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.get_weekly_average(team)

@router.get("/team/{team_name}/best-week")
def get_best_week_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    best_week, best_score = services.get_best_week(team)
    return {"best_week": best_week, "best_score": best_score}

@router.get("/team/{team_name}/worst-week")
def get_worst_week_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    worst_week, worst_score = services.get_worst_week(team)
    return {"worst_week": worst_week, "worst_score": worst_score}

@router.get("/team/{team_name}/longest-streak")
def get_longest_streak_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    max_win, max_loss = services.get_longest_streak(team)
    return {"max_win_streak": max_win, "max_loss_streak": max_loss}

@router.get("/team/{team_name}/sleeper")
def get_sleeper_star_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    sleeper, avg_points, proj_points = services.get_sleeper_star(team)
    return {"sleeper": sleeper.name, "avg_points": avg_points, "projected_avg_points": proj_points}

@router.get("/team/{team_name}/bust")
def get_bust_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    bust, avg_points, proj_points = services.get_bust(team)
    return {"bust": bust.name, "avg_points": avg_points, "projected_avg_points": proj_points}

@router.get("/team/{team_name}/clutch")
def find_clutch_player_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.find_clutch_player(team)

@router.get("/team/{team_name}/best-matchup")
def find_best_team_matchup_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.find_best_team_matchup(team)

@router.get("/team/{team_name}/worst-matchup")
def find_worst_team_matchup_route(league: League = Depends(services.get_league), team_name: str = ""):  
    team = services.get_team_by_name(league, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return services.find_worst_team_matchup(team)

