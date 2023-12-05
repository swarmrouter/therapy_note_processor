#!/bin/bash

LOCAL_DIR=""
DOWNLOAD_DIR=""
EXT1="*.pdf"
EXT2="*.out"

# delete command
RM_BIN="/bin/rm -frv "

# clean up local directory
echo "$RM_BIN $LOCAL_DIR/$EXT1"
echo "$RM_BIN $LOCAL_DIR/$EXT2"
$RM_BIN $LOCAL_DIR/$EXT1
$RM_BIN $LOCAL_DIR/$EXT2

# clean up data downloads
echo "$RM_BIN $DOWNLOAD_DIR/$EXT1"
echo "$RM_BIN $DOWNLOAD_DIR/$EXT2"
$RM_BIN $DOWNLOAD_DIR/$EXT1
$RM_BIN $DOWNLOAD_DIR/$EXT2
