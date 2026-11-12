import os
import pandas as pd

odi='data/ODI'
t20='data/T20I'
test='data/Test'
f1=os.listdir(odi)
f2=os.listdir(t20)
f3=os.listdir(test)
odi_match=[]
t20_match=[]
test_match=[]

for i in f1:
    if i.endswith('.csv') and not i.endswith('_info.csv'):
        odi_match.append(i)

for j in f2:
    if j.endswith('.csv') and not j.endswith('_info.csv'):
        t20_match.append(j)

for k in f3:
    if k.endswith('.csv') and not k.endswith('_info.csv'):
        test_match.append(k)

all_odi=[]
for p in range(len(odi_match)):
    path1=os.path.join(odi,odi_match[p])
    all_odi.append(pd.read_csv(path1))
df_odi=pd.concat(all_odi,ignore_index=True)

all_t20=[]
for q in range(len(t20_match)):
    path2=os.path.join(t20,t20_match[q])
    all_t20.append(pd.read_csv(path2))
df_t20=pd.concat(all_t20,ignore_index=True)

all_test=[]
for r in range(len(test_match)):
    path3=os.path.join(test,test_match[r])
    all_test.append(pd.read_csv(path3))
df_test=pd.concat(all_test,ignore_index=True)

class Batter_Stats:
    def __init__(self,df,name):
        self.df=df
        self.name=name

    def total_innings(self):
        data=self.df[self.df['striker']==self.name]
        t_in=data[['match_id','innings']].drop_duplicates().shape[0]
        return t_in

    def total_runs(self):
        total=0
        data=self.df[self.df['striker']==self.name]
        for run in data['runs_off_bat']:
            total+=run
        return total

    def average(self):
        try:
            runs=self.total_runs()
            dismissals=self.df[self.df['player_dismissed']==self.name].shape[0]
            avg=runs/dismissals
            return round(avg,2)
        except ZeroDivisionError:
            return runs

    def strike_rate(self):
        data=self.df[self.df['striker']==self.name]
        runs=self.total_runs()
        wides=data[data['wides']>0].shape[0]
        balls_faced=data.shape[0]-wides
        str_rate=(runs/balls_faced)*100
        return round(str_rate,2)

    def fours(self):
        data=self.df[self.df['striker']==self.name]
        total_fours=data[data['runs_off_bat']==4].shape[0]
        return total_fours

    def sixes(self):
        data=self.df[self.df['striker']==self.name]
        total_sixes=data[data['runs_off_bat']==6].shape[0]
        return total_sixes

    def highscore(self):
        data=self.df[self.df['striker']==self.name]
        match=data.groupby(['match_id','innings'])
        runs_per_inning=match['runs_off_bat'].sum()
        highest=runs_per_inning.max()
        return highest

    def half_centuries(self):
        data=self.df[self.df['striker']==self.name]
        match=data.groupby(['match_id','innings'])
        runs_per_inning=match['runs_off_bat'].sum()
        fifties=runs_per_inning[(runs_per_inning>=50)&(runs_per_inning<100)].shape[0]
        return fifties

    def centuries(self):
        data=self.df[self.df['striker']==self.name]
        match=data.groupby(['match_id','innings'])
        runs_per_inning=match['runs_off_bat'].sum()
        hundreds=runs_per_inning[runs_per_inning>=100].shape[0]
        return hundreds


class Bowler_Stats:
    def __init__(self,df,name):
        self.df=df
        self.name=name

    def total_innings(self):
        data=self.df[self.df['bowler']==self.name]
        t_in=data[['match_id','innings']].drop_duplicates().shape[0]
        return t_in

    def total_wickets(self):
        data=self.df[self.df['bowler']==self.name]
        all_wic=data['player_dismissed'].count()
        run_out=data[data['wicket_type']=='run out'].shape[0]
        bowler_wickets=all_wic-run_out
        return bowler_wickets

    def three_wicket_hauls(self):
        data=self.df[self.df['bowler']==self.name]
        data=data[data['wicket_type']!='run out']
        match_w=data.groupby(['match_id','innings'])
        wickets=match_w['player_dismissed'].count()
        three_wic=wickets[(wickets>=3)&(wickets<5)]
        return three_wic.shape[0]

    def five_wicket_hauls(self):
        data=self.df[self.df['bowler']==self.name]
        data=data[data['wicket_type']!='run out']
        match_w=data.groupby(['match_id','innings'])
        wickets=match_w['player_dismissed'].count()
        five_wic=wickets[(wickets>=5)]
        return five_wic.shape[0]

    def total_dot_balls(self):
        data=self.df[self.df['bowler']==self.name]
        dot_balls=data[(data['runs_off_bat']==0)&(data['wides'].fillna(0)==0)&(data['noballs'].fillna(0)==0)].shape[0]
        return dot_balls

    def runs_conceded(self):
        data = self.df[self.df['bowler'] == self.name]
        runs = data['runs_off_bat'].sum()
        wides = data['wides'].fillna(0).sum()
        noballs = data['noballs'].fillna(0).sum()
        return runs + wides + noballs

    def legal_balls(self):
        data = self.df[self.df['bowler'] == self.name]
        wides = data['wides'].fillna(0)
        noballs = data['noballs'].fillna(0)
        balls = data[(wides == 0) & (noballs == 0)].shape[0]
        return balls

    def economy(self):
        balls = self.legal_balls()
        if balls == 0:
            return 0
        return round((self.runs_conceded() * 6) / balls,2)

    def average(self):
        wickets = self.total_wickets()
        if wickets == 0:
            return 0
        return round(self.runs_conceded() / wickets,2)

    def strike_rate(self):
        wickets = self.total_wickets()
        if wickets == 0:
            return 0
        return round(self.legal_balls() / wickets,2)

while True:
    player_name=input('Enter name of the player: ')
    player_format=input('Enter format ODI/T20/Test: ')
    player_role=input('Enter role of player Batter/Bowler: ')
    if player_format.lower()=='odi':
        df=df_odi
    elif player_format.lower()=='t20':
        df=df_t20
    elif player_format.lower()=='test':
        df=df_test
    else:
        print('Invalid Format')
        df=None

    if df is not None:
        if player_role.lower()=='batter':
            player=Batter_Stats(df,player_name)
            if player.total_innings()==0:
                print('Player has not played in this format')
            else:
                print("Innings:", player.total_innings())
                print("Runs:", player.total_runs())
                print("Average:", player.average())
                print("Strike Rate:", player.strike_rate())
                print("Fours:", player.fours())
                print("Sixes:", player.sixes())
                print("Highest Score:", player.highscore())
                print("50s:", player.half_centuries())
                print("100s:", player.centuries())

        elif player_role.lower()=='bowler':
            player=Bowler_Stats(df,player_name)
            if (player.total_innings()==0):
                print('Player has not played in this format')
            else:
                print("Innings:", player.total_innings())
                print("Wickets:", player.total_wickets())
                print("Average:", player.average())
                print("Strike Rate:", player.strike_rate())
                print("Economy:", player.economy())
                print("3 Wicket Hauls:", player.three_wicket_hauls())
                print("5 Wicket Hauls:", player.five_wicket_hauls())
                print("Dot Balls:", player.total_dot_balls())

        else:
            print('Invalid Role')

        choice=input('Search more players Yes/No?')
        if choice.lower()=='no':
            break
