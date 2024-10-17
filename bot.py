import json
import random
import urllib.parse
from convert import get
from curl_cffi import requests
from colorama import Fore, Style, init
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor, as_completed


def log_message(message, color=Style.RESET_ALL):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{Fore.LIGHTBLACK_EX}{current_time}{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")


class Notpx:
    def __init__(self):

        pass

    def get_template(self, header):
        url = "https://notpx.app/api/v1/image/template/list?limit=12&offset=0"
        try:
            response = requests.get(url, headers=header,
                                    impersonate="chrome101", verify=False, timeout=10)
            if response.status_code == 200:
                data = random.choice(response.json())
                return data.get("templateId")
            else:
                return 6989019093
        except Exception:
            return 6989019093

    def get_color(self, pixel, header):
        url = f"https://notpx.app/api/v1/image/get/{pixel}"
        try:
            response = requests.get(url, headers=header,
                                    impersonate="chrome101", verify=False, timeout=10)
            if response.status_code == 401:
                return -1
            return response.json()['pixel']['color']
        except Exception:
            return "#000000"

    def get_pixel(self, x, y):
        return y * 1000 + x + 1

    def get_pos(self, pixel, size_x):
        return pixel % size_x, pixel // size_x

    def get_canvas_pos(self, x, y):

        str_canvas_pos = f'{y}{x + 1}'

        return int(str_canvas_pos)

    def paint(self, px, canvas_pos, color, header):
        data = {
            "pixelId": canvas_pos,
            "newColor": color
        }

        try:
            response = requests.post(f"https://notpx.app/api/v1/repaint/start", data=json.dumps(data), headers=header,
                                     timeout=10)
            # x, y = self.get_pos(canvas_pos, 1000)

            if response.status_code == 200:
                log_message(f"Paint: {px},balance:{response.json()['balance']}", Fore.GREEN)
                return True
            else:
                log_message("Out of energy", Fore.RED)
                return False



        except Exception as e:
            log_message(f"Failed to paint: {e}", Fore.RED)
            return False

    def claim(self, header):
        log_message("Claiming resources", Fore.CYAN)
        try:
            requests.get(f"https://notpx.app/api/v1/mining/claim", headers=header, timeout=10)
        except Exception as e:
            log_message(f"Failed to claim resources: {e}", Fore.RED)

    def logins(self, header):
        try:
            # print(header)
            response = requests.get(f"https://notpx.app/api/v1/users/me", headers=header, timeout=10)
            # print(response.json())
            if response.status_code == 200:
                data = response.json()

                # user_balance = data.get('userBalance', 'Unknown')
                log_message(f"验证成功！", Fore.MAGENTA)
            else:
                log_message(f"Failed to fetch mining data: {response.status_code}", Fore.RED)
        except Exception as e:
            log_message(f"Error fetching mining data: {e}", Fore.RED)

    def fetch_mining_data(self, header):
        try:
            # print(header)
            response = requests.get(f"https://notpx.app/api/v1/mining/status", headers=header, timeout=10)
            # print(response.json())
            if response.status_code == 200:
                data = response.json()

                user_balance = data.get('userBalance', 'Unknown')
                log_message(f"Balance: {user_balance}", Fore.MAGENTA)
            else:
                log_message(f"Failed to fetch mining data: {response.status_code}", Fore.RED)
        except Exception as e:
            log_message(f"Error fetching mining data: {e}", Fore.RED)

    def get_template_info(self, templateId, header):
        url = f"https://notpx.app/api/v1/image/template/{templateId}"

        try:
            response = requests.get(url, headers=header, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                data = {
                    "id": 6989019093,
                    "url": "https://static.notpx.app/templates/6989019093.png",
                    "x": 528,
                    "y": 872,
                    "imageSize": 128,
                    "subscribers": 1141519,
                    "hits": 3695043,
                    "createdAt": 1728588842
                }
                return data
        except Exception:
            return {
                "id": 6989019093,
                "url": "https://static.notpx.app/templates/6989019093.png",
                "x": 528,
                "y": 872,
                "imageSize": 128,
                "subscribers": 1141519,
                "hits": 3695043,
                "createdAt": 1728588842
            }

    def thread_main(self, auth):
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; V1938T Build/PQ3A.190605.08021643; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36',
            'origin': 'https://app.notpx.app',
            'x-requested-with': 'org.telegram.messenger',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.notpx.app/',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
            'authorization': 'initData ' + auth
        }
        try:
            username = self.extract_username_from_initdata(auth)
            log_message(f"--- STARTING SESSION FOR ACCOUNT: {username} ---", Fore.BLUE)
            self.logins(headers)
            self.fetch_mining_data(headers)
            self.claim(headers)
            # 获取一个模板id
            templateId = self.get_template(headers)
            templateinfo = self.get_template_info(templateId, headers)
            start_x = templateinfo.get("x")
            start_y = templateinfo.get("y")
            # templateurl = templateinfo.get("url")
            image = get(start_x, start_y, templateId)
            random.shuffle(image)
            if self.subscribe_img(templateId, headers):
                log_message(f"模板指定成功", Fore.MAGENTA)
            for row in image:
                for px, color in row.items():
                    x = int(px.split(',')[0])
                    y = int(px.split(',')[1])

                    canvas_pos = self.get_canvas_pos(x, y)
                    response_color = self.get_color(canvas_pos, headers)
                    if response_color == color:
                        log_message(f"{px}: 颜色是对的！", Fore.RED)
                        continue
                    else:
                        res = self.paint(px, canvas_pos, color, headers)
                        if not res:
                            return
        except Exception as e:
            log_message(f"Network error in account {auth}: {e}", Fore.RED)

    def extract_username_from_initdata(self, init_data):
        # URL decode the init data
        decoded_data = urllib.parse.unquote(init_data)

        # Find the part that contains "username"
        username_start = decoded_data.find('"username":"') + len('"username":"')
        username_end = decoded_data.find('"', username_start)

        if username_start != -1 and username_end != -1:
            return decoded_data[username_start:username_end]

        return "Unknown"

    def process_accounts(self, thread_count):
        phone_list = open("data.txt", "r", encoding="utf-8").read().splitlines()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for accounts in phone_list:
                futures.append(executor.submit(self.thread_main, accounts))
            for future in as_completed(futures):
                print(future.result())

    def subscribe_img(self, img_id, headers):
        url = f"https://notpx.app/api/v1/image/template/subscribe/{img_id}"
        res = requests.put(url, headers=headers)
        if res.status_code == 204:
            return True
        else:
            return False

if __name__ == '__main__':
    n = Notpx()
    threadcount = 10
    n.process_accounts(threadcount)
