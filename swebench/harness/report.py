import argparse
import json
import os
import traceback

from collections import Counter
from rich import print
from swebench import (
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION,
    get_eval_report,
    get_logs_eval,
    get_model_report,
    get_resolution_status,
    run_evaluation,
    get_eval_refs,
)
from swebench.harness.constants import (
    INSTALL_FAIL,
)
from unidiff import PatchSet


def main(predictions_path, log_dir, swe_bench_tasks):
    # Check if paths exist
    if not os.path.exists(predictions_path):
        raise FileNotFoundError(f"Predictions path {predictions_path} does not exist")
    eval_refs = get_eval_refs(swe_bench_tasks)
    for k, v in eval_refs.items():
        eval_refs[k] = {key: v[key] for key in [KEY_INSTANCE_ID, "FAIL_TO_PASS", "PASS_TO_PASS"]}

    # Change model_name_or_patch field to directory name for all predictions
    directory = os.path.dirname(predictions_path)
    directory_name = directory.rsplit("/", 1)[-1]
    pred_path_orig = predictions_path
    if pred_path_orig.endswith(".jsonl"):
        pred_path_temp = predictions_path.replace(".jsonl", "_filtered.jsonl")
    else:
        pred_path_temp = predictions_path.replace(".json", "_filtered.json")


    if any([pred_path_orig.endswith(x) for x in [".jsonl", ".jsonl.all"]]):
        predictions = list()
        with open(pred_path_orig) as f:
            for line in f.readlines():
                predictions.append(json.loads(line))
    else:
        with open(pred_path_orig) as f:
            predictions = json.load(f)

    pred_total, pred_will_eval = 0, 0
    for p in predictions:
        pred_total += 1
        # Exclude predictions w/ empty strings
        # if p[KEY_PREDICTION] is not None and p[KEY_PREDICTION].strip() != "":
        pred_will_eval += 1
    print(
        f"Found {pred_total} total predictions, will evaluate {pred_will_eval} ({pred_total-pred_will_eval} are empty)"
    )
    print(f"Log directory for evaluation run: {log_dir}")

    # Iterate through predictions
    scorecards = []
    for p in predictions:
        scorecard = {KEY_INSTANCE_ID: p[KEY_INSTANCE_ID], "statuses": [], "stats": {}}

        # Add trajectory statistics if traj_path exists
        traj_path = os.path.join(directory, f"{p[KEY_INSTANCE_ID]}.traj")
        if os.path.exists(traj_path):
            traj_data = json.load(open(traj_path, "r"))
            scorecard["stats"]["traj_num_steps"] = len(traj_data["trajectory"])
            scorecard["stats"]["traj_action_dist"] = dict(
                Counter(
                    [
                        entry["action"].strip().split()[0]
                        if entry["role"] == "assistant" and "action" in entry and len(entry["action"]) > 0
                        else None
                        for entry in traj_data["history"]
                    ]
                )
            )
            scorecard["exit_status"] = (
                traj_data["info"]["exit_status"]
                if "exit_status" in traj_data["info"]
                else "n/a"
            )

        # Check that a prediction was generated
        #if p[KEY_PREDICTION] is None or p[KEY_PREDICTION].strip() == "":
        #    scorecard["statuses"].append("not_generated")
        #    scorecards.append(scorecard)
        #    continue
        scorecard["statuses"].append("generated")

        # Get log file
        log_path = os.path.join(
            log_dir, f"{p[KEY_INSTANCE_ID]}.{directory_name}.eval.log"
        )
        if not os.path.exists(log_path):
            scorecard["statuses"].append("build_failure")
            scorecards.append(scorecard)
            continue

        # Get evaluation logs
        eval_sm, found = get_logs_eval(log_path)

        # Check that the prediction generated
        if not found:
            scorecards.append(scorecard)
            continue
        scorecard["statuses"].append("applied")

        with open(log_path, "r") as f:
            log_contents = f.read()
            if INSTALL_FAIL in log_contents:
                scorecard["statuses"].append("install_fail")

        # Get resolution status
        report = get_eval_report(eval_sm, eval_refs[p[KEY_INSTANCE_ID]])
        scorecard["test_results"] = {
            "failure": {
                "FAIL_TO_PASS": report["FAIL_TO_PASS"]["failure"],
                "PASS_TO_PASS": report["PASS_TO_PASS"]["failure"],
            },
            "success": {
                "FAIL_TO_PASS": report["FAIL_TO_PASS"]["success"],
                "PASS_TO_PASS": report["PASS_TO_PASS"]["success"],
            }
        }
        resolution_status = get_resolution_status(report)
        scorecard["statuses"].append(resolution_status)

        diff_obj = PatchSet(p[KEY_PREDICTION])
        scorecard["patch_files"] = [
            x.path
            for x in diff_obj.modified_files
            + diff_obj.added_files
            + diff_obj.removed_files
        ]
        scorecard["patch_lines_add"] = sum([f.added for f in diff_obj])
        scorecard["patch_lines_del"] = sum([f.removed for f in diff_obj])
        scorecards.append(scorecard)

    # Calculate cumulative results
    get_ids_with_status = lambda x: [
        s[KEY_INSTANCE_ID] for s in scorecards if x in s["statuses"]
    ]
    report = {
        "# Not Generated": len(get_ids_with_status("not_generated")),
        "# Generated": len(get_ids_with_status("generated")),
        "# Applied": len(get_ids_with_status("applied")),
        "# Resolved": len(get_ids_with_status("RESOLVED_FULL")),
        "# Install Fail": len(get_ids_with_status("install_fail")),
    }
    print(f"== Evaluation Report ==\n{report}")

    report_exits = dict(
        Counter([s["exit_status"] if "exit_status" in s else "n/a" for s in scorecards])
    )

    # Save to summary, scorecard json
    path_scorecards = os.path.join(directory, "scorecards.json")
    with open(path_scorecards, "w") as f:
        json.dump(scorecards, fp=f, indent=2)
    print(f"- Wrote per-instance scorecards to {path_scorecards}")

    path_results = os.path.join(directory, "results.json")
    with open(path_results, "w") as f:
        json.dump(
            {
                "report": report,
                "report_exits": report_exits,
                "not_generated": get_ids_with_status("not_generated"),
                "generated": get_ids_with_status("generated"),
                "applied": get_ids_with_status("applied"),
                "resolved": get_ids_with_status("RESOLVED_FULL"),
                "not_resolved": get_ids_with_status("RESOLVED_NO"),
                "install_fail": get_ids_with_status("install_fail"),
            },
            fp=f,
            indent=2,
        )
    print(f"- Wrote summary of run to {path_results}")

    # Sanity check against get_model_report
    report = get_model_report(
        directory_name, pred_path_orig, swe_bench_tasks, log_dir
    )
    by_outcome = {}
    by_outcome_func = lambda status: len(
        [
            instance_id
            for _, v in report.items()
            if isinstance(v, dict)
            for instance_id in v[status]
        ]
    )
    by_outcome["# Not Generated"] = by_outcome_func("none")
    by_outcome["# Generated"] = by_outcome_func("generated")
    by_outcome["# Applied"] = by_outcome_func("applied")
    by_outcome["# Resolved"] = by_outcome_func("resolved")
    by_outcome["# Install Fail"] = by_outcome_func("install_fail")
    print(f"Reference Report:\n{by_outcome}")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predictions_path",
        type=str,
        help="Path to predictions file (.jsonl)",
        required=True,
    )
    parser.add_argument(
        "--log_dir", type=str, help="Path to log directory", required=True
    )
    parser.add_argument(
        "--swe_bench_tasks",
        type=str,
        help="Path to SWE-bench task instances file",
        required=True,
    )

    args = parser.parse_args()
    main(**vars(args))
