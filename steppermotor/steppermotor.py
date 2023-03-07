import RPi.GPIO as GPIO
from time import sleep

'''
motor pins
En0 14
St0 15
Dir0 18
min0 4
max0 17
-----
En1 23
St1 24
Dir1 25
min1 27
max1 22
-----
En2 16
St2 20
Dir2 21
min2    currently using pin GPIO 10 for min 
max2 10 not using max as pin gpio 10 is used for min

Direction To Origin -
x-motor: anti-clockwise
y-motor: anti-clockwise
w-motor: clockwise 

'''

class StepperHandler():
	
	__CLOCKWISE = 1
	__ANTI_CLOCKWISE = 0
	
	def __init__(self,  delay=0.208, stepsPerRevolution=200):
		
		# Configure instance
		self.CLOCKWISE = self.__CLOCKWISE
		self.ANTI_CLOCKWISE = self.__ANTI_CLOCKWISE
		self.Delay = delay
		self.RevolutionSteps = stepsPerRevolution
		self.CurrentDirection = self.CLOCKWISE
		self.CurrentStep = 0

		self.EnableX = 16
		self.StepX = 20
		self.DirectionX = 21
		self.EnableY = 23
		self.StepY = 24
		self.DirectionY = 25
		self.EnableW = 14
		self.StepW = 15
		self.DirectionW = 18

		self.Xmin = 10 #actually pin max
		self.Xmax = 9  #not assigned pin
		self.Ymin = 27
		self.Ymax = 22
		self.Wmin = 4
		self.Wmax = 17

		# Setup gpio pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(self.StepX, GPIO.OUT)
		GPIO.setup(self.EnableX, GPIO.OUT)
		GPIO.setup(self.DirectionX, GPIO.OUT)
		GPIO.setup(self.StepY, GPIO.OUT)
		GPIO.setup(self.EnableY, GPIO.OUT)
		GPIO.setup(self.DirectionY, GPIO.OUT)
		GPIO.setup(self.StepW, GPIO.OUT)
		GPIO.setup(self.EnableW, GPIO.OUT)
		GPIO.setup(self.DirectionW, GPIO.OUT)

		GPIO.setup(self.Xmin, GPIO.IN)
		GPIO.setup(self.Xmax, GPIO.IN)
		GPIO.setup(self.Ymin, GPIO.IN)
		GPIO.setup(self.Ymax, GPIO.IN)
		GPIO.setup(self.Wmin, GPIO.IN)
		GPIO.setup(self.Wmax, GPIO.IN)

	def setParking(self):
		print("Parking radiation source in source holder")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor

		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymax)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionW, self.CLOCKWISE)
		while GPIO.input(self.Wmin)==1:
			GPIO.output(self.StepW, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepW, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionX, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Xmin)==1:
			GPIO.output(self.StepX, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepX, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionY, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Ymin)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.EnableW, GPIO.HIGH)   #w-motor
		GPIO.output(self.EnableY, GPIO.HIGH)	#y-motor 
		GPIO.output(self.EnableX, GPIO.HIGH)	#x-motor
	
	def getReadyForScan(self):
		print("Getting Ready for source scan")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor

		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymax)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

	def Step(self, enablePin, stepPin, directionPin, stepsToTake, direction = __CLOCKWISE):
		
		GPIO.setup(stepPin, GPIO.OUT)
		GPIO.setup(enablePin, GPIO.OUT)
		GPIO.setup(directionPin, GPIO.OUT)

		print("Step Pin: " + str(stepPin) + " Direction Pin: " + str(directionPin) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(enablePin, GPIO.LOW)
		GPIO.output(directionPin, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
			print("Step " + str(x))
			GPIO.output(stepPin, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(stepPin, GPIO.LOW)
			sleep(self.Delay)

		#GPIO.output(senablePin, GPIO.HIGH)

# Define pins
ENABLE_PIN = 14
STEP_PIN = 15
DIRECTION_PIN = 18

stepperHandler = StepperHandler(0.005)
# Create a new instance of our stepper class (note if you're just starting out with this you're probably better off using a delay of ~0.1)
stepperHandler.getReadyForScan()
# Go forwards once
#stepperHandler.Step(100)
stepperHandler.Step(ENABLE_PIN, STEP_PIN, DIRECTION_PIN, 400, stepperHandler.ANTI_CLOCKWISE)
stepperHandler.setParking()
# Go backwards once
#stepperHandler.Step(100, stepperHandler.ANTI_CLOCKWISE)
