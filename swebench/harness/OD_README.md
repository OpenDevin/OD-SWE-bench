# Setup

Please create a new, clean environment for evaluation purposes. DO NOT use the original `swe-bench` environment.

```shell
sudo apt-get update
sudo apt-get install libffi-dev
sudo apt-get install build-essentials

conda create -n swe-bench-eval python==3.11.5
conda activate swe-bench-eval
pip install requests python-dotenv GitPython datasets pandas beautifulsoup4 ghapi
```

## Troubleshooting

If you encounter erros similar to the one below during running installation commands that use `/bin/sh`, it might be due to the shell environment.

```shell
Error stderr: /bin/sh: 5: /home/swe-bench/miniconda3/envs/sphinx-doc__sphinx__3.5/etc/conda/deactivate.d/deactivate-gxx_linux-64.sh: Syntax error: "(" unexpected

Error traceback: Traceback (most recent call last):
  File "/home/swe-bench/swebench/harness/context_manager.py", line 55, in __call__
    output = subprocess.run(cmd, **combined_args)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/swe-bench/miniconda3/lib/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '. /home/swe-bench/miniconda3/etc/profile.d/conda.sh && conda activate sphinx-doc__sphinx__3.5 && conda install gxx_linux-64 gcc_linux-64 make -y' returned non-zero exit status 2.
```

The default `/bin/sh` might not point to `bash`. Switching to `bash` can resolve this issue.

```shell
sudo ln -sfn /bin/bash /bin/sh
```

You may revert to your original shell if necessary.

```shell
sudo ln -sfn {your_default_shell} /bin/sh
```

# Prepare data

To prepare the data necessary for running evaluations, run the following script.

```shell
cd swebench/harness
chmod +x prepare_data.sh
conda activate swe-bench-eval
./prepare_data.sh
```

Below is the structure of the `eval_data` directory, which organizes the resources needed for the evaluation:

```shell
├── eval_data
│   ├── eval_logs   # dir for evaluation logs
│   ├── eval_temp   # temp dir for evaluation
│   ├── instances   # dir for raw test instances
│   ├── outputs     # dir for model/agent outputs
│   ├── testbed_logs  # dir for engine testbed logs
│   └── testbeds      # dir for testbeds
```


# Run engine testbed

This step is actually optional, but we strongly recommend executing it first. Failing to prepare the testbeds beforehand may lead to failures in **multi-processing** evaluation.

The `engine_testbed.py` script performs a sanity check on the repository installation and test patch application. It saves the testbeds and creates reusable conda environments.

Execute the `engine_testbed.py` script with your conda path:
```shell
python engine_testbed.py \
    --instances_path eval_data/instances/swe-bench-test-lite.json \
    --log_dir  eval_data/testbed_logs \
    --conda_path YOUR_CONDA_PATH \
    --testbed eval_data/testbeds \
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

To evaluate `devin_swe_passed` predictions, use the `run_evaluation.py` script with your conda path.

```shell
python run_evaluation.py \
    --predictions_path eval_data/outputs/devin_swe_passed.json \
    --swe_bench_tasks eval_data/instances/swe-bench-test.json \
    --temp_dir eval_data/eval_temp \
    --log_dir eval_data/eval_logs \
    --testbed eval_data/testbeds \
    --conda_path YOUR_CONDA_PATH \
    --num_processes 4 \
    --skip_existing \
    --timeout 1000 \
    --verbose
```
> Warning ⚠️: Running the evaluation in **multi-processing** mode may lead to errors if the testbeds are not prepared. You are adviced to run engine testbed first and we will try to fix the issue.

> Tip: Uncomment L129 in `run_evaluation.py` to test gold patches. This is a temporary workaround and will be addressed in future updates.

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
