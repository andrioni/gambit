//
// FILE: gnumber.h -- Number class for Gambit project. 
//
// $Id$
//

#ifndef GNUMBER_H
#define GNUMBER_H

#include "gmisc.h"
#include "rational.h"
#include "gpool.h"

class gOutput;

typedef enum { precDOUBLE, precRATIONAL } gPrecision;

class gNumber  {
protected:
  gPrecision rep;
  union {
    gRational *rval;
    double dval;
  };

  static gPool pool;

public:
  class DivideByZero : public gException  {
  public:
    virtual ~DivideByZero()  { }
    gText Description(void) const;
  };

  // CONSTRUCTORS, DESTRUCTOR, CONSTRUCTIVE OPERATORS
  gNumber(void);
  gNumber(double);
  gNumber(int n);
  gNumber(long n);
  gNumber(const gInteger &y);
  gNumber(const gRational &y);
  gNumber(const gNumber &y);
  ~gNumber();

  gNumber &operator=(const gNumber &y);

  // OPERATOR OVERLOADING
  friend bool operator==(const gNumber &x, const gNumber &y);
  friend bool operator!=(const gNumber &x, const gNumber &y);
  friend bool operator< (const gNumber &x, const gNumber &y);
  friend bool operator<=(const gNumber &x, const gNumber &y);
  friend bool operator> (const gNumber &x, const gNumber &y);
  friend bool operator>=(const gNumber &x, const gNumber &y);

  friend gNumber operator+(const gNumber &x, const gNumber &y);
  friend gNumber operator-(const gNumber &x, const gNumber &y);
  friend gNumber operator*(const gNumber &x, const gNumber &y);
  friend gNumber operator/(const gNumber &x, const gNumber &y);
  friend gNumber operator-(const gNumber &x);

  gNumber &operator+=(const gNumber &y);
  gNumber &operator-=(const gNumber &y);
  gNumber &operator*=(const gNumber &y);
  gNumber &operator/=(const gNumber &y);

  friend gOutput &operator<<(gOutput &s, const gNumber &y);
  friend gInput &operator>>(gInput &s, gNumber &y);

  // MISCELLANEOUS MATHEMATICAL FUNCTIONS
  friend gNumber pow(const gNumber&,long);

  // PRECISION-RELATED FUNCTIONS AND CASTS
  operator double() const;
  operator gRational() const;
  gPrecision Precision(void) const { return rep; }
  bool IsInteger(void) const;
};

gOutput &operator<<(gOutput &, const gNumber &);

#endif 
