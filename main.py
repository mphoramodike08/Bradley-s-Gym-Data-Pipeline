import time
import pipeline
import audit_data
import clean_data
import analyze_data

def run_end_to_end_pipeline():
    """Executes all stages of Bradley's Gym Data Pipeline in sequence."""
    start_time = time.time()
    
    print("🚀 STARTING BRADLEY'S GYM ENTERPRISE DATA PIPELINE")
    print("=" * 60)
    
    # Stage 1: Data Generation
    print("\n[STAGE 1/4] Generating Raw Synthetic Datasets...")
    df_members = pipeline.generate_members(num_members=10000)
    df_checkins = pipeline.generate_checkins(df_members, num_checkins=100000)
    df_members.to_csv("raw_members.csv", index=False)
    df_checkins.to_csv("raw_checkins.csv", index=False)
    print("✅ Raw datasets generated and written to disk.")
    
    # Stage 2: Data Audit
    print("\n[STAGE 2/4] Executing Raw Data Audit & Profiling...")
    audit_data.audit_dataset()
    
    # Stage 3: Data Cleaning & Transformation
    print("\n[STAGE 3/4] Running Data Cleaning & Foreign Key Enforcement...")
    clean_data.clean_dataset()
    
    # Stage 4: Analytics Warehousing
    print("\n[STAGE 4/4] Running Analytical Queries in DuckDB...")
    analyze_data.run_analytics()
    
    elapsed_time = round(time.time() - start_time, 2)
    print("\n" + "=" * 60)
    print(f"🎉 PIPELINE EXECUTION COMPLETE IN {elapsed_time} SECONDS!")

if __name__ == "__main__":
    run_end_to_end_pipeline()