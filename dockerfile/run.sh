#!/bin/bash

for IREP in {97..100}
do
    occam-run -n node35 -s 500g francesca.lonigro/simunet "n3fit /simunet_git/SIMUnet/runcards/simultaneous_runcard_jets.yaml $IREP"
done
    
