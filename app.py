import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')

df_summer = preprocessor.preprocess(df,region)
df_winter = preprocessor.process(df,region)

st.sidebar.title("Olympics Data Analysis")
st.sidebar.image("OL.jpg")

# Create a selectbox for choosing between Summer and Winter Olympics
selected_season = st.sidebar.selectbox("Select Olympics Season", ("Summer Olympics", "Winter Olympics"))

# Define options for both Summer and Winter Olympics
summer_options = ('Medal Tally', 'Top Athletes by Medals', 'Top Athletes by country', 'Top Athletes by Games', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')
winter_options = ('Medal Tally', 'Top Athletes by Medals', 'Top Athletes by country', 'Top Athletes by Games', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')

# Display options based on the selected season
if selected_season == "Summer Olympics":
    user_menu = st.sidebar.radio('Select an option', summer_options, key="summer_radio")

    if user_menu == 'Medal Tally':
        st.title('Summer Medal Tally')
        year, country = helper.country_year_list(df_summer)

        selected_year = st.selectbox("Select Year", year)
        selected_country = st.selectbox("Select Country", country)

        medal_tally = helper.fetch_medal_tally(df_summer, selected_year, selected_country)

        if selected_year == 'Overall' and selected_country == 'Overall':
            st.title('Overall Tally')
        if selected_year != 'Overall' and selected_country == 'Overall':
            st.title('Medal Tally in ' + str(selected_year) + " Olympics")
        if selected_year == 'Overall' and selected_country != 'Overall':
            st.title(selected_country + ' Overall Performance')
        if selected_year != 'Overall' and selected_country != 'Overall':
            st.title(selected_country + " performance in " + str(selected_year) + ' Olympics')

        st.table(medal_tally)

    elif user_menu == 'Top Athletes by Medals':
        new_df, player_list, summer_top_athletes = helper.player_details(df_summer)

        selected_player = st.selectbox("Select a Player", player_list)
        if selected_player == 'Overall':
            st.title("Top Athletes by Medals")
            st.write(summer_top_athletes)
        else:
            selected_player_data = summer_top_athletes[summer_top_athletes['Name'] == selected_player]
            st.title("Medals won by " + selected_player)
            st.write(selected_player_data)


    elif user_menu == 'Top Athletes by country':
        country_list = df_summer['region'].dropna().unique().tolist()
        country_list.sort()
        st.title("Top Athletes by country")
        selected_country = st.selectbox("Select a Country", country_list)
        st.title("Top Athletes of " + selected_country)
        top15_df = helper.most_successful_countrywise(df_summer, selected_country)
        st.table(top15_df)


    elif user_menu == 'Top Athletes by Games':
        sport_list = df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        st.title("Top Athletes by Games")
        selected_sport = st.selectbox("Select a Sport", sport_list)
        st.title("Most Successful " + selected_sport + " Player" )
        athlete_medal_counts = helper.most_successful(df_summer, selected_sport)
        st.table(athlete_medal_counts)


    elif user_menu == 'Overall Analysis':
        editions = df_summer['Year'].unique().shape[0] - 1
        cities = df_summer['City'].unique().shape[0]
        athletes = df_summer['Name'].unique().shape[0]
        region = df_summer['region'].unique().shape[0]
        sport = df_summer['Sport'].unique().shape[0]
        event = df_summer['Event'].unique().shape[0]

        st.title("1. Top stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Host")
            st.title(cities)
        with col3:
            st.header("Athletes")
            st.title(athletes)
            # col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Nations")
            st.title(region)
        with col2:
            st.header("Sport")
            st.title(sport)
        with col3:
            st.header("Event")
            st.title(event)

        nations_over_time = helper.data_over_time(df_summer, 'region')
        st.title("2. Participating nations over time")
        fig = px.line(nations_over_time, x="Year", y="region", title='Participating nations over time')
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df_summer, 'Event')
        st.title("3. Events over time")
        fig = px.line(events_over_time, x="Year", y="Event", title='Events over time')
        st.plotly_chart(fig)

        athletes_over_time = helper.data_over_time(df_summer, 'Name')
        st.title("4. Participating Athletes over time")
        fig = px.line(athletes_over_time, x="Year", y="Name", title='Participating Athletes over time')
        st.plotly_chart(fig)

        sports_over_time = helper.data_over_time(df_summer, 'Sport')
        st.title("5. Participating Sports over time")
        fig = px.line(sports_over_time, x="Year", y="Sport", title='Participating Sports over time')
        st.plotly_chart(fig)

        st.title("6. Events over Year")
        fig, ax = plt.subplots(figsize=(25, 20))
        heatmap_data = df_summer.drop_duplicates(['Sport', 'Year', 'Event'])
        ax = sns.heatmap(heatmap_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True, cmap='viridis', cbar=True)
        st.pyplot(fig)

        st.title("7. Most Successful Player")
        sport_list = df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox("Select a Sport", sport_list)
        athlete_medal_counts = helper.most_successful(df_summer, selected_sport)
        st.table(athlete_medal_counts)

    elif user_menu == 'Country wise Analysis':
        st.title("Country wise Analysis")
        country_list = df_summer['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.selectbox("Select a Country", country_list)
        country_df = helper.yearwise_medal_tally(df_summer, selected_country)
        fig = px.line(country_df, x="Year", y="Medal", title='Medals won by ' + selected_country + ' over years')
        st.title("1." + selected_country + " medal tally over years")
        st.plotly_chart(fig)

        st.title("2." + selected_country + " data in following sports")
        pt = helper.country_event_heatmap(df_summer, selected_country)
        if pt.empty:
            st.write("No data available for " + selected_country)
        else:
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True, cmap='viridis', cbar=True)
            st.pyplot(fig)

        st.title("3. Top Athletes of " + selected_country)
        top15_df = helper.most_successful_countrywise(df_summer, selected_country)
        st.table(top15_df)

    elif user_menu == 'Athlete wise Analysis':
        st.title("1. Distribution of Age w.r.t Medals")
        athlete_df = df_summer.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
        fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                         'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
                         'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                         'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling',
                         'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
                         'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                         'Rhythmic Gymnastics', 'Rugby Sevens',
                         'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

        # Collect age data for gold medalists in each sport
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        st.title("2. Distribution of Age w.r.t Sports")
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)

        sport_list = df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        st.title('3. Height vs Weight')
        selected_sport = st.selectbox("Select a Sport", sport_list)
        temp_df = helper.weight_verses_height(df_summer, selected_sport)
        fig, ax = plt.subplots()
        # Assuming 'temp_df' is your DataFrame
        ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=50)
        st.pyplot(fig)

        st.title("4. Men vs Women")
        final = helper.men_vs_women(df_summer)
        fig = px.line(final, x='Year', y=["Male", "Female"], color_discrete_map={"Male": "red", "Female": "green"})
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)

