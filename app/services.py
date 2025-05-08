from espn_api.basketball import League
import requests

def find_trae_young(league_id: int, season_id: int, espn_s2: str, swid: str):

    "Im gonna find trae young!"

    league = League(league_id=league_id, season_id=season_id, espn_s2=espn_s2, swid=swid)
    players = league.players
    for player in players:
        if "Trae Young" in player.name.lower():
            return {
                "found trae young!"
            }
        
    return {"didn't find trae young"}
