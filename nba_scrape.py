# -*- coding: utf-8 -*-
"""
Created on Sat May 25 16:08:38 2019

@author: Brendan Non-Admin

People are unhappy about Klay Thompson not being on all NBA team so wanted to
see how he compared to other guards

"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import seaborn as sns
sns.set(style='whitegrid')

url = 'http://www.espn.com/nba/seasonleaders'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
cols_tr = (soup.find('table', class_='tablehead')
           .find('tr', class_='colhead'))
cols = [td.text for td in cols_tr.find_all('td')]

rows = list()
for tr in soup.find('table', class_='tablehead').find_all('tr')[2:]:
    if tr.find('td').text != 'RK':
        row = defaultdict()
        for i, td in enumerate(tr.find_all('td')):
            row[cols[i]] = td.text
        rows.append(row)

df = (pd.DataFrame(rows)
      .rename(columns=str.lower)
      .assign(position=lambda x: (x.player.str.split(',', expand=True)[1]
                                  .str.strip()),
              player=lambda x: x.player.str.split(',', expand=True)[0],
              pts=lambda x: x.pts.astype('float64')))

palette = sns.color_palette("Blues_d")
ax = (df.loc[df.position.isin(['SG', 'PG']), ['player', 'pts']]
      .nlargest(15, 'pts')
      .pipe((sns.barplot, 'data'), x='pts', y='player', palette=palette))
ax.set(xlabel='Points Per Game', ylabel='', title='NBA Guards 2018-2019 PPG')

url = 'https://www.nba.com/history/awards/all-nba-team'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


def team_soup(soup, team_str):
    return soup.find('strong', string=team_str).parent.parent.next_sibling


all_nba = list()

team_soup_html = team_soup(soup, 'FIRST TEAM')
for i, player in enumerate(team_soup_html.stripped_strings):
    if i % 2 == 1:
        player_dict = dict()
        player_dict['player'] = player.split(', ')[0]
        player_dict['all_nba_team'] = 'first'
        all_nba.append(player_dict)

team_soup_html = team_soup(soup, 'SECOND TEAM')
for i, player in enumerate(team_soup_html.stripped_strings):
    if i % 2 == 1:
        player_dict = dict()
        player_dict['player'] = player.split(', ')[0]
        player_dict['all_nba_team'] = 'second'
        all_nba.append(player_dict)
        
team_soup_html = team_soup(soup, 'THIRD TEAM')
for i, player in enumerate(team_soup_html.stripped_strings):
    if i % 2 == 1:
        player_dict = dict()
        player_dict['player'] = player.split(', ')[0]
        player_dict['all_nba_team'] = 'third'
        all_nba.append(player_dict)
        

df_all_nba = (pd.DataFrame(all_nba)
              .query('player != "Official release & voting totals"'))

df = (pd.merge(df, df_all_nba, how='outer', on='player')
      .assign(all_nba_team=lambda x: x.all_nba_team.fillna('N/A')))

ax = (df.loc[df.position.isin(['SG', 'PG']), ['player', 'pts', 'all_nba_team']]
      .nlargest(15, 'pts')
      .pipe((sns.barplot, 'data'), x='pts', y='player', hue='all_nba_team'))
ax.set(xlabel='Points Per Game', ylabel='', title='NBA Guards 2018-2019 PPG')