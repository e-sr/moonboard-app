Moonboard LED APP
========

DIY web-application for moonboard.

Remarks:

the app has ben developed to work on a raspberry-pi with touch screen.
On the raspberry pi, due the lack of good touch-screen integration in raspbian os, the app works best on
chromium webbrowser with installed virtualkeyboard plugin.


##Installation

1. clone git repo

3. python2.7:
    install and setup virtualenvwrapper
    install eventlet
    install pillow can be difficult

2. make virtualenv
    - toggleglobalsitepackages
    - mkvirtualenv -r requirements.txt moonboardvenv

https://gist.github.com/jongrover/6831346
https://www.danpurdy.co.uk/wp-content/cache/page_enhanced/www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/_index.html

On Rpi
3. enable spi and connect led strips
4. Open chromium webbrowser and connet browser on localhost:5000
5. save app shortcut to dektop for further usage