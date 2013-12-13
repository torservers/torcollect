#!/bin/bash
TORCOLLECT=/var/lib/torcollect/
TORFOLDER=/var/lib/tor/
rm -r $TORCOLLECT*
find /var/lib/tor -name bridge-stats -type f | sed 's/\/var\/lib\/tor\///g' | sed 's/\/stats\/bridge-stats//g' | xargs -I{} sh -c "mkdir -p $TORCOLLECT{}/stats && cp $TORFOLDER{}/stats/bridge-stats $TORCOLLECT{}/stats/"

