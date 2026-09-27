import pandas as pd
import numpy as np

def clean_dataset():
    """"Cleans and standardizes raw datasets based on audit findings."""
    print("Stage 3: DATA CLEANING & TRANSFORMATION\n" + "="*40)

    # 1. Load raw datasets
    df_members = pd.read_csv("raw_members.csv")
    df_checkins = pd.read_csv("raw_checkins.csv")

    # Members csv clean up
    # Drop exact row duplicates
    df_members.drop_duplicates(inplace=True)

    # Fix negative fees: convert to absolute values
    df_members["monthly_fee"] = df_members["monthly_fee"].abs()

    # Standardize membership_tier casing and fill nulls with 'Basic'
    df_members["membership_tier"] = df_members["membership_tier"].str.capitalize()
    df_members["membership_tier"] = df_members["membership_tier"].fillna("Basic")

    # Ensure 'join_date' is datetime
    df_members["join_date"] = pd.to_datetime(df_members["join_date"])

    # Check-ins csv clean up
    # Drop orphan check-ins (foreign key enforcement)
    valid_ids = set(df_members["member_id"].unique())
    df_checkins = df_checkins[df_checkins["member_id"].isin(valid_ids)]

    # Fix negative durations: convert to absolute values
    df_checkins["duration_minutes"] = df_checkins["duration_minutes"].abs()

    # Fill missing workout types with 'General Gym'
    df_checkins["workout_type"] = df_checkins["workout_type"].fillna("General Gym")

    # Convert checkin_datetime to datetime type
    df_checkins["checkin_datetime"] = pd.to_datetime(df_checkins["checkin_datetime"])

    # 4. Sve the datasets
    df_members.to_csv("clean_members.csv", index=False)
    df_checkins.to_csv("clean_checkins.csv", index=False)

if __name__ == "__main__":
    clean_dataset()
