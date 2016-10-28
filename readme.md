# Facebook Messenger Bot - SoCal Echo Bot
This is a simple Python template that uses Flask to build a webhook for Facebook's Messenger Bot API.
Deploys to Heroku. 

### Welcome Screen

![Image of Welcome Screen](http://ibarromay.com/assets/images/SoCalEchoBot.PNG)

To learn how to create a customized greeting text message and get started button visit: http://ibarromay.com/facebook-messenger-bot-set-greeting-text-and-get-started-button-on-heroku/

### Functionality

- Echoes back text and emojis
- Special keywords: `image`, `video`, `audio`, `file`, `button`, `generic`, and `share`.
- Fail-safe: if cannot echo back message will display `Message with attachment received`.
