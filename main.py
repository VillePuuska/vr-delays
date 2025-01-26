from utils.fetch import fetch_train_for_date
import datetime
import asyncio


async def main() -> None:
    response = await fetch_train_for_date(
        train=40, date=datetime.date(year=2025, month=1, day=24)
    )

    if len(response.root) == 0:
        print("No data for the day. Is the train scheduled for said day?")
        return
    assert len(response.root) == 1, "a train-line is assumed to only run once per day"

    time_table_rows = response.root[0].time_table_rows
    tpe_departure = [
        row
        for row in time_table_rows.root
        if row.station_short_code == "TPE" and row.type == "DEPARTURE"
    ][0]
    psl_arrival = [
        row
        for row in time_table_rows.root
        if row.station_short_code == "PSL" and row.type == "ARRIVAL"
    ][0]

    print(f"{response.root[0].train_type} {response.root[0].train_number}")
    print(tpe_departure)
    print(psl_arrival)


if __name__ == "__main__":
    asyncio.run(main())
