"""
Multi-module project simulation — used in Notebook 03 (Advanced Debugging).

Simulates a real project with data_loader → processor → reporter pipeline.
Each module is a class so we can demonstrate cross-file stepping.
"""


# --- data_loader.py -----------------------------------------------------------

def load_records(source: str) -> list[dict]:
    """Simulate loading records from an external source."""
    raw = [
        {"id": 1, "name": "Alice", "score": "95"},
        {"id": 2, "name": "Bob", "score": "invalid"},  # bad data
        {"id": 3, "name": "Charlie", "score": "78"},
        {"id": 4, "name": None, "score": "88"},  # missing name
    ]
    print(f"[data_loader] Loaded {len(raw)} records from '{source}'")
    return raw


# --- processor.py -------------------------------------------------------------

def validate_record(record: dict) -> bool:
    """Check if a record has all required valid fields."""
    if not record.get("name"):
        return False
    try:
        int(record["score"])
        return True
    except (ValueError, KeyError):
        return False


def process_records(records: list[dict]) -> list[dict]:
    """Validate and transform records."""
    processed = []
    for record in records:
        if validate_record(record):
            processed.append({
                "id": record["id"],
                "name": record["name"].upper(),
                "score": int(record["score"]),
            })
    return processed


# --- reporter.py --------------------------------------------------------------

def generate_report(data: list[dict]) -> str:
    """Create a formatted report from processed data."""
    lines = ["=" * 40, "STUDENT REPORT", "=" * 40]
    for item in data:
        lines.append(f"  {item['name']}: {item['score']} points")
    lines.append(f"\nTotal students: {len(data)}")
    avg = sum(d["score"] for d in data) / len(data) if data else 0
    lines.append(f"Average score: {avg:.1f}")
    return "\n".join(lines)


# --- pipeline entry point -----------------------------------------------------

def run_pipeline(source: str = "students.csv") -> None:
    records = load_records(source)
    clean = process_records(records)
    report = generate_report(clean)
    print(report)


if __name__ == "__main__":
    run_pipeline()
