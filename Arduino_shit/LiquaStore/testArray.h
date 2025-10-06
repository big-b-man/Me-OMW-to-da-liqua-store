#ifndef TESTARRAY_H
#define TESTARRAY_H

// Header used for testing an array similar to the one in LiquorStoreDatabase.h
// So I can wrap my head around PROGMEM before the rest of the parts show up

#include <avr/pgmspace.h>
#include <stdint.h>

volatile extern const uint16_t testArray[4][2] PROGMEM;

#endif /*TESTARRAY_H*/