import pandas as pd
import duckdb

def run_analytics():
    """Loads clean datasets into DuckDB and runs analytical SQL queries."""
    print("STAGE 4: DATA WAREHOUSING & ANALYTICS (DUCKDB)\n"+"="*50)

    # 1. Load cleaned datasets
    df_members = pd.read_csv("clean_members.csv")
    df_checkins = pd.read_csv("clean_checkins.csv")

    # Ensure correct datetime parsing
    df_members["join_date"] = pd.to_datetime(df_members["join_date"])
    df_checkins["checkin_datetime"] = pd.to_datetime(df_checkins["checkin_datetime"])

    # 2. Register DataFrames as SQL tables in DuckDB
    con = duckdb.connect(database="memory")
    con.register("members", df_members)
    con.register("checkins", df_checkins)

    # --- QUERY 1: Monthly Recurring Revenue (MRR) by Membership Tier ---
    print("\n Query 1: Monthly Revenue & Member Count by Tier")
    q1 = """
        SELECT 
            membership_tier, 
            COUNT(member_id) AS total_members,
            ROUND(SUM(monthly_fee), 2) AS total_monthly_revenue,
            ROUND(AVG(monthly_fee), 2) AS avg_fee_per_month
        FROM members
        WHERE status = 'Active'
        GROUP BY membership_tier
        ORDER BY total_monthly_revenue;
    """
    print(con.execute(q1).fetchdf().to_string(index=False))

    # --- QUERY 2: Peak Workout Hours ---
    q2 = """
        SELECT
            EXTRACT(HOUR FROM checkin_datetime) AS checkin_hour,
            COUNT(checkin_id) AS total_checkins,
            ROUND(AVG(duration_minutes), 1) AS avg_duration_mins
        FROM checkins
        GROUP BY checkin_hour
        ORDER BY total_checkins DESC
        LIMIT 5;
    """
    print(con.execute(q2).fetchdf().to_string(index=False))

    # --- QUERY 3: Most Popular Workout Activities ---
    print("\n Query 3: Most Popular Workout Types")
    q3 = """
        SELECT 
            workout_type, 
            COUNT(checkin_id) AS session_count,
            ROUND(SUM(duration_minutes) / 60.0, 1)AS total_hours_logged
        FROM checkins 
        GROUP BY workout_type
        ORDER BY session_count DESC;
    """
    print(con.execute(q3).fetchdf().to_string(index=False))

    # --- QUERY 4: Member Engagement (Top 5 Gym Enthusiasts)
    print("\n Query 4: Top 5 Most Active Gym Members")
    q4 = """
        SELECT 
            m.member_id,
            m.full_name, 
            m.membership_tier,
            COUNT(c.checkin_id) AS total_checkins,
            SUM(c.duration_minutes) AS total_minutes_spent
        FROM members m
        JOIN checkins c ON m.member_id = c.member_id
        GROUP BY m.member_id, m.full_name, m.membership_tier
        ORDER BY total_checkins DESC
        LIMIT 5;    
    """
    print(con.execute(q4).fetchdf().to_string(index=False))

if __name__ == "__main__":
    run_analytics()
