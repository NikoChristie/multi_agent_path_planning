$input = $args[0]

# Single Interval Path Planning
echo $null >> sipp_output.yaml
python ./sipp/multi_sipp.py $input sipp_output.yaml
python ./sipp/visualize_sipp.py $input sipp_output.yaml --video 'sipp.gif' --speed 1

# Conflict Based Search
echo $null >> cbs_output.yaml
python ./cbs/cbs.py $input cbs_output.yaml
python visualize.py $input cbs_output.yaml --video 'cbs.gif' --speed 1