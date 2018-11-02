
const int Analyze = 12;
const int Finish = 11;

int buttonPressAnalyze = 0;
int buttonPressFinish = 0;

void setup() {
  pinMode(Analyze, INPUT);
  pinMode(Finish, INPUT);
  
}

void loop() {
  int buttonPressAnalyze = digitalRead(Analyze);
  int buttonPressFinish = digitalRead(Finish);

//reading the button pushing

  if (buttonPressAnalyze == HIGH) {
    Serial.write("analyze");
     
  }else if(buttonPressFinish==HIGH) {
    Serial.write("finish");
    
  }
}
