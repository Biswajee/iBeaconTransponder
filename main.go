package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"github.com/paypal/gatt"
	"github.com/paypal/gatt/examples/option"
)

var deviceID int64 =  1622347;

func onStateChanged(device gatt.Device, s gatt.State) {
	switch s {
	case gatt.StatePoweredOn:
		fmt.Println("Scanning for iBeacon Broadcasts...")
		device.Scan([]gatt.UUID{}, true)
		return
	default:
		device.StopScanning()
	}
}

func onPeripheralDiscovered(p gatt.Peripheral, a *gatt.Advertisement, rssi int) {
	b, err := NewiBeacon(a.ManufacturerData)
	if err == nil {
		req, err := http.NewRequest("GET", "https://us-central1-lastleafd.cloudfunctions.net/beaconiee/", nil)
		if err != nil {
			log.Print(err)
			os.Exit(1)
		}
		q := req.URL.Query()
		q.Add("id", deviceID)
		q.Add("lat", b.minor)
		q.Add("lon", b.major)
		req.URL.RawQuery = q.Encode()
			 
		fmt.Println("UUID: ", b.uuid)
		fmt.Println("Major: ", b.major)
		fmt.Println("Minor: ", b.minor)
		fmt.Println("RSSI: ", rssi)
	}
}

func main() {
	device, err := gatt.NewDevice(option.DefaultClientOptions...)
	if err != nil {
		log.Fatalf("Failed to open device, err: %s\n", err)
		return
	}
	device.Handle(gatt.PeripheralDiscovered(onPeripheralDiscovered))
	device.Init(onStateChanged)
	select {}
}
