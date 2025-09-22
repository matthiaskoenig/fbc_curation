from pathlib import Path

import bottle as bottle
import pandas as pd
import json

import altair as alt

alt.renderers.enable("mimetype")

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


def process_jsons(results_dir: Path) -> pd.DataFrame:
    """Processes the results JSON in the results folder."""
    json_paths = list(results_dir.glob("**/*.json"))
    json_paths = [p for p in json_paths if not str(p).endswith("metadata.json")]
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
    df.to_csv(results_dir / "analysis.tsv", sep="\t")
    return df


def plot_results_matplotlib(df: pd.DataFrame):
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
    legend_lines = [
        Line2D([0], [0], color=colors[c], marker="s", linestyle="") for c in collections
    ]

    # ax1: plt.Axes = fig.add_subplot(gs[1, 1])
    # sns.catplot(x="collection", y="success", data=df, ax=ax1)

    # execution time
    ax: plt.Axes = fig.add_subplot(gs[2, 0:2])
    for collection in collections:
        ax.plot(
            df.time[df.collection == collection] / 1000,
            marker="s",
            color=colors[collection],
        )
    ax.set_xlabel("model index")
    ax.set_ylabel("execution time [s]")
    ax.set_yscale("log")
    ax.grid(axis="y")
    ax.set_title("Execution time (fbc_curation)")

    # legend

    ax.legend(legend_lines, collections)

    plt.show()


def plot_results_altair(df: pd.DataFrame):
    """Plot results with altair."""
    print("creating altair plot")
    alt.Chart(df).mark_circle(size=60).encode(
        x="index",
        y="time",
        color="collection",
        tooltip=["collection", "mid", "valid1", "valid2"],
    ).interactive()


# -----------------------

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("analysis.html", plot="<b>plot 1</b>")


# Flask
# altair
# lifereload
# bottle

if __name__ == "__main__":
    from livereload import Server

    results_dir = Path(__file__).parent.parent / "results1"
    df = process_jsons(results_dir=results_dir)
    # plot_results_matplotlib(df)
    plot_results_altair(df)

    app.debug = True
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run('0.0.0.0', 8085, debug=True, extra_files=["templates/analysis.html"])
    server = Server(app.wsgi_app)
    server.watch()
    # server.serve()
