from machine import Pin, ADC, I2C
import ssd1306
import time
import random

# 初始化I2C和OLED顯示器
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 初始化Joystick
joystick_x = ADC(0)  # X軸
joystick_y = Pin(15, Pin.IN, Pin.PULL_UP)  # Y軸（D8）
buzzer = Pin(14, Pin.OUT)  # 假設蜂鳴器接在D12針腳


# 遊戲參數
player_x = 64  # 玩家初始位置（OLED寬度的一半）
asteroids = []  # 隕石列表
score = 0  # 初始分數
game_time = 30  # 計時30秒
last_spawn_time = time.time()  # 隕石生成時間

def play_game_over_sound():
    # 播放結束音效
    for i in range(3):  # 播放三次
        buzzer.on()  # 開啟蜂鳴器
        time.sleep(0.1)  # 持續0.1秒
        buzzer.off()  # 關閉蜂鳴器
        time.sleep(0.1)  # 間隔0.1秒
        
def spawn_asteroid_row():
    # 隨機生成一排隕石
    row = [20, 40, 60, 80, 100]
    asteroids.extend(row)

def display_game(player_x, shoot=False):
    oled.fill(0)  # 清屏
    oled.text('R', player_x, 50)  # 顯示玩家（字母R）

    # 顯示隕石
    for asteroid_x in asteroids:
        oled.text('X', asteroid_x, 0)  # 隕石在第一行

    # 當射擊時，顯示光線
    if shoot:
        for y in range(40, -10, -10):  # 從玩家Y位置向上
            oled.text('|', player_x, y)

        # 檢查光線是否穿過隕石（正負3格範圍）
        for offset in range(-3, 4):  # 檢查範圍
            if (player_x + offset) in asteroids:
                asteroids.remove(player_x + offset)  # 移除隕石
                global score
                score += 10  # 增加分數

    oled.show()  # 更新顯示

def display_game_over():
    oled.fill(0)  # 清屏
    oled.text('GAME OVER!', 10, 30)
    oled.text('You get ' + str(score) + ' score.', 0, 50)
    oled.show()
    play_game_over_sound()  # 播放結束音效

# 等待開始遊戲
oled.fill(0)
oled.text('Space Protector!', 10, 20)
time.sleep(3)
oled.show()

# 主循環
start_time = time.time()  # 遊戲開始時間
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    # 檢查遊戲時間是否結束
    if elapsed_time >= game_time:
        display_game_over()
        break

    joystick_x_val = joystick_x.read()  # 讀取X軸值
    joystick_y_val = joystick_y.value()  # 讀取Y軸值

    # 根據Joystick位置調整玩家位置
    if joystick_x_val < 100:  # 向左推
        player_x -= 3  # 向左移動3格
    elif joystick_x_val > 900:  # 向右推
        player_x += 3  # 向右移動3格

    # 限制玩家位置在OLED顯示範圍內
    player_x = max(0, min(player_x, 120))

    # 檢查是否射擊
    shoot = joystick_y.value() == 1  # 當Y軸為1時射擊
    display_game(player_x, shoot)

    # 每3秒生成一排隕石
    if current_time - last_spawn_time > 3:
        spawn_asteroid_row()
        last_spawn_time = current_time
    
    time.sleep(0.04)  # 每0.04秒更新一次