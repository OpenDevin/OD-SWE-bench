from swebench.metrics.report import get_instance_report
import argparse

def main(log_path, swe_bench_task):
    report = get_instance_report(log_path, swe_bench_task)
    for k, v in report.items():
        print(f"- {k}: {len(v)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path", help="Path to the log file")
    parser.add_argument("--swe_bench_task", help="SWE bench task")
    
    args = parser.parse_args()
    
    main(args.log_path, args.swe_bench_task)
