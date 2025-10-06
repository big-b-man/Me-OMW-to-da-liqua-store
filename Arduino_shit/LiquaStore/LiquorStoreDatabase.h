#ifndef LIQUORSTOREDATABASE_H
#define LIQUORSTOREDATABASE_H

//Declares the liquor store database array

#include <avr/pgmspace.h>
#include <stdint.h>

volatile extern const uint16_t liquorStores[963][2] PROGMEM;

#endif /*LIQUORSTOREDATABASER_H*/