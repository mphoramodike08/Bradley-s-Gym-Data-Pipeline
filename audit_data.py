import pandas as pd

def audit_dataset():
    """Audits raw members and check-ins datasets for quality anomalies."""
    print("STAGE 2: DATA AUDITING & PROFILING")

    # 1. Load the generated raw CSV datasets into pandas DataFrame
    df_members = pd.read_csv("raw_members.csv")
    df_checkins = pd.read_csv("raw_checkins.csv")

    print(f"Members Dataset Shape: {df_members.shape[0]} rows, {df_members.shape[1]} columns")
    print(f"Checkins Dataset Shape: {df_checkins.shape[0]} rows, {df_checkins.shape[1]} columns\n")

    # 2. Audit Members Table
    print("--- MEMBER PROFILES AUDIT ---")
    member_nulls = df_members.isnull().sum()
    member_dupes = df_members.duplicated().sum()
    invalid_fees = (df_members["monthly_fee"] < 0).sum()
    inconsistent_tiers = df_members["membership_tier"].value_counts(dropna=False).to_dict()

    print(f"Missing Values per Column:\n{member_nulls.to_string()}")
    print(f"Duplicated Member Rows: {member_dupes}")
    print(f"Invalid Negative Fees (< $0): {invalid_fees}")
    print(f"Membership Tier Breakdown (Note casting & nulls): {inconsistent_tiers}")

    # 3. Audit Check-Ins Table a& Referential Integrity
    print("--- CHECK-IN LOGS AUDIT ---")
    checkin_nulls = df_checkins.isnull().sum()
    invalid_durations = (df_checkins["duration_minutes"] < 0).sum()

    # Check Referential Integrity: Find check-ins referencing non-existing members
    valid_member_ids = set(df_members["member_id"].dropna().unique())
    orphan_checkins = (~df_checkins["member_id"].isin(valid_member_ids)).sum()

    print(f"Missing Values per Column:\n{checkin_nulls.to_string()}")
    print(f"Invalid Negative Durations (< 0 mins): {invalid_durations}")
    print(f"Orphan Check-Ins (Foreign Key Violations): {orphan_checkins}")

if __name__ == "__main__":
    audit_dataset()
