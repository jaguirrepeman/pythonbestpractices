"""Docstring Examples — Google Style Reference.

This module provides comprehensive examples of Google Style docstrings
for every type of Python construct. Use these as copy-paste templates
when writing documentation for your own code.

All examples follow the conventions validated by `pydocstyle --convention=google`
and are compatible with mkdocstrings for automatic API documentation generation.

Usage:
    Use the autoDocstring VS Code extension configured with:
        "autoDocstring.docstringFormat": "google"

    Validate with:
        $ pydocstyle --convention=google docstring_examples.py

Author:
    Data Science Team

Since:
    v1.0.0
"""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generator

import pandas as pd


# =============================================================================
# 1. MODULE-LEVEL CONSTANTS
# =============================================================================

#: Default number of lag periods for time series feature generation.
DEFAULT_LAG_PERIODS: list[int] = [1, 7, 14, 28]

#: Maximum allowed line length in characters.
MAX_LINE_LENGTH: int = 120

#: Supported file formats for data loading.
SUPPORTED_FORMATS: set[str] = {"csv", "parquet", "json", "feather"}


# =============================================================================
# 2. ENUMS
# =============================================================================


class ModelStatus(Enum):
    """Status of a machine learning model in the lifecycle.

    Each status represents a stage in the model's journey from
    development to retirement.

    Attributes:
        DRAFT: Model is under development, not yet validated.
        VALIDATED: Model has passed validation criteria.
        DEPLOYED: Model is actively serving predictions.
        DEPRECATED: Model is scheduled for retirement.
        RETIRED: Model is no longer in use.

    Example:
        >>> status = ModelStatus.DEPLOYED
        >>> status.is_active()
        True
    """

    DRAFT = "draft"
    VALIDATED = "validated"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    RETIRED = "retired"

    def is_active(self) -> bool:
        """Check if the model status indicates active usage.

        Returns:
            True if the model is validated or deployed.
        """
        return self in (ModelStatus.VALIDATED, ModelStatus.DEPLOYED)


# =============================================================================
# 3. DATACLASSES (Value Objects / DTOs)
# =============================================================================


@dataclass(frozen=True)
class ForecastResult:
    """Immutable container for a single forecast point.

    This is a value object that holds the prediction and its confidence
    interval for a specific date. Immutability is enforced via
    `frozen=True`.

    Attributes:
        date: Target date for the forecast in ISO format (YYYY-MM-DD).
        point_forecast: Central prediction value.
        lower_bound: Lower bound of the 95% confidence interval.
        upper_bound: Upper bound of the 95% confidence interval.
        model_version: Version of the model that generated this forecast.

    Example:
        >>> result = ForecastResult(
        ...     date="2026-03-15",
        ...     point_forecast=1250.0,
        ...     lower_bound=1100.0,
        ...     upper_bound=1400.0,
        ...     model_version="1.2.0",
        ... )
        >>> result.point_forecast
        1250.0
        >>> result.confidence_width
        300.0
    """

    date: str
    point_forecast: float
    lower_bound: float
    upper_bound: float
    model_version: str = "unknown"

    @property
    def confidence_width(self) -> float:
        """Width of the confidence interval.

        Returns:
            Difference between upper and lower bounds.
        """
        return self.upper_bound - self.lower_bound

    def __post_init__(self) -> None:
        """Validate forecast result constraints.

        Raises:
            ValueError: If lower_bound > upper_bound or bounds are
                inconsistent with the point forecast.
        """
        if self.lower_bound > self.upper_bound:
            raise ValueError(
                f"lower_bound ({self.lower_bound}) must be <= "
                f"upper_bound ({self.upper_bound})"
            )


