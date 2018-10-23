
const int buttonPin = 7;
int buttonState = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(buttonPin,INPUT); 
}

void loop() {
  // put your main code here, to run repeatedly:
   buttonState = digitalRead(buttonPin);

   if (buttonState == HIGH) {
    Serial.print("boop");
   }
   else {
     Serial.print("noop");
   }
}
