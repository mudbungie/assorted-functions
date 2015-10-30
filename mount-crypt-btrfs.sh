#!/bin/bash

# for mounting encrypted btrfs array
# designed for one btrfs RAID inside of encrypted partitions

DRIVES="ata-Hitachi_HDS722020ALA330_JK1171YAGA006S-part1 ata-Hitachi_HDS722020ALA330_JK1171YAGJD73N-part1 ata-Hitachi_HDS722020ALA330_JK1171YAGPLUSS-part1 ata-Hitachi_HDS722020ALA330_JK1171YAGT085S-part1 ata-Hitachi_HDS722020ALA330_JK1171YAGT1RAS-part1"

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
