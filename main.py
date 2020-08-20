import matplotlib.pyplot as plt
from collections import defaultdict

#misidentification risk
#mistake risk
from random import random, choice

def always_cooperate(hist):
    return 1

def always_cheat(hist):
    return 0

def tit_for_tat(hist):
    if len(hist) == 0:
        return 1

    return hist[-1]

def mostly_cooperate(hist):
    return random()<0.9

def rando(hist):
    return random()>0.5

types = {
    "always cooperate": always_cooperate,
    "always cheat": always_cheat,
    "tit_for_tat": tit_for_tat,
    "mostly_cooperate": mostly_cooperate,
    "rando": rando,
}

players = []

ID = 0
def new_id():
    global ID
    ID += 1
    return ID

def new_player(t):
    return {"id":new_id(),"type":t,"score":100,"history":defaultdict(list)}

for t in types:
    for i in range(5):
        players.append(new_player(t))

rounds = 50
cull_lowest_n = 1

typescore = defaultdict(list)
typecount = defaultdict(list)

for rnd in range(rounds):
    #everyone against everyone
    for player1 in players:
        for player2 in players:
            if player1 == player2:
                continue

            f1 = types[player1["type"]]
            d1 = f1(player1["history"][player2["id"]])

            f2 = types[player2["type"]]
            d2 = f2(player2["history"][player1["id"]])

            payoff = {(0,0):(-1,-1),(1,0):(-2,2),(0,1):(2,-2),(1,1):(1,1)}[(d1,d2)]
            player1["score"] += payoff[0]
            player2["score"] += payoff[1]

    for t in types:
        typescore[t].append(0)
        typecount[t].append(0)

    for player in players:
        typescore[player["type"]][-1] += player["score"]
        typecount[player["type"]][-1] += 1

    """
    for player in list(players):
    if player["score"] < 0:
    players.remove(player)
    """
    sortedplayers = sorted(players, key=lambda p:p["score"])

    for i in range(cull_lowest_n):
        lowestn = sortedplayers[0]["score"]#min(sortedplayers, key=lambda p:p["score"])["score"]
        lowest = []
        for p in sortedplayers:
            if p["score"] == lowestn:
                lowest.append(p)
            else:
                break

        remove = choice(lowest)
        print(remove)
        sortedplayers.remove(remove)

    players = sortedplayers

    classes = defaultdict(list)

    for player in players:
        classes[player["score"]].append(player)

    topN = []

    while len(topN) != cull_lowest_n:
        highest = sorted(classes.keys(), reverse=True)[0]
        top = choice(classes[highest])
        topN.append(top)
        classes[highest].remove(top)
        if len(classes[highest]) == 0:
            del classes[highest]

    for p in topN:
        players.append(new_player(p["type"]))




#print(players)
for t in types:
    ys = typecount[t]#typescore[t]
    plt.plot(ys, label=t)

plt.legend()
plt.show()
