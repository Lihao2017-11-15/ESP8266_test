"""
ESP8266已知的问题
http://docs.micropython.org/en/latest/esp8266/general.html
"""

import network
import webrepl
import webrepl_setup
from machine import Pin, I2C
import uos
from machine import UART
from machine import Pin
from machine import Timer
import time
import esp
import machine
from machine import I2C, Pin, SPI, UART
import os



def show_file(filename):
    """显示文件内容"""
    with open(filename, 'r') as f:
        for line in f.readlines():
            print(line)


def show_fw():
    """检查固件是否正确,仅ESP8266,ESP32等"""
    try:
        import esp
        print(esp.check_fw())
    except:
        return


# os.listdir()
# show_file('boot.py')
show_fw()
# i2c = I2C(1,scl=)

# 以下代码来自http://docs.micropython.org/en/latest/esp8266/quickref.html
machine.freq(160000000)
machine.freq()

esp.osdebug(None)       # turn off vendor O/S debugging messages
esp.osdebug(0)          # redirect vendor O/S debugging messages to UART(0)


time.sleep(1)           # sleep for 1 second
time.sleep_ms(500)      # sleep for 500 milliseconds
time.sleep_us(10)       # sleep for 10 microseconds
start = time.ticks_ms()  # get millisecond counter
delta = time.ticks_diff(time.ticks_ms(), start)  # compute time difference


# 计时器
# 支持虚拟（基于RTOS）计时器。使用计时器ID为-1 的machine.Timer类：
tim = Timer(-1)
tim.init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t: print(1))
tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t: print(2))
# 周期以毫秒为单位。


# 引脚和GPIO
# 使用machine.Pin类：
p0 = Pin(0, Pin.OUT)    # create output pin on GPIO0
p0.on()                 # set pin to "on" (high) level
p0.off()                # set pin to "off" (low) level
p0.value(1)             # set pin to on/high

p2 = Pin(2, Pin.IN)     # create input pin on GPIO2
print(p2.value())       # get value, 0 or 1

p4 = Pin(4, Pin.IN, Pin.PULL_UP)  # enable internal pull-up resistor
p5 = Pin(5, Pin.OUT, value=1)  # set pin high on creation
# 可用的引脚为：0、1、2、3、4、5、12、13、14、15、16，它们对应于ESP8266芯片的实际GPIO引脚编号。请注意，许多最终用户板使用其自己的临时引脚编号（例如，标记为D0，D1等）。由于MicroPython支持不同的板卡和模块，因此选择了物理引脚编号作为最低的公分母。有关板逻辑引脚和物理芯片引脚之间的映射，请查阅板文档。
# 请注意，引脚（1）和引脚（3）分别是REPL UART TX和RX。另请注意，Pin（16）是一个特殊的引脚（用于从深度睡眠模式唤醒），可能不适用于诸如的更高级别的类 Neopixel。

# UART（串行总线）
# 参见machine.UART。

uart = UART(0, baudrate=9600)
uart.write('hello')
uart.read(5)  # read up to 5 bytes
# 提供两个UART。UART0在引脚1（TX）和3（RX）上。UART0是双向的，默认情况下用于REPL。UART1位于引脚2（TX）和8（RX）上，但是引脚8用于连接闪存芯片，因此UART1仅是TX。

# 当UART0连接到REPL时，UART（0）上的所有传入字符都直接进入stdin，因此uart.read（）将始终返回None。如果需要从UART（0）读取字符，同时又将其用于REPL（或分离，读取然后重新连接），请使用sys.stdin.read（）。分离后，UART（0）可用于其他目的。

# 如果在启动REPL（硬复位或软复位）时，任何一个dupterm插槽中没有任何对象，则将自动连接UART（0）。否则，恢复没有REPL的主板的唯一方法是完全擦除并重新刷新（这将安装连接REPL的默认boot.py）。

# 要将REPL与UART0分离，请使用：

uos.dupterm(None, 1)
# 默认情况下，REPL是附加的。如果已拆离它，请使用以下方法重新连接它：

uart = machine.UART(0, 115200)
uos.dupterm(uart, 1)




sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print("connecting to network...")
    sta_if.active(True)
    # Connect to an AP <ap_name>&<password> is your route name&password
    sta_if.connect("HOWO2.4G", "gsds-1512")
    while not sta_if.isconnected():  # Check for successful connection
        pass
print("network config:", sta_if.ifconfig())
webrepl.start()

webrepl_setup

# WebREPL（Web浏览器交互式提示）
# WebREPL（通过WebSockets进行的REPL，可通过Web浏览器访问）是ESP8266端口可用的实验性功能。从https: // github.com/micropython/webrepl（可从http: // micropython.org/webrepl获得的托管版本）下载Web客户端，并通过执行以下命令对其进行配置：
# 并按照屏幕上的说明进行操作。重新启动后，它将可用于连接。如果禁用了启动时自动启动，则可以使用以下命令按需运行配置的守护程序：

webrepl.start()
# 支持的使用WebREPL的方式是通过连接到ESP8266接入点，但如果守护程序处于活动状态，则守护进程也会在STA接口上启动，因此，如果您的路由器已设置且正常工作，则在连接到正常Internet时也可以使用WebREPL接入点（如果遇到任何问题，请使用ESP8266 AP连接方法）。
# 除了可以访问终端/命令提示符外，WebREPL还提供了文件传输功能（上传和下载）。Web客户端具有用于相应功能的按钮，或者您可以使用webrepl_cli.py 上面存储库中的命令行客户端。
