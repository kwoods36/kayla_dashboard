import pandas as pd
import streamlit as st

@st.cache_data

def display_names():
    DISPLAY_NAMES = {
    # Dates
    "Survey_Date": "Date",
    
    # Core wellness
    "Mood_Number": "Overall Mood",
    "Sleep_Hours": "Sleep Hours",
    "Sleep_Quality": "Sleep Quality",
    "Meals_Quality": "Nutrition Quality",
    "Prac_Energy_Level": "Practice Energy",
    "Prac_energy_next_day": "Next Day Practice Energy",
    "Prac_Feel": "Practice Feeling Description",
    "Mood_Descript": "Mood Description",
    
    # Context
    "Comp_day": "Competition Day",
    "Travel_day": "Travel Day",
    "Period_day": "Period Day",
    "Alcoholic_Drinks": "Alcoholic Drinks",
    
    # Workout types
    "Workout_Type":"Workout Type",
    "Active Recovery": "Active Recovery Workout",
    "Comp": "Competition",
    "Jump": "Jump Session",
    "Off": "Rest Day",
    "Premeet": "Pre-Meet Workout",
    "Speed": "Speed Workout",
    
    # Event-specific competition fields
    "TJ_Comp": "Triple Jump Competition",
    "LJ_Comp": "Long Jump Competition",
    
    # Recovery activities
    "RR_Act": "Relax/Recovery Activity",
    "boots": "Recovery Boots",
    "journaled": "Journaling",
    "pressure_tension_release": "Pressure/Tension Release",
    "red_light": "Red Light Therapy",
    "rolling": "Foam Rolling",
    "stim/tens": "Stim/TENS",
    "time_outside": "Time Outside",
    "time_w_god": "Time with God",
    
    # Protein sources
    "Beef": "Ate Beef",
    "Chicken": "Ate Chicken",
    "Pork": "Ate Pork",
    "Salmon": "Ate Salmon",
    "Other": "Ate Other Protein Source",
    "Beef_lag": "Ate Beef (Previous Day)",
    "Chicken_lag": "Ate Chicken (Previous Day)",
    "Pork_lag": "Ate Pork (Previous Day)",
    "Salmon_lag": "Ate Salmon (Previous Day)",
    "Other_lag": "Ate Other Protein Source (Previous Day)",
    
    # Mood tags
    "Anxious": "Felt Anxious",
    "Confident": "Felt Confident",
    "Happy": "Felt Happy",
    "Sad": "Felt Sad",
    "Stressed": "Felt Stressed",
    "Tired": "Felt Tired",
    
    # Practice feeling tags
    "bloated": "Felt Bloated",
    "fast": "Felt Fast",
    "flat": "Felt Flat",
    "focused": "Felt Focused",
    "frustrated": "Felt Frustrated",
    "hungry": "Felt Hungry",
    "sore": "Felt Sore",
    "springy/exploseive": "Felt Springy/Explosive",
    "strong": "Felt Strong",
    "tired": "Felt Tired at Practice",
    
    # Pain areas
    "cramps": "Cramps",
    "general_body_soreness": "General Body Soreness",
    "headache": "Headache",
    "knee": "Knee Pain",
    "left_shin": "Left Shin Pain",
    "left_foot": "Left Foot Pain",
    "lower_back": "Lower Back Pain",
    "right_shin": "Right Shin Pain",
    "tight_hips": "Tight Hips",
    "traps": "Trap Pain/Tightness",
    "Morning_Back_Pain": "Morning Back Pain",
    "Next_Morning_Back_Pain": "Next Morning Back Pain",
    
    # Sleep trends
    "sleep_lag1": "Previous Night Sleep",
    "sleep_lag2": "Sleep Two Nights Ago",
    "sleep_3day_avg": "Sleep (3-Day Average)",
    "sleep_5day_avg": "Sleep (5-Day Average)",
    "Sleep_Next_Night": "Next Night Sleep",
    
    # Cycle tracking
    "cycle_day_in_period": "Day of Period",
    "cycle_phase_detail": "Detailed Cycle Phase",
    "is_period": "On Period",
    "period_start": "First Day of Period",
    "cycle_id": "Cycle Number",
    "cycle_day": "Cycle Day",
    "cycle_phase": "Cycle Phase",
    "days_until_period": "Days Until Next Period",

    
    # Summary metrics
    "total_pain": "Total Pain Score"
    }
    return DISPLAY_NAMES