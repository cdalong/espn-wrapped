from __future__ import annotations

import time
from espn_api.basketball import * # espn api says to only import league, but this way python recognizes player and team class
import requests

# stats does not include playoffs
# i should standardize retrun types so its more convinient
class Services:

    # league_id is specific to league, year is season year, espn_s2 and swid are cookies
    # espn_s2 grants permission to access fantasy league data
    # swid is specific to user and allows us to idenitfy which team is theirs
    def __init__(self, league_id: int, year: int, espn_s2: str, swid: str):
        self.league = League(
            league_id=league_id,
            year=year,
            espn_s2=espn_s2,
            swid=swid
        )
        self.team = None
        
        for team in self.league.teams:
            for user in team.owners:
                if swid == user.get('id'):
                    self.team = team

        if self.team is None:
            print("User's team not found in this league.")

    def find_trae_young(self) -> str:

        #Im gonna find trae young!
        for player in self.team.roster:
            if "trae young" in player.name.lower():
                return "found trae young!"
              
        return "didn't find trae young aw man"

    # def get_total_points(self): - > team class has points_for

    def get_weekly_average(self) -> float: 
        return self.team.points_for / 20 

    def get_best_week(self) -> tuple[int, int]:
        best_week = 0
        best_score = 0
        for week in range(20):
            score = self.team.schedule[week].home_final_score if (self.team == self.team.schedule[week].home_team) else self.team.schedule[week].away_final_score 
            if score > best_score:
                best_week = week + 1
                best_score = score
        return best_week, best_score

    def get_worst_week(self) -> tuple[int, int]:
        worst_week = 0
        worst_score = float('inf')
        for week in range(20):
            score = self.team.schedule[week].home_final_score if (self.team == self.team.schedule[week].home_team) else self.team.schedule[week].away_final_score
            if score < worst_score:
                worst_week = week + 1
                worst_score = score 
        return worst_week, worst_score

    def get_longest_streak(self) -> tuple[int, int]:
        win_count = 0
        max_win = 0
        loss_count = 0
        max_loss = 0
        for matchup in self.team.schedule:
            if (matchup.home_team == self.team and matchup.winner == 'HOME') or (matchup.home_team != self.team and matchup.winner == 'AWAY'):
                win_count += 1
                loss_count = 0
            else:
                win_count = 0
                loss_count += 1

            max_win = max(max_win, win_count)
            max_loss = max(max_loss, loss_count)
            
        return max_win, max_loss

    def get_sleeper_star(self) -> tuple[Player, float, float]:
        sleeper = None
        final_diff = 0
        for player in self.team.roster:
            new_combined_diff = player.avg_points - player.projected_avg_points + player.total_points - player.projected_total_points
            if new_combined_diff > final_diff:
                final_diff = new_combined_diff
                sleeper = player
        return sleeper, sleeper.avg_points, sleeper.projected_avg_points

    def get_bust(self) -> tuple[Player, float, float]: 
        bust = None
        final_diff = 0
        for player in self.team.roster:
            new_combined_diff = player.projected_avg_points - player.avg_points + player.projected_total_points - player.total_points
            if new_combined_diff > final_diff:
                final_diff = new_combined_diff
                bust = player
        return bust, bust.avg_points, bust.projected_avg_points

    def find_clutch_player(self) -> Player | str:  #this method should work but doesnt
        point_diff_threshold = 100
        count = {}
        for i in range(20):
            max_points = -1
            clutch_player = None

            # checking if you won, and if point diff was close enough
            if (self.team.schedule[i].home_team == self.team and self.team.schedule[i].winner == 'HOME') or (self.team.schedule[i].home_team != self.team and self.team.schedule[i].winner == 'AWAY'):
                home_score = self.team.schedule[i].home_final_score
                away_score = self.team.schedule[i].away_final_score
                point_diff = abs(home_score - away_score)

                if point_diff <= point_diff_threshold:
                    final_games = self.league.box_scores(i + 1, 6, False)
                    for box_score in final_games:
                        if (self.team == box_score.home_team) or (self.team == box_score.away_team):
                            matchup = box_score
                            print(box_score.home_lineup) # home lineup pops up empty??????
                            break
                    print(matchup.home_lineup) # 
                    lineup  = matchup.home_lineup if matchup.home_team == self.team else matchup.away_lineup
                    print(lineup) #
                    for player in lineup:
                        if player.slot_position != 'BE' and player.slot_position != 'IR' and player.points > max_points and player.points > player.avg_points: 
                            max_points = player.points
                            clutch_player = player
                    if clutch_player is not None:
                        if clutch_player in count:
                            count[clutch_player] += 1
                        else:
                            count[clutch_player] = 1
    
        return max(count, key=count.get) if count else "No clutch player found. you drafted tatum?"

    def find_best_team_matchup(self) -> str | Team:
        win_counts = {}

        for matchup in self.team.schedule:
            home_score = matchup.home_final_score
            away_score = matchup.away_final_score

            if matchup.home_team == self.team.team_id and home_score > away_score:
                win_counts[matchup.away_team] = win_counts.get(matchup.away_team, 0) + 1
            elif matchup.away_team_id == self.team.team_id and away_score > home_score:
                win_counts[matchup.home_team] = win_counts.get(matchup.home_team, 0) + 1

        if not win_counts:
            return "How did you not win a single game you bum. quit."

        best_opponent = max(win_counts, key=win_counts.get)
        return best_opponent

    def find_worst_team_matchup(self) -> str | Team:
        loss_counts = {}

        for matchup in self.team.schedule:
            home_score = matchup.home_final_score
            away_score = matchup.away_final_score

            if matchup.home_team == self.team.team_id and home_score < away_score:
                loss_counts[matchup.away_team] = loss_counts.get(matchup.away_team, 0) + 1
            elif matchup.away_team_id == self.team.team_id and away_score < home_score:
                loss_counts[matchup.home_team] = loss_counts.get(matchup.home_team, 0) + 1

        if not loss_counts:
            return "Maybe your the goat, maybe ur name is jacob. Maybe both"

        worst_opponent = max(loss_counts, key=loss_counts.get)
        return worst_opponent
    

# my swid used for testing 
s = Services(league_id=332773775, year=2025, espn_s2='AEB%2FraVAzJUuPQQx%2FZbZyHlQBgCLq%2FRJZeRW%2FD2PS9L1c89tj7UCmG7Y8jGvoYKhToVRtrWmOV8wHyGr8PkOlQJ%2Bc6WyPrTJHE8s2fgroHPV2Z3vA3Hp1QbO0ZlHFu0YvNBT1OMvExX1l7vPZPi5Is4Fmqx8AJDu8aGb5sdXtY5G1oEJ5imB9sjcwj3QUnA0lBdCWbQ%2BUcs%2FDnBNkWDd%2Fe191amCJFp7S0%2BnH1ut5HMOPlo%2B6gh3FhScoJQNIhqkGL2gQr0Bv0WIrSA%2F7Cg8ywpJPBwCDr9tpfwAmfqFWYzABQ%3D%3D', swid='{1A576FEF-EB0A-4EAC-A122-54A7CB7DD0FF}')

   