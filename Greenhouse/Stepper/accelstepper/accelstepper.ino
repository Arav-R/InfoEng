// Defines pins
#define stepPin 3
#define dirPin 2
#define leftSwitchPin 10
#define rightSwitchPin 11

// Define states for the state machine
enum State {
  HOMING,
  MOVING_TO_POSITION,
  IDLE
};

State currentState = HOMING;
int targetSteps = 0;
int currentPos = 0;

bool motorMoving = false;

// Map input positions (1-10) to target steps
const int positionMap[] = {2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000};

void setup() {
  // Sets the pins as outputs or inputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(leftSwitchPin, INPUT_PULLUP);
  pinMode(rightSwitchPin, INPUT_PULLUP);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  switch (currentState) {
    case HOMING:
      Serial.println("Homing: ");
      homingState();
      break;
    case MOVING_TO_POSITION:
      Serial.println("Moving!");
      if (targetSteps >= 0) {
        moveRight(targetSteps);
      } else {
        moveLeft(targetSteps);
      }
      break;
    case IDLE:
      // Motor is idle
      // Serial.println("Idle: ");
      serialEvent();
      break;
  }
}

void homingState() {
  // Check the state of the left limit switch
  bool leftSwitchState = digitalRead(leftSwitchPin);

  // Print the state of the left limit switch to the serial monitor
  Serial.print("Left Switch: ");
  Serial.println(leftSwitchState);

  // If the left limit switch is not triggered, rotate the motor clockwise
  if (leftSwitchState) {
      Serial.println("homing left");
      for (int x = 0; x < 200; x++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(200);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(200);
      }

  } else {
    // If the left limit switch is triggered, stop the motor
    stopMotor();
    // Move to the next state
    currentState = IDLE;
  }
}

void moveLeft(int steps) {
  // Rotate the motor to the left
  digitalWrite(dirPin, LOW);

  // Rotate the motor for the specified number of steps
  for (int x = 0; x < abs(steps); x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(300);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(300);
  }

  // Motor has reached the target position, stop the motor
  stopMotor();
  // Move to the IDLE state
  Serial.print("Current Pos: ");
  Serial.println(currentPos);
  currentState = IDLE;
}

void moveRight(int steps) {
  // Rotate the motor to the right
  digitalWrite(dirPin, HIGH);

  // Rotate the motor for the specified number of steps
  for (int x = 0; x < abs(steps); x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(300);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(300);
  }

  // Motor has reached the target position, stop the motor
  stopMotor();
  // Move to the IDLE state
  Serial.print("Current Pos: ");
  Serial.println(currentPos);
  currentState = IDLE;
}

void stopMotor() {
  // Stop the motor by setting both step and direction pins low
  digitalWrite(stepPin, LOW);
  digitalWrite(dirPin, LOW);
}

void serialEvent() {
  // Check if serial data is available
  while (Serial.available()) {
    // Read the command from the serial monitor
    int position = Serial.parseInt();

    // Ignore any remaining characters in the serial buffer, including newline
    while (Serial.available() > 0) {
      Serial.read();
    }

    // Map the input position to target steps
    if (position >= 1 && position <= 10) {
      targetSteps = positionMap[position - 1];
    } else {
      Serial.println("Invalid position input.");
      targetSteps = 0; // Reset targetSteps if input is invalid
    }

    // Print feedback to the serial monitor
    Serial.print("Moving motor to position ");
    Serial.println(targetSteps);
    
    // Move to the MOVING_TO_POSITION state
    currentState = MOVING_TO_POSITION;

    targetSteps = targetSteps - currentPos;

    currentPos = currentPos + targetSteps; // Update current position

    Serial.print("Relative Steps: ");
    Serial.println(targetSteps);
  }
}