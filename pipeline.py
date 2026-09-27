import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker and lock random seeds for reproducible data generation
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)


def generate_members(num_members=10000):
    """Generates realistic gym member profiles using Faker."""
    
    # 1. Format member IDs as zero-padded numbers: MEMBER-00001 to MEMBER-10000
    member_ids = [f"MEMBER-{i+1:05d}" for i in range(num_members)]
    
    # 2. Categorical choices with intentional casing bugs and nulls
    tiers = ["Basic", "Premium", "VIP", "BASIC", None]
    statuses = ["Active", "Cancelled", "Frozen", "Active"]
    
    data = []  # List to hold member profile dictionaries
    
    # 3. Loop to generate rich member records
    for member_id in member_ids:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        phone = fake.phone_number()
        join_date = fake.date_between(start_date="-2y", end_date="today")
        tier = random.choice(tiers)
        status = random.choice(statuses)
        monthly_fee = random.choice([29.99, 59.99, 99.99, -29.99])  # Injected negative fee anomaly
        
        data.append({
            "member_id": member_id,
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "phone": phone,
            "membership_tier": tier,
            "status": status,
            "join_date": join_date,
            "monthly_fee": monthly_fee
        })
        
    df = pd.DataFrame(data)
    
    # 4. Duplicate the first 15 rows to test duplication detection at scale
    df = pd.concat([df, df.iloc[:15]], ignore_index=True)
    return df


def generate_checkins(member_df, num_checkins=100000):
    """Generates check-in activity logs referencing member profiles."""
    
    # 1. Pull valid member IDs from the generated members DataFrame
    valid_members = member_df["member_id"].dropna().unique().tolist()
    
    # 2. Inject 100 orphan member IDs (MEMBER-99001 to MEMBER-99100) for foreign key violation testing
    orphan_members = [f"MEMBER-{99001 + i:05d}" for i in range(100)]
    all_member_pool = valid_members + orphan_members
    
    data = []  # List to hold check-in dictionaries
    start_date = datetime(2026, 1, 1)
    workout_types = ["Weights", "Cardio", "HIIT", "Yoga", "Spin", None]
    
    # 3. Loop to simulate high-volume gym check-ins
    for i in range(num_checkins):
        checkin_id = f"CHK-{i+1:06d}"  # Format: CHK-000001 to CHK-100000
        member_id = random.choice(all_member_pool)
        checkin_days = random.randint(0, 60)
        hour = random.choice([5, 6, 7, 8, 12, 16, 17, 18, 19, 20, 21])
        checkin_time = start_date + timedelta(days=checkin_days, hours=hour)
        workout = random.choice(workout_types)
        duration_mins = random.choice([30, 45, 60, 120, -15])  # Injected negative duration anomaly
        
        data.append({
            "checkin_id": checkin_id,
            "member_id": member_id,
            "checkin_datetime": checkin_time,
            "workout_type": workout,
            "duration_minutes": duration_mins
        })
        
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Generating large-scale synthetic data for Bradley's Gym...")
    
    # 1. Execute generation functions for 10,000 members and 100,000 check-ins
    df_members = generate_members(num_members=10000)
    df_checkins = generate_checkins(df_members, num_checkins=100000)
    
    # 2. Export generated DataFrames to raw CSV files
    df_members.to_csv("raw_members.csv", index=False)
    df_checkins.to_csv("raw_checkins.csv", index=False)
    
    # 3. Output completion to terminal
    print(f"Created 'raw_members.csv' with {len(df_members)} records.")
    print(f"Created 'raw_checkins.csv' with {len(df_checkins)} records.")

