import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import statsmodels.api as sm
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from data_loader import load_data
from constants import display_names

st.title("Insights and Predictions")
st.subheader("Explore relationships between training, recovery, nutrition, and wellness metrics, and predict likely outcomes based on different scenarios.")
df, df_orig = load_data()
st.write(f"Due to dataset size, choose a maximum of {int(len(df)/10)+1} features for best results.")


st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7fb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DISPLAY_NAMES = display_names()
REVERSE_DISPLAY_NAMES = {
    v: k for k, v in DISPLAY_NAMES.items()
}

tab1,tab2 = st.tabs([
    "Exploring Relationships",
    "Predictions: Practice Feeling, Mood, and Pains"
])

# ----------------------
# TAB 1: Regression Explorer 1
# ----------------------
with tab1:
    # -----------------------------
    # FILTERS
    # -----------------------------
    st.write("Outcome Variable: The result you want to explain, understand, or predict (for example, sleep quality or practice energy). \n\n Predictor Variables: The factors that may help explain changes in that result (for example, sleep, nutrition, recovery habits, travel, or training type). \n\n This analysis looks at how the outcome changes as the predictors change and identifies which factors appear to have the strongest relationships with the outcome.")
    st.sidebar.header("Filters")
    
    comp_filter = st.sidebar.selectbox(
        "Competition Days",
        ["All", "Only Comp Days", "Exclude Comp Days"]
    )
    
    travel_filter = st.sidebar.selectbox(
        "Travel Days",
        ["All", "Only Travel Days", "Exclude Travel Days"]
    )
    
    cycle_filter = st.sidebar.selectbox(
        "Period Days",
        ["All", "Only Period Days", "Exclude Period Days"]
    )
    
    # -----------------------------
    # APPLY FILTERS
    # -----------------------------
    filtered_df = df.copy()
    
    if comp_filter == "Only Comp Days":
        filtered_df = filtered_df[filtered_df["Comp_day"] == 1]
    
    elif comp_filter == "Exclude Comp Days":
        filtered_df = filtered_df[filtered_df["Comp_day"] == 0]
    
    if travel_filter == "Only Travel Days":
        filtered_df = filtered_df[filtered_df["Travel_day"] == 1]
    
    elif travel_filter == "Exclude Travel Days":
        filtered_df = filtered_df[filtered_df["Travel_day"] == 0]
    
    if cycle_filter == "Only Period Days":
        filtered_df = filtered_df[filtered_df["Period_day"] == 1]
    
    elif cycle_filter == "Exclude Period Days":
        filtered_df = filtered_df[filtered_df["Period_day"] == 0]
    
    # -----------------------------
    # TARGET VARIABLE
    # -----------------------------
    st.header("Choose Outcome Variable")
    target_options = ["Prac_Energy_Level",
            "Mood_Number",
            "Sleep_Next_Night",
            "Next_Morning_Back_Pain",
            "Prac_energy_next_day"]
    
    target_display = st.selectbox(
        "Outcome Variable (Y)",
        [DISPLAY_NAMES.get(col, col) for col in target_options]
    )
    
    target = REVERSE_DISPLAY_NAMES.get(target_display)
    # -----------------------------
    # FEATURE OPTIONS
    # -----------------------------
    possible_features = [
        "Sleep_Hours",
        "Travel_day",
        "Comp_day",
        "Period_day",
        "Sleep_Quality",
        "Mood_Number",
        "Meals_Quality",
        "Alcoholic_Drinks",
        "Prac_Energy_Level",
        "Morning_Back_Pain",
        "Sleep_Hours",
        "Active Recovery",
        "Jump",
        "Speed",
        "Off",
        "Premeet",
        "Chicken",
        "Beef",
        "Salmon",
        "Pork",
        "Happy",
        "Stressed",
        "Anxious",
        "Tired",
        "focused",
        "sore",
        "strong",
        "sleep_lag1",
        "sleep_3day_avg",
        "right_shin",
        "left_shin",
        "knee",
        "lower_back",
        "left_foot",
        "tight_hips",
        "traps",
        "boots",
        "journaled",
        "pressure_tension_release",
        "red_light",
        "rolling",
        "stim/tens",
        "time_outside",
        "time_w_god",
        "Beef",
        "Chicken",
        "Salmon",
        "Other",
        "Beef_lag",
        "Chicken_lag",
        "Salmon_lag",
        "Other_lag",
    ]
    
    # Remove target from predictors
    possible_features = [x for x in possible_features if x != target]
    
    # -----------------------------
    # FEATURE SELECTION
    # -----------------------------
    st.header("Choose Predictor Variables")
    
    feature_display = st.multiselect(
        "Predictors (X)",
        [DISPLAY_NAMES.get(col, col) for col in possible_features]
    )
    features = [REVERSE_DISPLAY_NAMES.get(col, col) for col in feature_display]
    
    # -----------------------------
    # RUN REGRESSION
    # -----------------------------
    
    if len(features) > 0:
    
        reg_df = filtered_df[[target] + features].dropna()
    
        X = reg_df[features]
        y = reg_df[target]
    
        # Add intercept
        X = sm.add_constant(X)
    
        # Fit model
        model = sm.OLS(y, X).fit()
    
        # -----------------------------
        # OUTPUTS
        # -----------------------------
        st.header("Regression Results")
    
        st.write(f"Days of data: {len(reg_df)}")
    
        st.write("### R-squared")
        st.write("This tells you how much of the variation in the outcome is explained by the predictors. Higher values (typically between 0.1 and 0.3) mean the predictors explain more of what affects the outcome, but it does not guarantee prediction accuracy.")
        st.write(round(model.rsquared, 3))

        st.write("### Coefficients")
        st.write("A 1-unit increase (or a yes answer) in a predictor is associated with a change in the outcome variable by the coefficient value, holding all other variables constant.")
        st.dataframe(model.params)
    
        st.write("### P-values")
        st.write("This indicates how likely it is that a relationship between a predictor and outcome is due to random chance. Smaller values (less than 0.1) suggest stronger evidence of a real association, but results should be interpreted cautiously given limited data.")
        st.dataframe(model.pvalues)
    
        # st.write("### Full Summary")
        # st.text(model.summary())
    
        # -----------------------------
        # ACTUAL VS PREDICTED
        # -----------------------------
        reg_df["Predicted"] = model.predict(X)
    
        fig, ax = plt.subplots()
    
        sns.scatterplot(
            x=reg_df[target],
            y=reg_df["Predicted"],
            ax=ax
        )
    
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title("Actual vs Predicted")
    
        st.pyplot(fig)
    
    else:
        st.warning("Please select at least one predictor variable.")
        
