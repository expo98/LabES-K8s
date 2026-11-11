import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def val(x):
    s = str(x)
    if s.endswith("m"):
        return float(s[:-1]) / 1000
    try:
        return float(s)
    except ValueError:
        return float("nan")

runs = {"E1": "CPU %", "E2": "CPU %", "E3": "req/s per Pod", "E4": "req/s per Pod"}
for e, label in runs.items():
    try:
        d = pd.read_csv(f"evidence/{e}-samples.csv")
    except FileNotFoundError:
        print("missing", e); continue
    d["t"] = pd.to_datetime(d["time"], format="%H:%M:%S")
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9, 5))
    ax[0].step(d.t, d.current, where="post", label="current")
    ax[0].step(d.t, d.desired, where="post", linestyle="--", label="desired")
    ax[0].set_ylabel("replicas"); ax[0].legend()
    ax[0].set_title(f"{e}: replicas and driving metric")
    ax[1].plot(d.t, d["metric"].map(val)); ax[1].set_ylabel(label)
    plt.tight_layout(); plt.savefig(f"evidence/{e}-replicas.png", dpi=150); plt.close()
    print("saved", e)
