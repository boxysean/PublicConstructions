Public Constructions
====================

A 64-channel light installation using construction barrier objects.

![images/flowers.jpg](flowers)

This repo contains all the code used for the installation, including:

- *FlowerGardenModel:* OpenFrameworks code used to 3D model the installation.
- *pru_sw:* a C and assembly interface for a BeagleBone. It takes in an ad-hoc network protocol and outputs DMX on a pin.
- *MasterControl:* python code to send patterns to the BeagleBone interface.

The *FlowerGardenModel* is also a network server that accepts packets from *MasterControl* to visualize the patterns run on the installation without needing to run it on the installation.

![images/model.png](model)


