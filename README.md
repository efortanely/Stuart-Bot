# Stuart-Bot

This is a bot that tweets photos of Stuart to [@TheStuartBot](https://twitter.com/TheStuartBot). It does this by getting a snapshot from the video feed streamed by the Onion Omega 2+, identifying the objects in it using ResNet-50, then if a cat exists a picture is tweeted.

To run the program yourself, you will need:

- An Onion Omega 2+ and dock
- A webcam with a USB
- The [ResNet-50 model](https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/resnet50_coco_best_v2.0.1.h5)
- A Twitter Development account (which has a waiting period before you can start creating apps)
- A .env file containing the environment variables found in the stuart-bot.py file.

Then follow these steps:

- Set up your Onion Omega 2+ using the steps found [here.](https://docs.onion.io/omega2-docs/first-time-setup.html)
- SSH into your Omega using the command "ssh root@omega-XXXX.local", where XXXX is the last 4 digits on the Omega's sticker.
- Configure it to always stream video when powered on using the steps found [here.](https://onion.io/streaming-video-over-wifi/)
- Run the stuart-bot.py file, and you should be getting a cat picture tweeted about every hour as long as it's aimed at a cat!


Inspired by [Alex Morley](https://github.com/alexmorley/auto-human)
