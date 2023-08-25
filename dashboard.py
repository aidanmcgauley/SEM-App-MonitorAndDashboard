import os
import requests
import json
import datetime
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import threading

# Dummy data for input
dummy_data = {
    "item_1": "Lecture sessions",
    "item_2": "Lab sessions",
    "item_3": "Support sessions",
    "item_4": "Canvas activities",
    "attendance_1": "5",
    "attendance_2": "10",
    "attendance_3": "15",
    "attendance_4": "20",
    "total_hours_1": "33",
    "total_hours_2": "22",
    "total_hours_3": "44",
    "total_hours_4": "55",

    "cut_off_score": "50",
    "engagement_score": "33"  ########## CHANGE BACK TO 33 TO MAKE IT PASS
}

# Expected output for each function
expected_output = {
    "getSortedByPercentage":    {
                                    "sorted_by_percentage":[
                                        {"item":"Lab sessions","attendance":10,"total_hours":22,"percentage":45.45454545454545},
                                        {"item":"Canvas activities","attendance":20,"total_hours":55,"percentage":36.36363636363637},
                                        {"item":"Support sessions","attendance":15,"total_hours":44,"percentage":34.090909090909086},
                                        {"item":"Lecture sessions","attendance":5,"total_hours":33,"percentage":15.151515151515152}
                                    ]
                                },

    "getRisk":  {
                    "risk": "at risk", 
                    "engagement_score": 33, 
                    "cut_off_score": 50
                },

    "getEngagementScore":   {
                                "error": False,
                                "engagement_score": 33
                            },

    "getMaxMin":{
                    "error": False,
                    "max_items": ["Canvas activities - 20"],
                    "min_items": ["Lecture sessions - 5"]
                },

    "getSortedAttendance": {
                                "error": False,
                                "items": ["Lecture sessions", "Lab sessions", "Support sessions", "Canvas activities"],
                                "attendance": ["5", "10", "15", "20"],
                                "sorted_attendance": [
                                    {"item": "Canvas activities", "attendance": "20"},
                                    {"item": "Support sessions", "attendance": "15"},
                                    {"item": "Lab sessions", "attendance": "10"},
                                    {"item": "Lecture sessions", "attendance": "5"}
                                ]
                            },
    
    "getTotal": {'total_hours': 50}
}

endpoints = {
    "getEngagementScore": "http://sem-engagementscore1.40058902.qpc.hal.davecutting.uk/",
    "getMaxMin": "http://sem-maxmin1.40058902.qpc.hal.davecutting.uk/",
    "getRisk": "http://sem-riskoffailure1.40058902.qpc.hal.davecutting.uk/",
    "getSortedAttendance": "http://sem-sort1.40058902.qpc.hal.davecutting.uk/",
    "getSortedByPercentage": "http://sem-sortbypercentage.40058902.qpc.hal.davecutting.uk/",
    "getTotal": "http://sem-totalhours1.40058902.qpc.hal.davecutting.ukKKK/" ####### DELETE EXTRA LETTERS
}

