import numpy as np

def fetch_medal_tally(df_summer, year, country):
    medal_df = df_summer.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x

def medal_tally(df_summer):
    medal_tally = df_summer.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df_summer):
    year = np.unique(df_summer['Year'].dropna().values).tolist()
    year.sort()
    year.insert(0, 'Overall')
    # Convert each element in the list to an integer, keeping 'Overall' as a string
    year = [int(y) if y != 'Overall' else y for y in year]

    country = np.unique(df_summer['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year,country

def data_over_time(df_summer,col):
    # participating nations over time
    nations_over_time = df_summer.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count': col}, inplace=True)

    return nations_over_time

def most_successful(df_summer, sport):
    temp_df = df_summer.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    # Group by athlete name and count the number of medals & Sort the athletes by the number of medals in descending order
    athlete_medal_counts = temp_df.groupby('Name')['Medal'].count().reset_index().sort_values(by='Medal',ascending=False).head(30)
    # Merge based on 'Name' and take required columns 'Name','Medal_x','Sport','region' & then drop duplicates based on 'Name' columns
    athlete_medal_counts = athlete_medal_counts.merge(df_summer, on='Name', how='left')[['Name', 'Medal_x', 'Sport', 'region']].drop_duplicates('Name')
    # Rename columns 'Medal_x' to 'Medals'
    athlete_medal_counts.rename(columns={'Medal_x': 'Medals'}, inplace=True)

    return athlete_medal_counts

def yearwise_medal_tally(df_summer,country):
    temp_df = df_summer.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    country_df = new_df.groupby('Year')['Medal'].count().reset_index()

    return country_df

def country_event_heatmap(df_summer,country):
    temp_df = df_summer.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    new_df = new_df.groupby('Year')['Medal'].count().reset_index()

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')

    return pt

def most_successful_countrywise(df_summer, country):
    temp_df = df_summer.dropna(subset=['Medal'])
    # if sport != 'Overall':
    temp_df = temp_df[temp_df['region'] == country]
    # Group by athlete name and count the number of medals & Sort the athletes by the number of medals in descending order
    athlete_medal_counts = temp_df.groupby('Name')['Medal'].count().reset_index().sort_values(by='Medal',ascending=False).head(20)
    # Merge based on 'Name' and take required columns 'Name','Medal_x','Sport','region' & then drop duplicates based on 'Name' columns
    athlete_medal_counts = athlete_medal_counts.merge(df_summer, on='Name', how='left')[['Name', 'Medal_x', 'Sport']].drop_duplicates('Name')
    # Rename columns 'Medal_x' to 'Medals'
    athlete_medal_counts.rename(columns={'Medal_x': 'Medals'}, inplace=True)

    return athlete_medal_counts

def weight_verses_height(df_summer, sport):
    athlete_df = df_summer.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df_summer):
    athlete_df = df_summer.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

def player_details(df_summer):
    summer_top_athletes = df_summer.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    summer_top_athletes['Total'] = summer_top_athletes['Gold'] + summer_top_athletes['Silver'] + summer_top_athletes['Bronze']
    summer_top_athletes = summer_top_athletes[['Name', 'Gold', 'Silver', 'Bronze', 'Total']].sort_values('Total',ascending=False).reset_index()
    summer_top_athletes.drop('index', axis=1, inplace=True)
    new_df = summer_top_athletes[['Name']]
    player_list = new_df['Name'].head(500).tolist()

    player_list.insert(0, 'Overall')

    summer_top_athletes = summer_top_athletes.merge(df_summer[['Name','Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return new_df, player_list, summer_top_athletes



               ###  WINTER OLYMPICS  ###

def fetch_medal_tally(df_winter, year, country):
    medal_df = df_winter.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x

def medal_tally(df_winter):
    medal_tally = df_winter.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df_winter):
    year = np.unique(df_winter['Year'].dropna().values).tolist()
    year.sort()
    year.insert(0, 'Overall')
    # Convert each element in the list to an integer, keeping 'Overall' as a string
    year = [int(y) if y != 'Overall' else y for y in year]

    country = np.unique(df_winter['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year, country

def data_over_time(df_winter,col):
    # participating nations over time
    nations_over_time = df_winter.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count': col}, inplace=True)

    return nations_over_time

def most_successful(df_winter, sport):
    temp_df = df_winter.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    # Group by athlete name and count the number of medals & Sort the athletes by the number of medals in descending order
    athlete_medal_counts = temp_df.groupby('Name')['Medal'].count().reset_index().sort_values(by='Medal',ascending=False).head(25)
    # Merge based on 'Name' and take required columns 'Name','Medal_x','Sport','region' & then drop duplicates based on 'Name' columns
    athlete_medal_counts = athlete_medal_counts.merge(df_winter, on='Name', how='left')[['Name', 'Medal_x', 'Sport', 'region']].drop_duplicates('Name')
    # Rename columns 'Medal_x' to 'Medals'
    athlete_medal_counts.rename(columns={'Medal_x': 'Medals'}, inplace=True)

    return athlete_medal_counts

def yearwise_medal_tally(df_winter,country):
    temp_df = df_winter.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    country_df = new_df.groupby('Year')['Medal'].count().reset_index()

    return country_df

def country_event_heatmap(df_winter,country):
    temp_df = df_winter.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    z = new_df.groupby('Year')['Medal'].count().reset_index()

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')

    return pt

def most_successful_countrywise(df_winter, country):
    temp_df = df_winter.dropna(subset=['Medal'])
    # if sport != 'Overall':
    temp_df = temp_df[temp_df['region'] == country]
    # Group by athlete name and count the number of medals & Sort the athletes by the number of medals in descending order
    athlete_medal_counts = temp_df.groupby('Name')['Medal'].count().reset_index().sort_values(by='Medal',ascending=False).head(20)
    # Merge based on 'Name' and take required columns 'Name','Medal_x','Sport','region' & then drop duplicates based on 'Name' columns
    athlete_medal_counts = athlete_medal_counts.merge(df_winter, on='Name', how='left')[['Name', 'Medal_x', 'Sport']].drop_duplicates('Name')
    # Rename columns 'Medal_x' to 'Medals'
    athlete_medal_counts.rename(columns={'Medal_x': 'Medals'}, inplace=True)

    return athlete_medal_counts

def weight_verses_height(df_winter, sport):
    athlete_df = df_winter.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df_winter):
    athlete_df = df_winter.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

def winter_player_details(df_winter):
    winter_top_athletes = df_winter.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    winter_top_athletes['Total'] = winter_top_athletes['Gold'] + winter_top_athletes['Silver'] + winter_top_athletes['Bronze']
    winter_top_athletes = winter_top_athletes[['Name', 'Gold', 'Silver', 'Bronze', 'Total']].sort_values('Total',ascending=False).reset_index()
    winter_top_athletes.drop('index', axis=1, inplace=True)
    new_df = winter_top_athletes[['Name']]
    player_list = new_df['Name'].head(500).tolist()

    player_list.insert(0, 'Overall')

    winter_top_athletes = winter_top_athletes.merge(df_winter[['Name','Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return new_df, player_list, winter_top_athletes




