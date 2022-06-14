from feapder.network.user_pool import GuestUser, GuestUserPool
from typing import Optional
import time, requests
from feapder.utils.tools import get_cookies
from feapder import setting


class XueqiuCookiePool(GuestUserPool):
    def login(self) -> Optional[GuestUser]:
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        }
        proxy_virjar = setting.get_random_proxy()
        proxies = {"https": proxy_virjar, "http": proxy_virjar}
        url = "https://xueqiu.com"
        response = requests.get(url, headers=headers, proxies=proxies, timeout=3)

        cookies = get_cookies(response)
        if cookies:
            user = GuestUser(cookies=cookies)
            return user


xueqiu_cookie_pool = XueqiuCookiePool(redis_key="xueqiu:gen_cookie",min_users=5)

if __name__ == "__main__":
    user = xueqiu_cookie_pool.get_user()
    print(user)