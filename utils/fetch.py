from typing import Any
import datetime
import aiohttp


async def fetch_train_for_date(train: int, date: datetime.date) -> list[dict[str, Any]]:
    date_formatted = date.strftime(format="%Y-%m-%d")
    async with aiohttp.ClientSession() as session:
        response = await session.request(
            method="GET",
            url=f"https://rata.digitraffic.fi/api/v1/trains/{date_formatted}/{train}",
        )
        response.raise_for_status()

        response_json = await response.json()
    return response_json
