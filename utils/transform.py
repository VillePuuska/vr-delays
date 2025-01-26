from .fetch import TrainList
from typing import Any
import polars as pl


def train_list_to_dataframe(
    train_list: TrainList, departure: str, arrival: str
) -> pl.DataFrame:
    rows = []
    for train in train_list.root:
        row: dict[str, Any] = {}
        row["train_number"] = train.train_number
        row["departure_date"] = train.departure_date
        row["cancelled"] = train.cancelled
        row["train_type"] = train.train_type

        dep_rows = [
            row
            for row in train.time_table_rows.root
            if row.station_short_code == departure and row.type == "DEPARTURE"
        ]

        if len(dep_rows) != 1:
            continue

        dep_row = dep_rows[0]
        row["departure_scheduled_time"] = dep_row.scheduled_time
        row["departure_actual_time"] = dep_row.actual_time
        row["departure_difference_in_minutes"] = dep_row.difference_in_minutes
        if dep_row.actual_time is not None:
            row["departure_actual_difference"] = (
                dep_row.actual_time - dep_row.scheduled_time
            ).total_seconds() / 60.0
        else:
            row["departure_actual_difference"] = None

        arr_rows = [
            row
            for row in train.time_table_rows.root
            if row.station_short_code == arrival and row.type == "ARRIVAL"
        ]

        if len(arr_rows) != 1:
            continue

        arr_row = arr_rows[0]
        row["arrival_scheduled_time"] = arr_row.scheduled_time
        row["arrival_actual_time"] = arr_row.actual_time
        row["arrival_difference_in_minutes"] = arr_row.difference_in_minutes
        if arr_row.actual_time is not None:
            row["arrival_actual_difference"] = (
                arr_row.actual_time - arr_row.scheduled_time
            ).total_seconds() / 60.0
        else:
            row["arrival_actual_difference"] = None

        rows.append(row)

    return pl.DataFrame(data=rows)