# -----------------------------
# TAB2: Classifications or something
# -----------------------------

with tab2:
    st.subheader("Beta Model- Not Enough Data")
    st.write("Use this tool to explore how different combinations of sleep, training, recovery, nutrition, and cycle factors are associated with specific outcomes.")

    st.header("Choose Prediction Target")
    target_options = ["Practice Feeling", "Overall Feeling", "Pain Location"]

    prac_feelings = ["bloated", "fast", "flat", "focused",
                     "frustrated", "hungry", "sore", "springy/exploseive","strong", "tired"]
    
    pain_loc = ["right_shin", "left_shin", "knee", "lower_back", "left_foot", "tight_hips", "traps", "general_body_soreness", "headache"]

    moods = ["Happy", "Stressed", "Anxious", "Tired", "Confident", "Sad"]
    
    
    target_display = st.selectbox(
        "Prediction Target",
        target_options
    )
    target_dict = {
        "Practice Feeling" : prac_feelings,
        "Overall Feeling": moods,
        "Pain Location": pain_loc
    }
    model_targets=target_dict.get(target_display)

    predict_features = [
        "Sleep_Hours",
        "Travel_day",
        "Comp_day",
        "Period_day",
        "Sleep_Quality",
        "Mood_Number",
        "Meals_Quality",
        "Alcoholic_Drinks",
        "Prac_Energy_Level",
        "Morning_Back_Pain",
        "sleep_lag1",
        "sleep_3day_avg",
        "Overall Feeling",
        "Practice Feeling",
        "Workout Type",
        "Relax/Recovery Activity",
        "Pain Location",
        "Protein Type",
        "Protein Type Night Prior"
    ]
    
    # Remove target from predictors
    predict_features = [x for x in predict_features if x != target_display]
    
    # -----------------------------
    # FEATURE SELECTION
    # -----------------------------
    st.header("Choose Input Variables")
    
    predict_feature_display = st.multiselect(
        "Features",
        [DISPLAY_NAMES.get(col, col) for col in predict_features]
    )
    predict_features = [REVERSE_DISPLAY_NAMES.get(col, col) for col in predict_feature_display]
    
    # input data based on feature

    if len(predict_features) > 0:
        filtered_df = df.copy()
        input_dict = {}
        model_features=[]
        for f in predict_features:
            st.write(f)
            if f in df.columns:
                model_features.append(f)
                if df[f].isin([0, 1]).all():
                    yn_response = st.radio(f"{DISPLAY_NAMES.get(f)}?", ("Yes", "No"))
                    if yn_response == "Yes":
                        input_dict[f] = 1
                    else:
                        input_dict[f] = 0
            
                if df[f].dropna().astype(int).all():
                    filtered_df[f] = filtered_df[f].astype('Int64')
                    f_min = df[f].dropna().astype(int).min()
                    f_max = df[f].dropna().astype(int).max()
                    f_slider = st.slider(label = f"Select {DISPLAY_NAMES.get(f)}", min_value = f_min, max_value = f_max, step=1)
                    input_dict[f] = f_slider
            else:
                if f == "Protein Type":
                    protein = st.radio("Protein Type", ("Chicken", "Beef", "Pork", "Salmon", "Other"))
                    protein_types = ["Chicken", "Beef", "Pork", "Salmon", "Other"]
                    other_proteins = [x for x in protein_types if x != protein]
                    model_features.append(protein)
                    input_dict[protein] = 1
    
                if f == "Protein Type Night Prior":
                    protein = st.radio("Protein Type (Previous Day)", ("Chicken", "Beef", "Pork", "Salmon", "Other"))
                    prior_protein_map = {
                        "Beef": "Beef_lag",
                        "Chicken": "Chicken_lag",
                        "Pork": "Pork_lag",
                        "Salmon": "Salmon_lag",
                        "Other": "Other_lag",
                    }
                    prior_protein = prior_protein_map[protein]
                    model_features.append(prior_protein)
                    input_dict[prior_protein] = 1
                    
                if f == "Pain Location":
                    pain_select = st.multiselect("Pain Location", [DISPLAY_NAMES.get(col,col) for col in pain_loc],
                                                default = [DISPLAY_NAMES.get(col,col) for col in pain_loc][0])
                    pain = [REVERSE_DISPLAY_NAMES.get(col,col) for col in pain_select]
                    other_pains = [x for x in pain_loc if x not in pain]
                    model_features+=pain
                    for p in pain:
                        input_dict[p] = 1
                    
                if f == "Workout Type" or f == "Workout_Type":
                    workout_types = ["Active Recovery","Jump", "Speed", "Off", "Premeet"]
                    workout = st.radio("Workout Type", ("Active Recovery","Jump", "Speed", "Off", "Premeet"))
                    other_workouts = [x for x in workout_types if x != workout]
                    model_features.append(workout)
                    input_dict[workout] = 1
                    
                if f == "Practice Feeling":
                    prac_feeling_select = st.multiselect("Practice Feelings", [DISPLAY_NAMES.get(col,col) for col in prac_feelings],
                                                        default = [DISPLAY_NAMES.get(col,col) for col in prac_feelings][0])
                    prac_feel = [REVERSE_DISPLAY_NAMES.get(col,col) for col in prac_feeling_select]
                    other_feels = [x for x in prac_feelings if x not in prac_feel]
                    model_features+=prac_feel
                    for p in prac_feel:
                        input_dict[p] = 1
                    
                if f == "Overall Feeling":
                    mood_select = st.multiselect("Overall Feeling", [DISPLAY_NAMES.get(col,col) for col in moods],
                                               default = [DISPLAY_NAMES.get(col,col) for col in moods][0])
                    mood = [REVERSE_DISPLAY_NAMES.get(col,col) for col in mood_select]
                    other_moods = [x for x in moods if x not in mood]
                    model_features+=mood
                    for m in mood:
                        input_dict[m] = 1
                
                if f == "Relax/Recovery Activity" or f == "RR_Act":
                    rr_acts = ["boots", "journaled","pressure_tension_release","red_light","rolling","stim/tens","time_outside","time_w_god"]
                    rr_select = st.multiselect("Relax/Recovery Acitivty", [DISPLAY_NAMES.get(col,col) for col in rr_acts],
                                               default = [DISPLAY_NAMES.get(col,col) for col in rr_acts][0])
                    rr = [REVERSE_DISPLAY_NAMES.get(col,col) for col in rr_select]
                    model_features += rr
                    for r in rr:
                        input_dict[r] = 1
    
        input_df = pd.DataFrame([input_dict])
        input_df = input_df.reindex(columns=model_features, fill_value=0)
        X = df[model_features].copy()
        X = X.fillna(0)
        models = {}
        na_data = []
        for outcome in model_targets:
            y=df[outcome]
        # skip outcomes with too little data
            if y.sum() < 5:
                na_data.append(outcome)
                continue
        
            model = LogisticRegression(max_iter=500)
            model.fit(X, y)
        
            models[outcome] = model
    
        results = {}
        for outcome, model in models.items():
            prob = model.predict_proba(input_df)[0][1]
            results[outcome] = prob
        
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
        st.write(f"Interpretation: The percentages below represent the estimated probability of experiencing each {target_display} based on the selected inputs.")
        for k, v in sorted_results.items():
            st.write(f"{DISPLAY_NAMES.get(k, k)}: {v:.0%}")
            
        st.write(f"Not enough data on {[DISPLAY_NAMES.get(y) for y in na_data]} for prediction.")

        feature_importance = {}

        for outcome, model in models.items():
            coefs = model.coef_[0]
        
            for feature, coef in zip(model_features, coefs):
                if feature not in feature_importance:
                    feature_importance[feature] = []
        
                feature_importance[feature].append(abs(coef))
        avg_importance = {}

        for feature, values in feature_importance.items():
            avg_importance[feature] = sum(values) / len(values)

        ranked_features = sorted(
        avg_importance.items(),
        key=lambda x: x[1],
        reverse=True
        )

        top_features = ranked_features[:5]

        st.subheader("Factor Influence")
        
        for feature, importance in top_features:
            display_name = DISPLAY_NAMES.get(feature, feature)
        
            if importance >= 1.0:
                text = "appears strongly related"
            elif importance >= 0.4:
                text = "shows a moderate relationship"
            else:
                text = "shows a weak relationship"
        
            st.write(f"• {display_name} {text} to the predicted outcomes.")
        
    else:
        st.warning("Please select at least one input variable.")


