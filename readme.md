## Lastleaf - Raspberry pi client utility

#### About the repository
Lastleaf for raspberry pi is a background unix service (process) for reporting emergency situation inside a vechile. The service resides inside the `Lastleaf IOT hardware setup`. The service is written in `Python` and `Go`.

#### Prerequisites
+ Configure a `Firebase` project with `Google Cloud Functions` using [this](https://github.com/Biswajee/Harvest) repository.
+ Set up a Go project and copy `ibeacon.go` and `main.go` to your `go` project directory.
+ Download `go` resources for the project using :
`go get github.com/paypal/gatt`.
Yes, you only need this one 😊.

#### Building and running
+ `git clone` the repository.
+ In your `go` project directory, execute: `env GOOS=linux GOARCH=arm GOARM=5 go build`
+ Copy the binary executable to your raspberry pi, probably using `ssh`:
`scp ./name-of-binary-file pi@raspberrypi.local:~/`
+ Rename the fragment to _your executable_ at line **34** of `Majimak.py`:
    ```
    subprocess.call([
        "sudo","./your_lastleaf"
        ])
    ``` 
+ Plug in a bluetooth device if your raspberry pi doesn't have one. For `raspberry pi zero W`, there is no such requirement.
+ Run the go executable in `sudo` mode to check if everything's okay.

Hurray! You are halfway already 🎉.

#### Setting up Soracom Account

+ Head over [here](https://www.soracom.jp/) to create your Soracom Account. For international, head [here](https://console.soracom.io/).
+ Register your SIM card and record your `API_KEY` and `API_TOKEN`.
+ Plug the `Soracom` SIM card to your mobile phone.

#### Configuring `Majimak.py` _(Yes, the last !)_
+ Give your device a specific `CONST_DEVICE_ID` as constant.
+ Plug in your API_KEY and API_TOKEN in the program.
+ Plug in your `HC-SR04` sensor with the raspberry pi GPIO pins as declared in `Majimak.py` or customize them.
+ Copy the `Lastleaf.service` file into your directory. 
+ Now,  run the following commands inside your raspberry pi shell:
    
    ```
    sudo cp Lastleaf.service /lib/systemd/system
    sudo chmod 644 /lib/systemd/system/Lastleaf.service
    sudo systemctl daemon-reload
    sudo systemctl enable Lastleaf.service
    ```

+ Now, `sudo reboot` your raspberry pi.
+ Perform `sudo systemctl status Lastleaf.service` to check if the service is running !

+ Now, head [here](https://github.com/Biswajee/Lastleaf) to the Android client application to get instructions on deploying the complementary beacon generator for the raspberry pi.

You're done ! ✔ 