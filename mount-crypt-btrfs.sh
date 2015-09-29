#!/bin/bash

# for mounting encrypted btrfs array
# designed for one btrfs RAID inside of encrypted partitions

DRIVES="ata-WDC_WD30EFRX-68EUZN0_WD-WMC4N1888670-part1 ata-WDC_WD30EFRX-68EUZN0_WD-WMC4N2023900-part1 ata-WDC_WD30EFRX-68EUZN0_WD-WMC4N2196016-part1"

NUM_OF_DRIVES=`echo $DRIVES |wc -w`
echo $NUM_OF_DRIVES	
LABEL="pool0"

echo "Decryption key: " 
read -s KEY

for i in `seq $NUM_OF_DRIVES`
do
	DRIVE=`echo $DRIVES | cut -d ' ' -f $i`
	echo $KEY |cryptsetup luksOpen /dev/disk/by-id/$DRIVE $DRIVE
done
btrfs device scan
mount -v -t btrfs /dev/disk/by-label/$LABEL /$LABEL 
