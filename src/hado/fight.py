import random
from itertools import combinations

# 初始化人员和队伍
players = [f'P{i + 1}' for i in range(12)]
random.shuffle(players)
teams = {
    'A': players[:3],
    'B': players[3:6],
    'C': players[6:9],
    'D': players[9:]
}


def match(team1, team2):
    """模拟比赛，随机决定胜者"""
    print(f"{team1} vs {team2}")
    winner = random.choice([team1, team2])
    print(f"Winner: {winner}\n")
    return winner


# 比赛过程
def round_robin(teams):
    matches = list(combinations(teams.keys(), 2))
    for team1, team2 in matches:
        match(team1, team2)


# 输出队伍信息
for team, members in teams.items():
    print(f"Team {team}: {members}")

print("\nStarting Round Robin Tournament...\n")
round_robin(teams)
