from abc import ABC, abstractmethod



# 1. PARTICIPANT


class Participant(ABC):
    def __init__(self, participant_id, name):
        if participant_id is None or not str(participant_id).strip():
            raise ValueError("Participant ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")

        self.id = participant_id
        self.name = name.strip()

    @abstractmethod
    def get_info(self):
        pass



# 2. HUMAN PLAYER



class HumanPlayer(Participant):
    def __init__(self, player_id, name, role):
        super().__init__(player_id, name)

        if not isinstance(role, str) or not role.strip():
            raise ValueError("Player role cannot be empty.")

        self.role = role.strip()
        self.is_banned = False

    def ban(self):
        if self.is_banned:
            raise ValueError("Player is already banned.")

        self.is_banned = True

    def unban(self):
        if not self.is_banned:
            raise ValueError("Player is not banned.")

        self.is_banned = False

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "is_banned": self.is_banned
        }


# 3. TEAM


class Team(Participant): 
    def __init__(self, team_id, name):
        super().__init__(team_id, name)

        self.players = []
        self.is_active = True

    def add_player(self, player):
        if not isinstance(player, HumanPlayer):
            raise TypeError("Only HumanPlayer objects can join a team.")

        if any(p.id == player.id for p in self.players):
            raise ValueError("Player ID already exists in this team.")

        self.players.append(player)

    def remove_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                self.players.remove(player)
                return

        raise ValueError("Player was not found in this team.")

    def get_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player

        return None

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active,
            "players_count": len(self.players)
        }



# 4. MATCH


class Match(ABC):
    VALID_STATUSES = ("Upcoming", "Live", "Finished")

    def __init__(self, match_id, team1, team2):
        if not isinstance(team1, Team) or not isinstance(team2, Team):
            raise TypeError("A match requires two Team objects.")

        if team1 is team2:
            raise ValueError("A team cannot play against itself.")

        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2

        self.score = None
        self.status = "Upcoming"

    def start_match(self):
        if self.status != "Upcoming":
            raise RuntimeError("Only upcoming matches can be started.")

        if not self.team1.is_active or not self.team2.is_active:
            raise RuntimeError("Both teams must be active.")

        self.status = "Live"

    def finish_match(self, team1_score, team2_score):
        if self.status != "Live":
            raise RuntimeError("Only live matches can be finished.")

        for value in (team1_score, team2_score):
            if type(value) is not int or value < 0:
                raise ValueError(
                    "Scores must be non-negative integers."
                )

        self.score = (team1_score, team2_score)
        self.status = "Finished"

    def get_result(self):
        if self.status != "Finished":
            return None

        score1, score2 = self.score

        if score1 > score2:
            winner = self.team1.name
        elif score2 > score1:
            winner = self.team2.name
        else:
            winner = "Draw"

        return {
            "match_id": self.match_id,
            "team1": self.team1.name,
            "team2": self.team2.name,
            "score": self.score,
            "winner": winner,
            "status": self.status
        }

    @abstractmethod
    def get_match_details(self):
        pass



# 5. FOOTBALL MATCH


class FootballMatch(Match):
    def __init__(self, match_id, team1, team2):
        super().__init__(match_id, team1, team2)

        self.yellow_cards = []
        self.red_cards = []
        self.yellow_count = {}
        self.sent_off_players = set()

    def add_card(self, player, card_type):
        if self.status != "Live":
            raise RuntimeError("Cards can only be given during live matches.")

        if not isinstance(player, HumanPlayer):
            raise TypeError("A valid HumanPlayer object is required.")

        participating_players = (
            self.team1.players + self.team2.players
        )

        if not any(p is player for p in participating_players):
            raise ValueError(
                "Player does not belong to either team in this match."
            )

        if player.is_banned:
            raise ValueError("A banned player cannot participate.")

        if player.id in self.sent_off_players:
            raise ValueError("This player has already been sent off.")

        if not isinstance(card_type, str):
            raise ValueError("Card type must be a string.")

        card_type = card_type.strip().lower()

        if card_type == "yellow":
            self.yellow_cards.append(player)

            self.yellow_count[player.id] = (
                self.yellow_count.get(player.id, 0) + 1
            )

            # Two yellow cards result in a red card.
            if self.yellow_count[player.id] == 2:
                self._send_off(player, reason="second_yellow")

        elif card_type == "red":
            self._send_off(player, reason="direct_red")

        else:
            raise ValueError(
                "Invalid card type. Use 'yellow' or 'red'."
            )

    def _send_off(self, player, reason):
        self.red_cards.append({
            "player": player,
            "reason": reason
        })

        self.sent_off_players.add(player.id)

    def get_match_details(self):
        return {
            "match_id": self.match_id,
            "team1": self.team1.name,
            "team2": self.team2.name,
            "score": self.score,
            "status": self.status,
            "yellow_cards": len(self.yellow_cards),
            "red_cards": len(self.red_cards)
        }



# 6. TOURNAMENT


