class Game:
  def __init__(self, date, time, home_team, away_team, pos_odds, neg_odds, home_points, away_points, winner):
    self.date = date
    self.time = time
    self.home_team = home_team
    self.away_team = away_team
    self.pos_odds = pos_odds
    self.neg_odds = neg_odds
    self.home_points = home_points
    self.away_points = away_points
    self.winner = winner

  def __str__(self):
    return (f"Date: {self.date}, Time: {self.time}, Home: {self.home_team}, Away: {self.away_team}, "
      f"Pos Odds: {self.pos_odds}, Neg Odds: {self.neg_odds}, Home Points: {self.home_points}, "
      f"Away Points: {self.away_points}")
