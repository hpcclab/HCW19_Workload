python homer_refurb_file_gen_spike.py
python convertWorkLoad_spk.py
python trimNumArrivals.py ./trials_prop1.0/trial_ 800
mmv ./trials_prop1.0/trial_\* ./trials_prop1.0/spk10k800_\#1
mv ./trials_prop1.0 ./spike_10k_800task
rm -r final_en_tests_50k
