"""
Sample project with intentional bugs — used throughout the debugging masterclass.

Covers every concept across the three notebooks:
  - Part 1 (Fundamentals): breakpoints, variables, watch, stepping
  - Part 2 (Intermediate): conditional breakpoints, logpoints, call stack
  - Part 3 (Advanced): exceptions, Debug Console, multi-bug challenge

Usage (from the debug/ folder):
    python debug_example.py
"""


def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.

    Bug: off-by-one — the loop starts at index 1 instead of 0,
    so the first element is never added to the total.
    """
    total = 0.0
    for i in range(1, len(numbers)):  # BUG: should be range(0, ...)
        total += numbers[i]
    return total / len(numbers)


def find_max_profit(prices: list[float]) -> float:
    """Find the maximum single-buy/sell profit from a price series.

    Bug: the comparison inside the loop checks against min_price
    instead of max_profit, so large profits are missed.
    """
    min_price = prices[0]
    max_profit = 0.0

    for price in prices:
        if price < min_price:
            min_price = price
        profit = price - min_price
        if profit > min_price:  # BUG: should be `profit > max_profit`
            max_profit = profit

    return max_profit


def count_vowels(text: str) -> dict[str, int]:
    """Count occurrences of each vowel in text.

    Bug: the vowel set has 'a' duplicated and 'u' missing.
    """
    vowels = "aeioa"  # BUG: 'a' duplicated, 'u' missing → should be "aeiou"
    counts: dict[str, int] = {}
    for char in text.lower():
        if char in vowels:
            counts[char] = counts.get(char, 0) + 1
    return counts


# ===========================================================================
# PART 2 — Intermediate: conditional breakpoints, logpoints, call stack
# ===========================================================================

def audit_transactions(transactions: list[dict]) -> dict:
    """Audit a list of financial transactions.

    Practice:
      - Conditional breakpoint on `total += t["amount"]`
        with expression:  t["user"] == "charlie" and t["amount"] > 1000
      - Logpoint on the same line with message:
        {t["user"]}: ${t["amount"]:.2f} | running total: ${total:.2f}
    """
    total = 0.0
    suspicious: list[dict] = []
    by_user: dict[str, float] = {}

    for t in transactions:
        total += t["amount"]
        by_user[t["user"]] = by_user.get(t["user"], 0) + t["amount"]
        if t["amount"] > 500:
            suspicious.append(t)

    return {"total": total, "suspicious": suspicious, "by_user": by_user}


def factorial(n: int) -> int:
    """Recursive factorial — set a breakpoint on the return line
    and watch the Call Stack grow with each recursive call.

    Click different frames in the Call Stack panel to see `n`
    at each recursion level.
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# ===========================================================================
# PART 3 — Advanced: exceptions, Debug Console, final challenge
# ===========================================================================

import json  # noqa: E402


