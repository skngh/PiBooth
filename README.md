# PiBooth

(Everything below is written assuming you've seen [this](https://youtu.be/JYDAor1Wx60) video)

Welcome welcome! This is a tutorial on how to make what I call PiBooth! It's a "photobooth" that takes a photo and puts filtering on it to look like my roommates art. If you're not interested in making the full project but just certain aspects of it, then it is hopefully still covered in here! For the most part, I'll just be linking the videos that helped me, so full credit to all the creators below! You can refer to the table of contents below

# Table of Contents

1. [Step by step guide to PiBooth](#making-the-pibooth-from-start-to-finish)
2. [Convert laptop screen to HDMI monitor](#how-to-convert-old-laptop-screen-hdmi-monitor)
3. [Getting a Raspberry Pi](#getting-a-raspberry-pi)
   - [Setting up your Pi](#setting-up-your-pi)
4. [Code](#code)
   - [Processing](#processing)
   - [OpenCV Python](#opencv-python)
   - [Run Script on Startup](#how-to-run-our-python-script-on-startup)
5. [Bonus](#bonus)

## Making the PiBooth from start to finish

Here are step by step instructions on how to get my exact code I wrote working on your Raspberry Pi. Then after I will dive into each individual step in more detail, for those that don't want to make the exact project I did.

#### List of materials:

- **Raspberry Pi** (I only tested this on a Pi4 with 4Gb ram, so i cannot confirm nor deny whether this would all work on a different model)
- **Raspberry Pi case with Fan.** Any one will do. You can always 3D print one.
- **Camera for the Raspberry Pi.** There are many cheap cameras out there for the Pi. I bought this one [here](https://www.amazon.com/dp/B07L82XBNM?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_3). There are some that are USB connected that I'm not sure would directly work with the code I wrote, so a ribbon connected one is best.
- **External screen.** I used an old laptop screen, but any screen will do.
- **Button & jumper cables.** I just used a simple 2 pin button I had laying around.
- **Screen/system enclosure for presentation.** This part is totally up to you! You can follow how I did it in the video, or create your own version. I had a mount for my Pi, button, and camera.

### Steps:

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and plug in your Pi's microSD card.
   - Open the imager, select your Pi version and recommended OS.
   - Click "Edit Settings" to apply OS Costumisation.
   - Make your hostname a simple one like the default "pi". (**_The rest of these instructions will be written assuming your hostname is pi_**)
   - Add a simple username and password
   - Add your Wifi login
   - Hit "Services" and make sure "Use SSH" with password authentication is checked.
   - Then hit Save and flash it onto your Pi.
2. Once it's flashed, put the SD card back and boot up your Pi
   - Type `ping pi.local` in your terminal to try and get your Pi's IP address. If that doesn't work, you can download [IP Scanner](https://apps.apple.com/us/app/ip-scanner/id6443819966) and check there.
   - Type `ssh pi@[ipAddress]` then type in your Pi's password.
   - Once logged into your Pi, type `sudo raspi-config`, go to "Interface Options," "VNC," and hit "Yes" to enable
   - Then download [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/?lai_vid=8r8GXQgGdfBlE&lai_sr=5-9&lai_sl=l), open it, right click and hit "New Connection", and type in your Pi's username and password. Now you should be connected to your Pi! **_Technically you could get this whole project running with only using SSH, but I think it's handy to fully connect to the Pi sometimes_**
3. Hook up your camera's ribbon cable to the [correct part on your Pi](https://www.youtube.com/watch?v=lAbpDRy-gc0).
4. Hook up your button with jumper cables to your Pi's GPIO pin 2. You can follow this article [here](https://projects.raspberrypi.org/en/projects/button-switch-scratch-pi/1).
5. Download my Python file and type `scp [path To File To Copy] pi@[IpAdress]:/home/pi`
   - So for example, if I wanted to copy a file in my Desktop on my Mac, to my home directory on my Pi, I would type `scp /Users/samknight/Desktop/PiBooth.py pi@[ipAdress]:/home/pi` (You could also just cd into your files directory and skip putting the whole file path).
   - Go watch [this video](https://www.youtube.com/watch?v=QzVYnG-WaM4) to get OpenCV working on the Pi.
   - Run your python script and test if it is working. There are a few dependencies (picamera2 & RPi.gpio) that depending on your OS version, come preinstalled with the Pi. If you're getting errors about them, you can easily google each one to find the correct way to install them.
   - After that, your code should hopefully run when calling it directly from your terminal.
6. Now go into your Pi's terminal (either with ssh or through the VNC Viewer)
   - Type `sudo nano /etc/systemd/system/pibooth.service`
   - A text editor should open up, and now you can copy and paste my service file into the text editor in the terminal (If using VNC Viewer on a mac, I've found I have to right click and hit paste or it's kinda finicky).
   - Reload systemd process in terminal with `sudo systemctl daemon-reload`
   - Then type ```sudo systemctl enable pibooth.service
   - You can then check your service with `sudo systemctl pibooth.service`
7. Restart your Pi and see if it works!

## How to convert old laptop screen to HDMI monitor

There's plenty of videos online on how to do this. I don't recall the exact one I used, but this seems to be a good and popular one [here!](https://www.youtube.com/watch?app=desktop&v=6L0TPJEXiAI&t=64s)

[This](https://www.amazon.com/dp/B08CXQCLM4?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2) is also the EDP LCD controller that I purchased. I do remember having bought one and it came broken, so be weary of some of the ones you buy!

Overall it's a good option if you have an old laptop, but there's also many many screens out there you can buy to use for a project like this. Especially if you have a 3D printer, there are some pretty cool enclosures out there you can make if you look around!

## Getting a Raspberry Pi

Now this is a very big world that many know better than me. If you're just curious what I had, it was a RP4 Model B with 4GB ram, and I bought [this](https://www.microcenter.com/product/659157/micro-connectors-aluminum-case-with-fan-for-raspberry-pi-4-black) case at my local Microcenter.

But this doesn't mean you need to run out and get that! Raspberry Pi's have been known to get expensive recently, so honestly just going on ebay or local tech stores and seeing what's at a reasonable price may be your best bet. And if you have a 3D printer, you can always just print a case and buy a separate fan instead!

## Setting up your Pi!

I pretty much covered this in the "Sam's Masterclass" section of my video at !!!ADD TIME!!!, but for those that want a slower pace I thought I'd link a full video for setting it up!

[Here's](https://www.youtube.com/watch?v=m6aS9YF-0xo) a great video covering how to setup your Pi without having you ever hook it up to an external monitor or mouse & keyboard like I showed.

[Here's](https://www.youtube.com/watch?v=l4VDWhKsFgs) also a video that I think is worthwhile to understand the different types of remote connection to the Pi.

Of course, if you have plenty of extra screens and keyboard/mice onhand you can always just hook those up to your Pi, but I'm sure at some point you'll want the efficiency of connecting to it on your main computer, so I think these are are worth the time (overall definitely takes less time than to hookup up your entire Pi with peripherals)

# Code

As you saw in the video, I first started with the programming language Processing, and then later switched to Python because I couldn't get processing on the Pi. I've included a short section talking about my struggles with processing and then I'll move to Python.

## Processing

Processing is such a cool language and very fun to play around with. Going over all it can do is out of the scope of this, but I recommend everyone check it out! I initally thought it would be perfect for this project, but I was proven wrong eventually.

#### Why it didn't work for me:

Since my project involved the webcam, that comes with a needed webcam package for processing. This is where lots and lots of compatibility issues appeared. If you have a Pi 3, it's my understanding that this would be much easier and is something you could look into, but I would save the time if looking at the 4 (or even the 3, if it's webcam stuff OpenCV is prob the way to go).

But! If you're just looking to display graphics that don't involve a webcam, processing could totally work. Overall it was still very easy to go and install on the Pi, and it worked seamlessly without the webcam.

For those that are playing around with processing themselves, I included 2 versions of the code I wrote. One is a version that takes a photo once motion is detected, and then will display that until motion is detected again. And the other you just press a button to trigger the photo.

Could be a fun project to just add your own filtering/style to the image! Would not be hard at all to go and implement your own stuff there even if you're just starting out.

## OpenCV Python

And now that brings us to Python! Specifically with using the OpenCV library. openCV is a very comprehensive library, so there are many many many more things you can do than the little things covered here, but all you need to know is it's used mainly for computer vision and machine learning related things.

While I really just looked for specific tutorials to accomplish exactly what I needed (plus some ChatGPT help), I still stumbled across some nice tutorials for general stuff for those interested.

[This](https://www.youtube.com/watch?v=zSa-fOGh8es&t=342s) was a good series to get you started.

And to get the webcam working I found that [this article](https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/) was plenty to get me started.

### Getting the Pi to work with OpenCV

To get OpenCV working on the Pi, you're going to have to install some things first. Instead of writing out all this, [here's a video detailing all of it! ](https://www.youtube.com/watch?v=QzVYnG-WaM4)

## How to run our Python script on startup

Instead of having to start your script everytime you turn off and on your Pi, we can pretty easily have it run on startup. There are many different ways to do this, and after trying them all I really only found one method that worked for me

#### crontab

One of the methods is to add our script to Cron, which is a job scheduler that we can tell to perform tasks at certain times. For some reason, this method did not work for me. This is most likely due to dependencies being needed that aren't loaded yet before the script runs. Either way, incase you're running a different script than this project, [here's](https://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/) an article detailing how to do it (I'm including this because if you do have a simple script, this definitely seems to be the easiest method available).

Also with a quick search you'll see some people saying that for contab you can put "sleep {seconds}" after @reboot and that will fix dependencies issues, but that still didn't make it work for me, so I more robust service was needed.

### Systemd

A quick google search tells us that systemd "is a system and service manager for Linux, acting as the init system that manages the boot process, starts and stops services, and handles system shutdowns," which is pretty much about all I can say about it. For our purposes, it'll be a reasonably easy way to setup running our script on startup, but it's just a bit more involved than cron

In order to run our script, we'll need to make a systemd service file. There are a couple posts written about how to do this, so I'll link those.

On [this](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) article there's an area at the bottom explaining systemd that should get you setup. [This](https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/) is a great article too.

If you want a more in depth explanation on how systemd works, [this github post](https://github.com/thagrol/Guides/blob/main/boot.pdf) goes into more detail about each section and their meaning.

I included my service file [in the repo](https://github.com/skngh/PiBooth/blob/main/Python%20Code/pibooth.service) if you want to check it out. I found that ChatGPT was pretty helpful in writing the file so that's where you may see things that weren't mentioned in the links above. (I can't fully explain what they mean, but I was having problems with the service opening and using my correct screen, and after asking chatGPT it spit out that code and it worked).

# Bonus

As shown in the video, I used a smart outlet and plugged both my screen and pi into so I can have it auto turn on and off during the night. I highly recommend this whenever doing art installation kind of stuff so they never have to run when they wouldn't otherwise be seen/used.

Also I'm not including any of the 3D models I printed for the project, because I felt they were very specific to my exact setup and I assume no one would find value in them, but if someone out there thinks a specific model I made or used would be helpful to them, feel free to reach out to me.
