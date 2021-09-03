  #include <WiFi.h>
  #include <PubSubClient.h>
  #include <ESP32Servo.h>
  
  WiFiClient espClient;
  PubSubClient client(espClient);


  // servo motors and their working pins
  Servo servo1;  
  Servo servo2;
  Servo servo3;
  Servo servo4;
  Servo servo5;

  const int servoPin1 = 13; 
  const int servoPin2 = 12;
  const int servoPin3 = 14;
  const int servoPin4 = 27;
  const int servoPin5 = 26;

  // sensor pins
  int sens1 = 33;
  int sens2 = 32;
  int sens3 = 35;
  int sens4 = 34;
  int sens5 = 39;

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
      servo1.setPeriodHertz(50);
      servo2.setPeriodHertz(50);
      servo3.setPeriodHertz(50);
      servo4.setPeriodHertz(50);
      servo5.setPeriodHertz(50);    
      servo1.attach(servoPin1); 
      servo2.attach(servoPin2);
      servo3.attach(servoPin3);
      servo4.attach(servoPin4);
      servo5.attach(servoPin5);
  }


  void setUpSensors(){
    pinMode(sens1, INPUT);
    pinMode(sens2, INPUT);
    pinMode(sens3, INPUT);
    pinMode(sens4, INPUT);
    pinMode(sens5, INPUT);  
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
      String topicName(topic);
  
      if(topicName == "room1"){
          if(message == "0"){
            turnOffUpperServo();
          }else{
            turnOnUpperServo();
          }
      }else if(topicName == "room2"){
          if(message == "0"){
            turnOffLowerServo();
          }else{
            turnOnLowerServo();
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
      client.subscribe("room1");
      client.subscribe("room2");
  }
  
   
  void loop(){
      client.loop();
  }


 ////////////////// temproray methods but servo's angles are right ////////////////////
  void turnOnUpperServo(){
       Serial.println("turn on upper");
       servo1.write(105);
       delay(500);
       servo1.write(40);
       delay(500);
       servo1.write(80);
  }


  void turnOffUpperServo(){
       Serial.println("turn off upper");
       servo1.write(105);
  }



  void turnOnLowerServo(){
       Serial.println("turn on lower");
       servo2.write(65);
       delay(500);
       servo2.write(140);
       delay(500);
       servo2.write(100);
  }


  void turnOffLowerServo(){
       Serial.println("turn off lower");
       servo2.write(65);
  }
  
