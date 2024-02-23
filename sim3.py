import random
import copy

# CONFIG
simulations = 100000
verbose = False
power_ups = True
accounting_error_win_boost_factor = 1.1


def score(position: int, power_up: str):

  if power_up == "double_edged_sword":
    if position == 1: return 15
    if position == 2: return 9
    if position == 3: return 5
    if position == 4: return 1
    return -1


  if position == 1: return 9
  if position == 2: return 6
  if position == 3: return 4
  if position == 4: return 2
  return 1

games = [
  "world_of_warcraft",
  "battleblock_theater", 
  "kerbal_space_program", 
  "geoguessr", 
  "jump_king", 
  "planet_coaster", 
  "war_thunder", 
  "hollow_knight", 
  "pummel_party",
  "pubg"
]

people = [
  "jakob",
  "jorgen",
  "tobias",
  "william",
  "kristin"
]

game_chosen_by = {
  "world_of_warcraft": "william",
  "battleblock_theater": "kristin", 
  "kerbal_space_program": "jakob", 
  "geoguessr": "jorgen", 
  "jump_king": "tobias", 
  "planet_coaster": "jorgen", 
  "war_thunder": "jakob", 
  "hollow_knight": "kristin", 
  "pummel_party": "tobias",
  "pubg": "william"
}

# JAKOB

win_chances = {
  "jakob":   {"world_of_warcraft": 20, "battleblock_theater": 3, "kerbal_space_program": 90, "geoguessr": 20, "jump_king": 2, "planet_coaster": 40, "war_thunder": 70, "hollow_knight": 2, "pummel_party": 15, "pubg": 6},
  "jorgen":  {"world_of_warcraft": 10, "battleblock_theater": 1, "kerbal_space_program": 2, "geoguessr": 70, "jump_king": 2, "planet_coaster": 50, "war_thunder": 1, "hollow_knight": 0.1, "pummel_party": 5, "pubg": 1},
  "tobias":  {"world_of_warcraft": 10, "battleblock_theater": 25, "kerbal_space_program": 6, "geoguessr": 4, "jump_king": 85, "planet_coaster": 5, "war_thunder": 25, "hollow_knight": 2, "pummel_party": 60, "pubg": 6},
  "william": {"world_of_warcraft": 50, "battleblock_theater": 1, "kerbal_space_program": 0, "geoguessr": 6, "jump_king": 5, "planet_coaster": 0, "war_thunder": 2, "hollow_knight": 0.2, "pummel_party": 5, "pubg": 80},
  "kristin": {"world_of_warcraft": 10, "battleblock_theater": 65, "kerbal_space_program": 0.5, "geoguessr": 0, "jump_king": 6, "planet_coaster": 5, "war_thunder": 2, "hollow_knight": 95, "pummel_party": 15, "pubg": 7}
}

power_up_chances = {
  "jakob":{
    "double_edged_sword": {"planet_coaster": 1}, 
    "accounting_error": {"world_of_warcraft": 1}
  },
  "jorgen":{
    "double_edged_sword": {"war_thunder": 0.7, "jump_king": 0.3}, 
    "accounting_error": {"world_of_warcraft": 0.5, "pummel_party": 0.5}
  },
  "tobias":{
    "double_edged_sword": {"hollow_knight": 0.5, "battleblock_theater": 0.5}, 
    "accounting_error": {"battleblock_theater": 0.25, "world_of_warcraft": 0.25, "geoguessr": 0.25, "planet_coaster": 0.25}
  },
  "william":{
    "double_edged_sword": {"geoguessr": 0.8, "pummel_party": 0.2}, 
    "accounting_error": {"world_of_warcraft": 0.2, "geoguessr": 0.4, "pummel_party": 0.4}
  },
  "kristin":{
    "double_edged_sword": {"jump_king": 0.7, "pummel_party": 0.15, "world_of_warcraft": 0.15}, 
    "accounting_error": {"planet_coaster": 0.4, "pummel_party": 0.4, "world_of_warcraft": 0.2}
  }
}

crystal_ballin_win_chance = {
  "jakob": 0.5,
  "jorgen": 0.3,
  "tobias": 0.5,
  "william": 0.3,
  "kristin": 0.5
}

