from enum import Enum, IntEnum
from dataclasses import dataclass
import csv
from typing import List, Tuple, Optional

NUMBER_OF_TEAMS = 3
NUMBER_OF_PLAYERS_PER_TEAM = 5


class Roles(Enum):
    FLEX = "flex"
    CONTROLLER = "controller"
    INITIATOR = "initiator"
    DUELIST = "duelist"
    SENTINEL = "sentinel"

class PlayerRankValue(IntEnum):
    UNRANKED = 0
    IRON = 150
    BRONZE = 450
    SILVER = 750
    GOLD = 1050
    PLATINUM = 1350
    DIAMOND = 1650

class PlayerRankEnum(Enum):
    UNRANKED = "Unranked"
    IRON = "Iron"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"

@dataclass
class Rank:
    rank: PlayerRankEnum
    rank_value: PlayerRankValue

    def __init__(self, rank: PlayerRankEnum):
        self.rank = rank
        self.rank_value = PlayerRankValue[rank.name]

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
        return (
            f"Player(name={self.name}, tag={self.tag}, discord_tag={self.discord_tag}, "
            f"agency={self.agency}, rank={str(self.rank.rank.value)}, rank_value={str(self.rank.rank_value.value)}, role={self.role.value}, "
            f"comment={self.comment})"
        )


    def __repr__(self):
        return f"""
        Player Card:
        -------------------------
        | Name       : {self.name}
        | Tag        : {self.tag}
        | Discord Tag: {self.discord_tag}
        | Agency     : {self.agency}
        | Rank       : {self.rank.rank.value}
        | Rank Value : {self.rank.rank_value.value}
        | Role       : {self.role.value}
        | Comment    : {self.comment}
        -------------------------
        """


# This is supposed to help with role handling but I don't think it's necessary
@dataclass
class Team:
    controller: Optional[Player] = None
    initiator: Optional[Player] = None
    sentinel: Optional[Player] = None
    duelist: Optional[Player] = None
    flex: Optional[Player] = None

    def __init__(self, players: list[Player]):
        for player in players:
            if player.role == Roles.CONTROLLER and self.controller is None:
                self.controller = player
            elif player.role == Roles.INITIATOR and self.initiator is None:
                self.initiator = player
            elif player.role == Roles.SENTINEL and self.sentinel is None:
                self.sentinel = player
            elif player.role == Roles.DUELIST and self.duelist is None:
                self.duelist = player
            elif player.role == Roles.FLEX and self.flex is None:
                self.flex = player

        if self.flex is None:
            for player in players:
                if player not in [
                    self.controller,
                    self.initiator,
                    self.sentinel,
                    self.duelist,
                    self.flex,
                ]:
                    self.flex = player
                    break


def load_players_from_csv_file(csv_file_path: str) -> list[Player]:
    """Load players from a CSV file and return a list of Player objects"""
    list_of_players = []
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            rank = Rank(PlayerRankEnum[row["Rank"].upper()])
            role = Roles[row["Rôle principal"].upper()]
            list_of_players.append(
                Player(
                    row["Nom + Prénom (@)"],
                    row["Tag Valorant"],
                    row["Tag Discord"],
                    row["Agence"],
                    rank,
                    role,
                    row["Commentaires"],
                )
            )
    return list_of_players


def generate_teams(
    players: List[Player], number_of_teams: int
) -> Tuple[List[List[Player]], List[Player]]:
    """Generate teams from a list of players using a greedy algorithm"""
    # Sort players by rank_value in descending order
    players.sort(key=lambda player: player.rank.rank_value, reverse=True)
    left_players = []
    # Initiate empty teams
    teams = [[] for _ in range(number_of_teams)]
    for player in players:
        # Sort teams by sum of rank_value in ascending order and add player to the team with the lowest sum
        teams.sort(key=lambda team: sum(player.rank.rank_value for player in team))
        for team in teams:
            # Check if team is not full and add player to the team if it is not full or to the next team with the lowest sum
            if len(team) < NUMBER_OF_PLAYERS_PER_TEAM:
                team.append(player)
    # Check if there are teams with less than 5 players and move those players to `left_players`
    for team in teams:
        if len(team) < NUMBER_OF_PLAYERS_PER_TEAM:
            left_players.extend(team)
    # Remove teams with less than 5 players
    teams = [team for team in teams if len(team) == NUMBER_OF_PLAYERS_PER_TEAM]
    # Return the teams and the players that couldn't be added to a team
    return teams, left_players


def calculate_average_rank(player_team: List[Player]) -> float:
    if not team:
        raise ValueError("Team can't be empty.")
    total = sum(player.rank.rank_value for player in player_team)
    return total / len(player_team)


player_list = load_players_from_csv_file("./Valorant.csv")
teams_of_player_list, left_players_list  = generate_teams(player_list, NUMBER_OF_TEAMS)
for team in teams_of_player_list:
    print(f"Team: {team}\n Average Rank: {calculate_average_rank(team)}\n\n")
print(f"Left players: {left_players_list}")