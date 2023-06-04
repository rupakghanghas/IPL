import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title="my IPL analysis")
# importing data
data=pd.read_csv('IPL_Ball_by_Ball_2008_2022.csv')
data_2=pd.read_csv('IPL_Matches_2008_2022.csv')
data_3=pd.read_csv('alldatabowling.csv')
data_4=pd.read_csv("batter.csv")
data_3["economy rate"]=data_3['Runs_Conceded']/data_3['Over']
data_3["average"]=data_3['Runs_Conceded']/data_3['Wickets']
data_3["strike rate"]=((data_3['Over'])*6)/data_3['Wickets']
data_3['average'] = data_3['average'].replace(np.inf, 0)
data_3['economy rate'] = data_3['economy rate'].replace(np.inf, 0)
data_3['strike rate'] = data_3['strike rate'].replace(np.inf, 0)
data['is_six']= data['batsman_run'].apply(lambda x: True if x == 6 else False)
data['is_four']= data['batsman_run'].apply(lambda x: True if x == 4 else False)
data['is_three']= data['batsman_run'].apply(lambda x: True if x == 3 else False)
data['is_two']= data['batsman_run'].apply(lambda x: True if x == 2 else False)
data['is_one']= data['batsman_run'].apply(lambda x: True if x == 1 else False)
# adding image and title
img = Image.open('download.jpeg')
st.image(image=img,width=200)
st.title("THE BIG IPL ANALYSIS")
st.text("BY Rupak Ghanghas")
# ###########   adding players as options in selectbox ##############################
options_1=data['batter'].unique()
selcted=st.sidebar.selectbox('CHOOSE PLAYER FOR BATTING OVERVIEW',options_1)
st.markdown("<hr>", unsafe_allow_html=True)
btn_1=st.sidebar.button("click here for batting overview")
if btn_1:
    st.write("_based on ipl data from 2008 to 2021._")
    st.title("***BATTING OVERVIEW***")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.title(selcted)
    st.markdown("<hr>", unsafe_allow_html=True)
    grp=data.groupby("batter")
    six=grp.is_six.sum()[selcted]
    four=grp.is_four.sum()[selcted]
    three=grp.is_three.sum()[selcted]
    two=grp.is_two.sum()[selcted]
    one=grp.is_one.sum()[selcted]
    runs= grp.batsman_run.sum()[selcted]
    
    
    table={"total runs scored in IPL":runs,
           "total number of sixes scored ":six,
           "total number of fours scored ":four,
           "total number of 3 taken ":three,
           "total number of doubles taken ":two,
           "total number of singles taken ":one,
           
           }  
    st.table(pd.Series(table))
    
    # ploting a graph 
    table_2={
           "sixes scored ":six*6,
           "fours scored ":four*4,
           "3 taken ":three*3,
           "doubles taken ":two*2,
           "singles taken ":one
           }  
    labels = list(table_2.keys())
    values = list(table_2.values())
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    plt.title('Pie Chart')
    st.pyplot(fig)
    # PERFORMANCE
    mom=data_2.Player_of_Match
    if selected in list(mom):
        var=(mom.value_counts()[selected])
    else:
        var=0
    st.subheader(f"Total Man of the match title won:{var}")
    st.markdown("<hr>", unsafe_allow_html=True)
    batting_avg=data_4[data_4['batter']==selected].squeeze()
    avg=batting_avg['avg'].round(2)
    st.subheader(f"average :{avg}")
    st.markdown("<hr>", unsafe_allow_html=True)
    stk=batting_avg['strike_rate'].round(2)
    st.subheader(f"Batting Strike Rate :{stk}")

options_2=data_3.Name
selected_2=st.sidebar.selectbox('CHOOSE PLAYER FOR BOWLING OVERVIEW',options_2)
btn_2=st.sidebar.button("click here for bowling overview")   
if btn_2:
    st.write("_based on ipl data from 2008 to 2021._")
    st.title("***BOWLING OVERVIEW***")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.title(selected_2)
    st.markdown("<hr>", unsafe_allow_html=True)
    cond=data_3[data_3.Name==selected_2]
    bowling_table={
        "total  number of overs bowled ":cond.Over.astype(int),
        "total runs Conceded  ":cond.Runs_Conceded,
        "total wickets taken":cond.Wickets,
        "total number of maiden overs ":cond.Maidens,	
        "total number of dot balls thrown":cond.Dots
    }
    df=pd.DataFrame(bowling_table)
    st.table(df.melt())
    # #####################bar graph for economy rate###########################3
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header(f"economy rate of {selected_2} is: {float(cond['economy rate'])}")
    # Sample data
    player1_name = selected_2
    player1_economy =cond['economy rate']

    player2_name = 'Average economy rate'
    player2_economy = data_3['economy rate'].mean()

    # Create a bar graph
    fig, ax = plt.subplots()
    ax.bar(player1_name, player1_economy,width=0.1, label=player1_name)
    ax.bar(player2_name, player2_economy,width=0.1, label=player2_name)

    # Customize the graph
    ax.set_xlabel('Player')
    ax.set_ylabel('Economy Rate')
    ax.set_title('Economy Rate Comparison')
    ax.legend()

    # Display the graph in Streamlit
    st.pyplot(fig)
    
    
    ############## bar graph for bowling average ##################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header(f"bowling average of {selected_2} is: {float(cond['average'])}")
    # Sample data
    player1_name = selected_2
    player1_avg =cond['average']

    player2_name = 'mean of bowling average of all players '
    player2_avg = data_3['average'].mean()

    # Create a bar graph
    fig, ax = plt.subplots()
    ax.bar(player1_name, player1_avg,width=0.1, label=player1_name)
    ax.bar(player2_name, player2_avg,width=0.1, label=player2_name)

    # Customize the graph
    ax.set_xlabel('Player')
    ax.set_ylabel('bowling average')
    ax.set_title('bowling average Comparison')
    ax.legend()
    st.pyplot(fig)

    ############## bar graph for bowling strike rate ##################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header(f"bowling strike rate of {selected_2} is: {float(cond['strike rate'])}")
    # Sample data
    player1_name = selected_2
    player1_stk =cond['strike rate']

    player2_name = 'average bowling strike rate '
    player2_stk = data_3['strike rate'].mean()

    # Create a bar graph
    fig, ax = plt.subplots()
    ax.bar(player1_name, player1_stk,width=0.1, label=player1_name)
    ax.bar(player2_name, player2_stk,width=0.1, label=player2_name)

    # Customize the graph
    ax.set_xlabel('Player')
    ax.set_ylabel('bowling strike rate')
    ax.set_title('bowling strike rate Comparison')
    ax.legend()
    st.pyplot(fig)
    
    
