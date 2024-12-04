import pandas as pd
import numpy as np
import json
import warnings

pd.options.mode.chained_assignment = None
warnings.filterwarnings("ignore")

path = "WyscoutData/Events/events_France.json"
with open(path) as f:
    data = json.load(f)

df1 = pd.DataFrame(data)
df1 = df1.reset_index()

path = "WyscoutData/Events/events_Germany.json"
with open(path) as f:
    data = json.load(f)

df2 = pd.DataFrame(data)
df2 = df2.reset_index()

path = "WyscoutData/Events/events_Italy.json"
with open(path) as f:
    data = json.load(f)

df3 = pd.DataFrame(data)
df3 = df3.reset_index()

path = "WyscoutData/Events/events_Spain.json"
with open(path) as f:
    data = json.load(f)

df4 = pd.DataFrame(data)
df4 = df4.reset_index()

df = pd.concat([df1, df2, df3, df4], axis=0, ignore_index=True)
df = df.reset_index()

next_event = df.shift(-1, fill_value=0)
df["nextEvent"] = next_event["subEventName"]
df["kickedOut"] = df.apply(lambda x: 1 if x.nextEvent == "Ball out of the field" else 0, axis = 1)

interruption = df.loc[df["eventName"] == "Interruption"]
df = df.drop(interruption.index)

lost_duels = df.loc[df["eventName"] == "Duel"]
lost_duels = lost_duels.loc[lost_duels.apply (lambda x:{"id":1802} in x.tags, axis = 1)]
df = df.drop(lost_duels.index)

out_of_ball = df.loc[df["subEventName"] == "Ball out of the field"]
df = df.drop(out_of_ball.index)

goalies = df.loc[df["subEventName"].isin(["Goalkeeper leaving line", "Save attempt", "Reflexes"])]
df = df.drop(goalies.index)

def isolateChains(df):
    df["nextTeamId"] = df.shift(-1, fill_value=0)["teamId"]
    chain_team = df.iloc[0]["teamId"]
    period = df.iloc[0]["matchPeriod"]
    stop_criterion = 0
    chain = 0
    df["possession_chain"] = 0
    df["possession_chain_team"] = 0

    for i, row in df.iterrows():
        df.at[i, "possession_chain"] = chain
        df.at[i, "possession_chain_team"] = chain_team
        if row["eventName"] == "Pass" or row["eventName"] == "Duel":
            if row["teamId"] == chain_team and {"id": 1802} in row["tags"]:
                    stop_criterion += 1
            if row["teamId"] != chain_team and {"id": 1801} in row["tags"]:
                    stop_criterion += 1
        if row["eventName"] == "Others on the ball":
               if row["teamId"] == row["nextTeamId"]:
                   stop_criterion += 2
        if row["eventName"] in ["Shot", "Foul", "Offside"]:
                stop_criterion += 2
        if row["kickedOut"] == 1:
                stop_criterion += 2
        if row["matchPeriod"] != period:
                chain += 1
                stop_criterion = 0
                chain_team = row["teamId"]
                period = row["matchPeriod"]
                df.at[i, "possession_chain"] = chain
                df.at[i, "possession_chain_team"] = chain_team
        if stop_criterion >= 2:
            chain += 1
            stop_criterion = 0
            chain_team = row["nextTeamId"]
    return df

df = isolateChains(df)

def prepareChains(df):
    df["Shot"] = 0
    no_chains = max(df["possession_chain"].unique())
    indicies = []
    for i in range(no_chains+1):
        possession_chain_df = df.loc[df["possession_chain"] == i]
        if len(possession_chain_df) > 0:
            if possession_chain_df.iloc[-1]["eventName"] == "Shot":
                df.loc[df["possession_chain"] == i, "Shot"] = 1
                k = i-1
                if k > 0:
                    try:
                        prev = df.loc[df["possession_chain"] == k]
                        while prev.iloc[-1]["eventName"] == "Foul":
                            df.loc[df["possession_chain"] == k, "Shot"] = 1
                            k = k-1
                            prev = df.loc[df["possession_chain"] == k]
                    except:
                        k = k-1
            team_indicies = possession_chain_df.loc[possession_chain_df["teamId"] == possession_chain_df.teamId.mode().iloc[0]].index.values.tolist()
            indicies.extend(team_indicies)

    df = df.loc[indicies]
    return df

