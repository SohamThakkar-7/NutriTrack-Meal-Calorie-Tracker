"""Quick smoke test for NLP + diet modules — no file upload needed."""
import sys
sys.path.insert(0, ".")

from helpers.medical_nlp import extract_and_classify
from helpers.report_diet import get_diet_recommendations, generate_summary

SAMPLE_TEXT = """
LABORATORY REPORT
Patient: Test User
Date: 25 Apr 2026

Complete Blood Count:
  Hemoglobin (Hb): 10.8 g/dL    [Reference: 12.0-16.0]

Vitamins Panel:
  Vitamin B12: 185 pg/mL         [Reference: 200-900]

Anthropometric:
  BMI: 27.3 kg/m2                [Reference: 18.5-24.9]
"""

def run():
    print("=" * 55)
    print("NutriTrack — Medical NLP Smoke Test")
    print("=" * 55)

    metrics = extract_and_classify(SAMPLE_TEXT)
    print("\n[METRICS]")
    for name, data in metrics.items():
        print(f"  {name:15s} value={data['value']}  unit={data['unit']}  status={data['status']}")

    plan = get_diet_recommendations(metrics)
    print(f"\n[DIET PLAN] — {len(plan)} condition(s) triggered")
    for entry in plan:
        print(f"  Condition  : {entry['condition']}")
        print(f"  First rec  : {entry['recommendations'][0]}")
        print()

    summary = generate_summary(metrics, plan)
    print("[SUMMARY]")
    print(summary)
    print("=" * 55)
    print("PASS — all modules imported and executed correctly")

if __name__ == "__main__":
    run()
