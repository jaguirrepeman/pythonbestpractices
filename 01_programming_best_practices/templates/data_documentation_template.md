# Data Documentation Template

> **Template:** Copy this file and adapt it for each dataset in your project.

---

## Dataset: `[dataset_name]`

### Overview

| Field | Value |
|-------|-------|
| **Name** | `dataset_name` |
| **Description** | [What does this dataset represent?] |
| **Source** | [Where does the data come from?] |
| **Owner** | [Team / person responsible] |
| **Update frequency** | [Real-time / Daily / Weekly / Monthly / One-time] |
| **Granularity** | [1 row = 1 X × 1 Y × 1 Z] |
| **Approximate row count** | [~N rows] |
| **Time range** | [YYYY-MM-DD to present / YYYY-MM-DD to YYYY-MM-DD] |
| **Partitioned by** | [Column name or N/A] |
| **Format** | [Parquet / CSV / JSON / Delta / etc.] |
| **Location** | [s3://bucket/path/ or local path] |
| **Sensitivity** | [Public / Internal / Confidential / Restricted] |

---

### Data Dictionary

| # | Column Name | Type | Nullable | Description | Constraints | Example | Foreign Key |
|---|------------|------|----------|-------------|-------------|---------|-------------|
| 1 | `date` | DATE | No | Date of the record | — | 2026-01-15 | — |
| 2 | `entity_id` | STRING | No | Unique identifier for entity | — | ENT-001 | `entities.id` |
| 3 | `metric_value` | DECIMAL(12,2) | No | Primary metric value | >= 0 | 1259.99 | — |
| 4 | `category` | STRING | Yes | Category classification | One of: A, B, C | B | `categories.code` |
| 5 | `is_flag` | BOOLEAN | No | Whether condition X applies | — | true | — |

---

### Quality Rules

| # | Rule | Severity | Automated |
|---|------|----------|-----------|
| 1 | No nulls in primary key columns | Critical | ✅ Yes |
| 2 | `metric_value >= 0` | Critical | ✅ Yes |
| 3 | `date <= current_date` | Warning | ✅ Yes |
| 4 | No duplicate primary key combinations | Critical | ✅ Yes |
| 5 | Row count within ±10% of historical average | Warning | ✅ Yes |
| 6 | All `entity_id` values exist in reference table | Error | ✅ Yes |

#### Quality monitoring tool

- [ ] Great Expectations
- [ ] Soda
- [ ] dbt tests
- [ ] Custom Python scripts
- [ ] Other: ___

---

### Data Lineage

#### Upstream (sources)

| Dataset | Description | Owner |
|---------|-------------|-------|
| `raw_source_1` | Raw data from source system | Data Engineering |
| `reference_table` | Reference/dimension data | Data Engineering |

#### Downstream (consumers)

| Dataset / System | Description | Owner |
|-----------------|-------------|-------|
| `feature_table` | Features for ML model | Data Science |
| `dashboard_x` | Analytics dashboard | BI Team |

#### Lineage diagram

```
[Source System A] ──→ [Raw Landing] ──→ [Cleaned Data] ──→ [This Dataset]
                                                               │
                                                    ┌──────────┼──────────┐
                                                    ▼          ▼          ▼
                                              [Features]  [Dashboard]  [Report]
```

---

### Transformations Applied

| Step | Description | Logic / SQL | Input | Output |
|------|-------------|-------------|-------|--------|
| 1 | Deduplication | Remove exact duplicate rows | raw_source | deduped |
| 2 | Null handling | Fill nulls in metric_value with 0 | deduped | clean |
| 3 | Aggregation | SUM(metric_value) GROUP BY date, entity_id | clean | aggregated |
| 4 | Join reference | LEFT JOIN with reference_table on entity_id | aggregated | enriched |

---

### Access & Permissions

| Role | Access Level | How to Request |
|------|-------------|---------------|
| Data Science Team | Read/Write | Automatic |
| BI Team | Read-only | Request via Jira |
| External partners | No access | N/A |

---

### SLA & Freshness

| Metric | Value |
|--------|-------|
| **Data available by** | 06:00 UTC (T+1) |
| **Maximum acceptable delay** | 2 hours |
| **Alerting** | PagerDuty / Slack #data-alerts |
| **Backfill policy** | Automated for last 7 days; manual for older |

---

### Change History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-01 | Initial documentation | [Name] |
| 2026-03-01 | Added quality rules | [Name] |

---

### Notes

<!-- Any additional context, known issues, or caveats -->

- Known issue: [describe any known data quality issues]
- Caveat: [describe any limitations or edge cases]
