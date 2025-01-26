from utils.fetch import fetch_train_for_date
from typing import Any
import datetime
import json
import asyncio


async def main() -> None:
    response_json = await fetch_train_for_date(
        train=40, date=datetime.date(year=2025, month=1, day=24)
    )
    assert isinstance(response_json, list)

    if len(response_json) == 0:
        print("No data for the day. Is the train scheduled for said day?")
        return
    assert len(response_json) == 1, "a train-line is assumed to only run once per day"

    time_table_rows: list[dict[str, Any]] = response_json[0]["timeTableRows"]
    tpe_departure = [
        row
        for row in time_table_rows
        if row["stationShortCode"] == "TPE" and row["type"] == "DEPARTURE"
    ][0]
    psl_arrival = [
        row
        for row in time_table_rows
        if row["stationShortCode"] == "PSL" and row["type"] == "ARRIVAL"
    ][0]

    print(f"{response_json[0]['trainType']} {response_json[0]['trainNumber']}")
    print(json.dumps(tpe_departure, indent=2))
    print(json.dumps(psl_arrival, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
