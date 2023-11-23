import time

# ソフトウェアPWM
class SoftwarePWM:
    pin = 0
    duty = 0
    cnt = 0

    #コンストラクタ
    def __init__(self, pin):
        self.pin = pin
        print("GPIO.setup(self.pin, GPIO.OUT)")

    # モーターの回転
    def start(self, duty, cnt):
        self.duty = duty
        # if cnt < self.duty:
        #     print("GPIO.output(self.pin, GPIO.HIGH)")
        # else:
        #     print("GPIO.output(self.pin, GPIO.LOW)")

    # モーターの停止
    def stop(self):
        print("モータを停止します")
        print("GPIO.output(self.pin, GPIO.LOW)")

#エンコーダの値取得
class getEncoderValue:
    pinA = 0
    pinB = 0
    count = 0
    backEncoderA = 0
    backEncoderB = 0
    EncoderA = 0
    EncoderB = 0

    #コンストラクタ
    def __init__(self, pinA, pinB):
        self.pinA = pinA
        self.pinB = pinB
        print("エンコーダピンのセットアップ!")
        # GPIO.setup(self.pinA, GPIO.IN)
        # GPIO.setup(self.pinB, GPIO.IN)
    
    # エンコーダA相の値取得
    def getA(self, A):
        return A
    
    # エンコーダB相の値取得
    def getB(self, B):
        return B
    
    # エンコーダの値取得（ループ毎に呼び出し必須！）
    def checkEncoder(self, A, B):
        self.EncoderA = self.getA(A)
        self.EncoderB = self.getB(B)
        if self.EncoderA == 1 and self.EncoderB == 0  and self.backEncoderA == 0 and self.backEncoderB == 0:
            self.count += 1        
        elif self.EncoderA == 1 and self.EncoderB == 1  and self.backEncoderA == 1 and self.backEncoderB == 0:
            self.count += 1
        elif self.EncoderA == 0 and self.EncoderB == 1  and self.backEncoderA == 1 and self.backEncoderB == 1:
            self.count += 1
        elif self.EncoderA == 0 and self.EncoderB == 0  and self.backEncoderA == 0 and self.backEncoderB == 1:
            self.count += 1
        elif self.EncoderA == 0 and self.EncoderB == 1  and self.backEncoderA == 0 and self.backEncoderB == 0:
            self.count -= 1
        elif self.EncoderA == 1 and self.EncoderB == 1  and self.backEncoderA == 0 and self.backEncoderB == 1:
            self.count -= 1
        elif self.EncoderA == 1 and self.EncoderB == 0  and self.backEncoderA == 1 and self.backEncoderB == 1:
            self.count -= 1
        elif self.EncoderA == 0 and self.EncoderB == 0  and self.backEncoderA == 1 and self.backEncoderB == 0:
            self.count -= 1
        self.backEncoderA = self.EncoderA
        self.backEncoderB = self.EncoderB
        return self.count
    

# GPIOピンのナンバリング設定
# GPIO.setmode(GPIO.BCM)

# GPIOピンの初期化
shakeMotorCW = SoftwarePWM(23)
shakeMotorCCW = SoftwarePWM(24)
proppelerMotor = SoftwarePWM(13)

# エンコーダの初期化
shakeEncoder = getEncoderValue(16, 20)
proppelerEncoder = getEncoderValue(5, 6)

# モーターの回転
cnt = 0
tempCnt = 0
cntA=25
tempCntA=0
encoderA=0
encoderB=0
while cnt < 1000000:
    # カウントアップ
    cnt += 1
    tempCnt = cnt % 100
    cntA += 1
    tempCntA = cntA % 100

    if tempCnt < 50:
        encoderA = 0
    else:
        encoderA = 1

    if tempCntA < 50:
        encoderB = 0
    else:
        encoderB = 1
    

    # モーターの回転
    shakeMotorCW.start(50, tempCnt)
    shakeMotorCCW.start(50, tempCnt)
    proppelerMotor.start(50, tempCnt)

    # エンコーダの値取得
    shake = shakeEncoder.checkEncoder(encoderA, encoderB)
    proppeler = proppelerEncoder.checkEncoder(encoderA, encoderB)
    print(encoderA,encoderB,shake,proppeler, end="\n")
          
    # エンコーダの値表示
    if cnt % 1000 == 0:
        print("首振りエンコーダのカウント" + str(shake))
        print("プロペラエンコーダのカウント" + str(proppeler))

    # 0.001秒待機
    time.sleep(0.001)