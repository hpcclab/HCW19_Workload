# HCW19_Workload
This repository includes Constant and variable rate workload trials used in HCW '19 workshop. Generated by Chavit Denninnart

constant.zip contains pre-generated task arrivals for constant arrival workload.

spiky.zip contains pre-generated task arrivals for spiky arrival workload.

class_2.etc is the etc matrix for simulating heterogeneous system.

homo_2.etc is the etc matrix for simulating homogeneous system.

To generate a new workload, edit generation numbers in homer_refurb_file_gen_spike.py or homer_refurb_file_gen.py

Then 

1.) call 

python homer_refurb_file_gen_spike.py  (or homer_refurb_file_gen.p )

to generate a lot of arrival tasks

2.) call 

python convertWorkLoad_spk.py (or python convertWorkLoad.py)

to generate deadline for each tasks and some format conversion

3.) call

python trimNumArrivals.py ./trials_prop1.0/trial_ 800

to trim arrival tasks down to 800 tasks for experiments
