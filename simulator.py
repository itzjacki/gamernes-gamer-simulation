import random

def score(position: int, power_up: str):

  if power_up == "double_up":
    if position == 1: return 14
    if position == 2: return 8
    if position == 3: return 4
    return 2
  
  if power_up == "safety_net":
    if position == 1: return 5
    if position == 2: return 3
    if position == 3: return 3
    return 3

  if position == 1: return 7
  if position == 2: return 4
  if position == 3: return 2
  return 1

games = [
  "hearthstone", 
  "curve_fever", 
  "the_sims_4", 
  "warcraft_3", 
  "poker", 
  "wreckfest", 
  "total_war_empire", 
  "league_of_legends"
]

win_chances = {
  "jakob":   {"hearthstone": 0.10, "curve_fever": 0.09, "the_sims_4": 0.60, "warcraft_3": 0.10, "poker": 0.25, "wreckfest": 0.30, "total_war_empire": 0.80, "league_of_legends": 0.25},
  "jorgen":  {"hearthstone": 0.10, "curve_fever": 0.10, "the_sims_4": 0.05, "warcraft_3": 0.05, "poker": 0.40, "wreckfest": 0.00, "total_war_empire": 0.13, "league_of_legends": 0.30},
  "tobias":  {"hearthstone": 0.40, "curve_fever": 0.75, "the_sims_4": 0.30, "warcraft_3": 0.10, "poker": 0.20, "wreckfest": 0.45, "total_war_empire": 0.07, "league_of_legends": 0.25},
  "william": {"hearthstone": 0.40, "curve_fever": 0.06, "the_sims_4": 0.05, "warcraft_3": 0.75, "poker": 0.15, "wreckfest": 0.25, "total_war_empire": 0.00, "league_of_legends": 0.20}
}

power_up_chances = {
  "jakob":{
    "double_up": {"wreckfest": 1}, 
    "safety_net": {"curve_fever": 1}, 
    "gamba_time": {"hearthstone": (1, "tobias")}
  },
  "jorgen":{
    "double_up": {"curve_fever": 0.75, "total_war_empire": 0.25}, 
    "safety_net": {"wreckfest": 1}, 
    "gamba_time": {"hearthstone": (0.4, "tobias"), "wreckfest": (0.6, "jakob")}
  },
  "tobias":{
    "double_up": {"warcraft_3": 0.2, "hearthstone": 0.7, "poker": 0.1}, 
    "safety_net": {"total_war_empire": 0.4, "poker": 0.3, "league_of_legends": 0.3}, 
    "gamba_time": {"poker": (0.2, "jakob"), "hearthstone": (0.2, "jorgen"), "league_of_legends": (0.6, "william")}
  },
  "william":{
      "double_up": {"league_of_legends": 0.7, "wreckfest": 0.15, "league_of_legends": 0.15}, 
    "safety_net": {"total_war_empire": 0.95, "the_sims_4": 0.05}, 
    "gamba_time": {"wreckfest": (0.5, "jakob"), "poker": (0.5, "tobias")}
  }
}

class player:
  def __init__(self, name: str, win_chances: dict, power_up_chances: dict):
    self.name = name
    self.points = 0
    self.win_chances = win_chances
    self.power_up_chances = power_up_chances
    self.power_ups_choices = {
      "double_up": pick_from_probabilities([(game, self.power_up_chances["double_up"][game]) for game in self.power_up_chances["double_up"]]),
      "safety_net": pick_from_probabilities([(game, self.power_up_chances["safety_net"][game]) for game in self.power_up_chances["safety_net"]]),
      "gamba_time": pick_gamba_power_up(self.power_up_chances["gamba_time"])
    }

  def add_points(self, points: int):
    self.points += points

  def __str__(self):
    return self.name + ": " + str(self.points)

def pick_from_probabilities(options_with_probabilities: list):
  win_number = random.random() * sum([option[1] for option in options_with_probabilities])
  for option in options_with_probabilities:
    if win_number <= option[1]:
      return option[0]
    win_number -= option[1]
  Exception("No winner found")

