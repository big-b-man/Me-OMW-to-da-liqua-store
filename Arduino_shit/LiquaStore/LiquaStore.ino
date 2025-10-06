#define F_CPU 16000000UL

#include "liquorStoreDatabase.h"
#include "testArray.h"
#include <avr/io.h>
#include <util/delay.h>

int main(void){
  DDRD = 0x3C; // Pins 2-5 set to write

  while(1){
    for (uint8_t row = 0; row < 4; row++) {
      for (uint8_t column = 0; column < 2; column++){
        PORTD = (pgm_read_word_near(&(testArray[row][column]))) << PIND2;
        _delay_ms(500);
      }
    }
  }
}