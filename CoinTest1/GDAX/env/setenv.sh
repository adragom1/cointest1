#!/bin/bash
export GDAX_HOME=~/git/CoinTest1/GDAX
export GDAX_CFG=$GDAX_HOME/cfg/
export GDAX_DATA=$GDAX_HOME/data
export GDAX_LOG=$GDAX_HOME/log
export LOGLEVEL=DEBUG

function print_vars() {
  echo "GDAX_HOME=$GDAX_HOME"
  echo "GDAX_CFG =$GDAX_CFG"
  echo "GDAX_DATA=$GDAX_DATA"
  echo "GDAX_LOG =$GDAX_LOG"
  echo "LOGLEVEL =$LOGLEVEL"
}
print_vars