def pick_gamba_power_up(gamba_power_up_chances: dict):
  game_picked = pick_from_probabilities([(game, gamba_power_up_chances[game][0]) for game in gamba_power_up_chances])
  player_picked = gamba_power_up_chances[game_picked][1]
  return (game_picked, player_picked)

def check_gamba_points(player: player, game: str, winner, verbose: bool):
  if player.power_ups_choices["gamba_time"][0] == game:
    if verbose:
      print(player.name, "used gamba time on", player.power_ups_choices["gamba_time"][1])
    gamba_target = player.power_ups_choices["gamba_time"][1]
    if winner == gamba_target:
      if verbose:
        print(player.name, "won gamba time")
      player.add_points(3)

def pick_next_best_position(game: str, players: list):
  # construct list of players with win probabilities
  players_with_probabilities = []
  for player in players:
    players_with_probabilities.append((player.name, player.win_chances[game]))
    
  # pick winner
  winner = pick_from_probabilities(players_with_probabilities)

  # remove winner from player list
  players = [player for player in players if player.name != winner]

  return winner, players

def check_if_power_up(player: player, game: str, verbose: bool):
  if player.power_ups_choices["double_up"] == game:
    if verbose:
      print(player.name + " used double up")
    return "double_up"
  if player.power_ups_choices["safety_net"] == game:
    if verbose:
      print(player.name + " used safety net")
    return "safety_net"
  return "none"


def do_turn(game: str, players: list, verbose: bool):
  if verbose:
    print("\n" + game + " round:")

  players_of_round = players
  
  first, players_of_round = pick_next_best_position(game, players_of_round)
  second, players_of_round = pick_next_best_position(game, players_of_round)
  third, players_of_round = pick_next_best_position(game, players_of_round)
  fourth, players_of_round = pick_next_best_position(game, players_of_round)

  # Add points to players
  for player in players:
    check_gamba_points(player, game, first, verbose)
    if player.name == first:
      player.add_points(score(1, check_if_power_up(player, game, verbose)))
    if player.name == second:
      player.add_points(score(2, check_if_power_up(player, game, verbose)))
    if player.name == third:
      player.add_points(score(3, check_if_power_up(player, game, verbose)))
    if player.name == fourth:
      player.add_points(score(4, check_if_power_up(player, game, verbose)))

  
  if verbose:
    print("First:", first, "| Second:", second, "| Third:", third, "| Fourth:", fourth)

def simulate_tournament(verbose: bool = False):
  players = [
    player("jakob", win_chances["jakob"], power_up_chances["jakob"]), 
    player("jorgen", win_chances["jorgen"], power_up_chances["jorgen"]), 
    player("tobias", win_chances["tobias"], power_up_chances["tobias"]), 
    player("william", win_chances["william"], power_up_chances["william"])
  ]
  
  for game in games:
    do_turn(game, players, verbose)
    if verbose:
      for p in players:
        print("Point scores after " + game + ":")
        print(p)

  return players


simulations = 100000
verbose = False

wins = {
  "jakob": 0,
  "jorgen": 0,
  "tobias": 0,
  "william": 0
}

point_sums = {
  "jakob": 0,
  "jorgen": 0,
  "tobias": 0,
  "william": 0
}

for i in range(simulations):
  players = simulate_tournament( verbose)
  for p in players:
    point_sums[p.name] += p.points
    if p.points == max([p.points for p in players]):
      wins[p.name] += 1

point_averges = {
  "jakob": point_sums["jakob"] / simulations,
  "jorgen": point_sums["jorgen"] / simulations,
  "tobias": point_sums["tobias"] / simulations,
  "william": point_sums["william"] / simulations
}

print("\n------------------------------------------\n")
print(simulations, "simulations completed, results:")
print("\nWin distribution: ")
print(wins)
print("\nAverage point distribution: ")
print(point_averges)
