#!/bin/sh
LOG_FILE="data/logs/$(date +%F%R).log"
#LOG_RECIPIENT="logs@releaseourdata.com"
LOG_RECIPIENT="parker@madebyparker.com"
./scripts/update_data_and_mirror_based_on_cdc_site.sh > $LOG_FILE 2>&1
mail -s "Output from cdc phil update script" $LOG_RECIPIENT < $LOG_FILE
