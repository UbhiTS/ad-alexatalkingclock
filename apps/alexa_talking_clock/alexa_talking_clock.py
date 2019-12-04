import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Talking Clock AppDeamon App for Home Assistant
# Developed by @UbhiTS on GitHub
#
# Args:
#

class AlexaTalkingClock(hass.Hass):

  def initialize(self):
    
    self.alexa = self.args["alexa"]
    self.start_hour = self.args["start_hour"]
    self.start_minute = self.args["start_minute"]
    self.end_hour = self.args["end_hour"]
    self.end_minute = self.args["end_minute"]
    self.announce_hour = self.args["announce_hour"]
    self.announce_half_hour = self.args["announce_half_hour"]
    self.announce_quarter_hour = self.args["announce_quarter_hour"]

    self.frequency = self.get_frequency()
    self.next_start = self.get_next_start()
    
    self.log("INITIALIZE start:" + str(self.next_start) + ", frequency:" + str(self.frequency.interval) + ", times:" + str(self.frequency.announce_times))
    
    if self.frequency.interval is not None:
      self.run_every(self.time_announce, self.next_start, (60 * self.frequency.interval))


  def get_frequency(self):
    
    frequency = Frequency()
    
    if (self.announce_hour):
      frequency.interval = 60
      frequency.announce_times.append(0)
    
    if (self.announce_half_hour):
      frequency.interval = 30
      frequency.announce_times.append(0)
      frequency.announce_times.append(30)
      
    if (self.announce_quarter_hour):
      frequency.interval = 15
      frequency.announce_times.append(0)
      frequency.announce_times.append(15)
      frequency.announce_times.append(30)
      frequency.announce_times.append(45)
    
    frequency.announce_times = set(frequency.announce_times)
    frequency.announce_times = sorted(frequency.announce_times)
    
    return frequency


  def get_next_start(self):
    
    now = datetime.datetime.now()
    next_start_min = None
    
    for min in self.frequency.announce_times:
      if now.minute < min:
        next_start_min = min
    
    if next_start_min is None:
      next = now.replace(minute = 0, second = 0) + datetime.timedelta(hours=1)
    else:
      next = now.replace(minute = next_start_min, second = 0)
    
    return next


  def time_announce(self, kwargs):
    now = datetime.datetime.now()
    msg = self.time_to_text(now.hour, now.minute)
    
    if msg is not None:
      self.log("HOUR_ANNOUNCE_MESSAGE " + msg)
      self.call_service("notify/alexa_media", data = {"type":"announce", "method":"all"}, target = self.alexa, message = msg)


  def time_to_text(self, hour, minute):
    
    if hour >= self.start_hour and hour <= self.end_hour:
      
      if hour == self.start_hour and minute < self.start_minute:
        return
      if hour == self.end_hour and minute > self.end_minute:
        return

      ampm_str = "AM" if hour <= 11 else "PM"
      
      if hour == 7 and minute == 0:
        return "Good morning. It's 7 AM."
      elif hour == 12 and minute == 0:
        return "Good afternoon. It's 12 PM."
      elif hour == 17 and minute == 0:
        return "Good Evening. It's 5 PM."
      elif hour == 21:
        return "It's 9 PM. Good night. And sweet dreams."
        
      hour = hour - 12 if hour > 12 else hour
    
      if minute == 0:
        return "It's " + str(hour) + " " + ampm_str
      else:
        return "It's " + str(hour) + ":" + str(minute) + " " + ampm_str


class Frequency:
  
    def __init__(self):
      
        self.announce_times = []
        self.interval = None
