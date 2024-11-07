import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BOARD)  # BOARDでピン指定
    GPIO.setup(12, GPIO.OUT)  # 制御パルスの出力

def cleanup():
    GPIO.cleanup()  # GPIOのクリーンアップ

def create_servo():
    servo = GPIO.PWM(12, 50)  # PWMの設定（50Hzで正しい20msの周期）
    servo.start(0)
    return servo

def move_servo(servo, start, end, step):
    # スムーズに回転
    for duty_cycle in range(start, end, step):
        servo.ChangeDutyCycle(duty_cycle / 10.0)
        time.sleep(0.02)  # 短いスリープでスムーズな動きを実現
    servo.ChangeDutyCycle(0)
    time.sleep(1)  # 最終位置で少し待つ

def unlock(servo):
    print("Opening...")
    move_servo(servo, 125, 25, -1)

def lock(servo):
    print("Closing...")
    move_servo(servo, 25, 126, 1)