class Tournament:
    def __init__(self, name):
        if not self.validate_tournament_name(name):
            raise ValueError(
                "Tournament name must contain at least 3 characters."
            )

        self.name = name.strip()
        self.teams = []
        self.matches = []
        self.schedule_generated = False

    @staticmethod
    def validate_tournament_name(name):
        return (
            isinstance(name, str)
            and len(name.strip()) >= 3
        )

    def register_team(self, team):
        if self.schedule_generated:
            raise RuntimeError(
                "Cannot register teams after schedule generation."
            )

        if not isinstance(team, Team):
            raise TypeError("Only Team objects can be registered.")

        if any(t.id == team.id for t in self.teams):
            raise ValueError("A team with this ID is already registered.")

        if any(
            t.name.casefold() == team.name.casefold()
            for t in self.teams
        ):
            raise ValueError("A team with this name is already registered.")

        self.teams.append(team)

    def get_team(self, team_id):
        for team in self.teams:
            if team.id == team_id:
                return team

        return None

    def generate_schedule(self):
        if self.schedule_generated:
            raise RuntimeError("Schedule has already been generated.")

        active_teams = [
            team for team in self.teams if team.is_active
        ]

        if len(active_teams) < 2:
            raise ValueError(
                "At least two active teams are required."
            )

        match_id = 1

        for i in range(len(active_teams)):
            for j in range(i + 1, len(active_teams)):
                match = FootballMatch(
                    match_id,
                    active_teams[i],
                    active_teams[j]
                )

                self.matches.append(match)
                match_id += 1

        self.schedule_generated = True

    def get_match(self, match_id):
        for match in self.matches:
            if match.match_id == match_id:
                return match

        return None

    def get_standings(self):
        table = {}

        for team in self.teams:
            table[team.id] = {
                "team": team,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_difference": 0,
                "points": 0
            }

        for match in self.matches:
            if match.status != "Finished":
                continue

            score1, score2 = match.score

            t1 = table[match.team1.id]
            t2 = table[match.team2.id]

            t1["played"] += 1
            t2["played"] += 1

            t1["goals_for"] += score1
            t1["goals_against"] += score2

            t2["goals_for"] += score2
            t2["goals_against"] += score1

            if score1 > score2:
                t1["won"] += 1
                t2["lost"] += 1
                t1["points"] += 3

            elif score2 > score1:
                t2["won"] += 1
                t1["lost"] += 1
                t2["points"] += 3

            else:
                t1["drawn"] += 1
                t2["drawn"] += 1
                t1["points"] += 1
                t2["points"] += 1

        for row in table.values():
            row["goal_difference"] = (
                row["goals_for"] - row["goals_against"]
            )

        standings = sorted(
            table.values(),
            key=lambda row: (
                row["points"],
                row["goal_difference"],
                row["goals_for"],
                row["team"].name.casefold()
            ),
            reverse=True
        )

        return [
            {"rank": index, **row}
            for index, row in enumerate(standings, start=1)
        ]

    def display_schedule(self):
        print(f"\n=== {self.name}: Match Schedule ===")

        for match in self.matches:
            if match.score is None:
                score = "Not played"
            else:
                score = f"{match.score[0]} - {match.score[1]}"

            print(
                f"Match {match.match_id}: "
                f"{match.team1.name} vs {match.team2.name} | "
                f"{score} | {match.status}"
            )

    def display_standings(self):
        standings = self.get_standings()

        print(f"\n=== {self.name}: Standings ===")
        print(
            f"{'Rank':<5} {'Team':<20} {'P':<3} "
            f"{'W':<3} {'D':<3} {'L':<3} "
            f"{'GF':<4} {'GA':<4} {'GD':<4} {'Pts':<4}"
        )
        print("-" * 65)

        for row in standings:
            team = row["team"]

            print(
                f"{row['rank']:<5} "
                f"{team.name:<20} "
                f"{row['played']:<3} "
                f"{row['won']:<3} "
                f"{row['drawn']:<3} "
                f"{row['lost']:<3} "
                f"{row['goals_for']:<4} "
                f"{row['goals_against']:<4} "
                f"{row['goal_difference']:<4} "
                f"{row['points']:<4}"
            )





##to test of oop =====================
#>>>>>>>>>>>>>>>>>>>>>>>
# Create a tournamentif __name__ == "__main__":
tournament = Tournament("Elite Football League")
team1 = Team(1, "Real Madrid")
team2 = Team(2, "Barcelona")
team3 = Team(3, "Liverpool")
player1 = HumanPlayer(101, "Player One", "Forward")
player2 = HumanPlayer(102, "Player Two", "Defender")
player3 = HumanPlayer(201, "Player Three", "Goalkeeper")
team1.add_player(player1)
team1.add_player(player2)
team2.add_player(player3)
tournament.register_team(team1)
tournament.register_team(team2)
tournament.register_team(team3)
tournament.generate_schedule()
tournament.display_schedule()
match = tournament.get_match(1)
match.start_match()
match.add_card(player1, "yellow")
match.finish_match(3, 1)
match2 = tournament.get_match(2)
match2.start_match()
match2.finish_match(0, 0)
match3 = tournament.get_match(3)
match3.start_match()
match3.finish_match(1, 2)
tournament.display_schedule()
tournament.display_standings()
print(match.get_match_details())
print(player1.get_info())