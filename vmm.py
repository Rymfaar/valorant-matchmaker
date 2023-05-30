from enum import Enum, IntEnum
from dataclasses import dataclass
import csv
from typing import Union

class Roles(Enum):
    FLEX = "flex"
    CONTROLLER = "controller"
    INITIATOR = "initiator"
    DUELIST = "duelist"
    SENTINEL = "sentinel"

class RankValue(IntEnum):
    UNRANKED = 0
    IRON = 150
    BRONZE = 450
    SILVER = 750
    GOLD = 1050
    PLATINIUM = 1350
    DIAMOND = 1650

class RankEnum(Enum):
    UNRANKED = "Unranked"
    IRON = "Iron"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINIUM = "Platinum"
    DIAMOND = "Diamond"

@dataclass
class Rank: 
    rank: RankEnum
    rank_value: RankValue
    def __init__(self, rank: RankEnum):
        self.rank = rank
        self.rank_value = RankValue[rank.name]

@dataclass
class Player:
    name: str
    tag: str
    discord_tag: str
    agency: str
    rank: Rank
    role: Roles
    comment: str

    def __str__(self):
        return (f'Player(name={self.name}, tag={self.tag}, discord_tag={self.discord_tag}, '
                f'agency={self.agency}, rank={str(self.rank.rank.value)}, rank_value={str(self.rank.rank_value.value)}, role={self.role.value}, '
                f'comment={self.comment})')
    
    def __repr__(self):
        return (f'Player(name={self.name}, tag={self.tag}, discord_tag={self.discord_tag}, '
                f'agency={self.agency}, rank={str(self.rank.rank.value)}, rank_value={str(self.rank.rank_value.value)}, role={self.role.value}, '
                f'comment={self.comment})')

def get_players_from_csv_file(filename:str)->list[Player]:
    """Get players from a csv file"""   
    players = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            rank = Rank(RankEnum[row['Rank'].upper()])
            role = Roles[row['Rôle principal'].upper()]
            players.append(Player(row['Nom + Prénom (@)'], row['Tag Valorant'], row['Tag Discord'], row['Agence'], rank, role, row['Commentaires']))
    return players


def generate_teams(players: list[Player], number_of_teams: int) -> Union[list[list[Player]], list[Player]]:
    """Generate teams from a list of players"""
    teams = [[] for _ in range(number_of_teams)]
    players.sort(key=lambda player: player.rank.rank_value, reverse=True)
    left_players = []

    for player in players:
        # Calculate the average rank_value for each non-full team
        avg_rank_values = [sum(p.rank.rank_value.value for p in team) / len(team) if team else 0 for team in teams if len(team) < 5]
        
        if avg_rank_values:
            # Append the player to the non-full team with the lowest average rank_value
            min_avg_rank_value_team = avg_rank_values.index(min(avg_rank_values))
            teams[min_avg_rank_value_team].append(player)
        else:
            left_players.append(player)
            
    return teams, left_players



players = get_players_from_csv_file('./Valorant.csv')
# for player in players:
#     print(player)

teams,left_players = generate_teams(players, 3)
print(f"Teams: {teams}")
print(f"Left players: {left_players}")