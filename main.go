package main

import (
	"fmt"
	"log"
	"net/http"
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
		resp, err := http.PostForm("https://us-central1-lastleafd.cloudfunctions.net/beaconiee/",
					 url.Values{"id": {deviceID}, "lat": {b.minor}, "lon":{b.major}})
					 
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
