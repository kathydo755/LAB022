import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

st.title("Your Steps Visualized 📈")
st.write("This page displays important information about your steps!")

if "csv_data" not in st.session_state:
    st.session_state.csv_data = pd.DataFrame()

if "json_data" not in st.session_state:
    st.session_state.json_data = {}

st.divider()
st.header("Steps in the CSV")
csv_path = "data.csv"
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0 and st.session_state.csv_data.empty:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    if df.shape[1] < 2 or "Day" not in df.columns:
        df = pd.read_csv(csv_path, header=None, names=["Day", "Steps"], encoding="utf-8-sig")
    
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)
    if "Value" in df.columns:
        df = df.rename(columns={"Value": "Steps"})
    df = df[df["Steps"].astype(str).str.isnumeric()]
    df["Steps"] = df["Steps"].astype(int)
    df = df.drop_duplicates(subset="Day", keep="last")
    st.session_state.csv_data = df 
if not st.session_state.csv_data.empty:
    st.dataframe(st.session_state.csv_data)
else:
    st.warning("Error generating data.")
    
uploaded_file = st.file_uploader("JSON load",type="json")
if uploaded_file is not None:
    st.session_state.json_data = json.load(uploaded_file)

json_path = "data.json"
if os.path.exists(json_path) and not st.session_state.json_data:
    try:
        with open(json_path, 'r') as f:
            st.session_state.json_data = json.load(f)
        st.success("Loading successful!")
    except json.JSONDecodeError:
        st.error("Loading unsuccessful.")
        st.session_state.json_data = {}
        
st.divider()
st.header("Graphs")

if not st.session_state.csv_data.empty:
    st.subheader("Graph 1: Your latest weekly steps")
    latest = st.session_state.csv_data.tail(7)
    day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    latest['Day'] = pd.Categorical(latest['Day'], categories=day_order, ordered=True)
    latest = latest.sort_values('Day')
    st.bar_chart(latest.set_index('Day')['Steps']) #NEW st.bar_chart
else:
    st.warning("No valid CSV data available for graph.")
st.write("This graph shows the amount of steps taken in a week.")

##This is using csv from sessionstate


st.subheader("Graph 2: Dynamic")
daysWeek= ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
if "selectDays" not in st.session_state:
    st.session_state.selectDays = daysWeek
st.session_state.selectDays = st.multiselect( #NEW st.multiselect
    "Select the day(s) to display in the graph:",
    options = daysWeek,
    default = st.session_state.selectDays 
)
if not st.session_state.csv_data.empty and st.session_state.selectDays:
    newDf = st.session_state.csv_data[
        st.session_state.csv_data["Day"].isin(st.session_state.selectDays)
    ]
    newDf["Day"] = pd.Categorical(newDf["Day"],categories=daysWeek, ordered = True)
    newDf= newDf.sort_values("Day")
    st.line_chart(newDf.set_index("Day")["Steps"])#NEW st.line_chart
    st.write("This graph shows the amount of steps you've taken on selected days.")
else:
    st.warning("No data avaliable for the days you selected.")


st.subheader("Graph 3: Scatterplot of steps taken") 

if st.session_state.json_data:
    json_data = st.session_state.json_data
    if "data_points" in json_data and isinstance(json_data["data_points"], list):
        df_json = pd.DataFrame(json_data["data_points"])
        df_json = df_json.rename(columns={"label": "Day", "value": "Steps"})
    else:
        df_json = pd.DataFrame(list(json_data.items()), columns=["Day", "Steps"])
    df_json["Steps"] = pd.to_numeric(df_json["Steps"], errors="coerce")
    df_json = df_json.dropna(subset=["Steps"])
    if df_json.empty:
        st.error("There was an error.")
        st.stop()
    min_steps = int(df_json["Steps"].min(skipna=True))
    max_steps = int(df_json["Steps"].max(skipna=True))
    st.session_state.min_filter = st.slider( #NEW st.slider
        "Filter steps data:",
        min_value=min_steps,
        max_value=max_steps,
        value=min_steps,
        step=1,
    )
    df_filtered = df_json[df_json["Steps"] >= st.session_state.min_filter]
    st.scatter_chart(df_filtered, x="Day", y="Steps")
    st.write("This displays the steps taken on a scatterplot. Interact with the slider and the graph!")

else:
    st.warning("Error generating scatterplot.")
