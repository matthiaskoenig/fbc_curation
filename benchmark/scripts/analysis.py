from pathlib import Path
from pprint import pprint
import pandas as pd
import json
import re

from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D




def process_jsons(results_dir: Path) -> pd.DataFrame:
    """Processes the results JSON in the results folder."""
    json_paths = list(results_dir.glob('**/*.json'))
    json_paths = [p for p in json_paths if not str(p).endswith('metadata.json')]
    # pprint(json_paths)
    # pprint(len(json_paths))

    info_dicts = []
    for p in json_paths:
        with open(p, "r") as f_json:
            d = json.load(f_json)
        valid = d["valid"]
        d["valid1"] = valid[0]
        d["valid2"] = valid[1]

        p_tokens = str(p).split("/")
        collection, mid = p_tokens[-2], p_tokens[-1][:-5]
        d["collection"] = collection
        d["mid"] = mid
        del d["model_path"]
        info_dicts.append(d)

    df = pd.DataFrame(data=info_dicts)
    # print(df.columns)
    df = df[["collection", "mid", "status", "equal", "valid1", "valid2", "time"]]
    print("-" * 80)
    print(df)
    print("-" * 80)

    # store processed results
    df.to_csv(results_dir / "analysis.tsv", sep="ţ")
    return df


def results_plot(df: pd.DataFrame):
    """Create overview plot of results."""
    # ax = sns.barplot(x="collection", y="status", data=df)
    # plt.show()

    # subplots
    # 1. success (Y/N) execution (barplot)
    # 2. equal (Y/N) (barplot)
    # 3. valid1 (Y/N) (barplot)
    # 4. valid2 (Y/N) (barplot)
    # 5. index ~ time (scatter, colored by collection)

    # global plot settings
    colors = {
        "bigg": "tab:blue",
        "optflux": "tab:green",
        "ebrahim": "tab:red",
    }
    parameters = {
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "normal",
    }
    plt.rcParams.update(parameters)

    # create figure
    fig: plt.Figure = plt.figure(
        figsize=(10, 10),
        dpi=150,
    )
    gs = GridSpec(nrows=3, ncols=2, figure=fig)
    collections = df.collection.unique()
    legend_lines = [Line2D([0], [0], color=colors[c], marker="s", linestyle="") for c in
                    collections]

    # execution time
    ax: plt.Axes = fig.add_subplot(gs[2, 0:2])
    for collection in collections:
        ax.plot(
            df.time[df.collection == collection] / 1000,
            marker='s',
            color=colors[collection]
        )
    ax.set_xlabel("model index")
    ax.set_ylabel("execution time [s]")
    ax.set_yscale("log")
    ax.grid(axis="y")
    ax.set_title("Execution time (fbc_curation)")

    # legend

    ax.legend(legend_lines, collections)

    plt.show()

if __name__ == "__main__":
    results_dir = Path(__file__).parent.parent / "results1"
    df = process_jsons(results_dir=results_dir)