def construct_url(endpoint_key, dummy_data):
    if endpoint_key == "getSortedByPercentage":
        url = endpoints["getSortedByPercentage"] + "?item_1=" + dummy_data["item_1"] + "&attendance_1=" + dummy_data["attendance_1"] + "&total_hours_1=" + dummy_data["total_hours_1"] + "&item_2=" + dummy_data["item_2"] + "&attendance_2=" + dummy_data["attendance_2"] + "&total_hours_2=" + dummy_data["total_hours_2"] + "&item_3=" + dummy_data["item_3"] + "&attendance_3=" + dummy_data["attendance_3"] + "&total_hours_3=" + dummy_data["total_hours_3"] + "&item_4=" + dummy_data["item_4"] + "&attendance_4=" + dummy_data["attendance_4"] + "&total_hours_4=" + dummy_data["total_hours_4"]
    elif endpoint_key == "getEngagementScore":
        url = endpoints["getEngagementScore"] + "?item_1=" + dummy_data["item_1"] + "&attendance_1=" + dummy_data["attendance_1"] + "&total_hours_1=" + dummy_data["total_hours_1"] + "&item_2=" + dummy_data["item_2"] + "&attendance_2=" + dummy_data["attendance_2"] + "&total_hours_2=" + dummy_data["total_hours_2"] + "&item_3=" + dummy_data["item_3"] + "&attendance_3=" + dummy_data["attendance_3"] + "&total_hours_3=" + dummy_data["total_hours_3"] + "&item_4=" + dummy_data["item_4"] + "&attendance_4=" + dummy_data["attendance_4"] + "&total_hours_4=" + dummy_data["total_hours_4"]
    elif endpoint_key == "getMaxMin":
        url = endpoints["getMaxMin"] + "?item_1=" + dummy_data["item_1"] + "&attendance_1=" + dummy_data["attendance_1"] + "&item_2=" + dummy_data["item_2"] + "&attendance_2=" + dummy_data["attendance_2"] + "&item_3=" + dummy_data["item_3"] + "&attendance_3=" + dummy_data["attendance_3"] + "&item_4=" + dummy_data["item_4"] + "&attendance_4=" + dummy_data["attendance_4"] + "&total_hours_1=" + dummy_data["total_hours_1"] + "&total_hours_2=" + dummy_data["total_hours_2"] + "&total_hours_3=" + dummy_data["total_hours_3"] + "&total_hours_4=" + dummy_data["total_hours_4"]
    elif endpoint_key == "getSortedAttendance":
        url = endpoints["getSortedAttendance"] + "?item_1=" + dummy_data["item_1"] + "&attendance_1=" + dummy_data["attendance_1"] + "&item_2=" + dummy_data["item_2"] + "&attendance_2=" + dummy_data["attendance_2"] + "&item_3=" + dummy_data["item_3"] + "&attendance_3=" + dummy_data["attendance_3"] + "&item_4=" + dummy_data["item_4"] + "&attendance_4=" + dummy_data["attendance_4"] + "&total_hours_1=" + dummy_data["total_hours_1"] + "&total_hours_2=" + dummy_data["total_hours_2"] + "&total_hours_3=" + dummy_data["total_hours_3"] + "&total_hours_4=" + dummy_data["total_hours_4"]
    elif endpoint_key == "getTotal":
        url = endpoints["getTotal"] + "?item_1=" + dummy_data["item_1"] + "&attendance_1=" + dummy_data["attendance_1"] + "&item_2=" + dummy_data["item_2"] + "&attendance_2=" + dummy_data["attendance_2"] + "&item_3=" + dummy_data["item_3"] + "&attendance_3=" + dummy_data["attendance_3"] + "&item_4=" + dummy_data["item_4"] + "&attendance_4=" + dummy_data["attendance_4"] + "&total_hours_1=" + dummy_data["total_hours_1"] + "&total_hours_2=" + dummy_data["total_hours_2"] + "&total_hours_3=" + dummy_data["total_hours_3"] + "&total_hours_4=" + dummy_data["total_hours_4"]
    elif endpoint_key == "getRisk":
        url = endpoints["getRisk"] + "?engagement_score=" + str(dummy_data["engagement_score"]) + "&cut_off_score=" + str(dummy_data["cut_off_score"])
    return url

# SendGrid method for sending email alerts:
def sendEmail(subject, text):
    
    message = Mail(from_email='aidanmcgauley@gmail.com',
                    to_emails='aidanmcgauley@gmail.com',
                    subject=subject,
                    plain_text_content=text,
                    html_content = text.replace('\n', '<br>') # My gmail was displaying body as 1 line
                    )
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        #print(response.status_code)    
        #print(response.body)
        #print(response.headers)
    except Exception as e:
        print(e.message)

