from machine import Pin, ADC
from time import sleep

# 設定 LED 腳位
led_up = Pin(5, Pin.OUT)    # GPIO5
led_down = Pin(4, Pin.OUT)  # GPIO4
led_left = Pin(0, Pin.OUT)  # GPIO0
led_right = Pin(2, Pin.OUT) # GPIO2

# 設定搖桿輸入 (ESP32)
vrx = ADC(Pin(35))  # GPIO34 用於 X 軸
vry = ADC(Pin(36))  # GPIO35 用於 Y 軸

# 設定 ADC 參數 (ESP32 特有)
vrx.atten(ADC.ATTN_11DB)    # 設置衰減為 11dB (0-3.3V)
vry.atten(ADC.ATTN_11DB)    # 設置衰減為 11dB (0-3.3V)
vrx.width(ADC.WIDTH_12BIT)  # 設置解析度為 12 位 (0-4095)
vry.width(ADC.WIDTH_12BIT)  # 設置解析度為 12 位 (0-4095)

# 閾值設定
X_CENTER = 2048     # 中心值 (12位ADC，範圍0-4095)
Y_CENTER = 2048
THRESHOLD = 1000  # 靈敏度範圍（可調）

def clear_leds():
    led_up.off()
    led_down.off()
    led_left.off()
    led_right.off()

def get_smooth_value(adc):
    values = []
    for _ in range(5):  # 讀取5次
        values.append(adc.read())
        sleep(0.01)
    
    # 排除極端值
    values.sort()
    return values[2]  # 返回中間值

def control_leds(x_val, y_val):
    clear_leds()
    
    # 顯示詳細資訊
    print("-" * 40)
    print("X軸: {}, Y軸: {}".format(x_val, y_val))
    
    # 控制左右 LED (X軸)
    if x_val < X_CENTER - THRESHOLD:
        led_right.on()
        print("右")
    elif x_val > X_CENTER + THRESHOLD:
        led_left.on()
        print("左")
        
    # 控制上下 LED (Y軸)
    if y_val < Y_CENTER - THRESHOLD:
        led_down.on()
        print("下")
    elif y_val > Y_CENTER + THRESHOLD:
        led_up.on()
        print("上")


# 等待搖桿穩定
print("等待搖桿穩定...")
sleep(2)

# 主循環
while True:
    try:
        # 讀取搖桿值
        x = get_smooth_value(vrx)
        y = get_smooth_value(vry)
        
        # 控制 LED
        control_leds(x, y)
        
        # 延遲
        sleep(0.1)
        
    except Exception as e:
        print("錯誤：", e)
        sleep(1)