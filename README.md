# Flashbird Home assistant integration
SMT Performance is a French company that delivers a motor bike tracker called "Flashbird".
You can have more inforamtion regarding this brand here: [https://smtperformances.fr/](https://smtperformances.fr/)

## The sensors
The integration provides several sensors:
- tracker : exposes the GPS coordinate of the tracker
- mileage: exposes the total mileage (in km) made by the tracker
- lock: enable or disable the alerting
- connected status: exposes if the tracker is connected to the network or not
- battery level: exposes the current battery level of the tracker
- bike battery: exposes the battery voltage of the bike
- smartKey battery: exposes the battery level of the Smart key associated to the tracker

## Polling information
The value of each sensor is polled from the Flashbird server each 5 minutes.

## How to use
Once the Flashbird integration is added into Homeassistant you just need to click on the "Add integration" button, search for Flashbird and fill the information presented in the connexion screen (login / password / serial number of the tracker / name of the tracker). 

The login and password will not be stored in the system but used to generate a token. When the token will be revoked by Flashbird API, you will be prompted to login again.

The Serial number can be found in the Flashbird mobile app.

The name of the tracker will just be used in Home assistant to prefix all the entity ids.

Once you complete the process, 2 new devices will be created, one for the tracker, and one for its smart key.


## Licencing / Bug reporting
This project is open source and done only on spare time, so do not expect bug free extension.
Feel free to contribute if you are interested.