
const int Analyze = 2;
const int Space = 3;
const int Finish = 4;

int AnalyzeState = 0;   
int SpaceState = 0;
int FinishState = 0;



void setup() {
  pinMode(Analyze, INPUT);
  pinMode(Space, INPUT);
  pinMode(Finish, INPUT);
  
}

void loop() {
  buttonPressAnalyze = digitalRead(Analyze);
  buttonPressSpace = digitalRead(Space);
  buttonPressFinish = digitalRead(Finish);

//reading the button pushing

  if (buttonPressAnalyze == HIGH) {
    Serial.println("analyze")
    
  } else if (buttonPressSpace==HIGH) {
    Serial.println("space")
    
  } else if(buttonPressFinish==HIGH) {
    Serial.println("finish")
    
  }
}
