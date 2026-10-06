# MLflow vs DVC

## 1. Main Difference

Both MLflow and DVC help make ML projects reproducible, but they focus on different parts of the workflow.

| Tool | Main Focus |
|---|---|
| **DVC** | Data, artifacts, and pipeline versioning |
| **MLflow** | Experiment tracking and model lifecycle |

---

## 2. DVC

### Main Role

DVC answers:

> **What data, code, parameters, and pipeline state produced this result?**

### DVC manages

- **Datasets and data versions** — Keeps track of different versions of the data used by the project.
- **Model artifacts** — Stores and versions files produced by training, such as `model.pkl`.
- **Pipeline stages** — Defines the steps of an ML workflow, such as `prepare → train → evaluate`.
- **Dependencies and outputs** — Records which files each stage needs and which files it produces.
- **Parameters** — Tracks configurable values used by the pipeline, such as `test_size` or `random_state`.
- **Reproducibility** — Allows the same pipeline to be recreated using the correct data, code, and parameters.
- **Remote data storage** — Stores large DVC-tracked files outside Git while Git keeps their metadata.

### Typical workflow

```text
Data
  ↓
DVC Pipeline
  ↓
Model
  ↓
Reproducible result
```

Important commands:

```bash
dvc add
dvc repro
dvc push
dvc pull
dvc exp run
```

---

## 3. MLflow

### Main Role

MLflow answers:

> **Which experiment configuration produced this result?**

### MLflow manages

- **Experiment runs** — A single execution of a training workflow with a specific configuration.
- **Parameters** — Values used during a run, such as learning rate or batch size.
- **Metrics** — Numerical results used to evaluate a run, such as accuracy or F1-score.
- **Artifacts** — Files generated during a run, such as plots, reports, or model files.
- **Models** — Trained ML models that can be stored, registered, and managed.
- **Model versions** — Different versions of a registered model as it is updated over time.

### Typical workflow

```text
Experiment
    ↓
MLflow Run
    ↓
Parameters + Metrics
    ↓
Compare experiments
```

---

## 4. When to Use Each

### Use DVC When...

The main problem is **data, pipeline, or reproducibility**.

Examples:

- You have large datasets or model files that should not be stored directly in Git.
- You need to version datasets and other ML artifacts.
- You want to reproduce a pipeline using a specific data and code version.
- You want to know which data, parameters, and pipeline produced a model.

```text
DVC
Data → Pipeline → Version → Reproduce
```

### Use MLflow When...

The main problem is **tracking and comparing experiments**.

Examples:

- You are running many training experiments.
- You want to compare parameters and metrics between runs.
- You want to keep a history of model experiments.
- You want to manage and track model versions for deployment.

```text
MLflow
Run → Parameters → Metrics → Compare → Model
```

---

## 5. DVC + MLflow Together

They are **complementary tools**, not replacements for each other.

```text
                  ML Project
                      │
           ┌──────────┴──────────┐
           ↓                     ↓
          DVC                 MLflow
           │                     │
    Data + Pipeline       Experiments
    Versioning            + Metrics
    + Artifacts           + Models
           │                     │
           └──────────┬──────────┘
                      ↓
              Reproducible ML
```

For example:

```text
DVC:
dataset v2
+ code v3
+ params
+ pipeline
       ↓
    training
       ↓
   model.pkl
       ↓
MLflow:
accuracy = 0.91
precision = 0.89
run configuration
```

---

## 6. Simple Rule

Ask:

> **What am I trying to track?**

**Data + pipeline + reproducibility → DVC**

**Experiments + metrics + model tracking → MLflow**

**Need both → DVC + MLflow**

### Mental Model

> **DVC manages the data and pipeline. MLflow manages the experiments and model tracking.**

```text
Version → Reproduce → Train → Track → Compare
   DVC       DVC        DVC    MLflow    MLflow
```
```
