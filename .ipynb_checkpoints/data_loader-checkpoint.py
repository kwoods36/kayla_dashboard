import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def load_data():
    #df = pd.read_csv('Kayla_Daily_Survey.csv')
    url ="https://docs.google.com/spreadsheets/d/1iXGYKpSNqwDI99m1zxIbrgD9TQcaNZufkqdGFrnkC6s/export?format=csv"
    df = pd.read_csv(url)
    df = df.drop(columns=["Timestamp"])

    df_orig=df.copy()
    
    df["Survey_Date"] = pd.to_datetime(df["Survey_Date"])
    df = df.sort_values(["Survey_Date"])

    df_orig["Survey_Date"] = pd.to_datetime(df_orig["Survey_Date"]).dt.date
    df_orig = df_orig.sort_values(["Survey_Date"])
    
    # Yes/No Cols
    yes_no_cols = [
        "Comp_day",
        "Travel_day",
        "Period_day",
        "Morning_Back_Pain"
    ]
    
    for col in yes_no_cols:
        df[col] = df[col].map({
            "Yes": 1,
            "No": 0
        })
    
    df["Next_Morning_Back_Pain"] = df["Morning_Back_Pain"].shift(-1)
    
    # Alcoholic drinks
    alc_map = {
        "1 drink" : 1,
        "0 drinks" : 0
    }
    df["Alcoholic_Drinks"] = df["Alcoholic_Drinks"].map(alc_map)
    
    # categorical
    
    # workout type
    workout_dummies = df["Workout_Type"].str.get_dummies()
    df = pd.concat([df, workout_dummies], axis=1)
    df = df.drop(columns=["Workout_Type"])
    
    # multi-select cols
    
    # Pain
    pain_dummies = df["Pain"].str.get_dummies(sep=", ")
    pain_dummies.columns = (
        pain_dummies.columns
        .str.lower()
        .str.replace(" ", "_")
    )
    df = pd.concat([df, pain_dummies], axis=1)
    df = df.drop(columns=["Pain"])
    df = df.drop(columns = ["shin"])
    
    # Relax/Recovery
    df["RR_Act"] = df["RR_Act"].replace("None", pd.NA)
    rr_dummies = df["RR_Act"].str.get_dummies(sep=", ")
    rr_dummies.columns = (
        rr_dummies.columns
        .str.lower()
        .str.replace(" ", "_")
    )
    df = pd.concat([df, rr_dummies], axis=1)
    df = df.drop(columns=["RR_Act"])
    
    # Protein types
    protein_dummies = df["Protein"].str.get_dummies(sep=", ")
    df = pd.concat([df, protein_dummies], axis=1)
    df = df.drop(columns=["Protein"])
    
    # Mood description
    mood_dummies = df["Mood_Descript"].str.get_dummies(sep=", ")
    df = pd.concat([df, mood_dummies], axis=1)
    df = df.drop(columns=["Mood_Descript"])
    
    # Practice feeling
    df["Prac_Feel"] = df["Prac_Feel"].replace("NA", pd.NA)
    prac_dummies = df["Prac_Feel"].str.get_dummies(sep=", ")
    prac_dummies.columns = (
        prac_dummies.columns
        .str.lower()
        .str.replace(" ", "_")
    )
    df = pd.concat([df, prac_dummies], axis=1)
    df = df.drop(columns=["Prac_Feel"])
    
    # ----------------------------
    # Adding lags and rolling averages
    # ----------------------------
    df["sleep_lag1"] = df["Sleep_Hours"].shift(1)
    df["sleep_lag2"] = df["Sleep_Hours"].shift(2)
    df["Sleep_Next_Night"] = df["Sleep_Hours"].shift(-1)
    
    df["sleep_3day_avg"] = df["Sleep_Hours"].rolling(3).mean()
    df["sleep_5day_avg"] = df["Sleep_Hours"].rolling(5).mean()

    df["Prac_energy_next_day"] = df["Prac_Energy_Level"].shift(-1)
    
    df["Chicken_lag"] = df["Chicken"].shift(1)
    df["Beef_lag"] = df["Beef"].shift(1)
    df["Salmon_lag"] = df["Salmon"].shift(1)
    df["Pork_lag"] = df["Pork"].shift(1)
    df["Other_lag"] = df["Other"].shift(1)

    # ----------------------------------------------------
    # MENSTRUAL CYCLE FEATURES
    # ----------------------------------------------------
    
    # Ensure sorted by date
    df = df.sort_values("Survey_Date").reset_index(drop=True)
    
    # Binary indicator
    df["is_period"] = df["Period_day"] == 1
    
    # First day of each period
    df["period_start"] = (
        df["is_period"] &
        ~df["is_period"].shift(fill_value=False)
    )
    
    # Dates of observed period starts
    period_starts = df.loc[df["period_start"], "Survey_Date"]
    
    # ----------------------------------------------------
    # Estimate average cycle length
    # ----------------------------------------------------
    
    cycle_lengths = period_starts.diff().dt.days.dropna()
    
    # Ignore implausible gaps (likely missing surveys)
    cycle_lengths = cycle_lengths[
        cycle_lengths.between(20, 40)
    ]
    
    if len(cycle_lengths) > 0:
        avg_cycle_length = round(cycle_lengths.mean())
    else:
        avg_cycle_length = 28
    
    print(f"Estimated cycle length: {avg_cycle_length} days")
    
    # ----------------------------------------------------
    # Assign cycle IDs
    # ----------------------------------------------------
    
    df["cycle_id"] = df["period_start"].cumsum()
    
    # Before the first observed period
    df.loc[df["cycle_id"] == 0, "cycle_id"] = pd.NA
    
    # ----------------------------------------------------
    # Cycle day
    # ----------------------------------------------------
    
    df["cycle_day"] = pd.NA
    
    for cycle in df["cycle_id"].dropna().unique():
    
        idx = df["cycle_id"] == cycle
    
        start_date = df.loc[idx, "Survey_Date"].min()
    
        df.loc[idx, "cycle_day"] = (
            df.loc[idx, "Survey_Date"] - start_date
        ).dt.days + 1
    
    df["cycle_day"] = df["cycle_day"].astype("Int64")
    
    # ----------------------------------------------------
    # Estimate cycle phase
    # ----------------------------------------------------

    def cycle_phase(day, cycle_length):
    
        if pd.isna(day):
            return pd.NA

        # Scale important points based on estimated cycle length
        ovulation_day = round(cycle_length / 2)
        late_luteal_start = cycle_length - round(cycle_length * 0.15)
    
        # Menstrual
        if day <= 2:
            return "Early Menstrual"
    
        elif day <= 5:
            return "Late Menstrual"
    
        # Follicular
        elif day <= ovulation_day - 4:
            return "Early Follicular"
    
        elif day <= ovulation_day - 1:
            return "Late Follicular"
    
        # Ovulation
        elif day <= ovulation_day + 1:
            return "Ovulatory"
    
        # Luteal
        elif day <= late_luteal_start:
            return "Early Luteal"
    
        else:
            return "Late Luteal"
    
    df["cycle_phase"] = df["cycle_day"].apply(
        lambda x: cycle_phase(x, avg_cycle_length)
    )

    return df, df_orig
