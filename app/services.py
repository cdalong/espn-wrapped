from __future__ import annotations

import time
from espn_api.basketball import * 
import requests

# stats does not include playoffs
# reminder to check cases where diff settings might affect methods (baby proof it)
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
                return "Found Trae Young!"
              
        return "didn't find trae young aw man"


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

    def get_longest_streak(self, team=None) -> tuple[int, int]:
        win_count = 0
        max_win = 0
        loss_count = 0
        max_loss = 0
        team = team or self.team
        for matchup in team.schedule:
            if (matchup.home_team == team and matchup.winner == 'HOME') or (matchup.home_team != team and matchup.winner == 'AWAY'):
                win_count += 1
                loss_count = 0
            else:
                win_count = 0
                loss_count += 1

            max_win = max(max_win, win_count)
            max_loss = max(max_loss, loss_count)
            
        return max_win, max_loss

    def get_sleeper_star(self) -> tuple[str, float, float]:
        sleeper = None
        final_diff = 0
        for player in self.team.roster:
            new_combined_diff = player.avg_points - player.projected_avg_points + player.total_points - player.projected_total_points
            if new_combined_diff > final_diff:
                final_diff = new_combined_diff
                sleeper = player
        return sleeper.name, sleeper.avg_points, sleeper.projected_avg_points

    def get_bust(self) -> tuple[str, float, float]: 
        bust = None
        final_diff = 0
        for player in self.team.roster:
            new_combined_diff = player.projected_avg_points - player.avg_points + player.projected_total_points - player.total_points
            if new_combined_diff > final_diff:
                final_diff = new_combined_diff
                bust = player
        return bust.name, bust.avg_points, bust.projected_avg_points

    def find_clutch_player(self) -> Player | str:
        point_diff_threshold = 100
        count = {}
        matchup_end_periods = [
        6, 13, 20, 27, 34, 41, 48, 55, 62, 69, 76, 83, 90, 97, 104, 111, 118, 132, 139, 146
        ]

        for i in range(20):
            max_diff = -1
            clutch_player = None

            matchup_obj = self.team.schedule[i]
            is_home = matchup_obj.home_team == self.team
            is_winner = (is_home and matchup_obj.winner == 'HOME') or (not is_home and matchup_obj.winner == 'AWAY')

            if is_winner:
                point_diff = abs(matchup_obj.home_final_score - matchup_obj.away_final_score)

                if point_diff <= point_diff_threshold:
                    end_period = matchup_end_periods[i]

                    final_games = self.league.box_scores(matchup_period=i + 1, scoring_period=end_period, matchup_total=False)

                    box_score = None
                    for matchup in final_games:
                        if self.team in (matchup.home_team, matchup.away_team):
                            box_score = matchup
                            break

                    if box_score:
                        lineup = box_score.home_lineup if box_score.home_team == self.team else box_score.away_lineup

                        for player in lineup:
                            # whichever player performed the most better than usual 
                            if (player.slot_position not in ['BE', 'IR'] and player.points > max_diff and player.points > player.avg_points):
                                max_diff = player.points - player.avg_points
                                clutch_player = player

                        if clutch_player:
                            count[clutch_player] = count.get(clutch_player, 0) + 1

        return max(count, key=count.get).name if count else "No clutch player found. you drafted tatum?"

    def find_best_team_matchup(self) -> tuple[str, int]:
        win_counts = {}

        for matchup in self.team.schedule[:20]:
            home_score = matchup.home_final_score
            away_score = matchup.away_final_score

            if matchup.home_team == self.team and home_score > away_score:
                win_counts[matchup.away_team] = win_counts.get(matchup.away_team, 0) + 1
            elif matchup.away_team == self.team and away_score > home_score:
                win_counts[matchup.home_team] = win_counts.get(matchup.home_team, 0) + 1

        if not win_counts:
            return "How did you not win a single game you bum. quit."

        best_opponent = max(win_counts, key=win_counts.get)
        return best_opponent.team_name, win_counts[best_opponent]

    def find_worst_team_matchup(self) -> tuple[str, int]:
        loss_counts = {}

        for matchup in self.team.schedule[:20]:
            home_score = matchup.home_final_score
            away_score = matchup.away_final_score

            if matchup.home_team == self.team and home_score < away_score:
                loss_counts[matchup.away_team] = loss_counts.get(matchup.away_team, 0) + 1
            elif matchup.away_team == self.team and away_score < home_score:
                loss_counts[matchup.home_team] = loss_counts.get(matchup.home_team, 0) + 1

        if not loss_counts:
            return "Maybe your the goat, maybe ur name is jacob. Maybe both"

        worst_opponent = max(loss_counts, key=loss_counts.get)
        return worst_opponent.team_name, loss_counts[worst_opponent]
    
    def get_biggest_comeback(self) -> tuple[int, int, Team]:
        # works now but takes forever
        # for some reason if i try to cache the box scores to make it quicker it stops working idk idk idk idk ikd idk idk idk idk

        opponent = None
        comeback_amount = -1
        week = -1
        for i in range(len(self.team.schedule)):
            max_diff = -1

            matchup_obj = self.team.schedule[i]
            is_home = matchup_obj.home_team == self.team
            is_winner = (is_home and matchup_obj.winner == 'HOME') or (not is_home and matchup_obj.winner == 'AWAY')

            if is_winner:
                for_cum = 0
                opp_cum = 0
                if i == 16:
                    week_count = 14
                else:
                    week_count = 7
                for j in range(week_count):
                    games = self.league.box_scores(matchup_period=i + 1, scoring_period=j + i * 7, matchup_total=False)
                    box_score = None
                    for matchup in games:
                        if self.team in (matchup.home_team, matchup.away_team):
                            box_score = matchup
                            break

                    if box_score:
                        for_cum += box_score.home_score if box_score.home_team == self.team else box_score.away_score
                        opp_cum += box_score.away_score if box_score.home_team == self.team else box_score.home_score
                        if opp_cum - for_cum > comeback_amount:
                            comeback_amount = opp_cum - for_cum
                            week = i + 1
                            opponent = box_score.away_team if box_score.home_team == self.team else box_score.home_team

                       

        return int(comeback_amount), week, opponent

    def bonus_title(self, team=None) -> list[str]:
        titles = []

        max_over = -1
        max_under = -1
        underdog = None
        overrated = None
        max_diff_plus = -1
        cakewalk = None
        toughie = None
        max_diff_minus = -1
        quick_hands = None
        
        max_count = -1

        for team in self.league.teams:
            total = 0
            total_projected = 0
            count = 0
            for player in team.roster:
                total += player.total_points
                total_projected += player.projected_total_points
                if player.acquisitionType == "ADD":
                    count += 1
            if count > max_count:
                quick_hands = team
                max_count = count

            if max_over < total - total_projected:
                max_over = total - total_projected
                underdog = team
            if max_under < total_projected - total:
                max_under = total_projected - total
                overrated = team

            if team.points_for - team.points_against > max_diff_plus:
                max_diff_plus = team.points_for - team.points_against
                cakewalk = team

            if team.points_against- team.points_for > max_diff_minus:
                max_diff_minus = team.points_against - team.points_for
                toughie = team

            
            
        if underdog == self.team:
            titles.append("underdog")
        if overrated == self.team:
            titles.append("overrated")
        if cakewalk == self.team:
            titles.append("cakewalk")
        if toughie == self.team:
            titles.append("toughie")
        if quick_hands == self.team:
            titles.append("quick hands")
        
        max_win, max_loss = self.get_longest_streak()
        break_win = False
        break_loss = False
        for team in self.league.teams:
            else_win, else_loss = self.get_longest_streak(team)
            if max_win < else_win:
                break_win = True
            if max_loss < else_loss:
                break_loss = True
            if break_win and break_loss:
                break
        if not break_win:
            titles.append("longest win streak")
        if not break_loss:
            titles.append("longest loss streak")


        if len(titles) == 0:
            titles.append("participation trophy")
        return titles
            
    # might cause error with leagues that have custom roster settings
    # slow because iterating through each player in lineup of each day of each week
    def missing_points(self) -> int:
        total_points = 0
        for i in range(len(self.team.schedule)):
            if i == 16:
                week = 14
            else: 
                week = 7
            for j in range(week): #special case for the two week matchups!!!!! fix for combeack method as well
                counter = 0
                potential_points = 0
                games = self.league.box_scores(matchup_period=i + 1, scoring_period=j + i * 7, matchup_total=False)
                box_score = None
                for matchup in games:
                    if self.team in (matchup.home_team, matchup.away_team):
                        box_score = matchup
                        break

                if box_score:
                    for player in box_score.home_lineup:
                        if player.slot_position != "BE" and player.slot_position != "IR" and player.points != 0:
                            counter += 1
                        if player.slot_position == "BE" or player.slot_position == "IR":
                            potential_points += player.points
                    
                    if counter < 10:
                        total_points += potential_points
        
        return total_points

       
    
    
# my swid used for testing 
# s = Services(league_id=332773775, year=2025, espn_s2='AEB%2FraVAzJUuPQQx%2FZbZyHlQBgCLq%2FRJZeRW%2FD2PS9L1c89tj7UCmG7Y8jGvoYKhToVRtrWmOV8wHyGr8PkOlQJ%2Bc6WyPrTJHE8s2fgroHPV2Z3vA3Hp1QbO0ZlHFu0YvNBT1OMvExX1l7vPZPi5Is4Fmqx8AJDu8aGb5sdXtY5G1oEJ5imB9sjcwj3QUnA0lBdCWbQ%2BUcs%2FDnBNkWDd%2Fe191amCJFp7S0%2BnH1ut5HMOPlo%2B6gh3FhScoJQNIhqkGL2gQr0Bv0WIrSA%2F7Cg8ywpJPBwCDr9tpfwAmfqFWYzABQ%3D%3D', swid='{1A576FEF-EB0A-4EAC-A122-54A7CB7DD0FF}')
