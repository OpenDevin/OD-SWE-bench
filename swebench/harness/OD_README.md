# Setup

Please create a clean env for evaluation. DO NOT use the original `swe-bench` env.

```shell
conda create -n swe-bench-eval python==3.11.5
pip install requests python-dotenv GitPython

# for cffi django__django__2.1
sudo apt-get update
sudo apt-get install libffi-dev
```

# Run engine testbed

The `engine_testbed.py` does the sanity check on repo installation and test patch application. It also saves the testbeds and creates conda envs.

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

All required conda envs for test instances will be created under your own conda. You can activate any of them.

The log of a successful run should be like

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