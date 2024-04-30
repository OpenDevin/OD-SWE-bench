# Create directories for storing data
mkdir -p eval_data/instances
mkdir eval_data/outputs
mkdir eval_data/testbed_logs
mkdir eval_data/testbeds
mkdir eval_data/eval_logs
mkdir eval_data/eval_temp

# Run python code to pull test instances from huggingface
python prepare_test_instances.py

# Get Devin's outputs
wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_passed.json -O eval_data/outputs/devin_swe_passed.json
wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_failed.json -O eval_data/outputs/devin_swe_failed.json
wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_outputs.json -O eval_data/outputs/devin_swe_full.json