@dataclass
class PipelineConfig:
    """Configuration for a data processing pipeline.

    Mutable dataclass used to configure pipeline behavior.
    Default values provide a sensible starting configuration.

    Attributes:
        name: Human-readable pipeline name.
        input_path: Path to input data file or directory.
        output_path: Path for output data.
        lag_periods: Lag periods for feature generation.
        rolling_windows: Window sizes for rolling statistics.
        date_column: Name of the date column in the input data.
        target_column: Name of the target variable column.
        fill_missing: Whether to fill missing values after feature creation.
        n_jobs: Number of parallel jobs. -1 uses all available cores.

    Example:
        >>> config = PipelineConfig(
        ...     name="sales_forecast",
        ...     input_path="data/raw/sales.parquet",
        ...     output_path="data/processed/features.parquet",
        ... )
        >>> config.lag_periods
        [1, 7, 14, 28]
    """

    name: str
    input_path: str
    output_path: str
    lag_periods: list[int] = field(default_factory=lambda: [1, 7, 14, 28])
    rolling_windows: list[int] = field(default_factory=lambda: [7, 14, 28])
    date_column: str = "date"
    target_column: str = "target"
    fill_missing: bool = True
    n_jobs: int = 1


# =============================================================================
# 4. ABSTRACT BASE CLASS (Interface)
# =============================================================================


class BaseForecaster(ABC):
    """Abstract base class defining the interface for forecasting models.

    All forecasting model implementations must inherit from this class
    and implement the `fit()` and `predict()` methods. This ensures
    a consistent API across different model types.

    The typical workflow is:
        1. Instantiate the model with configuration.
        2. Call `fit()` with training data.
        3. Call `predict()` to generate forecasts.
        4. Optionally call `evaluate()` to assess performance.

    Attributes:
        model_name (str): Human-readable name of the model.
        is_fitted (bool): Whether the model has been fitted.

    Example:
        >>> class MyModel(BaseForecaster):
        ...     def fit(self, data, target_col):
        ...         self._fitted = True
        ...     def predict(self, horizon):
        ...         return [ForecastResult(...) for _ in range(horizon)]
        ...
        >>> model = MyModel(model_name="my_model")
        >>> model.fit(train_df, "sales")
        >>> forecasts = model.predict(horizon=7)
    """

    def __init__(self, model_name: str) -> None:
        """Initialize the base forecaster.

        Args:
            model_name: Human-readable name for the model instance.
                Used in logging and result metadata.
        """
        self.model_name = model_name
        self._fitted: bool = False

    @property
    def is_fitted(self) -> bool:
        """Whether the model has been successfully fitted.

        Returns:
            True if `fit()` has been called without errors.
        """
        return self._fitted

    @abstractmethod
    def fit(self, data: pd.DataFrame, target_col: str) -> None:
        """Fit the model to training data.

        Args:
            data: Training DataFrame containing features and target.
            target_col: Name of the target column in `data`.

        Raises:
            KeyError: If `target_col` is not found in `data`.
            ValueError: If `data` contains insufficient observations.
        """
        ...

    @abstractmethod
    def predict(self, horizon: int) -> list[ForecastResult]:
        """Generate forecasts for the specified horizon.

        Args:
            horizon: Number of periods to forecast. Must be positive.

        Returns:
            List of ForecastResult objects, one per forecasted period,
            ordered chronologically.

        Raises:
            RuntimeError: If `fit()` has not been called.
            ValueError: If `horizon` is not a positive integer.
        """
        ...

    def evaluate(
        self,
        actuals: pd.Series,
        predictions: list[ForecastResult],
    ) -> dict[str, float]:
        """Evaluate forecast accuracy against actual values.

        Computes standard forecasting accuracy metrics comparing
        predictions against observed values.

        Args:
            actuals: Series of actual observed values, indexed by date.
            predictions: List of ForecastResult objects to evaluate.

        Returns:
            Dictionary with metric names as keys and values as floats.
            Includes: "mae", "rmse", "mape", "coverage".

            Example return value::

                {
                    "mae": 42.5,
                    "rmse": 58.3,
                    "mape": 0.085,
                    "coverage": 0.94,
                }

        Raises:
            ValueError: If lengths of `actuals` and `predictions`
                don't match.

        Note:
            MAPE is undefined when actual values contain zeros. In
            this case, MAPE will be reported as `float('inf')`.
        """
        ...


