# HASS AppDaemon : Alexa Talking Clock App

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This app was a result of my amazing wife's inability (who is a mother of 2 beautiful princesses BTW) to manage her time wisely ;). So this is dedicated to my wife Reena, without whom this world would not be worth my time (no pun intended!). 

However, this also wasnt possible without the amazing work done by the community at HASS, and of Keaton Taylor and Alan Tse on the Alexa Media Player integration for Home Assistant. *https://github.com/custom-components/alexa_media_player*

Now, Alexa greets us in the morning, keeps on reminding us of the time every half hour (politely) from 7 AM to 9 PM where it courteously tells us the time and also greets us with a good morning, good afternoon, and a good night & sweet dreams. How cool is that!

## Installation
**NEEDS THE [Alexa Media Player](https://github.com/custom-components/alexa_media_player) HACS Integration from Keaton Taylor and Alan Tse**

Use [HACS](https://github.com/custom-components/hacs) or [download](https://github.com/UbhiTS/HASS-AlexaTalkingClock/tree/master/apps/alexa_talking_clock) the `alexa_talking_clock` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `alexa_talking_clock` module.

## App Configuration

```yaml
alexa_talking_clock:
  module: alexa_talking_clock
  class: AlexaTalkingClock
  alexa: media_player.kitchen_alexa
  start_hour: 7
  start_minute: 0
  end_hour: 21
  end_minute: 0
  announce_hour: true
  announce_half_hour: true
  announce_quarter_hour: false
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`alexa` | False | string | | The Alexa device to target for the time reminder speech. You need the Alexa Media Player integration alive and kickin before you install this app.
`start_hour` | False | int | | The hour to start time remiders. This is in 24h format.
`start_minute` | False | int | | The minute to start time reminders. This can be 0, 15, 30, 45
`end_hour` | False | int | | The hour to end time remiders. This is in 24h format.
`end_minute` | False | int | | The minute to end time reminders. This can be 0, 15, 30, 45
`announce_hour` | False | bool | | Announce every hour (It's 8 AM, It's 9 AM)
`announce_half_hour` | False | bool | | Announce every half hour (It's 8 AM, It's 8:30 AM, It's 9 AM)
`announce_quarter_hour` | False | bool | | Announce every 15 minutes (It's 8 AM, It's 8:15 AM, It's 8:30 AM, It's 8:45 AM, It's 9 AM)

## Thank you for your time! (get it ;)
Ever since I've set this up in my home, it's become an indispensable part of our lives. It's amazing to see how a simple reminder of the current time can make people efficient :), I hope this app helps someone else as it has helped me and my family. 

If you like my work and feel gracious, you can buy me a coffee [here](https://www.buymeacoffee.com/ubhits)

# License
[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0. This is required for Home Assistant contributions.
