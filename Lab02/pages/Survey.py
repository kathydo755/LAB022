
import streamlit as st
import pandas as pd
import os 

st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

st.title("Steps Input📝")
st.write("Enter the number of steps for each day of the week.")

with st.form("survey_form"):
    steps_input = {
        "Sunday":st.number_input("Steps taken on Sunday:"),
        "Monday":st.number_input("Steps taken on Monday:"),
        "Tuesday":st.number_input("Steps taken on Tuesday:"),
        "Wednesday":st.number_input("Steps taken on Wednesday:"),
        "Thursday":st.number_input("Steps taken on Thursday:"),
        "Friday":st.number_input("Steps taken on Friday:"),
        "Saturday":st.number_input("Steps taken on Saturday:"),
        }       
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        new_rows = pd.DataFrame([
            {"Day": day, "Steps": int(steps)}
            for day, steps in steps_input.items()
        ])
        if os.path.exists("data.csv"):
            new_rows.to_csv("data.csv", mode='a', header=False, index = False)
        else:
            new_rows.to_csv("data.csv", mode='w', header=True, index = False)
        
        st.success("Your data has been submitted!")
        st.write(f"You entered:")
        for day, steps in steps_input.items():
            st.write(f"**{day}:** {steps}")

##st.divider()
##st.header("Current Data in CSV")
##if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
##    current_data_df = pd.read_csv('data.csv', encoding='utf-8-sig')
##    current_data_df.columns = ['Day', 'Steps']
##    if 'Value' in current_data_df.columns:
##        current_data_df = current_data_df.rename(columns={'Value': 'Steps'})
##    current_data_df = current_data_df[current_data_df['Steps'].astype(str).str.isnumeric()]
##    current_data_df['Steps'] = current_data_df['Steps'].astype(int)
##    current_data_df=current_data_df.drop_duplicates(subset='Day', keep= 'last')
##    st.dataframe(current_data_df)
##else:
##    st.warning("The 'data.csv' file is empty or does not exist yet.")
