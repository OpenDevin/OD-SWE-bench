#!/usr/bin/env python3

"""Run evaluation"""
import argparse
import logging
import os
from tqdm.auto import tqdm

# import sys
# sys.path.append("../../../OD-SWE-bench")

from multiprocessing import Pool
from swebench.harness.constants import (
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION,
)
from swebench.harness.engine_evaluation import main as eval_engine
from swebench.harness.engine_evaluation import evaluate_predictions
from swebench.harness.utils import get_instances, DotDict, extract_minimal_patch
from swebench.metrics.getters import get_eval_refs
from swebench.harness.context_manager import TestbedContextManager, TaskEnvContextManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("run_evaluation")


def setup_swe_env(data: dict, apply_test_patch=True, run_gold_tests=False):
    """
    Sets up task environment for a given task instance.

    Args:
        data: Dict containing task instances and other data
            task_instances: List of [task instance, prediction] pairs to evalute
            + setup_testbed args
    Returns:

    """
    data_dict = DotDict(data)
    for task_instance in tqdm(
        data_dict.task_instances,
        disable=data_dict.verbose,
        desc=f"Evaluating predictions for {data_dict.log_dir}"
    ):
        with TaskEnvContextManager(
            task_instance,
            data_dict.testbed,
            data_dict.venv,
            data_dict.log_dir,
            data_dict.conda_path,
            verbose=data_dict.verbose,
            timeout=data_dict.timeout,
            is_eval=True,
            log_suffix=data_dict.log_suffix,
        ) as tcm:
            # Attempt to set up environment with task instance
            if not tcm.reset_task_env(task_instance):
                print("Failed to reset task environment")
                return False
            
            if not tcm.run_install_task(task_instance):
                print("Failed to run install task")
                return False

            if apply_test_patch:
                if not tcm.apply_patch(task_instance["test_patch"], patch_type="test"):
                    print("Failed to apply test patch")
                    return False

            if run_gold_tests:
                if not apply_test_patch:
                    if not tcm.apply_patch(task_instance["test_patch"], patch_type="test"):
                        print("Failed to apply test patch")
                        return False

                # Attempt to apply gold patch
                patch_type = "pred_try" # This has been replaced with gold patch.
                if not tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type) \
                    and task_instance[KEY_PREDICTION] is not None:
                    task_instance[KEY_PREDICTION] = extract_minimal_patch(task_instance[KEY_PREDICTION])
                    patch_type = "pred_minimal_try"
                    if not tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type):
                        continue
                tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type, revert=True)
                patch_type = patch_type.replace("_try", "")

                # Run installation + testing script
                if (
                    not tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type)
                    or not tcm.run_tests_task(task_instance)
                ):
                    return False
            
            return True


def main(
    swe_bench_tasks: str,
    instance_id: str,
    log_dir: str,
    temp_dir: str,
    testbed: str,
    conda_path: str,
    timeout: int,
    verbose: bool,
):
    # Validate arguments
    if not os.path.exists(log_dir) or not os.path.isdir(log_dir):
        raise ValueError("--log_dir must exist and point at a directory")
    if not os.path.exists(testbed) or not os.path.isdir(testbed):
        raise ValueError("--testbed must exist and point at a directory")
    tasks = list(get_eval_refs(swe_bench_tasks).values())

    # Verify arguments are formatted correctly
    if not isinstance(tasks, list):
        raise ValueError(f"{swe_bench_tasks} must contain an array of tasks")
    tasks_map = {t[KEY_INSTANCE_ID]: t for t in tasks}
    task = tasks_map[instance_id]
    

    with TestbedContextManager(
        [task],
        log_dir,
        path_conda=conda_path,
        testbed=testbed,
        temp_dir=temp_dir,
        timeout=timeout,
        verbose=verbose,
    ) as tcm:
        distributed_task_list = tcm.get_distributed_tasks()
        assert len(distributed_task_list) == 1
        task_set = distributed_task_list[0]
        instance = task_set["task_instances"][0]
        conda_env_name = instance["repo"].replace("/", "__") + "__" + instance["version"]
        repo_path = os.path.join(testbed, conda_env_name)

        instance["model_patch"] = instance["patch"]
        instance["model_name_or_path"] = "gold"

        if not setup_swe_env(task_set, apply_test_patch=False, run_gold_tests=False):
            print("Failed to set up SWE environment")
            repo_path = None
            conda_env_name = None
        print("test_cmd:", instance["test_cmd"])
        print("repo_path:", repo_path)
        print("code_env_name:", conda_env_name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_dir", type=str, help="Path to log directory", required=True)
    parser.add_argument("--temp_dir", type=str, help="Path to temp directory", required=True)
    parser.add_argument("--swe_bench_tasks", type=str, help="Path to dataset file or HF datasets name", required=True)
    parser.add_argument("--instance_id", type=str, help="", required=True)
    parser.add_argument("--testbed", type=str, help="Path to testbed directory", required=True)
    parser.add_argument("--conda_path", type=str, default=None, help="(Optional) Path to conda installation to use")
    parser.add_argument("--timeout", type=int, help="(Optional) Timeout in seconds (default: 900)", default=900)
    parser.add_argument("--verbose", action="store_true", help="(Optional) Verbose mode")
    args = parser.parse_args()
    logger.propagate = args.verbose
    main(**vars(args))