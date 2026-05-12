// L293D Motor Driver - Obstacle Avoidance Robot
// Pin map:
//   Left Motor:  D11 (IN1), D12 (IN2)
//   Right Motor: D9  (IN3), D8  (IN4)
//   Ultrasonic:  D6  (trig), D5  (echo)

// Left Motor
const int motorPin1 = 11;
const int motorPin2 = 12;
// Right Motor
const int motorPin3 = 9;
const int motorPin4 = 8;
// Ultrasonic
const int trigPin = 6;
const int echoPin = 5;

// Thresholds
const int STOP_DISTANCE   = 15;         // cm — obstacle confirmed if closer than this
const int CLEAR_DISTANCE  = 30;         // cm — path is clear if farther than this
const int MIN_VALID_CM    = 2;          // reject sensor readings below this (glitch)
const int MAX_VALID_CM    = 400;        // reject sensor readings above this
const unsigned long PULSE_TIMEOUT  = 20000UL;  // µs — max echo wait
const unsigned long MAX_TURN_MS    = 3000UL;   // ms — max time turning one direction
const unsigned long BACKUP_MS      = 400UL;    // ms — reverse before turning
const unsigned long CLEAR_DRIVE_MS = 700UL;    // ms — drive forward after clearing obstacle

// State
int consecutiveClose = 0;

void setup() {
  Serial.begin(115200);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  sumoStop();

  // ── Sensor diagnostic ──────────────────────────────────────────────────
  // Open Serial Monitor at 115200. Hold your hand ~20 cm in front of the
  // sensor. You should see durations ~1200 µs and distances ~20 cm.
  // If every line shows "dur=0" the sensor has no power, a bad ground,
  // or trig/echo wires are swapped — swap TRIG_PIN / ECHO_PIN and retry.
  Serial.println("Booting... sensor diagnostic (5 raw readings):");
  delay(500);
  for (int i = 0; i < 5; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(4);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long dur = pulseIn(echoPin, HIGH, PULSE_TIMEOUT);
    Serial.print("  dur=");
    Serial.print(dur);
    Serial.print(" us  ->  ");
    Serial.print((int)(dur * 0.034f / 2.0f));
    Serial.println(" cm");
    delay(100);
  }

  Serial.println("Warming up sensor.");
  delay(1500);
  for (int i = 0; i < 10; i++) {
    getDistance();
    delay(60);
  }
  Serial.println("Ready. Moving.");
}

// ─── Sensor ──────────────────────────────────────────────────────────────────

int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(4);          // slightly longer reset clears any residual charge
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, PULSE_TIMEOUT);
  if (duration == 0) return 999;

  int d = (int)(duration * 0.034f / 2.0f);
  if (d < MIN_VALID_CM || d > MAX_VALID_CM) return 999;
  return d;
}

// Median-of-5 — robust against single noisy spikes
int getStableDistance() {
  int r[5];
  for (int i = 0; i < 5; i++) {
    r[i] = getDistance();
    delay(60);  // HC-SR04 needs ≥60 ms between pulses; shorter gaps cause echo bleed
  }
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4 - i; j++) {
      if (r[j] > r[j + 1]) {
        int tmp = r[j]; r[j] = r[j + 1]; r[j + 1] = tmp;
      }
    }
  }
  return r[2];
}

// ─── Main Loop ───────────────────────────────────────────────────────────────

void loop() {
  int distance = getStableDistance();

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" cm | consecutiveClose=");
  Serial.println(consecutiveClose);

  if (distance <= STOP_DISTANCE) {
    consecutiveClose++;
  } else {
    consecutiveClose = 0;
  }

  // Two confirmed close readings before reacting — kills false positives
  if (consecutiveClose >= 2) {
    Serial.println("CONFIRMED OBSTACLE. Avoiding.");
    avoidObstacle();
    consecutiveClose = 0;
  } else {
    forwardL();
    forwardR();
  }

  delay(50);
}

// ─── Avoidance ───────────────────────────────────────────────────────────────

// Turns in one direction until clear or timeout.
// goRight=true → pivot right (left wheel forward, right stopped).
// goRight=false → pivot left (right wheel forward, left stopped).
// Returns true if the path cleared within the timeout.
bool tryTurn(bool goRight, unsigned long timeout) {
  if (goRight) {
    forwardL();
    sumoStopR();
  } else {
    sumoStopL();
    forwardR();
  }

  unsigned long start = millis();
  while (millis() - start < timeout) {
    int d = getStableDistance();
    Serial.print("  Turning ");
    Serial.print(goRight ? "RIGHT" : "LEFT");
    Serial.print("  d=");
    Serial.println(d);
    if (d >= CLEAR_DISTANCE) {
      sumoStop();
      return true;
    }
    delay(30);
  }
  sumoStop();
  return false;
}

void avoidObstacle() {
  sumoStop();
  delay(200);

  // Step 1: back away from the obstacle
  reverseL();
  reverseR();
  delay(BACKUP_MS);
  sumoStop();
  delay(200);

  // Step 2: try turning right; if still blocked, sweep left
  Serial.println("  Trying RIGHT...");
  bool cleared = tryTurn(true, MAX_TURN_MS);

  if (!cleared) {
    // Swing past centre and try left — double timeout covers the extra angle
    Serial.println("  RIGHT blocked. Trying LEFT...");
    cleared = tryTurn(false, MAX_TURN_MS * 2);
  }

  if (!cleared) {
    // Completely boxed in — back up further and let the main loop retry
    Serial.println("  Both sides blocked. Reversing more.");
    reverseL();
    reverseR();
    delay(600);
    sumoStop();
    delay(300);
    return;
  }

  // Step 3: drive forward past the obstacle before handing back to loop()
  Serial.println("  Path clear — driving past obstacle.");
  forwardL();
  forwardR();
  delay(CLEAR_DRIVE_MS);
  sumoStop();
  delay(100);
}

// ─── Motor Control ───────────────────────────────────────────────────────────

void sumoStopL() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
}

void sumoStopR() {
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
}

void sumoStop() {
  sumoStopL();
  sumoStopR();
}

void forwardL() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
}

void forwardR() {
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
}

void reverseL() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
}

void reverseR() {
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
}
