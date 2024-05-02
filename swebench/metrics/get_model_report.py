from swebench.metrics.report import get_model_report
import argparse

def main(model, predictions_path, swe_bench_tasks, log_dir):
    report = get_model_report(model, predictions_path, swe_bench_tasks, log_dir)
    for k, v in report.items():
        print(f"- {k}: {len(v)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Path to the model file")
    parser.add_argument("--predictions_path", help="Path to the predictions file")
    parser.add_argument("--swe_bench_tasks", help="SWE bench tasks")
    parser.add_argument("--log_dir", help="Directory to save logs")

    args = parser.parse_args()

    main(args.model, args.predictions_path, args.swe_bench_tasks, args.log_dir)

