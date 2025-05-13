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

def get_weekly_average(team): 
    total_points = sum(player.fantasy_points for player in team.roster)
    return total_points / 20 

def get_best_week(team):
    best_week = 0
    best_score = 0
    for week in range(1, 21):
        if team.scores[week - 1] > best_score:
            best_week = week
            best_score = team.scores[week - 1]
    return best_week, best_score

def get_worst_week(team):
    worst_week = 0
    worst_score = team.scores[0]
    for week in range(2, 21):
        if team.scores[week - 1] < worst_score:
            worst_week = week
            worst_score = team.scores[week - 1]
    return worst_week, worst_score

def get_longest_streak(team):
    win_count = 0
    max_win = 0
    loss_count = 0
    max_loss = 0
    for i in (1, 21):
        if loss_count > max_loss:
            max_loss = loss_count
        if win_count > max_win:
            max_win = win_count
        if team.outcomes[i] == "WIN":
            win_count+=1
            loss_count = 0
        if team.outcomes[i] == "LOSS":
            loss_count+=1
            win_count = 0
        if team.outcomes[i] == "TIE":
            win_count = 0
            loss_count = 0
    return max_win, max_loss

def get_sleeper_star(team):
    sleeper = team.roster[0]
    final_diff = sleeper.avg_points - sleeper.projected_avg_points + sleeper.total_points - sleeper.projected_total_points
    for player in team.roster:
        new_combined_diff = player.avg_points - player.projected_avg_points + player.total_points - player.projected_total_points
        if new_combined_diff > final_diff:
            final_diff = new_combined_diff
            sleeper = player
    return sleeper, player.avg_points, player.projected_avg_points



