import os
import re
import logging
import RPi.GPIO as GPIO
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from servo_config import unlock,lock
from dotenv import load_dotenv
logging.basicConfig(level=logging.DEBUG)
load_dotenv()
# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ["SLACK_BOT_API"])

def setup_servo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    servo = GPIO.PWM(12, 50)
    servo.start(0)
    return servo
# メンションされたとき
@app.event("app_mention")
def message_mention(say):
    say(f"メンションしても何も出えへんで")


@app.message("unlock0510")
def handle_unlock(ack, say):
    ack()
    servo = setup_servo()
    try:
        print("Opening...")
        for duty_cycle in range(125, 25, -1):
            servo.ChangeDutyCycle(duty_cycle / 10.0)
            time.sleep(0.02)
        servo.ChangeDutyCycle(0)
        time.sleep(1)

    finally:
        servo.stop()
        GPIO.cleanup()

@app.message("lock0510")
def handle_lock(ack, say):
    ack()
    servo = setup_servo()
    try:
        print("Closing...")
        for duty_cycle in range(25, 126):
            servo.ChangeDutyCycle(duty_cycle / 10.0)
            time.sleep(0.02)
        servo.ChangeDutyCycle(0)
        time.sleep(1)
    
    finally:
        servo.stop()
        GPIO.cleanup()

# すべてのメッセージに対するデフォルトの応答
@app.message(re.compile(".*"))
def default_response(message, say):
    say(channel = "C07UWMP356W",text = "そのメッセージには対応してへんわ！")

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_API"]).start()
    # lock()
