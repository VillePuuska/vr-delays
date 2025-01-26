from utils.fetch import fetch_train_for_dates
from typing import Any
import datetime
import polars as pl
import asyncio


async def main() -> None:
    train_list = await fetch_train_for_dates(
        train=40,
        dates=[
            datetime.date.today() - datetime.timedelta(days=diff) for diff in range(180)
        ],
        max_concurrent=5,
        sleep_after_sec=1.0,
    )

    rows = []
    for train in train_list.root:
        row: dict[str, Any] = {}
        row["train_number"] = train.train_number
        row["departure_date"] = train.departure_date
        row["cancelled"] = train.cancelled
        row["train_type"] = train.train_type

        tpe_dep_rows = [
            row
            for row in train.time_table_rows.root
            if row.station_short_code == "TPE" and row.type == "DEPARTURE"
        ]
        assert len(tpe_dep_rows) == 1
        tpe_dep_row = tpe_dep_rows[0]
        row["departure_scheduled_time"] = tpe_dep_row.scheduled_time
        row["departure_actual_time"] = tpe_dep_row.actual_time
        row["departure_difference_in_minutes"] = tpe_dep_row.difference_in_minutes

        psl_arr_rows = [
            row
            for row in train.time_table_rows.root
            if row.station_short_code == "PSL" and row.type == "ARRIVAL"
        ]
        assert len(psl_arr_rows) == 1
        psl_arr_row = psl_arr_rows[0]
        row["arrival_scheduled_time"] = psl_arr_row.scheduled_time
        row["arrival_actual_time"] = psl_arr_row.actual_time
        row["arrival_difference_in_minutes"] = psl_arr_row.difference_in_minutes

        rows.append(row)

    df = pl.DataFrame(data=rows)
    print(df)
    print(df.describe())


if __name__ == "__main__":
    asyncio.run(main())
