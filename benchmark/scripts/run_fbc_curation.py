"""
The script path is always relative to the Snakefile containing the directive
(in contrast to the input and output file paths, which are relative to the working
directory). It is recommended to put all scripts into a subfolder scripts as above.

Inside the script, you have access to an object `snakemake` that provides access to
the same objects that are available in the run and shell directives
(input, output, params, wildcards, log, threads, resources, config),
e.g. you can use snakemake.input[0] to access the first input file of above rule.
"""


# redirect standard output
import traceback

import json
from pathlib import Path
from timeit import default_timer

# with open(snakemake.log[0], "w") as f:
#     sys.stderr = sys.stdout = f

from fbc_curation.curator import Curator, FROGResults
from fbc_curation.curator.cameo_curator import CuratorCameo
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy


def run_fbc_curation(model_path: Path, results_path: Path, json_path: Path):
    """Run fbc curation on given model and store results in JSON."""

    time0 = default_timer()
    info = {
        "model_path": str(model_path),
    }
    try:
        if not results_path.exists():
            results_path.mkdir(parents=True, exist_ok=True)
        print("#" * 80)
        print(model_path)
        print("#" * 80)
        obj_info = Curator._read_objective_information(model_path)

        curator_keys = ["cobrapy", "cameo"]
        for k, curator_class in enumerate([CuratorCobrapy, CuratorCameo]):
            curator = curator_class(
                model_path=model_path, objective_id=obj_info.active_objective
            )
            results: FROGResults = curator.run()

            results.write_results(results_path / curator_keys[k])

        all_results = {}
        for curator_key in curator_keys:
            all_results[curator_key] = FROGResults.read_results(
                path_in=results_path / curator_key
            )

        # comparison
        info["valid"] = [r.validate() for r in all_results.values()]
        info["equal"] = FROGResults.compare_reports(all_results)

    except Exception as err:
        info["status"] = "exception"
        info["error"] = str(traceback.format_exc())
        raise err
    else:
        info["status"] = "success"
        info["error"] = None

    time1 = default_timer()
    info["time"] = (time1 - time0) * 1000

    with open(json_path, "w") as f_json:
        json.dump(info, f_json, indent=2)

    return info


run_fbc_curation(
    model_path=Path(snakemake.input[0]),
    json_path=Path(snakemake.output[0]),
    results_path=Path(snakemake.output[1]),
)