def test_endpoint(endpoint_key, dummy_data, expected):
    working = True

    try:
        # Construct the request URL using the construct_url function
        request_url = construct_url(endpoint_key, dummy_data)

        # Make request
        response = requests.get(request_url)
        response.raise_for_status()

        # Check if the response is a valid JSON
        try:
            response_content = response.json()
        except json.JSONDecodeError:
            print(f"{endpoint_key}: Invalid JSON Response")
            sendEmail("Invalid JSON Response Alert", f"{endpoint_key} returned an invalid JSON.\nURL: {request_url}")
            status = "INVALID JSON"
            return {
                "function": endpoint_key,
                "pass/fail": status,
                "latency(secs)": 0,
                "message": "Invalid JSON Response"
            }

        # Check if the response matches the expected result
        if response_content != expected:
            print(f"{endpoint_key}: FAIL")
            sendEmail("Test Failure Alert", f"{endpoint_key} failed.\nExpected: {expected}\nActual: {response_content}")
            working = False
        else:
            print(f"{endpoint_key}: PASS")
            working = True

        # Check latency
        latency = response.elapsed.total_seconds()
        print(latency)

        # Construct the result object
        return {
            "function": endpoint_key,
            "pass/fail": "PASS" if working else "FAIL",
            "latency(secs)": latency
        }

    except requests.exceptions.RequestException as e:
        print(f"Error while testing {endpoint_key}: Endpoint Unavailable")
        sendEmail("Endpoint Unavailable Alert", f"{endpoint_key} is unavailable.\nError: {e}")
        status = "UNAVAILABLE"
        return {
            "function": endpoint_key,
            "pass/fail": status,
            "latency(secs)": 0,
            "message": str(e)
        }


