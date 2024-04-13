from datasets import load_dataset
import pandas as pd

dataset = load_dataset("princeton-nlp/SWE-bench")
test = dataset["test"].to_pandas()
test.to_json("eval_data/instances/swe-bench-test.json", orient="records")