  #include <WiFi.h>
  #include <PubSubClient.h>
  
  WiFiClient espClient;
  PubSubClient client(espClient);
  
  // all working pins
  int led1 = 12;
  int led2 = 13;
  
  // wifi and broker data
  const char* ssid = "TP-LINK_5FEDE0";
  const char* password = "23604698";
  const char* mqttServer = "6.tcp.ngrok.io";
  const int mqttPort = 16889;
  const char* mqttUser = "";
  const char* mqttPassword = "";
   
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
  
  
  void reconnectToBroker(){
      while (!client.connected()) {
          Serial.println("Connecting to MQTT...");
          if (client.connect("ESP32Client", mqttUser, mqttPassword)){
              Serial.println("connected");
              client.publish("connect", "I'm connected");
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
            digitalWrite(led1, LOW );
          }else{
            digitalWrite(led1, HIGH);
          }
      }else if(topicName == "room2"){
          if(message == "0"){
            digitalWrite(led2, LOW );
          }else{
            digitalWrite(led2, HIGH);
          }
      }
  }
  
   
  void setup(){
      // setup serial and all working pins on esp
      pinMode(led1, OUTPUT);
      pinMode(led2, OUTPUT);
      Serial.begin(115200);
      
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

  
