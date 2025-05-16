from machine import Pin, ADC
from time import sleep

# LED接線設定 
led_up = Pin(5, Pin.OUT)    # D1/GPIO5 (紅) 上↑
led_down = Pin(4, Pin.OUT)  # D2/GPIO4 (綠) 下↓
led_left = Pin(0, Pin.OUT)  # D3/GPIO0 (黃) 左←
led_right = Pin(2, Pin.OUT) # D4/GPIO2 (藍) 右→

# 搖桿接線設定 (根據您提供的接法)
joystick_x = ADC(0)    # VRx接A0 (X軸模擬輸入)

# 參數設定
X_CENTER = 512      # X軸中心值
X_THRESHOLD = 150   # X軸靈敏度


def clear_leds():
    led_up.off()
    led_down.off()
    led_left.off()
    led_right.off()

while True:
    # 讀取搖桿值
    x_val = joystick_x.read()  # X軸: 0~1023
    
    clear_leds()  # 先關閉所有LED
    
    # X軸控制左右LED
    if x_val < X_CENTER - X_THRESHOLD:
        led_left.on()
    elif x_val > X_CENTER + X_THRESHOLD:
        led_right.on()
    
    sleep(0.1)  # 控制刷新率