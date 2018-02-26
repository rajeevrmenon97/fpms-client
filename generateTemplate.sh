#!/bin/bash
sudo rm f.bmp f.xyt -rf
sudo ./scanner f.bmp
nbis/bin/cwsq 2.25 wsq f.bmp -raw_in 320,480,8
nbis/bin/mindtct -m1 f.wsq f
rm f.brw f.dm f.hcm f.lcm f.lfm f.min f.qm f.wsq -rf