def parse_config(raw: str) -> dict:
    """Parse a JSON config and validate required keys.

    Practice exception breakpoints:
      - "Raised Exceptions" → pauses at json.loads() before except catches it
      - "Uncaught Exceptions" → pauses at ValueError for missing keys
    """
    try:
        config = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    required = ["name", "version", "settings"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Missing keys: {missing}")
    return config


def compute_metrics(values: list[float]) -> dict:
    """Compute basic stats — crashes on all-negative input.

    Bug: count only includes positive values, so if all are negative
    count=0 and division by zero occurs.
    """
    total = sum(values)
    count = len([v for v in values if v > 0])  # BUG: zero when all negative
    return {"total": total, "count": count, "average": total / count}


def analyze_sales(data: list[dict]) -> dict:
    """Analyze product sales — use the Debug Console while paused here.

    Debug Console experiments:
      len(data)
      [d for d in data if d["category"] == "electronics"]
      sum(d["price"] * d["quantity"] for d in data)
      data[0]["price"] = 9999.99   ← modify, then Continue
    """
    total_revenue = 0.0
    by_category: dict[str, float] = {}

    for item in data:
        revenue = item["price"] * item["quantity"]
        total_revenue += revenue
        cat = item["category"]
        by_category[cat] = by_category.get(cat, 0) + revenue

    return {
        "total_revenue": total_revenue,
        "by_category": by_category,
        "top_category": max(by_category, key=by_category.get),
    }


from datetime import datetime, timedelta  # noqa: E402


def days_between(start: str, end: str) -> int:
    """Count business days (Mon-Fri) between two dates.

    Bug: weekday check includes Saturday (should be < 5, not < 6).
    """
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    biz = 0
    cur = s
    while cur <= e:
        if cur.weekday() < 6:  # BUG: should be < 5 (Sat=5, Sun=6)
            biz += 1
        cur += timedelta(days=1)
    return biz


def calculate_salary(employees: list[dict]) -> list[dict]:
    """Calculate gross salary and tax for each employee.

    Contains 2 bugs:
      - overtime formula applies `* rate` twice
      - `if` instead of `elif` makes high earners get wrong tax bracket
    """
    results = []
    for emp in employees:
        hours, rate = emp["hours"], emp["rate"]

        if hours > 40:
            regular = 40 * rate
            overtime = (hours - 40) * rate * 1.5
            total = regular + overtime * rate  # BUG: extra `* rate`
        else:
            total = hours * rate

        if total > 5000:
            tax = total * 0.30
        if total > 3000:  # BUG: should be `elif`
            tax = total * 0.20
        else:
            tax = total * 0.10

        results.append({"name": emp["name"], "gross": round(total, 2), "tax": round(tax, 2)})
    return results


# ---------------------------------------------------------------------------
# Main — run all examples
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # === PART 1 — Fundamentals =============================================
    print("=" * 60)
    print("PART 1 — Breakpoints, Variables, Watch, Stepping")
    print("=" * 60)

    data = [10, 20, 30, 40, 50]
    avg = calculate_average(data)
    print(f"Average of {data}: {avg}")  # Expected: 30.0

    stock_prices = [7, 1, 5, 3, 6, 4]
    profit = find_max_profit(stock_prices)
    print(f"Max profit: {profit}")  # Expected: 5

    sentence = "The quick brown fox jumps over the lazy dog"
    vowel_counts = count_vowels(sentence)
    print(f"Vowel counts: {vowel_counts}")  # Expected: includes 'u'

    # === PART 2 — Intermediate =============================================
    print()
    print("=" * 60)
    print("PART 2 — Conditional breakpoints, Logpoints, Call Stack")
    print("=" * 60)

    transactions = [
        {"user": "alice",   "amount": 120.50,  "type": "purchase"},
        {"user": "bob",     "amount": 890.00,  "type": "transfer"},
        {"user": "alice",   "amount": 45.99,   "type": "purchase"},
        {"user": "charlie", "amount": 1500.00, "type": "withdrawal"},
        {"user": "bob",     "amount": 200.00,  "type": "purchase"},
        {"user": "alice",   "amount": 675.25,  "type": "transfer"},
        {"user": "diana",   "amount": 50.00,   "type": "deposit"},
        {"user": "charlie", "amount": 2200.00, "type": "transfer"},
    ]
    report = audit_transactions(transactions)
    print(f"Total: ${report['total']:.2f}")
    print(f"Suspicious: {len(report['suspicious'])}")

    print(f"5! = {factorial(5)}")

    # === PART 3 — Advanced =================================================
    print()
    print("=" * 60)
    print("PART 3 — Exceptions, Debug Console, Final Challenge")
    print("=" * 60)

    # Exception debugging
    try:
        parse_config('{"name": "app", version: 1}')  # invalid JSON
    except ValueError as e:
        print(f"Handled: {e}")

    # Uncomment to trigger ZeroDivisionError:
    # compute_metrics([-5, -3, 0, -1])

    # Debug Console practice
    sales = [
        {"product": "Laptop",     "category": "electronics", "price": 999.99, "quantity": 3},
        {"product": "Headphones", "category": "electronics", "price": 149.99, "quantity": 12},
        {"product": "Desk Chair", "category": "furniture",   "price": 299.99, "quantity": 5},
        {"product": "Monitor",    "category": "electronics", "price": 449.99, "quantity": 7},
        {"product": "Notebook",   "category": "stationery",  "price": 12.99,  "quantity": 50},
    ]
    result = analyze_sales(sales)  # ← set breakpoint here, use Debug Console
    print(f"Revenue: ${result['total_revenue']:,.2f} | Top: {result['top_category']}")

    # Final challenge — 3 bugs
    print()
    print("Business days Mar 2-13 2026:", days_between("2026-03-02", "2026-03-13"))  # expect 10

    employees = [
        {"name": "Alice",   "hours": 45, "rate": 50.0},
        {"name": "Bob",     "hours": 38, "rate": 35.0},
        {"name": "Charlie", "hours": 52, "rate": 75.0},
        {"name": "Diana",   "hours": 40, "rate": 60.0},
    ]
    for emp in calculate_salary(employees):
        print(f"  {emp['name']:10s} | Gross: ${emp['gross']:>10,.2f} | Tax: ${emp['tax']:>8,.2f}")