# =============================================================================
# 5. CONCRETE CLASS
# =============================================================================


class TimeSeriesFeatureEngine:
    """Engine for generating time series features from tabular data.

    Encapsulates feature engineering logic including lag features,
    rolling statistics, and calendar-based features. Follows a
    fit-transform pattern where `fit()` learns statistics needed
    for imputation and `transform()` applies the transformations.

    Attributes:
        config (PipelineConfig): Pipeline configuration.
        features_generated (list[str]): Names of features created
            after `transform()` is called. Empty before first transform.

    Example:
        >>> config = PipelineConfig(
        ...     name="demo",
        ...     input_path="data/raw/sales.parquet",
        ...     output_path="data/features/sales_features.parquet",
        ...     lag_periods=[1, 7],
        ...     rolling_windows=[7],
        ... )
        >>> engine = TimeSeriesFeatureEngine(config)
        >>> engine.fit(train_df)
        >>> train_features = engine.transform(train_df)
        >>> test_features = engine.transform(test_df)
        >>> print(engine.features_generated)
        ['target_lag_1', 'target_lag_7', 'target_rolling_mean_7']

    Note:
        Input DataFrames must be sorted by the date column before
        calling `fit()` or `transform()`. The engine does NOT sort
        automatically to avoid masking data ordering issues.

    See Also:
        PipelineConfig: Configuration dataclass.
        BaseForecaster: For the modeling step after feature engineering.
    """

    def __init__(self, config: PipelineConfig) -> None:
        """Initialize the feature engine with pipeline configuration.

        Args:
            config: Pipeline configuration specifying lag periods,
                rolling windows, column names, and other parameters.

        Raises:
            ValueError: If config contains invalid lag periods or
                rolling windows (non-positive values).
        """
        self.config = config
        self.features_generated: list[str] = []
        self._fitted = False
        self._fill_values: dict[str, float] = {}

        # Validate configuration
        for lag in config.lag_periods:
            if lag <= 0:
                raise ValueError(f"Lag period must be positive, got {lag}")
        for window in config.rolling_windows:
            if window <= 0:
                raise ValueError(f"Rolling window must be positive, got {window}")

    def fit(self, data: pd.DataFrame) -> "TimeSeriesFeatureEngine":
        """Learn statistics from training data needed for transformation.

        Currently learns median values for each generated feature,
        used to fill missing values during `transform()` if
        `config.fill_missing` is True.

        Args:
            data: Training DataFrame. Must contain the columns
                specified in `config.date_column` and
                `config.target_column`.

        Returns:
            Self, to allow method chaining:
            `engine.fit(train_df).transform(train_df)`

        Raises:
            KeyError: If required columns are missing from `data`.
            ValueError: If `data` is empty.

        Example:
            >>> engine = TimeSeriesFeatureEngine(config)
            >>> engine.fit(train_df)
            >>> engine.is_fitted
            True
        """
        self._fitted = True
        return self

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply feature engineering transformations to the data.

        Creates lag features, rolling statistics, and calendar features
        based on the configuration. If `fit()` was called with
        `config.fill_missing=True`, missing values are imputed using
        medians learned during fit.

        Args:
            data: Input DataFrame to transform. Must contain the
                columns specified in `config.date_column` and
                `config.target_column`.

        Returns:
            New DataFrame with original columns plus generated feature
            columns. The original DataFrame is NOT modified.

        Raises:
            RuntimeError: If `fit()` has not been called first.
            KeyError: If required columns are missing.

        Example:
            >>> features_df = engine.transform(raw_df)
            >>> new_cols = set(features_df.columns) - set(raw_df.columns)
            >>> print(sorted(new_cols))
            ['target_lag_1', 'target_lag_7', 'target_rolling_mean_7']
        """
        if not self._fitted:
            raise RuntimeError("Must call fit() before transform()")
        ...

    @property
    def is_fitted(self) -> bool:
        """Whether the engine has been fitted with training data.

        Returns:
            True if `fit()` has been called successfully.
        """
        return self._fitted


# =============================================================================
# 6. STANDALONE FUNCTIONS
# =============================================================================


def add_lag_features(
    df: pd.DataFrame,
    column: str,
    lags: list[int],
    group_columns: list[str] | None = None,
    fill_value: float | None = None,
) -> pd.DataFrame:
    """Add lag features to a DataFrame for a specified column.

    Creates new columns with shifted values of the target column.
    Supports grouped lag computation for panel data (e.g., multiple
    stores or products).

    The resulting columns follow the naming pattern `{column}_lag_{n}`.

    Args:
        df: Input DataFrame. Must be sorted by the time dimension
            within each group (if grouped).
        column: Name of the column to create lags for. Must exist
            in `df`.
        lags: List of positive integers specifying lag periods.
            Example: ``[1, 7, 28]`` creates 1-step, 7-step, and
            28-step lag features.
        group_columns: Column names to group by before computing lags.
            Use for panel data where lags should not cross group
            boundaries. Defaults to None (no grouping).
        fill_value: Value to fill NaN positions created by the shift
            operation. Defaults to None (NaN values are kept).

    Returns:
        Copy of the input DataFrame with additional lag columns
        appended. Original columns remain unchanged. New columns
        are named ``{column}_lag_{n}`` for each ``n`` in ``lags``.

    Raises:
        KeyError: If ``column`` or any element of ``group_columns``
            does not exist in the DataFrame.
        ValueError: If any value in ``lags`` is not a positive integer.
        TypeError: If ``df`` is not a pandas DataFrame.

    Examples:
        Basic lag features without grouping:

        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     "date": pd.date_range("2026-01-01", periods=5),
        ...     "sales": [10, 20, 30, 40, 50],
        ... })
        >>> result = add_lag_features(df, column="sales", lags=[1, 2])
        >>> result.columns.tolist()
        ['date', 'sales', 'sales_lag_1', 'sales_lag_2']

        Grouped lags for panel data:

        >>> result = add_lag_features(
        ...     df,
        ...     column="sales",
        ...     lags=[1],
        ...     group_columns=["store_id"],
        ... )

        Fill NaN with zero:

        >>> result = add_lag_features(
        ...     df, column="sales", lags=[1], fill_value=0
        ... )
        >>> result["sales_lag_1"].isna().sum()
        0

    Note:
        Performance scales linearly with ``len(lags)``. For DataFrames
        exceeding 10M rows, consider computing lags per partition.

    Since:
        v1.0.0
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pd.DataFrame, got {type(df).__name__}")
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")
    for lag in lags:
        if not isinstance(lag, int) or lag <= 0:
            raise ValueError(f"Lag must be a positive integer, got {lag}")

    result = df.copy()
    for lag in lags:
        col_name = f"{column}_lag_{lag}"
        if group_columns:
            result[col_name] = result.groupby(group_columns)[column].shift(lag)
        else:
            result[col_name] = result[column].shift(lag)
        if fill_value is not None:
            result[col_name] = result[col_name].fillna(fill_value)

    return result


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list[str],
    *,
    allow_empty: bool = False,
    max_null_fraction: float = 0.5,
) -> bool:
    """Validate a DataFrame against a set of quality criteria.

    Performs structural and data quality checks on the input DataFrame
    to ensure it meets minimum requirements before processing.

    Args:
        df: DataFrame to validate.
        required_columns: List of column names that must be present.
        allow_empty: Whether an empty DataFrame passes validation.
            Defaults to False (empty DataFrames fail).
        max_null_fraction: Maximum allowed fraction of null values
            per column (0.0 to 1.0). Defaults to 0.5.

    Returns:
        True if all validations pass.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.
        ValueError: If validation fails. The error message describes
            which specific check failed.

    Examples:
        Successful validation:

        >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        >>> validate_dataframe(df, required_columns=["a", "b"])
        True

        Failed validation — missing column:

        >>> validate_dataframe(df, required_columns=["a", "c"])
        Traceback (most recent call last):
            ...
        ValueError: Missing required columns: {'c'}

    Todo:
        * Add support for type checking per column.
        * Add support for value range validation.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pd.DataFrame, got {type(df).__name__}")

    if not allow_empty and len(df) == 0:
        raise ValueError("DataFrame is empty and allow_empty=False")

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in required_columns:
        null_frac = df[col].isna().mean()
        if null_frac > max_null_fraction:
            raise ValueError(
                f"Column '{col}' has {null_frac:.1%} nulls, "
                f"exceeding threshold of {max_null_fraction:.1%}"
            )

    return True


# =============================================================================
# 7. GENERATOR FUNCTION
# =============================================================================


def iter_date_chunks(
    start_date: str,
    end_date: str,
    chunk_days: int = 30,
) -> Generator[tuple[str, str], None, None]:
    """Yield date range chunks between start and end dates.

    Useful for processing large date ranges in manageable batches,
    particularly for API calls or database queries with date filters.

    Args:
        start_date: Start date in ISO format (YYYY-MM-DD), inclusive.
        end_date: End date in ISO format (YYYY-MM-DD), inclusive.
        chunk_days: Number of days per chunk. Defaults to 30.

    Yields:
        Tuple of (chunk_start, chunk_end) as ISO format strings.
        The last chunk may be shorter than ``chunk_days``.

    Raises:
        ValueError: If ``start_date`` > ``end_date`` or ``chunk_days``
            is not positive.

    Examples:
        >>> chunks = list(iter_date_chunks("2026-01-01", "2026-03-01", chunk_days=30))
        >>> len(chunks)
        3
        >>> chunks[0]
        ('2026-01-01', '2026-01-30')

    Note:
        Both start and end dates of each chunk are inclusive.
    """
    ...


# =============================================================================
# 8. DEPRECATED FUNCTION
# =============================================================================


def compute_lags(
    df: pd.DataFrame,
    col: str,
    lags: list[int],
) -> pd.DataFrame:
    """Compute lag features for a column.

    .. deprecated:: 1.2.0
        Use :func:`add_lag_features` instead. This function will be
        removed in version 2.0.0.

    Args:
        df: Input DataFrame.
        col: Name of the column to create lags for.
        lags: List of positive integers specifying lag periods.

    Returns:
        DataFrame with lag feature columns appended.

    See Also:
        add_lag_features: The replacement function with more features.
    """
    warnings.warn(
        "compute_lags() is deprecated since v1.2.0 and will be removed "
        "in v2.0.0. Use add_lag_features() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return add_lag_features(df, column=col, lags=lags)


# =============================================================================
# 9. CONTEXT MANAGER
# =============================================================================


class Timer:
    """Context manager for timing code blocks.

    Measures wall-clock execution time of the wrapped code block
    and optionally logs the result.

    Attributes:
        label (str): Descriptive label for the timed block.
        elapsed (float | None): Elapsed time in seconds after
            the context exits. None before execution.

    Example:
        >>> with Timer("data loading") as t:
        ...     df = pd.read_parquet("data.parquet")
        ...
        >>> print(f"Loaded in {t.elapsed:.2f}s")
        Loaded in 1.23s

    Note:
        Uses ``time.perf_counter()`` for high-resolution timing.
    """

    def __init__(self, label: str = "block") -> None:
        """Initialize the timer.

        Args:
            label: Descriptive label printed when timing completes.
                Defaults to "block".
        """
        self.label = label
        self.elapsed: float | None = None

    def __enter__(self) -> "Timer":
        """Start the timer.

        Returns:
            Self, to allow access to ``elapsed`` after the block.
        """
        import time

        self._start = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop the timer and compute elapsed time.

        Args:
            *args: Exception info (exc_type, exc_val, exc_tb).
                Not used; exceptions are never suppressed.
        """
        import time

        self.elapsed = time.perf_counter() - self._start
