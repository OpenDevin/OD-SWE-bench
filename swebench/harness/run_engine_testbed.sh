# Example call for getting versions by building the repo locally
TEMP=/home/PJLAB/libowen/Documents/Projects/codellm/OD/temp
python engine_testbed.py \
    --instances_path $TEMP/harness_materials/processed/swe-bench-test.json \
    --devin_output_path /home/PJLAB/libowen/Documents/Projects/codellm/OD/temp/outputs/devin_swe_passed.json \
    --log_dir  $TEMP/harness_materials/yizhou_logs \
    --conda_path /home/PJLAB/libowen/anaconda3 \
    --testbed $TEMP/harness_materials/yizhou_testbeds \
    --timeout 1000