import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

with st.echo(code_location='below'):
    st.title('Olympic Summer & Winter Games')
    @st.cache
    def get_data(url):
        return pd.read_csv(url)

    df_hosts = get_data("https://storage.googleapis.com/kagglesdsdata/datasets/1475786/3445521/olympic_hosts.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20220513%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220513T122640Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=194187a247a82164f810140af75a07ccdb23963984a0fc605945d6a54d237929d76b121454243e6e435e3ecd1ae9fae01c42297c0ccb12cef733ef18d5778626c0f9e8f3d71a4c54e167f83c0a027128d5a5334c8f0b87cc041cf6cb0bb817319d92f7af10c7a4474f4eb21fe98dccfc69739e17e92a3caa2242419034c8ba040290c43a70928bb0bb4a61bdd697006aaeb1da207ce44e1c06d3c6a43c6949059d3e9336739c2abfb893c93c2313e975e08ac795b688813f0ee5d9dbac8db8740c7002568bab63172b12ae339cd62c48fff52a6eaa076cf1d44b13acb72fe6d3fd2eea17487aa2210e39b1ff19ee553f7bbb2b469ef30d804c1ca7b4a423b484")
    df_medals = get_data("https://github.com/vbatina/first/raw/main/olympic_medals.csv")
    df_athletes = get_data("https://github.com/vbatina/first/raw/main/olympic_athletes.csv")
    df_more = get_data("https://query.data.world/s/cvsvl2742mgzlkolbxfjnwtkjntkaw")

    df_hosts["city"] = df_hosts["game_name"].str[0:-5]
    iso = pd.DataFrame({"Nation": df_more["Nation"], "Code": df_more["Code"]})
    df_hosts_iso = df_hosts.merge(iso, left_on='game_location', right_on='Nation', how='left')
    df_hosts_iso.iloc[2, 9] = "KOR"
    df_hosts_iso.iloc[4, 9] = "RUS"
    df_hosts_iso.iloc[17, 9] = "KOR"
    df_hosts_iso.iloc[21, 9] = "RUS"
    df_hosts_iso.iloc[25, 9] = "DEU"
    df_hosts_iso.iloc[33, 9] = "AUS"

    fig = px.scatter_geo(df_hosts_iso, locations="Code", color="game_season",
                         hover_name="game_name",
                         animation_frame="game_year",
                         projection="natural earth")
    st.plotly_chart(fig)

    nations_medals_s = pd.DataFrame({"Nation": df_more["Nation"], "Medal.1": df_more["Medal.1"]}).sort_values(
        "Medal.1",
        ascending=False).set_index(
        "Nation")
    nations_medals_s.loc['Other countries', :] = nations_medals_s.iloc[40:].sum(axis=0)
    other_contries = nations_medals_s.iloc[226]
    nations_medals_s.drop(nations_medals_s.tail(198).index, inplace=True)
    nations_summer = nations_medals_s.append(other_contries).reset_index()

    fig = px.pie(nations_summer, values='Medal.1', names='Nation', title='Total Number of Medals Won on Olympic Games')
    st.plotly_chart(fig)

    season = st.radio(
        "Выберите сезон",
        ('Summer', 'Winter'))

    if season == 'Summer':
        summer = pd.DataFrame(
            {"Nation": df_more["Nation"], "SO_Gold": df_more["SO_Gold"], "SO_Silver": df_more["SO_Silver"],
             "SO_Bronze": df_more["SO_Bronze"]})
        summer.loc[:, 'Total'] = summer.sum(axis=1)
        summer = summer[lambda x: x['Total'] > 0]
        medals_summer = summer.sort_values("Total", ascending=False)[:20]

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.set_color_codes()
        sns.barplot(x="SO_Bronze", y="Nation", data=medals_summer,
                    label="Bronze", color="brown", ax=ax)
        sns.set_color_codes()
        sns.barplot(x="SO_Silver", y="Nation", data=medals_summer,
                    label="Silver", color="silver", ax=ax)
        sns.set_color_codes()
        sns.barplot(x="SO_Gold", y="Nation", data=medals_summer,
                    label="Gold", color="gold", ax=ax)
        ax.legend(ncol=2, loc="lower right", frameon=True)
        ax.set(ylabel="", xlabel="Medals for Summer Olympic Games")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig)
    else:
        st.write("You didn't select comedy.")


