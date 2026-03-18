1.根据requirements.txt下载相关依赖库

2.打开surveil.py,填写自己的用户名密码

3.打开nn.py,运行程序。打开canvas直播挂着，当检测到二维码，会自动解析打印内容，尝试自动签到并鸣叫。预计输出：
```
>>> [忠诚的看门狗] 已启动！
>>> [任务] 每秒扫描全屏，发现二维码立刻尖叫。
>>> 按 Ctrl+C 可以让卑微的我停止工作。

!!! [警报] 发现二维码 !!!
内容: https://mlearning.sjtu.edu.cn/lms/mobile2/forscan/?courseCode=8......674d7482b951721af7fdf9ea5&fromType=scanRollCall
🚀 初始化干净的 Session...
🌐 [1/4] 访问签到链接，触发重定向...
   -> 截获当前 Cookie 凭证: {'JSESSIONID': 'FB9DBC2BA824702A9534C9FABA12AC3B.oauth114', 'canvas_sjtu_session': 'PFZvrF6lw8Sjh7kzF2qQFEeSzB......BNCyx1%2BnrK%2Bsfg%3D%3D'}
🔍 [2/4] 获取验证码 (UUID: 0e2d8869...)...
🤖 AI 识别结果: [xeyv] (已清理幽灵字符)
⏳ 伪装人类手速，停顿 1 秒以防触发 WAF 风控拦截...
🔥 [3/4] 提交核心数据...
   -> 服务器底牌: {'errno': 0, 'error': None, 'code': None, 'url': '/jaccount/jalogin?sid=jaoauth2201607......QsB7vEY%2BCOPrlqXpOw7tK9VW7osMsMdU4sLvrc5CuQqsjnxg9OgY'}
✅ [4/4] 登录成功！服务器已放行。
🔗 自动追溯最终签到链接，获取 JWT Token...
🔫 [终极刺杀] 正在提取原始令牌...
🎫 成功捕获令牌 (长度:177): eyJ0eXAiOiJKV1QiLCJh...
🎯 响应状态码: 200
🎯 最终响应: {"resultCode":"200","resultMessage":"操作成功！","body":{"status":"NORMAL"}}
🏆 恭喜！签到彻底成功！

Process finished with exit code -1
```
