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
            return "found trae young!"
        
        
    return "didn't find trae young aw man"

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
    for i in range(1, 21):
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
    return sleeper, sleeper.avg_points, sleeper.projected_avg_points

def get_bust(team): 
    bust = team.roster[0]
    final_diff = bust.projected_avg_points - bust.avg_points + bust.projected_total_points - bust.total_points
    for player in team.roster:
        new_combined_diff = player.projected_avg_points - player.avg_points + player.projected_total_points - player.total_points
        if new_combined_diff > final_diff:
            final_diff = new_combined_diff
            bust = player
    return bust, bust.avg_points, bust.projected_avg_points

def find_clutch_player(team):  #check method cause might not work well?
    point_diff_threshold = 100
    clutch_player = None
    max_points = -1

    for matchup in team.schedule:
        home_team_id = matchup.get("home", {}).get("teamId")
        away_team_id = matchup.get("away", {}).get("teamId")

        if team.team_id not in (home_team_id, away_team_id):
            continue

        home_score = matchup.get("home", {}).get("totalPoints", 0)
        away_score = matchup.get("away", {}).get("totalPoints", 0)
        point_diff = abs(home_score - away_score)

        if point_diff <= point_diff_threshold:
            final_game = matchup.get("home", {}).get("rosterForCurrentScoringPeriod", {}).get("entries", [])
            final_game += matchup.get("away", {}).get("rosterForCurrentScoringPeriod", {}).get("entries", [])

            for entry in final_game:
                player = entry.get("playerPoolEntry", {}).get("player", {})
                player_name = player.get("fullName")
                points = entry.get("appliedStatTotal", 0)

                if points > max_points:
                    max_points = points
                    clutch_player = player_name
    return clutch_player if clutch_player else "No clutch player found. you drafted tatum?"

def find_best_team_matchup(team):
    win_counts = {}

    for matchup in team.schedule:
        home_team_id = matchup.get("home", {}).get("teamId")
        away_team_id = matchup.get("away", {}).get("teamId")
        home_score = matchup.get("home", {}).get("totalPoints", 0)
        away_score = matchup.get("away", {}).get("totalPoints", 0)

        if home_team_id == team.team_id and home_score > away_score:
            win_counts[away_team_id] = win_counts.get(away_team_id, 0) + 1
        elif away_team_id == team.team_id and away_score > home_score:
            win_counts[home_team_id] = win_counts.get(home_team_id, 0) + 1

    if not win_counts:
        return "How did you not win a single game you bum. quit."

    best_opponent = max(win_counts, key=win_counts.get)
    return f"You beat {best_opponent} a total of {win_counts[best_opponent]} times."

def find_worst_team_matchup(team):
    loss_counts = {}

    for matchup in team.schedule:
        home_team_id = matchup.get("home", {}).get("teamId")
        away_team_id = matchup.get("away", {}).get("teamId")
        home_score = matchup.get("home", {}).get("totalPoints", 0)
        away_score = matchup.get("away", {}).get("totalPoints", 0)

        if home_team_id == team.team_id and home_score < away_score:
            loss_counts[away_team_id] = loss_counts.get(away_team_id, 0) + 1
        elif away_team_id == team.team_id and away_score < home_score:
            loss_counts[home_team_id] = loss_counts.get(home_team_id, 0) + 1

    if not loss_counts:
        return "Maybe your the goat, maybe ur name is jacob. Maybe both"

    worst_opponent = max(loss_counts, key=loss_counts.get)
    return f"You lost to {worst_opponent} a total of {loss_counts[worst_opponent]} times. go die"


