from pydantic import BaseModel, Field, RootModel
import datetime
import aiohttp
import asyncio


class TimeTableRow(BaseModel):
    station_short_code: str = Field(validation_alias="stationShortCode")
    type: str
    cancelled: bool
    scheduled_time: datetime.datetime = Field(validation_alias="scheduledTime")
    actual_time: datetime.datetime | None = Field(
        default=None, validation_alias="actualTime"
    )
    difference_in_minutes: int | None = Field(
        default=None, validation_alias="differenceInMinutes"
    )


class TimeTableRows(RootModel):
    root: list[TimeTableRow] = Field(default_factory=list)


class Train(BaseModel):
    train_number: int = Field(validation_alias="trainNumber")
    departure_date: datetime.date = Field(validation_alias="departureDate")
    train_type: str = Field(validation_alias="trainType")
    cancelled: bool
    time_table_rows: TimeTableRows = Field(validation_alias="timeTableRows")


class TrainList(RootModel):
    root: list[Train] = Field(default_factory=list)


async def fetch_train_for_date(train: int, date: datetime.date) -> TrainList:
    date_formatted = date.strftime(format="%Y-%m-%d")
    async with aiohttp.ClientSession() as session:
        response = await session.request(
            method="GET",
            url=f"https://rata.digitraffic.fi/api/v1/trains/{date_formatted}/{train}",
        )
        response.raise_for_status()

        response_json = await response.text()
    return TrainList.model_validate_json(json_data=response_json)


async def fetch_train_for_dates(
    train: int,
    dates: list[datetime.date],
    max_concurrent: int = 10,
    sleep_after_sec: float = 5.0,
) -> TrainList:
    sem = asyncio.Semaphore(value=max_concurrent)

    async def get_date(date: datetime.date) -> TrainList:
        async with sem:
            response = await fetch_train_for_date(train=train, date=date)
            await asyncio.sleep(delay=sleep_after_sec)
        return response

    futures = [get_date(date=date) for date in dates]
    responses = await asyncio.gather(*futures)
    res = []
    for r in responses:
        res.extend(r.root)

    return TrainList(root=res)
