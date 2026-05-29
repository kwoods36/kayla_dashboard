import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv('Kayla_Daily_Survey.csv')
    df = df.drop(columns=["Timestamp"])
    

    df = df.rename(columns={
    "Survery_Date": "Survey_Date"
    })
        # survey date to datetime
    
    df["Survey_Date"] = pd.to_datetime(df["Survey_Date"])
    df = df.sort_values(["Survey_Date"])

    df_orig=df.copy()
    
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
    

    df["sleep_lag1"] = df["Sleep_Hours"].shift(1)
    df["sleep_lag2"] = df["Sleep_Hours"].shift(2)
    df["Sleep_Next_Night"] = df["Sleep_Hours"].shift(-1)
    
    df["sleep_3day_avg"] = df["Sleep_Hours"].rolling(3).mean()
    df["sleep_5day_avg"] = df["Sleep_Hours"].rolling(5).mean()

    # ----------------------------
    # 1. Period flag
    # ----------------------------
    df["is_period"] = df["Period_day"] == 1
    
    # ----------------------------
    # 2. Identify period starts
    # ----------------------------
    df["period_start"] = (
        df["is_period"] &
        (~df["is_period"].shift(1).fillna(False))
    )
    
    # ----------------------------
    # 3. Assign cycle ID
    # ----------------------------
    df["cycle_id"] = df["period_start"].cumsum()
    
    # ----------------------------
    # 4. Default everything to non_cycle
    # ----------------------------
    df["cycle_phase"] = "non_cycle"
    
    # ----------------------------
    # 5. Assign PRE-PERIOD (3 days before any period start)
    # ----------------------------
    period_start_indices = df.index[df["period_start"]].tolist()
    
    for idx in period_start_indices:
        pre_idx = list(range(max(0, idx - 3), idx))
        df.loc[pre_idx, "cycle_phase"] = "pre_period"
    
    # ----------------------------
    # 6. Assign PERIOD days
    # ----------------------------
    df.loc[df["is_period"], "cycle_phase"] = "period"
    
    # ----------------------------
    # 7. (optional) split period into early/mid/late
    # ----------------------------
    df["cycle_day_in_period"] = df.groupby("cycle_id")["is_period"].cumsum()
    
    df.loc[df["cycle_phase"] == "period", "cycle_phase_detail"] = (
        df["cycle_day_in_period"].map(
            lambda x: "early" if x <= 2 else ("mid" if x <= 5 else "late")
        )
    )
    
    # ----------------------------
    # 8. Fill missing detail labels
    # ----------------------------
    df["cycle_phase_detail"] = df["cycle_phase_detail"].fillna(df["cycle_phase"])

    return df, df_orig