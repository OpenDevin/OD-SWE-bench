import argparse
import json
import logging

from context_manager import TestbedContextManager, TaskEnvContextManager
from typing import Dict

from utils import DotDict
import os.path as osp
from multiprocessing import Pool

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("engine_testbed")


def is_json(myjson: str):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def validate_args(args):
    if args.timeout is not None and args.timeout < 0:
        raise ValueError(f"Timeout must be a positive integer")

def verify_task_instances(data: Dict):
    """
    Sets up task environment context manager. Each task instance is then
    installed and validated within the context manager.
    Args:
        data: Dict containing task instances and other data
            task_instances: List of task instances
            + setup_testbed args
    """
    data_dict = DotDict(data)
    for task_instance in data_dict.task_instances:
        with TaskEnvContextManager(
            task_instance,
            data_dict.testbed,
            data_dict.venv,
            data_dict.log_dir,
            data_dict.conda_path,
            verbose=data_dict.verbose,
            timeout=data_dict.timeout,
            log_suffix=data_dict.log_suffix,
        ) as tcm:
            print("reset_task_env: ", tcm.reset_task_env(task_instance))
            print("run_install_task: ", tcm.run_install_task(task_instance))
            print("apply_test_patch: ", tcm.apply_patch(task_instance["test_patch"], patch_type="test"))

def setup_testbed(data: Dict):
    """
    Creates testbed context manager and runs verify_task_instances in parallel
    Args:
        data: Dict containing task instances and other data
            task_instances: List of task instances
            log_dir: Path to log directory
            path_conda: Path to miniconda3 or anaconda installation
            testbed: Path to testbed directory
            temp_dir: Path to temporary directory for storing virtual envs
            timeout: Timeout (seconds) for testing script execution
            verbose: Verbose mode
    """
    data_dict = DotDict(data)
    with TestbedContextManager(
        data_dict.task_instances,
        data_dict.log_dir,
        path_conda=data_dict.conda_path,
        testbed=data_dict.testbed,
        temp_dir=data_dict.temp_dir,
        timeout=data_dict.timeout,
        verbose=data_dict.verbose,
    ) as tcm:
        distributed_task_list = tcm.get_distributed_tasks()
        for task_list in distributed_task_list:
            print(
                f"{task_list['testbed']}: {len(task_list['task_instances'])} instances"
            )

        if len(distributed_task_list) == 1:
            data_dict.func(distributed_task_list[0])
            return

        pool = Pool(processes=len(distributed_task_list))
        pool.map(data_dict.func, distributed_task_list)
        pool.close()
        pool.join()
    return

def main(args):
    if args.devin_output_path:
        devin_output = json.load(open(args.devin_output_path, "r"))
        devin_instance_ids = [_["instance_id"] for _ in devin_output]
    else:
        devin_instance_ids = []

    instances_list = None
    if args.instances_path:
        with open(args.instances_path, 'r', encoding='utf-8') as f:
            instances_list = json.load(f)
    elif args.swe_bench_tasks:
        from swebench import get_eval_refs
        instances_list = list(get_eval_refs(args.swe_bench_tasks).values())

    if not instances_list:
        raise ValueError("No task instances found")

    for idx, item in enumerate(instances_list):
        # if (args.instance_id != item["instance_id"]):
        #     continue
        log_file = osp.join(args.log_dir, item["instance_id"] + ".log")

        if devin_instance_ids and item["instance_id"] not in devin_instance_ids:
            print(f"[{idx}/{len(instances_list)}] Skipping {item['instance_id']} as it is not in devin's output")
            continue
        elif osp.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()

            if "Init Succeeded" in log_content:
                print(f"[{idx}/{len(instances_list)}] Skipping {item['instance_id']} it's already initiated.")
                continue
        else:
            print(f"[{idx}/{len(instances_list)}] Processing {item['instance_id']}")

        task_instance = item
        data_group = {
                "task_instances": [task_instance],
                "func": verify_task_instances,
                **vars(args),
        }
        setup_testbed(data_group)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--instances_path", type=str, help="task instances path", required=False)
    parser.add_argument("--swe_bench_tasks", type=str, help="Path to dataset file or HF datasets name", required=False)
    # parser.add_argument("--instance_id", type=str, help="JSON String for an individual task instance", required=True)
    parser.add_argument("--log_dir", type=str, help="Path to log directory", required=True)
    parser.add_argument("--devin_output_path", type=str, help="Path to devin's output", required=False)
    parser.add_argument("--conda_path", type=str, help="(Optional) Path to miniconda3 or anaconda installation")
    parser.add_argument("--testbed", type=str, help="(Optional) Path to testbed directory")
    parser.add_argument("--venv", type=str, help="(Optional) Virtual environment for the test")
    parser.add_argument("--timeout", type=int, default=None, help="(Optional) Timeout (seconds) for testing script execution")
    parser.add_argument("--verbose", action="store_true", help="(Optional) Verbose mode")
    args = parser.parse_args()
    validate_args(args)
    logger.propagate = args.verbose
    main(args)