# Baby Seat Alarm
## Team Members
- Nick McClorey (mcclorns@mail.uc.edu)  (CS)
- Raeshawn Bart (bartrn@mail.uc.edu)    (CS)
- Advisor: David Tashjian

This page serves as the final report for our senior project. Use the table of contents below to navigate to the content of our Final Design Report

# Table of Contents

## 1. [Project Description](Project_Description.md)

## 2. User Interface Specification
- [Design Diagrams](hw/Diagrams.pdf)
- [Physical Layout Diagram](img/physical_layout.png)

## 3. [Test Plan](Test_Plan.pdf)

## 4. [User Manual](hw/UserManual.md)

## 4. Spring Final Presentation
### [Recording](output.mp4)
### [Slides](hw/Senior-Project-Slides.pdf)

## 6. [Final Expo Poster](Poster.pdf)

## 7. Assessments
### Fall Self-Assessments
- [Nicholas McClorey](hw/Nick_McClorey_individual_capstone_assessment.pdf)
- [Raeshawn Bart](hw/individual_capstone_raeshawn_bart.pdf)
### Spring Self-Assessments
- [Nicholas McClorey](hw/self_assessment_spring_Nick_McClorey.pdf)
- [Raeshawn Bart](hw/self_assesment_spring_raeshawn_bart.txt)

## 8. [Summery of Hours](hours.md)

## 9. [Summery of Expenses](expenses.md)

## 10. Final Design Result
### Overview
Our overall design consists of three main components: a mobile app, a raspberry pi, a weight sensor and a car seat. Below is a schematic of the physical layout.

![Physical design diagram](/img/physical_layout.png)

### Mobile App
In order to determine if the child is in the car, the mobile app continuously checks a HTTP endpoint hosted by the Raspberry Pi. This connection is supported by a LAN running on the Raspberry Pi. If the mobile app cannot make a connection, the app knows that the parent is no longer in the car and has walked out of range of the singal. If the child was never removed, the mobile app will remember this and alert the parent with a notification. The current logic works as so:

![Logic Diagram](/img/logic.png)

The mobile app was created with Android Studio. The repo for that has been included as a submodule of this repo.

### Raspberry Pi Configuration
The Raspberry Pi reads the weight in the carseat using the a [weight sensing resistor](https://www.amazon.com/SENSING-RESISTOR-SQUARE-1oz-22LBS-SPACING/dp/B00B887DBC/ref=sr_1_3?crid=1ERE37W2F4IEX&keywords=force+sensing+resistor&qid=1650579847&sprefix=force+sensing+resistor%2Caps%2C56&sr=8-3) from the company Pololu. When weight is applied to this sensor, the resistance drops. Using the GPIO pins in the Raspberry Pi, we can sense this drop.

![Weight Resistor](https://m.media-amazon.com/images/I/41iQeLY0DTL.jpg)

Our weight sensor is placed in the car seat betwen the padding and the plastic shell. It's placed near the bottom of the seat where most of the child's weight will be. Our car seat had vents in the bottom of the car seat so we ran the wires through them to the raspberry pi that was below.

![Wiring diagram](/img/wires.png)

Code for reading the GPIO pins can be found at [./pi_config/server.py](/pi_config/server.py). Wiring went from a Raspberry Pi GPIO pin into the weight resistor. The other wire of the weight resistor was run through a 320 Ohm resistor. The circuit is then run into the Raspberry Pi's ground GPIO pin.

This Python program must be run automatically when the system boots up. This is done with systemd which is a popular service manager for Linux. We created a service file, [carmonitor.service](/pi_config/carmonitor.service), and placed it in the /etc/systemd/system directory. We enabled the service. Now it runs the python server automatically on startup. A more detailed guide on creating systemd services can be found [online](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6)

Next we need to configure the HostAPD service to create a LAN. We installed HostAPD using the apt package manager and configured it with a [configuration file](/pi_config/hostapd.conf). We enabled this service and observed a LAN named "babyalarm" was created on startup. The network is visible to phones, laptops and any other Wi-Fi enabled device.


