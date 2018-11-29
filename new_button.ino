
#define ANALYZE 12
#define FINISH 10
#define SPACE 8


void setup() {
  pinMode(ANALYZE, INPUT);
  digitalWrite(ANALYZE, HIGH);

  pinMode(SPACE, INPUT);
  digitalWrite(SPACE, HIGH);
  
  pinMode(FINISH, INPUT);
  digitalWrite(FINISH, HIGH);
  
  Serial.begin(9600);
  
}

void loop() {
  if(digitalRead(ANALYZE) == LOW){
  Serial.println("A");
  }
  
  if(digitalRead(SPACE) == LOW){
  Serial.println("S");
  }
  
  if(digitalRead(FINISH) == LOW){
  Serial.println("F");
  }
  
delay(100);
    }
  
