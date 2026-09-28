# DVC Experiments

DVC experiments allow us to test different configurations of the same ML pipeline without creating a Git commit for every experiment.

## 1. Run an Experiment

Run the pipeline while temporarily changing a parameter:

```bash
dvc exp run -S train.test_size=0.30
```

`-S` overrides a parameter from `params.yaml` for that experiment.

Example:

```yaml
train:
  test_size: 0.25
  random_state: 42
```

Experiment:

```text
test_size = 0.30
random_state = 42
```

The original `params.yaml` does not need to be manually edited for each experiment.

---

## 2. Give an Experiment a Name

DVC can generate a random name automatically, or we can provide one:

```bash
dvc exp run -n test-size-03 -S train.test_size=0.30
```

---

## 3. List Experiments

```bash
dvc exp list
```

Shows the experiments associated with the repository.

---

## 4. Compare Experiments

```bash
dvc exp show
```

Shows parameters, metrics, and experiment information.

For a cleaner table:

```bash
dvc exp show --only-changed --param-deps
```

---

## 5. Find the Best Experiment

For example, sort by accuracy:

```bash
dvc exp show --sort-by=accuracy --sort-order=desc
```

This helps identify which experiment produced the highest accuracy.

---

## 6. Apply an Experiment

```bash
dvc exp apply <experiment-name>
```

Example:

```bash
dvc exp apply blown-teff
```

This takes the state of that experiment and applies it to the current workspace.

It can restore things such as:

```text
params.yaml
models/model.pkl
data/test.csv
metrics.json
```

The experiment is **not rerun**. Its recorded state is applied to the workspace.

---

## 7. Experiment vs Git Commit

An experiment is useful for trying different configurations without creating a Git commit for every trial.

```text
Same pipeline
     │
     ├── test_size=0.20 → Experiment A
     ├── test_size=0.30 → Experiment B
     └── test_size=0.40 → Experiment C
```

After comparing them, we can apply the experiment we want to keep:

```text
Experiment B
     ↓
dvc exp apply
     ↓
Workspace
     ↓
Git commit
```

This turns the selected experiment into a normal project state recorded in Git.

---

## 8. Important Mental Model

```text
params.yaml
     ↓
DVC Pipeline
     ↓
dvc exp run
     ↓
Experiment
     ↓
dvc exp show
     ↓
Compare experiments
     ↓
dvc exp apply
     ↓
Workspace
     ↓
Git commit
```

### Simple rule

> **DVC experiments are for trying different configurations. Git commits are for preserving the project states we decide to keep.**
