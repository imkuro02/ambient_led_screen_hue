// Example 2 - Receive with an end-marker

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

#include <FastLED.h>

#define LED_PIN     12
#define NUM_LEDS    24
#define BRIGHTNESS  255
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
CRGBArray<NUM_LEDS>leds;

void setup() {
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    Serial.begin(2000000);
    Serial.println("<Arduino is ready>");
}

int IRGB[4];
int cur_IRGB = 0; 
void loop() {
    recvWithEndMarker();
    showNewData();
    if(cur_IRGB==24){ // if all leds have been set) 
      FastLED.show(); 
      Serial.flush();
    }
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\\';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        //Serial.print(rc);

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

void showNewData() {
    if (newData == true) {
        //Serial.print("This just in ... ");
        //Serial.println(receivedChars);
        newData = false;

        char* d = strtok(receivedChars, ",");
        for(int i = 0; i<4; i++){
            //Serial.println(d);            
            int y = atoi(d);
            d = strtok(NULL, ",");                 
            IRGB[i] = y;     
        }
        
        //leds[IRGB[0]] = strtol("0xFFFFFF", NULL, 0);
        leds[IRGB[0]].setRGB( IRGB[1], IRGB[2], IRGB[3]);           
          
        cur_IRGB = IRGB[0]; 
    }
}