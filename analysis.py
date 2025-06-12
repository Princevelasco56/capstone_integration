# analysis.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
def run_analysis(prof_name=None):
    np.random.seed(42)
    faculty_names = ['Prof. Antonio', 'Prof. Miranda', 'Prof. Valdez', 'Prof. Enriquez', 'Prof. Santiago']
    dates = pd.date_range(start="2025-06-01", periods=30, freq='D')
    data = []

    for name in faculty_names:
        if prof_name and name != prof_name:
            continue  # Skip other names if filtering

        for date in dates:
            if date.weekday() >= 5:
                continue

            if name == 'Prof. Antonio':
                time_in = datetime.combine(date, datetime.strptime("08:00", "%H:%M").time()) + timedelta(minutes=np.random.randint(-10, 60))
                time_out = time_in + timedelta(hours=8) + timedelta(minutes=np.random.randint(-30, 30))
            elif name == 'Prof. Miranda':
                time_in = datetime.combine(date, datetime.strptime("09:00", "%H:%M").time()) + timedelta(minutes=np.random.randint(-5, 10))
                time_out = time_in + timedelta(hours=9)
            elif name == 'Prof. Valdez':
                time_in = datetime.combine(date, datetime.strptime("07:00", "%H:%M").time()) + timedelta(minutes=np.random.randint(-10, 15))
                time_out = time_in + timedelta(hours=7)
            elif name == 'Prof. Enriquez':
                time_in = datetime.combine(date, datetime.strptime("13:00", "%H:%M").time()) + timedelta(minutes=np.random.randint(-5, 5))
                time_out = time_in + timedelta(hours=4)
            elif name == 'Prof. Santiago':
                time_in = datetime.combine(date, datetime.strptime("10:00", "%H:%M").time()) + timedelta(minutes=np.random.randint(-20, 20))
                time_out = time_in + timedelta(hours=8)
                if np.random.rand() < 0.1:
                    time_out -= timedelta(hours=2)

            data.append([name, date.date(), time_in.time(), time_out.time()])

    if not data:
        return pd.DataFrame(columns=['faculty', 'date', 'time_in', 'time_out', 'work_hours', 'anomaly', 'status'])

    df = pd.DataFrame(data, columns=['faculty', 'date', 'time_in', 'time_out'])
    df['time_in'] = pd.to_datetime(df['time_in'].astype(str))
    df['time_out'] = pd.to_datetime(df['time_out'].astype(str))
    df['work_hours'] = (df['time_out'] - df['time_in']).dt.total_seconds() / 3600

    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(df[['work_hours']])
    df['status'] = df['anomaly'].apply(lambda x: 'Unusual' if x == -1 else 'Normal')

    return df
