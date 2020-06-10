#!/bin/sh

ROBOT_IP=192.168.200.12
scp data/coordinates.json root@$ROBOT_IP:/data/coordinates.json
scp data/colonies_processed.jpg root@$ROBOT_IP:/data/colonies_processed.jpg