def monitor():
    results = []

    # Setup for average latency
    total_latency = 0.0
    endpoint_count = len(endpoints)

    # Loop through each endpoint and call test_endpoint
    for endpoint_key in endpoints:
        test_result = test_endpoint(endpoint_key, dummy_data, expected_output[endpoint_key])
        total_latency += test_result["latency(secs)"]
        results.append(test_result)

    # Calculate avg latency
    average_latency = total_latency / endpoint_count if endpoint_count > 0 else 0
    print("Average latency: " + str(average_latency))

    now = datetime.now()

    # Read existing data
    try:
        with open('log.json', 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    now = datetime.now().isoformat()

    test_obj = {
        "date/time": now,
        "tests": results,
        "average_latency(secs)": average_latency
    }

    existing_data.append(test_obj)


    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to log.json
    log_file_path = os.path.join(script_dir, 'log.json')
    # Write updated data
    with open(log_file_path, 'w') as outfile:
        json.dump(existing_data, outfile, indent=4, sort_keys=True)

    return "Success"
    


# Start the background monitoring thread
def run_monitor_auto():
    while True:
        monitor()
        time.sleep(20)      # Change back to 60*20 to run every 20 mins 

# Code was executing every split second, so this check tries to avoid multiple threads
if not any(thread.name == 'monitor_thread' for thread in threading.enumerate()):
    monitor_thread = threading.Thread(target=run_monitor_auto, name='monitor_thread')
    monitor_thread.start()



# ---------- Streamlit dashboard code---------------

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Read log.json
def get_log_data():
    with open('log.json', 'r') as file:
        return json.load(file)

log_data = get_log_data()

# ------ ROW A -------
a1, a2, a3 = st.columns((2, 4, 4))
a1.image(Image.open('wepik-yellow-publisher-logo-20230820151246FTU5.png'))

date_time = log_data[-1]["date/time"]
date_time_obj = datetime.fromisoformat(date_time)
date_time_formatted = date_time_obj.strftime("%H:%M:%S    %d/%m/%Y")

last_avg_latency = log_data[-1]["average_latency(secs)"]
# Check if log_data has at least two records
if len(log_data) > 1:
    second_last_avg_latency = log_data[-2]["average_latency(secs)"]
    avg_latency_change = ((last_avg_latency - second_last_avg_latency) / second_last_avg_latency) * 100 if second_last_avg_latency != 0 else None
else:
    avg_latency_change = None

with a2:
    st.markdown("Average Latency")
    st.metric(f"{date_time_formatted} result:", f"{last_avg_latency:.3f}", f"{avg_latency_change:.1f}%" if avg_latency_change is not None else "N/A", "inverse")

number_of_services_operational = sum(test["pass/fail"] == "PASS" for test in log_data[-1]["tests"]) if log_data[-1]["tests"] else 0
with a3:
    st.markdown("Number of Services Operational")
    st.metric(f"{date_time_formatted} result:", str(number_of_services_operational))




# ----- ROW B ------
st.header("Function Status")
b1, b2, b3, b4, b5, b6 = st.columns(6)

# Mapping of status to symbols
status_symbols = {
    "Active": ":white_check_mark:",
    "Error": ":warning:",
    "Unavailable": ":x:",
}
# Populating Row B (b1 to b6)
status_mapping = {"PASS": "Active", "FAIL": "Error", "UNAVAILABLE": "Unavailable"}
for test, b_col in zip(log_data[-1]["tests"], [b1, b2, b3, b4, b5, b6]):
    function_name = test["function"]
    status = status_mapping[test["pass/fail"]]
    b_col.markdown(f"**{function_name}:**<br>{status_symbols[status]} {status}", unsafe_allow_html=True)



# ----- ROW C -----
st.header("Latency")
c1, c2, c3, c4, c5, c6 = st.columns(6)

# Populating Row C (c1 to c6)
if len(log_data) > 1:
    for test, prev_test, c_col in zip(log_data[-1]["tests"], log_data[-2]["tests"], [c1, c2, c3, c4, c5, c6]):
        latency = test["latency(secs)"]
        prev_latency = prev_test["latency(secs)"]
        delta = ((latency - prev_latency) / prev_latency) * 100 if prev_latency != 0 else None
        delta_str = f"{delta:.1f}%" if delta is not None else None
        c_col.metric(test["function"], f"{latency:.3f}", delta_str, "inverse")
else:
    for test, c_col in zip(log_data[-1]["tests"], [c1, c2, c3, c4, c5, c6]):
        latency = test["latency(secs)"]
        c_col.metric(test["function"], f"{latency:.3f}", None, "inverse")


# ----- Button to run monitor again -----
if st.button("Refresh results"):
    monitor()
    st.experimental_rerun()


# ----- History table -----

st.header("Test history")
# Create a list to hold data
table_data = []

# Status mapping
status_mapping = {
    "PASS": "Active",
    "FAIL": "Error",
    "UNAVAILABLE": "Unavailable"
}

# Reverse to get most recent logs first
for log in reversed(log_data):
    date_time = log["date/time"]
    date_time_obj = datetime.fromisoformat(date_time)
    date_time_formatted = date_time_obj.strftime("%H:%M:%S    %d/%m/%Y")
    for test in log["tests"]:
        service = test["function"]
        status = status_mapping[test["pass/fail"]]
        latency = test["latency(secs)"]
        message = test.get("message", "")  # Message may not always be present
        table_data.append([service, status, latency, message, date_time_formatted])

# Create dataframe
columns = ["Service", "Status", "Latency", "Message", "Last checked"]
table_df = pd.DataFrame(table_data, columns=columns)

fig = go.Figure(data=go.Table(
    columnwidth=[5,2,2,7,5],
    header=dict(values=columns,
        fill_color='#095591',
        align='left'),
    cells=dict(values=table_df.T.values,
        fill_color='#C2D8FE',
        align='center')
))

fig.update_layout(
    width=1100,
    height=600,
    margin=dict(l=5, r=5, b=10, t=10
    ))

st.write(fig)