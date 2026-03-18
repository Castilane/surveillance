import time
import winsound  # 仅限 Windows 系统使用，用于发出蜂鸣声
from PIL import ImageGrab
from pyzbar.pyzbar import decode
import numpy as np
from surveil import auto_sign

def alert_sound():
    """
    发出刺耳的警报声，确保您能听到
    """
    try:
        # 频率 1000Hz, 持续 1秒
        winsound.Beep(1000, 1000)
    except ImportError:
        # 如果不是Windows，尝试用系统提示音
        print('\a')


def simple_watchdog():
    print(">>> [忠诚的看门狗] 已启动！")
    print(">>> [任务] 每秒扫描全屏，发现二维码立刻尖叫。")
    print(">>> 按 Ctrl+C 可以让卑微的我停止工作。")

    while True:
        try:
            # 1. 抓取全屏
            # 我不敢遗漏屏幕的任何一个像素
            screen = ImageGrab.grab()

            # 转换格式给识别库吃
            # 这是一个将 PIL 图像转换为 numpy 数组的卑微过程
            frame = np.array(screen)

            # 2. 识别二维码
            decoded_objects = decode(frame)

            # 3. 判断结果
            if decoded_objects:
                # 发现目标！
                print("\n!!! [警报] 发现二维码 !!!")

                # 打印出内容给您审阅
                for obj in decoded_objects:
                    content = obj.data.decode('utf-8')
                    if content.startswith("https://mlearning.sjtu.edu.cn/lms/mobile2/forscan/?courseCode="):
                        try:
                            print(f"内容: {content}")
                            auto_sign(content)
                        except:
                            print("error")
                    else:
                        print(f"无法解析的内容: {content}")

                # 疯狂尖叫，呼唤主人
                alert_sound()
                # try: auto_sign(...)

                # 稍微暂停一下以免警报声连成一片太吵（或者您可以删掉这行让我一直叫）
                # time.sleep(0.5)
            else:
                pass

            # 4. 严格执行“每秒检测”
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n>>> 遵命，停止监听。")
            break
        except Exception as e:
            print(f"发生错误 (都是我的错): {e}")
            # 出错了也不停，休息一下继续干
            time.sleep(1)


if __name__ == "__main__":
    simple_watchdog()