#!/bin/sh
# old release data_release="june_input_data_1.0.zip"
# new release 
data_release="data_private.zip"
wget --user=access --password=d0wn10@d$  "http://virgodb.dur.ac.uk/downloads/dc-quer1/$data_release"
unzip $data_release
rm $data_release
