import requests
import os


class _TelegramConnector:
    def __init__(self):
        self._token = os.getenv('TELEGRAM_CHANNEL_TOKEN')
        self._chat_id = os.getenv('TELEGRAM_CHANNEL_ID')

    def send_message(self, message: str):
        url = f'https://api.telegram.org/bot{self._token}/sendMessage?chat_id={self._chat_id}&parse_mode=Markdown&text={message}'

        response = requests.get(url)

        return response.json()


telegram_connector_instance = _TelegramConnector()
