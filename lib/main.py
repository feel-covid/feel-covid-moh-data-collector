import settings
import datetime
from moh_request import moh_request
from feel_request import feel_request
from connectors import telegram_connector_instance
from apscheduler.schedulers.background import BlockingScheduler
from utils import gen_iso_string


def main():
    try:
        moh_data = moh_request()
        feel_data = feel_request()

        print('---------------------------')
        if feel_data.date != moh_data.date:
            url = f"https://priceless-murdock-f4daba.netlify.app/?moh-data={moh_data.as_base64_string()}"
            telegram_connector_instance.send_message(
                f"הנתונים בדשבורד הקורונה של משרד הבריאות עודכנו, ניתן לעדכן את האתר כאן:\n {url}")
            return
        else:
            print(f"{gen_iso_string(datetime.datetime.now())} - No Update Found")
            print(f"Feel Date - {feel_data.date}")
            print(f"Moh Date  - {moh_data.date}")

        values_diff = moh_data.compare_values(feel_data)

        if values_diff:
            header = 'נמצאו ערכים לא תואמים בין האתר לדשבורד משרד הבריאות'
            nl = '\n'
            telegram_connector_instance.send_message(f'{header}:{nl} {nl.join(values_diff)}')
        else:
            print('All values are correct')
        print('---------------------------')

    except Exception as ex:
        telegram_connector_instance.send_message(f'התרחשה שגיאה בבדיקה: {ex}')


if __name__ == '__main__':
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', seconds=85)
    scheduler.start()
