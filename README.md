# DVC Practice

A hands-on project for learning **Data Version Control (DVC)** and understanding how it works together with Git for reproducible machine learning workflows.

The project progressively covers data versioning, pipelines, experiments, metrics, plots, and switching between project versions.

---

## 🎯 Learning Goals

This repository is used to practice how to:

- Version datasets and ML artifacts with DVC
- Build reproducible ML pipelines
- Track pipeline dependencies and outputs
- Manage parameters and experiments
- Compare metrics between experiments and Git versions
- Visualize experiment results with DVC plots
- Restore data and model artifacts for older Git versions
- Understand the relationship between Git, DVC, and MLflow

---

## 🧠 Project Pipeline

The current ML pipeline is:

```text
data/dataset.csv
       ↓
   prepare.py
       ↓
data/processed.csv
       ↓
    train.py
       ↓
 ┌─────┴─────┐
 ↓           ↓
test.csv   model.pkl
 └─────┬─────┘
       ↓
  evaluate.py
       ↓
  metrics.json
```

### Pipeline stages

| Stage | Role |
|---|---|
| `prepare` | Prepares and normalizes the dataset |
| `train` | Splits the data, trains the model, and saves the model and test data |
| `evaluate` | Evaluates the trained model and records the accuracy |

---

## 📁 Project Structure

```text
dvc-practice/
│
├── data/
│   ├── dataset.csv
│   ├── processed.csv
│   └── test.csv
│
├── models/
│   └── model.pkl
│
├── plots/
│   └── accuracy.csv
│
├── src/
│   ├── prepare.py
│   ├── train.py
│   └── evaluate.py
│
├── dvc.yaml
├── dvc.lock
├── params.yaml
├── metrics.json
│
├── note.md
├── dvc-experiments.md
├── git-dvc-version-switching.md
└── mlflow-dvc.md
```

---

## 🔧 DVC Concepts Practiced

### Data Versioning

DVC tracks dataset versions while Git tracks the associated metadata.

```text
Git
 └── dataset.csv.dvc

DVC
 └── actual dataset
```

### DVC Remote

A local DVC remote is configured for this project:

```text
C:\Users\lenovo\dvc-storage
```

Used with:

```bash
dvc push
dvc pull
```

### Pipeline Reproduction

```bash
dvc repro
```

DVC checks dependencies and reruns the stages affected by changes.

### Parameters

Parameters are stored in:

```text
params.yaml
```

Example:

```yaml
train:
  test_size: 0.25
  random_state: 42
```

### Metrics

The evaluation stage produces:

```text
metrics.json
```

Example:

```json
{
  "accuracy": 0.88889
}
```

View metrics with:

```bash
dvc metrics show
```

### Experiments

Different parameter configurations can be tested without creating a Git commit for every trial.

```bash
dvc exp run -S train.test_size=0.20
dvc exp run -S train.test_size=0.30
dvc exp run -S train.test_size=0.40
```

Compare experiments:

```bash
dvc exp show
```

### Version Switching

Git selects a project version and DVC restores the corresponding data and artifacts.

```bash
git checkout <commit>
dvc checkout
```

Conceptually:

```text
git checkout
    ↓
Old code + DVC metadata
    ↓
dvc checkout
    ↓
Matching data + model
```

### Plots

Experiment results can also be visualized with:

```bash
dvc plots show
dvc plots diff
```

---

## 🔄 Typical Workflow

```text
1. Change data / code / parameters
          ↓
2. dvc status
          ↓
3. dvc repro
          ↓
4. Check metrics
          ↓
5. Run experiments
          ↓
6. Compare results
          ↓
7. Select a useful version
          ↓
8. Commit with Git
          ↓
9. dvc push
```

---

## 🔗 Git + DVC

Git and DVC have different responsibilities:

| Git | DVC |
|---|---|
| Code | Large datasets |
| `dvc.yaml` | Model artifacts |
| `dvc.lock` | DVC-tracked outputs |
| `params.yaml` | DVC remote storage |
| Project history | Data/artifact versions |

A useful mental model:

> **Git chooses the project version. DVC restores the data and artifacts belonging to that version.**

---

## 🆚 DVC vs MLflow

DVC and MLflow solve different problems.

```text
DVC
Data → Pipeline → Version → Reproduce

MLflow
Run → Parameters → Metrics → Compare → Model
```

### Use DVC for

- Dataset and artifact versioning
- Pipeline reproducibility
- Data dependencies
- Large ML files

### Use MLflow for

- Experiment tracking
- Parameter and metric logging
- Comparing model runs
- Model lifecycle management

### Use both when

You need both **reproducibility** and **experiment/model tracking**.

See [`mlflow-dvc.md`](mlflow-dvc.md) for more details.

---

## 📚 Learning Notes

| File | Topic |
|---|---|
| [`note.md`](note.md) | DVC fundamentals and commands |
| [`dvc-experiments.md`](dvc-experiments.md) | DVC experiment workflow |
| [`git-dvc-version-switching.md`](git-dvc-version-switching.md) | Git + DVC version switching |
| [`mlflow-dvc.md`](mlflow-dvc.md) | DVC vs MLflow |

---

## 🚀 Main Commands Learned

```bash
dvc init
dvc add
dvc status
dvc remote add
dvc remote list
dvc push
dvc pull

dvc stage add
dvc stage list
dvc repro

dvc metrics show
dvc metrics diff

dvc exp run
dvc exp show
dvc exp apply

dvc checkout

dvc plots show
dvc plots diff
```

---

## 🎯 Main Takeaway

The goal of this project is not just to memorize DVC commands, but to understand the workflow:

```text
Data
  ↓
Version
  ↓
Pipeline
  ↓
Experiment
  ↓
Metric
  ↓
Compare
  ↓
Select
  ↓
Reproduce
```

> **DVC makes data and ML pipelines versionable and reproducible, while Git provides the project history that connects those versions together.**