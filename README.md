Moon Pi
========

This project is heavily baseon https://github.com/e-sr/moonboard-app. The drivers have been updated to use WS2811 LEDs which are the original ones used by Moon. The software has been migrated to Python3 and the latest bibliopixel library.

I also added added options to setup on-the-fly custom problems, run calibration tests and a bunch of animations.

Moonboard LED DIY is an open source Web-application for driving MoonBoard LEDs. "The Moonboard LED DIY" consist on a webserver (programmed in
python using flask) hosted on the Raspberry pi. The webserver host a simple web application (user interface) accessible with a webbrowser.
Depending on the user actions the LEDS are driven by the raspberry.

On the raspberry Chromium is automatically loaded at startup and connect automatically to the webserver on `localhost:5000`.

**Remarks**
1. The  web app is in development status.
3. The app has ben developed to work on a raspberry pi with touch screen and chromium webbroser. Other possybilty are welcome
4. The Moonboard LED DIY is not compatible with the moonboard app for smartphones.


## Installation on the raspberry

**Hardware requirements:**

- [Raspberry Pi](https://www.raspberrypi.org/products/) or similar, necessary an SPI interface for driving the LEDS.
- [Touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/)
- 5V power supply, ~ 20W
- [Moonboard LEDS](https://moonclimbing.com/moonboard-led-kit-1.html) or any other WS2811 addressable led pixels.

Before the listed steps basics setup of the raspberry is necessary(wifi, touchscreen, accounts,...). After:

1. clone git repo on rpi

3. setup python3:
    - install and setup virtualenvwrapper
    - install eventlet and pillow from  raspbian repos
        ```sh
        sudo apt-get install python-pillow python-eventlet
        ```
    - install spidev
    - create a new virtualenvironmet:
        ```sh
        make virtualenv moonboard
        ```
    - then execute command `toggleglobalsitepackages`
    - install required packages:
        ```sh
        mkvirtualenv -r requirements.txt moonboardvenv
        ```

4. create systemd rule to run server script at statup, similar to
[this](http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) guide.
        ```
        [Unit]
        # sve file at  /lib/systemd/system/moonboard_led_server.service
        Description=moonboard server service
        After=multi-user.target

        [Service]
        Type=idle
        ExecStart=/home/pi/.virtualenvs/moonboard/bin/python2.7 /home/pi/moonboard-app/run.py

        [Install]
        WantedBy=multi-user.target

        ```
5. Connect LEDS (wire power supply directly to led strips)

**Optional steps**
7. Setup Rpi to start Chromium in kiosk mode at startup. Follow [link1](https://www.danpurdy.co.uk/wp-content/cache/page_enhanced/www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/_index.html
), [link2](https://gist.github.com/jongrover/6831346)

8. Setup rpi to periodically update the problem list. Create crontab job which run the moonboard_problems.py script.
    ```sh
    crontab -e
    ```
9. Add shutdown button as in this [link](https://gilyes.com/pi-shutdown-button/)


## Contribute

you are all welcome! and of course enjoy the app!




