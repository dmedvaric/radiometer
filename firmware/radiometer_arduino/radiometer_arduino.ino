#include <AD770X.h>
AD770X ad7705(65536);
int v;
//// Definiranje konstanti
const int irisRelayOut = 8;
//// Derfirnieanje varijabli
int irisCommand;
// Response wait timeout
int iris_timeout = 500; //mikrosekunde
int enableTimer = 0;
long sps_previous_micros = 0;
unsigned int ADCValue;
byte b1, b2;
void irisOff(){
  // zatvaranje bloka za pristizanje podataka
  digitalWrite(irisRelayOut, LOW);
  enableTimer = 0;
  delay(10);
  Serial.println("Response");
  }
void irisOn(){
  // Otvaranje bloka za pristizanje podataka
  digitalWrite(irisRelayOut, HIGH);
  Serial.println("Response");
  delay(200);
  enableTimer = 1;
  }
void checkIris()
{
    long         previousMicros = 0;
    previousMicros = micros();
    while((micros()-previousMicros)<iris_timeout)
    {
        if(Serial.available()>0)
        {
            // traženje slijedećeg cijelog broja u dolazećem toku podataka
            irisCommand = Serial.read();
            if (irisCommand == '1') irisOn();
            else if (irisCommand == '0') irisOff();
        }
    }
}
void setup()
{
 ad7705.reset();
 ad7705.init(AD770X::CHN_AIN1);  
 // ad7705.init(AD770X::CHN_AIN2);
   Serial.begin(115200);
}
void loop()
{
    if(enableTimer){
      //Serial.println(ad7705.readADResult(AD770X::CHN_AIN1));
      ADCValue = ad7705.readADResult(AD770X::CHN_AIN1);
      // pretvaranje podatka u 2 dijela za slanje
      b1 = ADCValue&0xFF;
      b2 = ( ADCValue >> 8 )& 0xFF;
      // Slanje podataka na Python
      Serial.write(b1);
      Serial.write(b2);
      // Serial.println(ADCValue);
      }
    checkIris();
/*  v = ad7705.readADResult(AD770X::CHN_AIN1);
  Serial.print(" : ");
  Serial.println(v);*/
}
