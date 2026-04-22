import json
import time
import urllib.parse
import urllib.request

TOKEN = '8260885309:AAGMLD2zwQscXLKZgWc4q_Gb3-QrxX7JK58'
API = f'https://api.telegram.org/bot{TOKEN}'


def api_call(method, data=None):
    data = data or {}
    payload = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(f'{API}/{method}', data=payload)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_message(chat_id, text):
    return api_call('sendMessage', {
        'chat_id': chat_id,
        'text': text,
    })


def handle_message(message):
    chat_id = message['chat']['id']
    text = (message.get('text') or '').strip()

    if text.startswith('/start'):
        send_message(
            chat_id,
            'Здравствуйте! Я бот для AmanJet SOS.\n\n'
            'Команды:\n'
            '/id — показать ваш Telegram chat ID\n'
            '/help — показать помощь\n\n'
            'Отправьте этот ID подростку, чтобы он сохранил его на сайте.'
        )
        return

    if text.startswith('/help'):
        send_message(
            chat_id,
            'Как подключить SOS:\n'
            '1) Напишите боту /id\n'
            '2) Скопируйте ваш Telegram chat ID\n'
            '3) Подросток вставляет этот ID на сайте AmanJet в разделе Telegram SOS\n'
            '4) При нажатии SOS вам придёт сообщение в Telegram'
        )
        return

    if text.startswith('/id'):
        send_message(
            chat_id,
            f'Ваш Telegram chat ID:\n{chat_id}\n\nСкопируйте его и сохраните на сайте AmanJet.'
        )
        return

    send_message(
        chat_id,
        'Неизвестная команда. Используйте /id чтобы получить ваш chat ID.'
    )


def main():
    print('Bot started...')
    offset = None
    while True:
        try:
            params = {'timeout': 25}
            if offset is not None:
                params['offset'] = offset
            result = api_call('getUpdates', params)
            for item in result.get('result', []):
                offset = item['update_id'] + 1
                message = item.get('message')
                if message:
                    handle_message(message)
        except Exception as e:
            print('Error:', e)
            time.sleep(3)


if __name__ == '__main__':
    main()
