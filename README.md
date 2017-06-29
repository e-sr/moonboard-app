Moonboard LED DIY
========

Moonboard LED DIY is an open source Web-application for driving MoonBoard LEDs. "The Moonboard LED DIY" consist on a webserver (programmed in
python using flask) hosted on the Raspberry pi. The webserver host a simple web application (user interface) accessible with a webbrowser.
Depending on the user actions the LEDS are driven by the raspberry using the SPI port.

On the raspberry Chromium is automatically loaded at startup and connect automatically to the webserver on `localhost:5000`.

**Remarks**
1. The  web app is in development status.
2. The problems are automatically downloaded from the moon [website](http://www.moonboard.com/problems/) and stored in a json file.
 Further improvements is to implement a public database (accesible througth RESTFUL api) to store all sort of moonboard  problem data.
3. The app has ben developed to work on a raspberry pi with touch screen and chromium webbroser. Other possybilty are welcome
4. The Moonboard LED DIY is not compatible with the moonboard app for smartphones.


## Installation on the raspberry

**Hardware requirements:**

- [Raspberry Pi](https://www.raspberrypi.org/products/) or similar, necessary an SPI interface for driving the LEDS.
- [Touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/)
- 5V power supply, ~ 20W
- 4x50 LEDs, addressable led pixels. I bought WS2801 LED pixels(4-wire SPI) with custom cable lenght of 25cm on Aliexpress.
I was happy with [this](https://it.aliexpress.com/store/312912) seller.


Before the listed steps basics setup of the raspberry is necessary(wifi, touchscreen, accounts,...). After:

1. clone git repo on rpi

3. setup python2.7:
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
5. Enable spi on rpi (raspy-config)
6. Connect LEDS (wire power supply directly to led strips)

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




