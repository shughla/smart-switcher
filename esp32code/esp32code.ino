  #include <WiFi.h>
  #include <PubSubClient.h>
  #include <ESP32Servo.h>
  
  WiFiClient espClient;
  PubSubClient client(espClient);

  const char TOPIC[9] = "switcher";
  const int TOTAL_NUMBER = 5;
  // servo motors and their working pins
  Servo servo1;  
  Servo servo2;
  Servo servo3;
  Servo servo4;
  Servo servo5;
  
  Servo servos[5] = {servo1,servo2,servo3,servo4,servo5};
  
  const int servoPin1 = 13; 
  const int servoPin2 = 12;
  const int servoPin3 = 14;
  const int servoPin4 = 27;
  const int servoPin5 = 26;
  
  int servoPins[5] = {servoPin1,servoPin2,servoPin3,servoPin4,servoPin5};
  
  // sensor pins
  int sens1 = 33;
  int sens2 = 32;
  int sens3 = 35;
  int sens4 = 34;
  int sens5 = 39;
  
  int sensors[] = {sens1,sens2,sens3,sens4,sens5};
  
  // the led which is turn on when esp is connected to the broker
  int brokerLed = 15;


  
  // wifi and broker data
  const char* ssid = "TP-LINK_5FEDE0";
  const char* password = "23604698";
  const char* mqttServer = "2.tcp.ngrok.io";
  const int mqttPort = 19423;
  const char* mqttUser = "junior";
  const char* mqttPassword = "project";
   
  static const int DELAY_FOR_RECONNECT_BROKER = 2000;
  static const int DELAY_FOR_RECONNECT_WIFI = 500;
  
  
  void setupWiFi(){
      WiFi.begin(ssid, password);
      while (WiFi.status() != WL_CONNECTED){
          delay(DELAY_FOR_RECONNECT_WIFI);
          Serial.println("Connecting to WiFi..");
      }
      Serial.println("Connected to the WiFi network");
  }
  

  void setUpServos(){
      ESP32PWM::allocateTimer(0); 
      ESP32PWM::allocateTimer(1);
      ESP32PWM::allocateTimer(2);
      ESP32PWM::allocateTimer(3);
      for(int i = 0;i < TOTAL_NUMBER;i++){
        servos[i].setPeriodHertz(50);
        servos[i].attach(servoPins[i]); 
      }
  }


  void setUpSensors(){
    for(int i = 0;i<TOTAL_NUMBER;i++){
      pinMode(sensors[i],INPUT);
    }
  }

  boolean readSensor(int n){
    double val  = analogRead(sensors[n]);
    return val < 20;
  }
  
    void sendSensorData(){
    for(int i = 0;i<TOTAL_NUMBER;i++){
      String st = String(i);
      if(readSensor(i)){
        client.publish(TOPIC,i + ":1");
      }else{
        client.publish(TOPIC,i + ":0");
      }
    }
  }
  
  void reconnectToBroker(){
      while (!client.connected()) {
          Serial.println("Connecting to MQTT...");
          if (client.connect("ESP32Client", mqttUser, mqttPassword)){
              Serial.println("connected");
              client.publish("connect", "Esp32 devkit v1 is connected");
              analogWrite(brokerLed, 80); // show that esp is connected to the broker using blue led
          }else{
              Serial.print("failed with state ");
              Serial.println(client.state());
              delay(DELAY_FOR_RECONNECT_BROKER);
          }
      }
  }
  
  
  void callback(char* topic, byte* payload, unsigned int length){
      Serial.print("Message arrived in topic: ");
      Serial.println(topic);
      Serial.print("Message:");
      for (int i = 0; i < length; i++){
          Serial.print((char)payload[i]);
      }
      Serial.println();
      Serial.println("-----------------------");
      
      // temproray code, must be changed by main bussines logic
      char p[length];
      memcpy(p, payload, length);
      p[length] = NULL;
      String message(p);
      if(message == "check"){
            sendSensorData();
        return;
      }
      
      int index = message.substring(0,message.length()-2).toInt();
      int value = (message[message.length() - 1] - '0');

      if(index%2 == 0){
          if(value == 0){
            turnOffUpperServo(index);
          }else{
            turnOnUpperServo(index);
          }
      }else{
         if(value == 0){
            turnOffLowerServo(index);
         }else{
            turnOnLowerServo(index);
         }
      }
      
  }
  

  void setup(){
      // setup serial and all working pins on esp
      Serial.begin(115200);
      pinMode(brokerLed, OUTPUT);

      // servos
      setUpServos();

      // sensors
      setUpSensors();
      
      // wifi
      setupWiFi();
      
      // initialise client
      client.setServer(mqttServer, mqttPort);
      client.setCallback(callback);
      
      // connect to the broker
      reconnectToBroker(); 
  
      // subrscribe all topics
      client.subscribe(TOPIC);
  }
  
   
  void loop(){
      client.loop();
  }


 ////////////////// temproray methods but servo's angles are right ////////////////////
  void turnOnUpperServo(int i){
       Serial.println("turn on upper");
       servos[i].write(105);
       delay(500);
       servos[i].write(40);
       delay(500);
       servos[i].write(80);
  }


  void turnOffUpperServo(int i){
       Serial.println("turn off upper");
       servos[i].write(105);
  }



  void turnOnLowerServo(int i){
       Serial.println("turn on lower");
       servos[i].write(65);
       delay(500);
       servos[i].write(140);
       delay(500);
       servos[i].write(100);
  }


  void turnOffLowerServo(int i){
       Serial.println("turn off lower");
       servos[i].write(65);
  }
  
