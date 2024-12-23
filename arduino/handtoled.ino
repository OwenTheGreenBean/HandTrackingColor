const int redPin = 9;    // Connect to red pin of RGB LED
const int greenPin = 10; // Connect to green pin of RGB LED
const int bluePin = 11;  // Connect to blue pin of RGB LED

void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String rgbValues = Serial.readStringUntil('\n');  // Read the incoming string until newline
    int commaIndex1 = rgbValues.indexOf(',');         // Find the first comma
    int commaIndex2 = rgbValues.lastIndexOf(',');     // Find the last comma

    // Parse the RGB values from the string
    int red = rgbValues.substring(0, commaIndex1).toInt();
    int green = rgbValues.substring(commaIndex1 + 1, commaIndex2).toInt();
    int blue = rgbValues.substring(commaIndex2 + 1).toInt();

    // Write the RGB values to the LED pins
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);
  }
}
