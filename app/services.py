from espn_api.basketball import League
import requests

def get_league(league_id: int, season_id: int, espn_s2: str, swid: str) -> League:
    if not hasattr(get_league, "league"):
        get_league.league = League(
            league_id=league_id,
            season_id=season_id,
            espn_s2=espn_s2,
            swid=swid
        )
    return get_league.league
    # what the freak is dependency injection


def get_team_by_name(league: League, team_name: str):
    for team in league.teams:
        if team_name.lower() in team.team_name.lower():
            return team
    return None

def find_trae_young(team):

    #Im gonna find trae young!
    for player in team.roster:
        if "trae young" in player.name.lower():
            return {
                "found trae young!"
            }
        
    return {"didn't find trae young aw man"}

def get_total_points(team):
    total_points = sum(player.fantasy_points for player in team.roster)
    return {
        "total_fantasy_points": total_points
    }
