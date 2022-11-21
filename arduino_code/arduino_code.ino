// Example 2 - Receive with an end-marker

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

#include <FastLED.h>

#define LED_PIN     10
#define NUM_LEDS    24
#define BRIGHTNESS  255
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
CRGBArray<NUM_LEDS>leds;

void setup() {
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    Serial.begin(115200);
    Serial.println("<Arduino is ready>");
}

void loop() {
    recvWithEndMarker();
    showNewData();

    
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\\';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        Serial.print(rc);

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}
int IRGB[4];
void showNewData() {
    if (newData == true) {
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
    

        /*
        char data [] = "12,34";
        Serial.println (data);

        char* d = strtok(data, ",");
        while (d != NULL) {
            Serial.println (d);
            d = strtok(NULL, ",");
        }
        */

        

        char* d = strtok(receivedChars, ",");
        for(int i = 0; i<4; i++){
            //Serial.println(d);
            
            int y = atoi(d);
            d = strtok(NULL, ",");
            
            
            IRGB[i] = y;
            //Serial.println(y);
            //Serial.println(IRGB[i]);
            //Serial.println("...");         
        }

        // this line makes it so one sample controls 6 pixels

        switch(IRGB[0]){
          case 0:
            leds[0].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[1].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[2].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[3].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;          
          case 1:
            leds[4].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[5].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[6].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[7].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;          
          case 2:
            leds[8].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[9].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[10].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[11].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;          
          case 3:
            leds[12].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[13].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[14].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[15].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;   
          case 4:
            leds[16].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[17].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[18].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[19].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;          
          case 5:
            leds[20].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[21].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[22].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
            leds[23].setRGB( IRGB[1], IRGB[2], IRGB[3]);   
          break;          
        }
        
                         
        

        
        /*
        leds[IRGB[0]].setRGB( IRGB[1], IRGB[2], IRGB[3]);
        FastLED.show();  
        Serial.flush();
        */
    }
    FastLED.show(); 
    Serial.flush();
    //pixels.clear();
    //pixels.setBrightness(10);
    //pixels.setPixelColor(IRGB[0], pixels.Color(IRGB[1], IRGB[2], IRGB[3]));

    
}