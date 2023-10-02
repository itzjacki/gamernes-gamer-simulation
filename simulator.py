import random

simulations = 5000
verbose = False


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

people = [
  "jakob",
  "jorgen",
  "tobias",
  "william"
]

game_chosen_by = {
  "hearthstone": "william",
  "curve_fever": "tobias",
  "the_sims_4": "jakob",
  "warcraft_3": "william",
  "poker": "jorgen",
  "wreckfest": "tobias",
  "total_war_empire": "jakob",
  "league_of_legends": "jorgen"
}

# JAKOB

win_chances = {
  "jakob":   {"hearthstone": 0.17, "curve_fever": 0.06, "the_sims_4": 0.60, "warcraft_3": 0.05, "poker": 0.25, "wreckfest": 0.30, "total_war_empire": 0.80, "league_of_legends": 0.25},
  "jorgen":  {"hearthstone": 0.17, "curve_fever": 0.05, "the_sims_4": 0.05, "warcraft_3": 0.025, "poker": 0.40, "wreckfest": 0.00, "total_war_empire": 0.10, "league_of_legends": 0.30},
  "tobias":  {"hearthstone": 0.26, "curve_fever": 0.85, "the_sims_4": 0.30, "warcraft_3": 0.025, "poker": 0.20, "wreckfest": 0.45, "total_war_empire": 0.10, "league_of_legends": 0.25},
  "william": {"hearthstone": 0.40, "curve_fever": 0.04, "the_sims_4": 0.05, "warcraft_3": 0.90, "poker": 0.15, "wreckfest": 0.25, "total_war_empire": 0.00, "league_of_legends": 0.20}
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
    "double_up": {"the_sims_4": 0.60, "hearthstone": 0.10, "total_war_empire": 0.30}, 
    "safety_net": {"warcraft_3": 1}, 
    "gamba_time": {"poker": (0.5, "jakob"), "league_of_legends": (0.5, "william")}
  },
  "william":{
    "double_up": {"league_of_legends": 0.7, "wreckfest": 0.15, "league_of_legends": 0.15}, 
    "safety_net": {"total_war_empire": 0.95, "the_sims_4": 0.05}, 
    "gamba_time": {"wreckfest": (0.5, "jakob"), "poker": (0.5, "tobias")}
  }
}

# TOBIAS

win_chances_tobias = {
  "jakob":   {"hearthstone": 0.20, "curve_fever": 0.12, "the_sims_4": 0.35, "warcraft_3": 0.20, "poker": 0.26, "wreckfest": 0.25, "total_war_empire": 0.40, "league_of_legends": 0.26},
  "jorgen":  {"hearthstone": 0.25, "curve_fever": 0.12, "the_sims_4": 0.20, "warcraft_3": 0.15, "poker": 0.30, "wreckfest": 0.00, "total_war_empire": 0.33, "league_of_legends": 0.28},
  "tobias":  {"hearthstone": 0.25, "curve_fever": 0.60, "the_sims_4": 0.30, "warcraft_3": 0.15, "poker": 0.18, "wreckfest": 0.45, "total_war_empire": 0.27, "league_of_legends": 0.18},
  "william": {"hearthstone": 0.30, "curve_fever": 0.16, "the_sims_4": 0.15, "warcraft_3": 0.50, "poker": 0.26, "wreckfest": 0.30, "total_war_empire": 0.00, "league_of_legends": 0.28}
}

power_up_chances_tobias = {
  "jakob":{
    "double_up": {"poker": 1}, 
    "safety_net": {"hearthstone": 1}, 
    "gamba_time": {"league_of_legends": (1, "william")}
  },
  "jorgen":{
    "double_up": {"hearthstone": 1}, 
    "safety_net": {"wreckfest": 1}, 
    "gamba_time": {"wreckfest": (1, "william")}
  },
  "william":{
    "double_up": {"wreckfest": 1}, 
    "safety_net": {"total_war_empire": 1}, 
    "gamba_time": {"poker": (1, "jakob")}
  }
}

# JØRGEN


# WILLIAM

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

def simulate_tournament(win_chances: dict, power_up_chances: dict, verbose: bool = False):
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

def simulationRun(print_results_per_simulation: bool, win_chances: dict, power_up_chances: dict, simulations: int):
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
    players = simulate_tournament(win_chances, power_up_chances, verbose=verbose)
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

  win_percentage = {
    "jakob": str(round(wins["jakob"] / simulations * 100, 2)) + "%",
    "jorgen": str(round(wins["jorgen"] / simulations * 100, 2)) + "%",
    "tobias": str(round(wins["tobias"] / simulations * 100, 2)) + "%",
    "william": str(round(wins["william"] / simulations * 100, 2)) + "%"
  }

  if print_results_per_simulation:
    print("\n------------------------------------------\n")
    print(simulations, "simulations completed, results:")
    print("\nWin distribution: ")
    print(win_percentage)
    print("\nAverage point distribution: ")
    print(point_averges)

  return win_percentage, point_averges

def optimize_power_ups(power_up_chances: dict, simulation_player: str ):
  power_up_combinations = []

  # Construct list of all valid combinations of powerup choices by the player
  for double_up_game in games:
    if game_chosen_by[double_up_game] != simulation_player:
      for safety_net_game in games:
        if game_chosen_by[safety_net_game] != simulation_player:
          for gamba_time_game in games:
            if game_chosen_by[gamba_time_game] != simulation_player:
              for person in people:
                if person != simulation_player and game_chosen_by[gamba_time_game] != person and len(set([double_up_game, safety_net_game, gamba_time_game])) == 3:
                  power_up_combinations.append({"double_up": {double_up_game: 1}, "safety_net": {safety_net_game: 1}, "gamba_time": {gamba_time_game: [1, person]}})

  print("Number of combinations:", len(power_up_combinations), "\nnumber of simulations:", simulations, "\ntotal number of simulations:", len(power_up_combinations) * simulations)

  results = []
  for combo in power_up_combinations:
    if False:
      # TODO fix
      print(combo)
    power_up_chances = {
      # TODO generate this dynamically based on simulation_player
      simulation_player: combo,
      "jorgen": power_up_chances["jorgen"], 
      "tobias": power_up_chances["tobias"], 
      "william": power_up_chances["william"]
    }
    run_wins, run_point_averages = simulationRun(False, win_chances, power_up_chances, simulations)
    results.append({"win_distribution": run_wins, "point_averages": run_point_averages, "power_up_combo": combo})

  sorted_results = sorted(results, key=lambda k: k['win_distribution'][simulation_player], reverse=True)
  print("Top 3 combinations:")
  print("\n------------------------------------------\n")
  print(sorted_results[0])
  print("\n------------------------------------------\n")
  print(sorted_results[1])
  print("\n------------------------------------------\n")
  print(sorted_results[2])
  print("\n------------------------------------------\n")

optimize_power_ups(power_up_chances, "jakob")