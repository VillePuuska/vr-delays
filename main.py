from utils.fetch import fetch_train_for_dates
from utils.transform import train_list_to_dataframe
import datetime
import asyncio


async def main() -> None:
    train_list = await fetch_train_for_dates(
        train=40,
        dates=[
            datetime.date.today() - datetime.timedelta(days=diff) for diff in range(10)
        ],
        max_concurrent=5,
        sleep_after_sec=1.0,
    )

    df = train_list_to_dataframe(train_list=train_list, departure="TPE", arrival="PSL")

    print(df)
    print(df.describe())


if __name__ == "__main__":
    asyncio.run(main())
