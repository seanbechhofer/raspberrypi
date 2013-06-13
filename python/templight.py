import BMP085, LedBorg, time

COLD = 14
COOL = 16
OK = 18
WARM = 20
HOT = 22

SLEEP = 5

colours = {
    COLD: "blue",
    COOL: "lightblue",
    OK: "yellow",
    WARM: "green",
    HOT: "pink",
    }

toasty = "red"

if __name__ == "__main__":
  bmp = BMP085.BMP085()
  lb = LedBorg.LedBorg()
  while True:
      temp = bmp.readTemperature()
      print temp
      if temp <= COLD:
          lb.show(colours[COLD])
      elif temp <= COOL:
          lb.show(colours[COOL])          
      elif temp <= OK:
          lb.show(colours[OK])          
      elif temp <= WARM:
          lb.show(colours[WARM])          
      elif temp <= HOT:
          lb.show(colours[HOT])          
      else:
          lb.show(toasty) 
      time.sleep(SLEEP)


