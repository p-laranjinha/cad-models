# Plug-n-play webcam from a Raspberry Pi Zero 2 W

## Raspberry Pi Zero 2 W model

Got **pi-zero-2-w.STEP** from https://grabcad.com/library/raspberry-pi-zero-2-w-1 .

## Setting up the Pi

Sources:
- https://www.raspberrypi.com/tutorials/plug-and-play-raspberry-pi-usb-webcam/
- https://forums.raspberrypi.com/viewtopic.php?t=371121
- https://www.einherjar.org/2025/01/05/raspberry-pi-zero-2-w-gadget-mode/
- https://github.com/maxbbraun/pisight
- https://docs.kernel.org/usb/gadget_uvc.html

Install **Raspberry Pi OS Lite (64-bit) Bookworm** on the Pi (I'll be using the user **camera**).

Connect to the Pi via SSH or directly/physically.

Update the Pi:
```bash
sudo apt update -y
sudo apt upgrade -y
```

Install dependencies:
```bash
sudo apt install git meson libcamera-dev libjpeg-dev -y
```

If you have a 3rd party camera you need to add it to the end of **/boot/firmware/config.txt**.
In my case, I have the IMX219:
```
dtoverlay=imx219
```

Add the following line to the end of **/boot/firmware/config.txt**:
```
dtoverlay=dwc2,dr_mode=peripheral
```

Download **uvc-gadget v0.4.0** (newer versions don't have the required arguments):
```bash
git clone -b v0.4.0 https://gitlab.freedesktop.org/camera/uvc-gadget.git
```

Install **uvc-gadget**:
```bash
cd uvc-gadget
make uvc-gadget
cd build
sudo meson install
sudo ldconfig
```

Create the bash script **/home/camera/rpi-uvc-gadget.sh** (change the **MANUF** and **PRODUCT** variables at the top to customize the name when connected) (these **create_frame** function calls are for my IMX219 camera, if it doesn't work for you, either set your own or go get the script from the source above):
```bash
#!/bin/bash

# Variables we need to make things easier later on.

MANUF="Raspberry Pi"
PRODUCT="RaspPi Camera"
CONFIGFS="/sys/kernel/config"
GADGET="$CONFIGFS/usb_gadget"
VID="0x0525"
PID="0xa4a2"
SERIAL="0123456789"
BOARD=$(strings /proc/device-tree/model)
UDC=`ls /sys/class/udc` # will identify the 'first' UDC

# Later on, this function is used to tell the usb subsystem that we want
# to support a particular format, framesize and frameintervals
create_frame() {
    # Example usage:
    # create_frame <function name> <width> <height> <format> <name> <intervals>

    FUNCTION=$1
    WIDTH=$2
    HEIGHT=$3
    FORMAT=$4
    NAME=$5

    wdir=functions/$FUNCTION/streaming/$FORMAT/$NAME/${HEIGHT}p

    mkdir -p $wdir
    echo $WIDTH > $wdir/wWidth
    echo $HEIGHT > $wdir/wHeight
    echo $(( $WIDTH * $HEIGHT * 2 )) > $wdir/dwMaxVideoFrameBufferSize
    cat <<EOF > $wdir/dwFrameInterval
$6
EOF
}

# This function sets up the UVC gadget function in configfs and binds us
# to the UVC gadget driver.
create_uvc() {
    CONFIG=$1
    FUNCTION=$2

    echo "	Creating UVC gadget functionality : $FUNCTION"
    mkdir functions/$FUNCTION

    # To select the fps you want, use the results you get from 10000000/<fps>
    create_frame $FUNCTION 640 480 uncompressed u "333333
416667
1000000
2000000"
    create_frame $FUNCTION 1280 720 uncompressed u "1250000
2000000"
    create_frame $FUNCTION 1920 1080 uncompressed u "3333333"

    create_frame $FUNCTION 640 480 mjpeg m "100000
166666
333333
416667
1000000
2000000"
    create_frame $FUNCTION 1280 720 mjpeg m "166666
333333
416667
1000000
2000000"
    create_frame $FUNCTION 1920 1080 mjpeg m "333333
416667
1000000
2000000"
    create_frame $FUNCTION 1640 1232 mjpeg m "333333
416667
1000000
2000000"
    create_frame $FUNCTION 3280 2464 mjpeg m "1250000
2000000"

    # This section links the format descriptors and their associated frames
    # to the header
    mkdir functions/$FUNCTION/streaming/header/h
    cd functions/$FUNCTION/streaming/header/h
    ln -s ../../uncompressed/u
    ln -s ../../mjpeg/m

    # This section ensures that the header will be transmitted for each
    # speed's set of descriptors. If support for a particular speed is not
    # needed then it can be skipped here.
    cd ../../class/fs
    ln -s ../../header/h
    cd ../../class/hs
    ln -s ../../header/h
    cd ../../class/ss
    ln -s ../../header/h
    cd ../../../control
    mkdir header/h
    ln -s header/h class/fs
    ln -s header/h class/ss
    cd ../../../

    # Specification indicates 1024/2048/3072 are the valid values
    # but 3072 doesn't work
    echo 2048 > functions/$FUNCTION/streaming_maxpacket

    ln -s functions/$FUNCTION configs/c.1
}

# This loads the module responsible for allowing USB Gadgets to be
# configured through configfs, without which we can't connect to the
# UVC gadget kernel driver
echo "Loading composite module"
modprobe libcomposite

# This section configures the gadget through configfs. We need to
# create a bunch of files and directories that describe the USB
# device we want to pretend to be.

if
[ ! -d $GADGET/g1 ]; then
    echo "Detecting platform:"
    echo "  board : $BOARD"
    echo "  udc   : $UDC"

    echo "Creating the USB gadget"

    echo "Creating gadget directory g1"
    mkdir -p $GADGET/g1

    cd $GADGET/g1
    if
[ $? -ne 0 ]; then
    echo "Error creating usb gadget in configfs"
    exit 1;
    else
    echo "OK"
    fi

    echo "Setting Vendor and Product ID's"
    echo $VID > idVendor
    echo $PID > idProduct
    echo "OK"

    echo "Setting English strings"
    mkdir -p strings/0x409
    echo $SERIAL > strings/0x409/serialnumber
    echo $MANUF > strings/0x409/manufacturer
    echo $PRODUCT > strings/0x409/product
    echo "OK"

    echo "Creating Config"
    mkdir configs/c.1
    mkdir configs/c.1/strings/0x409

    echo "Creating functions..."

    create_uvc configs/c.1 uvc.0

    echo "OK"

    echo "Binding USB Device Controller"
    echo $UDC > UDC
    echo "OK"
fi

# Run uvc-gadget. The -c flag sets libcamera as a source, arg 0 selects
# the first available camera on the system. All cameras will be listed,
# you can re-run with -c n to select camera n or -c ID to select via
# the camera ID.
uvc-gadget -c 0 uvc.0
```

Add execution permissions to the bash script:
```bash
sudo chmod +x /home/camera/rpi-uvc-gadget.sh
```

Create the systemctl service file **/etc/systemd/system/uvc-gadget.service**:
```
Description=UVC Gadget Setup Service
After=sys-kernel-config.mount
Requires=sys-kernel-config.mount

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/home/camera/rpi-uvc-gadget.sh

[Install]
WantedBy=multi-user.target
```

Make the systemctl service file run on startup:
```bash
sudo systemctl daemon-reload
sudo systemctl enable uvc-gadget.service
```

If you're already connected to your PC via the power+data port, reboot and test it:
```bash
sudo shutdown -r now
```
If not, shutdown and connect to your PC to test it:
```bash
sudo shutdown now
```
