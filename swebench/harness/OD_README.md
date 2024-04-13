# Setup

Please create a new, clean environment for evaluation purposes. DO NOT use the original `swe-bench` environment.

```shell
conda create -n swe-bench-eval python==3.11.5
conda activate swe-bench-eval
pip install requests python-dotenv GitPython datasets

# for django__django__2.1
sudo apt-get update
sudo apt-get install libffi-dev
```

# Prepare data

Get all SWE-bench test instances.
```python
from datasets import load_dataset
import pandas as pd

dataset = load_dataset("princeton-nlp/SWE-bench")
test = dataset["test"].to_pandas()
test.to_json("SOME_PATH/swe-bench-test.json", orient="records")
```

Get Devin's outputs processed for evaluations is available on [Huggingface](https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output).
- Devin-passed `wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_passed.json`
- Devin-failed `wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_failed.json`
- Devin-full `wget https://huggingface.co/datasets/OpenDevin/Devin-SWE-bench-output/raw/main/devin_swe_outputs.json`


# Run engine testbed (optional)

The `engine_testbed.py` script performs a sanity check on the repository installation and test patch application. It saves the testbeds and creates reusable conda environments.

Navigate to the `harness` directory and execute the `engine_testbed.py` script with your arguments:
```shell
cd OD-SWE-bench/swebench/harness
python engine_testbed.py \
    --instances_path PATH_TO_swe-bench-test.json \
    --devin_output_path PATH_TO_devin_swe_passed.json \
    --log_dir  DIR_OF_YOUR_LOGS \
    --conda_path PATH_TO_YOUR_CONDA \
    --testbed DIR_OF_YOUT_TESTBED \
    --timeout 1000
```

All required conda environments for test instances will be created under your specified conda path. You can activate any of them for testing.

A successful run will produce a log similar to the following:

```shell
Task Metadata:
	- Instance ID: astropy__astropy-7606
	- Testbed: /home/PJLAB/libowen/Documents/Projects/codellm/OD/temp/harness_materials/yizhou_testbeds/astropy__astropy__1.3
	- Virtual Env.: astropy__astropy__1.3
Installation Command: . /home/PJLAB/libowen/anaconda3/etc/profile.d/conda.sh && conda activate astropy__astropy__1.3 && echo 'activate successful' && pip install -e .[test]
Std. Output: activate successful
Obtaining file:///home/PJLAB/libowen/Documents/Projects/codellm/OD/temp/harness_materials/yizhou_testbeds/astropy__astropy__1.3
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Requirement already satisfied: numpy>=1.13.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (1.26.4)
Requirement already satisfied: pytest-astropy in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (0.11.0)
Requirement already satisfied: pytest>=4.6 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (8.1.1)
Requirement already satisfied: pytest-doctestplus>=1.0.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (1.2.1)
Requirement already satisfied: pytest-remotedata>=0.4.1 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (0.4.1)
Requirement already satisfied: pytest-astropy-header>=0.2.2 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (0.2.2)
Requirement already satisfied: pytest-arraydiff>=0.5 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (0.6.1)
Requirement already satisfied: pytest-filter-subpackage>=0.1.2 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (0.2.0)
Requirement already satisfied: pytest-cov>=2.3.1 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (5.0.0)
Requirement already satisfied: pytest-mock>=2.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (3.14.0)
Requirement already satisfied: attrs>=19.2.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (23.2.0)
Requirement already satisfied: hypothesis>=5.1 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-astropy) (6.100.0)
Requirement already satisfied: sortedcontainers<3.0.0,>=2.1.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from hypothesis>=5.1->pytest-astropy) (2.4.0)
Requirement already satisfied: exceptiongroup>=1.0.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from hypothesis>=5.1->pytest-astropy) (1.2.0)
Requirement already satisfied: iniconfig in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest>=4.6->pytest-astropy) (2.0.0)
Requirement already satisfied: packaging in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest>=4.6->pytest-astropy) (24.0)
Requirement already satisfied: pluggy<2.0,>=1.4 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest>=4.6->pytest-astropy) (1.4.0)
Requirement already satisfied: tomli>=1 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest>=4.6->pytest-astropy) (2.0.1)
Requirement already satisfied: coverage>=5.2.1 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from coverage[toml]>=5.2.1->pytest-cov>=2.3.1->pytest-astropy) (7.4.4)
Requirement already satisfied: setuptools>=30.3.0 in /home/PJLAB/libowen/anaconda3/envs/astropy__astropy__1.3/lib/python3.9/site-packages (from pytest-doctestplus>=1.0.0->pytest-astropy) (68.2.2)
Installing collected packages: astropy
  Running setup.py develop for astropy
Successfully installed astropy-3.1.dev22325

Std. Error: 

>>>>> Init Succeeded
>>>>> Applied Patch (test)

```

# Run evaluation

To evaluate predictions, use the `run_evaluation.py` script with the specified arguments.

```shell
cd OD-SWE-bench/swebench/harness
python run_evaluation.py \
    --predictions_path PATH_TO_PREDICTION_FILES \
    --swe_bench_tasks PATH_TO_swe-bench-test.json \
    --temp_dir PATH_TO_TEMP_DIR \
    --log_dir PATH_TO_LOG_DIR \
    --testbed PATH_TO_TESTBED_DIR \
    --conda_path PATH_TO_YOUR_CONDA \
    --num_processes 4 \
    --skip_existing \
    --timeout 1000 \
    --verbose
```

> Tip: uncomment L129 in `run_evaluation.py` to test gold patches. This is a temporary workaround and will be addressed in future updates.

Modifications differing from the original SWE-bench evaluation code include:
- Reuse testbeds and Conda environments.
- Additionally try `patch` command for patch application if `git apply` command fails.

# Results

## Results on SWE-bench-devin-passed

[🤗 OpenDevin/SWE-bench-devin-passed](https://huggingface.co/datasets/OpenDevin/SWE-bench-devin-passed)

| Model/Agent            | #instances | #init | #apply | #resolve |
|------------------------|------------|-------|--------|----------|
| Gold                   | 79         | 79    | 79     | 79       |
| Devin                  | 79         | 79    | 76     | 76       |

#init: number of instances where testbeds have been successfully initialized.

In the 3 Devin-failed instances (see below), Devin has made changes to the tests, which are incomptible with the provided test patch and causes failures during patch application. The evaluation adopted by Devin does not seem to align with the original SWE-bench evaluation.

```shell
django__django-11244
scikit-learn__scikit-learn-10870
sphinx-doc__sphinx-9367
```

## Results on SWE-bench-devin-failed

| Model/Agent            | #instances | #init | #apply | #resolve |
|------------------------|------------|-------|--------|----------|
| Gold                   | 491        | 491   | 491    | 371      |
| Devin                  | 491        | 491   | 463    | 7        |

Devin passes 7 instances on the `SWE-bench-devin-failed` subset. SWE-bench dataset appears to be noisy, evidenced by 120 instances where gold patches do not pass.

See the instance ids [here](../../inference/make_datasets/devin_failed_gold_failed.txt).

We have filtered out the problematic 120 instances, resulting in the creation of the `SWE-bench-devin-full-filtered` subset.

## Results on SWE-bench-devin-full-filtered

[🤗 OpenDevin/SWE-bench-devin-full-filtered](https://huggingface.co/datasets/OpenDevin/SWE-bench-devin-full-filtered)

| Model/Agent            | #instances | #init | #apply | #resolve |
|------------------------|------------|-------|--------|----------|
| Gold                   | 450        | 450   | 450    | 450      |
| Devin                  | 450        | 450   | 426    | 83       |
