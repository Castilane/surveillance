import requests
from bs4 import BeautifulSoup
import ddddocr
import re
from urllib.parse import urlparse, parse_qs
import json
import time

# fill in the contents
USERNAME = "pass"
PASSWORD = "pass"
url = "https://mlearning.sjtu.edu.cn/lms/mobile2/forscan/?..."


def auto_sign(TARGET_QR_URL):
    print("🚀 初始化干净的 Session...")
    session = requests.Session()
    session.trust_env = False

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    })

    print("🌐 [1/4] 访问签到链接，触发重定向...")
    login_page_resp = session.get(TARGET_QR_URL)

    # 诊断 Cookie：如果这里是空的，说明第一步就被墙了
    cookies_dict = session.cookies.get_dict()
    print(f"   -> 截获当前 Cookie 凭证: {cookies_dict}")

    parsed_url = urlparse(login_page_resp.url)
    params = parse_qs(parsed_url.query)

    sid = params.get('sid', [''])[0]
    client = params.get('client', [''])[0]
    returl = params.get('returl', [''])[0]
    se = params.get('se', [''])[0]

    soup = BeautifulSoup(login_page_resp.text, 'html.parser')

    uuid = ""
    uuid_match = re.search(r'uuid=([a-zA-Z0-9\-]+)', login_page_resp.text)
    if uuid_match:
        uuid = uuid_match.group(1)

    lt_tag = soup.find('input', {'name': 'lt'})
    lt = lt_tag['value'] if lt_tag else 'p'

    v_tag = soup.find('input', {'name': 'v'})
    v = v_tag['value'] if v_tag else ''

    if not uuid:
        print("❌ 致命错误：未找到 UUID，正则表达式匹配失败。")
        return

    print(f"🔍 [2/4] 获取验证码 (UUID: {uuid[:8]}...)...")
    captcha_url = f"https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid={uuid}"

    session.headers.update({'Referer': login_page_resp.url})
    captcha_resp = session.get(captcha_url)

    ocr = ddddocr.DdddOcr(show_ad=False)

    # 【修复1】：强制清除 ddddocr 可能带有的 \n、空格，并转为小写！
    raw_captcha = ocr.classification(captcha_resp.content)
    clean_captcha = raw_captcha.strip().lower()
    print(f"🤖 AI 识别结果: [{clean_captcha}] (已清理幽灵字符)")

    payload = {
        'sid': sid, 'client': client, 'returl': returl, 'se': se,
        'v': v, 'uuid': uuid, 'user': USERNAME, 'pass': PASSWORD,
        'captcha': clean_captcha, 'lt': lt
    }

    print("⏳ 伪装人类手速，停顿 2 秒以防触发 WAF 风控拦截...")
    time.sleep(1)  # 【修复2】：强制停顿，绝杀机器速率检测

    print("🔥 [3/4] 提交核心数据...")
    login_api_url = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"

    session.headers.update({
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://jaccount.sjtu.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    })

    final_resp = session.post(login_api_url, data=payload)
    final_resp.encoding = 'utf-8'

    try:
        result_json = final_resp.json()
        print(f"   -> 服务器底牌: {result_json}")

        if result_json.get("errno") == 0 or result_json.get("code") == "SUCCESS":
            print("✅ [4/4] 登录成功！服务器已放行。")
            redirect_url = result_json.get("url")
            if redirect_url:
                if not redirect_url.startswith("http"):
                    redirect_url = "https://jaccount.sjtu.edu.cn" + redirect_url
                print(f"🔗 自动追溯最终签到链接，获取 JWT Token...")
                # 这一步非常关键：请求这个跳转地址，session 会自动拿到那个 Set-Cookie 里的 token
                session.get(redirect_url)
                # ================= 第 6 步：显微镜级调试与刺杀 =================
                # ================= 第 6 步：终极刺杀（去掉 Bearer 伪装） =================
            print("🔫 [终极刺杀] 正在提取原始令牌...")

            import urllib.parse

            # 1. 寻找名为 'token' 的 Cookie
            jwt_token = ""
            for cookie in session.cookies:
                if cookie.name == 'token':
                    # 直接取值并进行 URL 解码，不加任何前缀
                    jwt_token = urllib.parse.unquote(cookie.value).strip('"')
                    break

            if jwt_token:
                print(f"🎫 成功捕获令牌 (长度:{len(jwt_token)}): {jwt_token[:20]}...")

                # 【核心修复】：Header 里的 Authorization 必须直接等于 jwt_token
                # 千万不要加 "Bearer "！截图中显示它们是直接发送的
                session.headers.clear()
                session.headers.update({
                    'Authorization': jwt_token,  # 这里是成败的关键
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Referer': 'https://mlearning.sjtu.edu.cn/lms/mobile/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                # 顺便把 token 放到 cookie 里也补全一下
                session.cookies.set('token', jwt_token, domain='mlearning.sjtu.edu.cn')
            else:
                print("⚠️ 警告：Session 中未发现 token！")

            # 2. 解析二维码参数
            parsed_qr = urlparse(TARGET_QR_URL)
            qr_params = parse_qs(parsed_qr.query)
            t = qr_params.get('rollCallToken', [''])[0]
            sid = qr_params.get('signHistoryId', [''])[0]
            real_sign_api = f"https://mlearning.sjtu.edu.cn/lms-lti-rollcall-sjtu/sign/scan/{t}/{sid}"

            # 3. 执行请求
            final_sign_resp = session.get(real_sign_api)

            print(f"🎯 响应状态码: {final_sign_resp.status_code}")
            print(f"🎯 最终响应: {final_sign_resp.text}")

            if "操作成功" in final_sign_resp.text or "200" in final_sign_resp.text:
                print("🏆 恭喜！签到彻底成功！")
            else:
                print("❌ 依然报错。请检查响应内容。")
        elif result_json.get("error") == "Wrong captcha" or result_json.get("code") == "WRONG_CAPTCHA":

           print(f"❌ 验证码错误！如果你确信 AI 没认错，大概率是 Cookie 没绑定上。")

        else:
            print(f"❌ 未知拒绝原因: {result_json}")

    except json.JSONDecodeError:
        print("❌ 解析 JSON 失败。响应内容如下：")
        print(final_resp.text[:300])


if __name__ == "__main__":
    auto_sign(url)