class player:
  def __init__(self, name: str, win_chances: dict, crystal_ballin_win_chance: float, power_up_chances: dict):
    self.name = name
    self.points = 0
    self.win_chances = win_chances
    self.crystal_ballin_win_chance = crystal_ballin_win_chance
    self.power_up_chances = power_up_chances
    self.power_ups_choices = {
      "double_edged_sword": pick_from_probabilities([(game, self.power_up_chances["double_edged_sword"][game]) for game in self.power_up_chances["double_edged_sword"]]),
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

def check_crystal_ballin_points(player: player, verbose: bool):
  if random.random() <= player.crystal_ballin_win_chance:
    if verbose:
      print(player.name, "won crystal ballin")
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
  if power_ups and player.power_ups_choices["double_edged_sword"] == game:
    if verbose:
      print(player.name + " used double up")
    return "double_edged_sword"
  return "none"

def mutate_win_chances(win_chances: dict, power_up_chances: dict):
  mutated_win_chances = copy.deepcopy(win_chances)
  for player in power_up_chances:
    mutate_win_probabilities = [(game, power_up_chances[player]["accounting_error"][game]) for game in power_up_chances[player]["accounting_error"]]
    chosen_game = pick_from_probabilities(mutate_win_probabilities)
    mutated_win_chances[player][chosen_game] = mutated_win_chances[player][chosen_game] * accounting_error_win_boost_factor
  return mutated_win_chances

def do_turn(game: str, players: list, verbose: bool):
  if verbose:
    print("\n" + game + " round:")

  players_of_round = players
  
  first, players_of_round = pick_next_best_position(game, players_of_round)
  second, players_of_round = pick_next_best_position(game, players_of_round)
  third, players_of_round = pick_next_best_position(game, players_of_round)
  fourth, players_of_round = pick_next_best_position(game, players_of_round)
  fifth, players_of_round = pick_next_best_position(game, players_of_round)

  # Add points to players
  for player in players:
    if player.name == first:
      player.add_points(score(1, check_if_power_up(player, game, verbose)))
    if player.name == second:
      player.add_points(score(2, check_if_power_up(player, game, verbose)))
    if player.name == third:
      player.add_points(score(3, check_if_power_up(player, game, verbose)))
    if player.name == fourth:
      player.add_points(score(4, check_if_power_up(player, game, verbose)))
    if player.name == fifth:
      player.add_points(score(5, check_if_power_up(player, game, verbose)))

  
  if verbose:
    print("First:", first, "| Second:", second, "| Third:", third, "| Fourth:", fourth, "| Fifth:", fifth)

def simulate_tournament(win_chances: dict, power_up_chances: dict, verbose: bool = False):
  mutated_win_chances = mutate_win_chances(win_chances, power_up_chances)

  players = [
    player("jakob", mutated_win_chances["jakob"], crystal_ballin_win_chance["jakob"], power_up_chances["jakob"]), 
    player("jorgen", mutated_win_chances["jorgen"], crystal_ballin_win_chance["jorgen"], power_up_chances["jorgen"]), 
    player("tobias", mutated_win_chances["tobias"], crystal_ballin_win_chance["tobias"], power_up_chances["tobias"]), 
    player("william", mutated_win_chances["william"], crystal_ballin_win_chance["william"], power_up_chances["william"]),
    player("kristin", mutated_win_chances["kristin"], crystal_ballin_win_chance["kristin"], power_up_chances["kristin"])
  ]

  for player_looked_at in players:
    check_crystal_ballin_points(player_looked_at, verbose)

  for game in games:
    do_turn(game, players, verbose)
    if verbose:
      print("Point scores after " + game + ":")
      for p in players:
        print(p)

  return players

def simulationRun(print_results_per_simulation: bool, win_chances: dict, power_up_chances: dict, simulations: int):
  wins = {
    "jakob": 0,
    "jorgen": 0,
    "tobias": 0,
    "william": 0,
    "kristin": 0
  }

  point_sums = {
    "jakob": 0,
    "jorgen": 0,
    "tobias": 0,
    "william": 0,
    "kristin": 0
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
    "william": point_sums["william"] / simulations,
    "kristin": point_sums["kristin"] / simulations
  }

  win_percentage = {
    "jakob": str(round(wins["jakob"] / simulations * 100, 2)) + "%",
    "jorgen": str(round(wins["jorgen"] / simulations * 100, 2)) + "%",
    "tobias": str(round(wins["tobias"] / simulations * 100, 2)) + "%",
    "william": str(round(wins["william"] / simulations * 100, 2)) + "%",
    "kristin": str(round(wins["kristin"] / simulations * 100, 2)) + "%"
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
  for double_edged_sword_game in games:
    if game_chosen_by[double_edged_sword_game] != simulation_player:
      for crystal_ballin_game in games:
        if game_chosen_by[crystal_ballin_game] != simulation_player:
          for accounting_error_game in games:
            if game_chosen_by[accounting_error_game] != simulation_player:
              for person in people:
                if person != simulation_player and game_chosen_by[accounting_error_game] != person and len(set([double_edged_sword_game, crystal_ballin_game, accounting_error_game])) == 3:
                  power_up_combinations.append({"double_edged_sword": {double_edged_sword_game: 1}, "crystal_ballin": {crystal_ballin_game: 1}, "accounting_error": {accounting_error_game: [1, person]}})

  print("Number of combinations:", len(power_up_combinations), "\nnumber of simulations:", simulations, "\ntotal number of simulations:", len(power_up_combinations) * simulations)

  results = []
  for combo in power_up_combinations:
    if False:
      # TODO fix
      print(combo)
    power_up_chances = {
      # TODO generate this dynamically based on simulation_player
      simulation_player: combo,
      "jakob": power_up_chances["jakob"], 
      "jorgen": power_up_chances["jorgen"], 
      "tobias": power_up_chances["tobias"]
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

simulationRun(True, win_chances, power_up_chances, simulations)