df = prepareChains(df)


df = df.loc[df.apply(lambda x: len(x.positions) == 2, axis = 1)]
df["x0"] = df.positions.apply(lambda cell: (cell[0]["x"]) * 105/100)
df["y0"] = df.positions.apply(lambda cell: abs(50 - cell[0]["y"]) * 68/100)
df["x1"] = df.positions.apply(lambda cell: (cell[1]["x"]) * 105/100)
df["y1"] = df.positions.apply(lambda cell: abs(50 - cell[1]["y"]) * 68/100)
df.loc[df["eventName"] == "Shot", "x1"] = 105
df.loc[df["eventName"] == "Shot", "y1"] = 0

df["Goal"] = df.apply(
    lambda row: 1 if row["eventName"] == "Shot" and 
                ({'id': 101} in row["tags"] or {"id": 102} in row["tags"]) 
                else 0, axis=1
)

goal_possession_chains = df.loc[df["Goal"] == 1, "possession_chain"].unique()
df.loc[df["possession_chain"].isin(goal_possession_chains), "Goal"] = 1

chains_to_remove = df[df["eventName"].isin(["Offside", "Free Kick"])]["possession_chain"].unique()

df = df[~df["possession_chain"].isin(chains_to_remove)]

df["possession_chain_count"] = df.groupby("possession_chain")["possession_chain"].transform("count")

df["possession_chain_count"] = np.where(df["possession_chain"].notnull(), df["possession_chain_count"], np.nan)

df = df[df["possession_chain_count"] >= 3]

path = "WyscoutData/Minutes_Played/minutes_played_per_game_France.json"
with open(path) as f:
    data = json.load(f)

df_players1 = pd.DataFrame(data)

path = "WyscoutData/Minutes_Played/minutes_played_per_game_Germany.json"
with open(path) as f:
    data = json.load(f)

df_players2 = pd.DataFrame(data)

path = "WyscoutData/Minutes_Played/minutes_played_per_game_Italy.json"
with open(path) as f:
    data = json.load(f)

df_players3 = pd.DataFrame(data)

path = "WyscoutData/Minutes_Played/minutes_played_per_game_Spain.json"
with open(path) as f:
    data = json.load(f)

df_players4 = pd.DataFrame(data)

df_players = pd.concat([df_players1, df_players2, df_players3, df_players4], axis=0, ignore_index=True)
df_players = df_players.reset_index()

df_recoveries = df.drop_duplicates(subset="possession_chain", keep="first")

df_minutes = df_players.copy()
df_players = df_players.drop_duplicates(subset="playerId")
df_players["shortName"] = df_players["shortName"].map(lambda x: x.encode("utf-8").decode("unicode_escape"))

df_recoveries = df_recoveries.merge(df_players[["playerId", "shortName"]], left_on="playerId", right_on="playerId", how="left")
df_recoveries.drop(columns="playerId", inplace=True)

player_shots = df_recoveries.groupby("shortName")["Shot"].sum().reset_index()
player_shots = player_shots.sort_values(by="Shot", ascending=False).reset_index(drop=True)

player_goals = df_recoveries.groupby("shortName")["Goal"].sum().reset_index()
player_goals = player_goals.sort_values(by='Goal', ascending=False).reset_index(drop=True)

player_minutes = df_minutes.groupby("shortName", as_index=False)["minutesPlayed"].sum()
player_minutes.columns = ["shortName", "total_minutes_played"]
player_minutes = player_minutes[player_minutes["total_minutes_played"] >= 900]

normalized_shots = player_shots.merge(player_minutes, on="shortName")
normalized_shots["shots_per_90"] = normalized_shots["Shot"] / (normalized_shots["total_minutes_played"] /90)
sorted_shots = normalized_shots.sort_values(by=["shots_per_90"], ascending=False)

normalized_goals = player_goals.merge(player_minutes, on="shortName")
normalized_goals["goals_per_90"] = normalized_goals["Goal"] / normalized_goals["total_minutes_played"] *90
sorted_goals = normalized_goals.sort_values(by=["goals_per_90"], ascending=False)

sorted_shots.to_json("sorted_shots.json", orient="records", indent=4)
sorted_goals.to_json("sorted_goals.json", orient="records", indent=4)