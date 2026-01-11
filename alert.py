import ssl
import json
import urllib.parse
import urllib.request
import argparse

with open('config.json', 'r', encoding='utf-8') as file:
    cfg = json.load(file)

if cfg['skip_ssl']:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

parser = argparse.ArgumentParser()

parser.add_argument('--severity', help='Уровень важности события')
parser.add_argument('--computer', help='Имя устройства, на котором произошло событие')
parser.add_argument('--domain', help='Имя домена устройства, на котором произошло событие')
parser.add_argument('--event', help='Имя типа события')
parser.add_argument('--description', help='Описание события')
parser.add_argument('--rise-time', help='Время создания события')
parser.add_argument('--task-name', help='Название задачи')
parser.add_argument('--product', help='Название программы')
parser.add_argument('--version', help='Номер версии программы')
parser.add_argument('--severity-num', help='Код уровня важности события')
parser.add_argument('--host-ip', help='IP-адрес устройства, на котором произошло событие')
parser.add_argument('--host-conn-ip', help='IP-адрес соединения устройства, на котором произошло событие')

def main():
    telegram_send_message(format_message(parser.parse_args()))

def format_message(args):
    return f"""
{get_severity_emoji(args.severity)} {args.event}
    
⚠️ *Уровень важности:* {args.severity}
🖥 *Устройство:* `{args.domain}\\\\{args.computer}`
⚙️ *Задача:* {args.task_name}

{safe_markdown(args.description)}
{get_ip_message_part(args)}{get_app_info_message_part(args)}
📆 *Время события:* {safe_markdown(args.rise_time)}
"""

def get_ip_message_part(args):
    if not cfg['hide_ip']:
        return f"""\n🔒 *IP:* {safe_markdown(f'{args.host_ip} (Соединение: {args.host_conn_ip})')}\n"""
    return ""


def get_app_info_message_part(args):
    if not cfg['hide_app_info']:
        return f"""\n🚧 *Название программы:* {safe_markdown(f'{args.product} ({args.version})')}\n"""
    return ""


def get_severity_emoji(severity):
    if severity == "Информационное":
        return '🟢'
    elif severity == "Предупреждение":
        return '⚠️'
    elif severity == "Сбой":
        return '❌'
    elif severity == "Критическое":
        return '‼️'
    return ""


def safe_markdown(text):
    if not text:
        return text
    chars_to_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>',
                       '#', '+', '-', '=', '|', '{', '}', '.', '!']

    result = []
    i = 0

    while i < len(text):
        char = text[i]

        if char in chars_to_escape:
            result.append('\\' + char)
        elif char == '\\':
            result.append('\\\\')
            if i + 1 < len(text) and text[i + 1] in chars_to_escape:
                i += 1
                if i < len(text):
                    result.append('\\' + text[i])
        else:
            result.append(char)

        i += 1

    return ''.join(result)

def telegram_send_message(text):
    encoded_text = urllib.parse.quote(text)

    url = f"https://api.telegram.org/bot{cfg['telegram']['bot_token']}/sendMessage?chat_id={cfg['telegram']['chat_id']}&text={encoded_text}&parse_mode=MarkdownV2"

    try:
        if cfg['skip_ssl']:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode('utf-8'))
        else:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))

        if data.get('ok'):
            print(f"Telegram send message successful!")

    except Exception as e:
        print(f"Error send telegram message: {e}")
        return False

if __name__ == '__main__':
    main()
