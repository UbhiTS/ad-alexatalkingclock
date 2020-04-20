import appdaemon.plugins.hass.hassapi as hass
import datetime
 
#
# Talking Clock AppDeamon App for Home Assistant
# Developed by @UbhiTS on GitHub
#
# Args:
#alexa_talking_clock:
#  module: alexa_talking_clock
#  class: AlexaTalkingClock
#  alexa: media_player.kitchen_alexa
#  whisper: false
#  pitch_offset: 0 # -33 to 50, default 0
#  volume_offset: 0 # -40 to 4, default 0
#  rate: 100 # 20 to 250, default 100
#  announce_bell: true
#  announce_half_hour: true
#  announce_quarter_hour: true
#  start_hour: 7
#  start_minute: 30
#  end_hour: 21
#  end_minute: 30
#  debug: false

class AlexaTalkingClock(hass.Hass):

  def initialize(self):
    
    self.alexa = self.args["alexa"]
    self.whisper = bool(self.args["whisper"]) if "whisper" in self.args else False
    self.pitch_offset = int(self.args["pitch_offset"]) if "pitch_offset" in self.args else 0
    self.volume_offset = int(self.args["volume_offset"]) if "volume_offset" in self.args else 0
    self.rate = int(self.args["rate"]) if "rate" in self.args else 100
    self.announce_bell = bool(self.args["announce_bell"]) if "announce_bell" in self.args else True
    self.announce_hour = True
    self.announce_half_hour = bool(self.args["announce_half_hour"]) if "announce_half_hour" in self.args else True
    self.announce_quarter_hour = bool(self.args["announce_quarter_hour"]) if "announce_quarter_hour" in self.args else False
    self.start_hour = int(self.args["start_hour"]) if "start_hour" in self.args else 7
    self.start_minute = int(self.args["start_minute"]) if "start_minute" in self.args else 30
    self.end_hour = int(self.args["end_hour"]) if "end_hour" in self.args else 21
    self.end_minute = int(self.args["end_minute"]) if "end_minute" in self.args else 30
    self.debug = bool(self.args["debug"]) if "debug" in self.args else False
    
    if self.pitch_offset < -33: self.pitch_offset = -33
    if self.pitch_offset > 50: self.pitch_offset = 50
    if self.volume_offset < -40: self.volume_offset = -40
    if self.volume_offset > 4: self.volume_offset = 4
    if self.rate < 20: self.rate = 20
    if self.rate > 250: self.rate = 250
    
    self.frequency = self.get_frequency()
    self.next_start = self.get_next_start()
    
    self.run_every(self.time_announce, self.next_start, (60 * self.frequency.interval))
    
    self.log("INITIALIZED: Start " + str(self.next_start.strftime("%H:%M:%S")) + ", Frequency " + str(self.frequency.interval) + ", Times " + str(self.frequency.announce_times))

    if self.debug: self.time_announce(None)
    

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
        break
    
    if next_start_min is None:
      next = now.replace(minute = 0, second = 0) + datetime.timedelta(hours=1)
    else:
      next = now.replace(minute = next_start_min, second = 0)
    
    return next


  def time_announce(self, kwargs):
    now = datetime.datetime.now()
    time_speech = self.time_to_text(now.hour, now.minute)
    
    if time_speech is not None:
      msg = self.set_speech_parameters(time_speech)
      self.log("HOUR_ANNOUNCE_MESSAGE " + time_speech)
      self.call_service("notify/alexa_media", data = {"type": "announce" if self.announce_bell else "tts", "method": "all"}, target = self.alexa, message = msg)


  def set_speech_parameters(self, time_speech):
    prefix = "<speak>"
    postfix = "</speak>"
    
    if self.whisper:
      prefix = prefix + "<amazon:effect name='whispered'>"
      postfix = "</amazon:effect>" + postfix

    str_rate = str(self.rate)
    str_pitch = "+" + str(self.pitch_offset) if self.pitch_offset >= 0 else str(self.pitch_offset)
    str_volume = "+" + str(self.volume_offset) if self.volume_offset >= 0 else str(self.volume_offset)
  
    prefix = prefix + "<prosody rate='" + str_rate + "%' pitch='" + str_pitch + "%' volume='" + str_volume + "dB'>"
    postfix = "</prosody>" + postfix
      
    return prefix + time_speech + postfix


  def time_to_text(self, hour, minute):
    
    prefix = ""
    postfix = ""
    time_speech = ""
    
    if not self.debug:
      if hour < self.start_hour or hour > self.end_hour:
        return
      if hour == self.start_hour and minute < self.start_minute:
        return
      if hour == self.end_hour and minute > self.end_minute:
        return

    ampm_str = "AM" if hour <= 11 else "PM"
    
    if hour == self.start_hour and minute == self.start_minute and hour <= 11:
      prefix = "Good morning."
    elif hour == 12 and minute == 0:
      prefix = "Good afternoon."
    elif hour == 17 and minute == 0:
      prefix = "Good evening."
    elif hour == self.end_hour and minute == self.end_minute and hour >= 20:
      postfix = "Good night. And sweet dreams."
      
    hour = hour - 12 if hour > 12 else hour
  
    if minute == 0:
      time_speech = f"It's {hour} {ampm_str}."
    else:
      time_speech = f"It's {hour}:{minute:02d} {ampm_str}."
    
    return prefix + " " + time_speech + " " + postfix


class Frequency:
  
    def __init__(self):
      
        self.announce_times = []
        self.interval = None