else:
    user_menu = st.sidebar.radio('Select an option', winter_options, key="winter_radio")

    if user_menu == 'Medal Tally':
        st.title('Winter Medal Tally')
        year, country = helper.country_year_list(df_winter)

        selected_year = st.selectbox("Select Year", year)
        selected_country = st.selectbox("Select Country", country)

        medal_tally = helper.fetch_medal_tally(df_winter, selected_year, selected_country)

        if selected_year == 'Overall' and selected_country == 'Overall':
            st.title('Overall Tally')
        if selected_year != 'Overall' and selected_country == 'Overall':
            st.title('Medal Tally in ' + str(selected_year) + " Olympics")
        if selected_year == 'Overall' and selected_country != 'Overall':
            st.title(selected_country + ' Overall Performance')
        if selected_year != 'Overall' and selected_country != 'Overall':
            st.title(selected_country + " performance in " + str(selected_year) + ' Olympics')

        st.table(medal_tally)


    elif user_menu == 'Top Athletes by Medals':
        new_df, player_list, winter_top_athletes = helper.winter_player_details(df_winter)

        selected_player = st.selectbox("Select a Player", player_list)
        if selected_player == 'Overall':
            st.title("Top Athletes by Medals")
            st.write(winter_top_athletes)
        else:
            selected_player_data = winter_top_athletes[winter_top_athletes['Name'] == selected_player]
            st.title("Medals won by " + selected_player)
            st.write(selected_player_data)


    elif user_menu == 'Top Athletes by country':
        country_list = df_winter['region'].dropna().unique().tolist()
        country_list.sort()
        st.title("Top Athletes by country")
        selected_country = st.selectbox("Select a Country", country_list)
        st.title("Top Athletes of " + selected_country)
        top15_df = helper.most_successful_countrywise(df_winter, selected_country)
        st.table(top15_df)


    elif user_menu == 'Top Athletes by Games':
        sport_list = df_winter['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        st.title("Top Athletes by Games")
        selected_sport = st.selectbox("Select a Sport", sport_list)
        st.title("Most Successful " + selected_sport + " Player" )
        athlete_medal_counts = helper.most_successful(df_winter, selected_sport)
        st.table(athlete_medal_counts)


    elif user_menu == 'Overall Analysis':
        editions = df_winter['Year'].unique().shape[0]
        cities = df_winter['City'].unique().shape[0]
        athletes = df_winter['Name'].unique().shape[0]
        region = df_winter['region'].unique().shape[0]
        sport = df_winter['Sport'].unique().shape[0]
        event = df_winter['Event'].unique().shape[0]

        st.title("1. Top stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Host")
            st.title(cities)
        with col3:
            st.header("Athletes")
            st.title(athletes)
            # col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Nations")
            st.title(region)
        with col2:
            st.header("Sport")
            st.title(sport)
        with col3:
            st.header("Event")
            st.title(event)

        nations_over_time = helper.data_over_time(df_winter, 'region')
        st.title("2. Participating nations over time")
        fig = px.line(nations_over_time, x="Year", y="region", title='Participating nations over time')
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df_winter, 'Event')
        st.title("3. Events over time")
        fig = px.line(events_over_time, x="Year", y="Event", title='Events over time')
        st.plotly_chart(fig)

        athletes_over_time = helper.data_over_time(df_winter, 'Name')
        st.title("4. Participating Athletes over time")
        fig = px.line(athletes_over_time, x="Year", y="Name", title='Participating Athletes over time')
        st.plotly_chart(fig)

        sports_over_time = helper.data_over_time(df_winter, 'Sport')
        st.title("5. Participating Sports over time")
        fig = px.line(sports_over_time, x="Year", y="Sport", title='Participating Sports over time')
        st.plotly_chart(fig)

        st.title("6. Events over Year")
        fig, ax = plt.subplots(figsize=(25, 20))
        heatmap_data = df_winter.drop_duplicates(['Sport', 'Year', 'Event'])
        ax = sns.heatmap(heatmap_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True, cmap='viridis', cbar=True)
        st.pyplot(fig)

        st.title("7. Most Successful Player")
        sport_list = df_winter['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox("Select a Sport", sport_list)
        athlete_medal_counts = helper.most_successful(df_winter, selected_sport)
        st.table(athlete_medal_counts)

    elif user_menu == 'Country wise Analysis':
        st.title("Country wise Analysis")
        country_list = df_winter['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.selectbox("Select a Country", country_list)
        country_df = helper.yearwise_medal_tally(df_winter, selected_country)
        fig = px.line(country_df, x="Year", y="Medal", title='Medals won by ' + selected_country + ' over years')
        st.title("1." + selected_country + " medal tally over years")
        st.plotly_chart(fig)

        st.title("2." + selected_country + " data in following sports")
        pt = helper.country_event_heatmap(df_winter, selected_country)
        if pt.empty:
            st.write("No data available for " + selected_country)
        else:
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True, cmap='viridis', cbar=True)
            st.pyplot(fig)

        st.title("3. Top 15 Athletes of " + selected_country)
        top15_df = helper.most_successful_countrywise(df_winter, selected_country)
        st.table(top15_df)

    elif user_menu == 'Athlete wise Analysis':
        st.title("1. Distribution of Age w.r.t Medals")
        athlete_df = df_winter.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
        fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = ['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
                         'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
                         'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
                         'Snowboarding', 'Short Track Speed Skating', 'Skeleton',
                         'Military Ski Patrol', 'Alpinism']

        # Collect age data for gold medalists in each sport
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        st.title("2. Distribution of Age w.r.t Sports")
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)

        sport_list = df_winter['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        st.title('3. Height vs Weight')
        selected_sport = st.selectbox("Select a Sport", sport_list)
        temp_df = helper.weight_verses_height(df_winter, selected_sport)
        fig, ax = plt.subplots()
        # Assuming 'temp_df' is your DataFrame
        ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=50)
        st.pyplot(fig)

        st.title("4. Men vs Women")
        final = helper.men_vs_women(df_winter)
        fig = px.line(final, x='Year', y=["Male", "Female"], color_discrete_map={"Male": "red", "Female": "green"})
        fig.update_layout(autosize=False, width=800, height=500)
        st.plotly_chart(fig)











