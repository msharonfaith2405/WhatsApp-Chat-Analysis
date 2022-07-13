import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     #file is currently a byte data stream
     #convert into string
     data=bytes_data.decode("utf-8")
     # st.text(data)
     df=preprocessor.preprocess(data)
     # st.dataframe(df)
     #printing the dataframe

     #fetch unique users for dropdown
     user_list=df['user'].unique().tolist()
     #remove group notifications
     user_list.remove('group_notification')
     #sort user names in ascending alphabetical order
     user_list.sort()
     #group analysis on clicking overall
     user_list.insert(0,"Overall")
     selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

     #SHOW ANALYSIS BUTTON
     if st.sidebar.button("ShowAnalysis"):
          #Stats Area
          num_messages,len_of_words,num_media_messages,num_url=helper.fetch_stats(selected_user,df)
          st.title("Top Statistics")
          col1,col2,col3,col4=st.columns(4)
          with col1:
               st.header("Total Messages")
               st.title(num_messages)
          with col2:
               st.header("Total Words")
               st.title(len_of_words)
          with col3:
               st.header("Media Shared")
               st.title(num_media_messages)
          with col4:
               st.header("URLs Shared")
               st.title(num_url)

          #monthly timeline
          st.title("Monthly Timeline")
          timeline=helper.monthly_timeline(selected_user,df)
          fig,ax=plt.subplots()
          ax.plot(timeline['time'],timeline['message'],color='red')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          #daily timeline
          st.title("Daily Timeline")
          daily_timeline_df = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline_df['only_date'],daily_timeline_df['message'], color='black')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          #activity map
          st.title('Activity Map')
          col1,col2=st.columns(2)

          with col1:
               st.header("Most busy day")
               busy_day=helper.week_activity_map(selected_user, df)
               fig,ax=plt.subplots()
               ax.bar(busy_day.index,busy_day.values)
               plt.xticks(rotation="vertical")
               st.pyplot(fig)
          with col2:
               st.header("Most busy month")
               busy_month = helper.month_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values)
               plt.xticks(rotation="vertical")
               st.pyplot(fig)

          #Activity heatmap
          st.title("Weekly activity Map")
          user_heatmap=helper.activity_heatmap(selected_user, df)
          fig,ax=plt.subplots()
          ax=sns.heatmap(user_heatmap)
          st.pyplot(fig)


          #finding the busiest users  in the group(Grouppppp Level Only)
          if(selected_user=='Overall'):
               st.title("Most Busy Users")
               busy_users,new_df=helper.most_busy_users(df)
               fig,ax=plt.subplots()
               col1,col2=st.columns(2);

               with col1:
                    ax.bar(busy_users.index, busy_users.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(new_df)


          #WordCloud
          # pip install wordcloud
          df_wc=helper.create_word_cloud(selected_user,df)
          #to display image
          fig,ax=plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          #most common words
          most_common_df=helper.most_common_words(selected_user,df)
          fig,ax=plt.subplots()
          ax.barh(most_common_df[0],most_common_df[1])
          plt.xticks(rotation='vertical')
          st.title("Most Common Words")
          st.pyplot(fig)
          #st.dataframe(most_common_df)

          #EMOJI ANALYSIS
          emoji_df=helper.emoji_helper(selected_user,df)
          st.title("Emoji Analysis")
          col1,col2=st.columns(2)
          with col1:
               st.dataframe(emoji_df)
          with col2:
               fig,ax=plt.subplots()
               ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
               st.pyplot(fig)


