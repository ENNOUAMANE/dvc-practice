# MLflow vs DVC

## 1. Main Difference

Both MLflow and DVC help make ML projects reproducible, but they focus on different parts of the workflow.

| Tool       | Main Focus                               |
| ---------- | ---------------------------------------- |
| **DVC**    | Data, artifacts, and pipeline versioning |
| **MLflow** | Experiment tracking and model lifecycle  |

---

## 2. DVC

### Main Role

DVC answers:

> **What data, code, parameters, and pipeline state produced this result?**

### DVC manages

* **Datasets and data versions** — Keeps track of different versions of the data used by the project.
* **Model artifacts** — Stores and versions files produced by training, such as `model.pkl`.
* **Pipeline stages** — Defines the steps of an ML workflow, such as `prepare → train → evaluate`.
* **Dependencies and outputs** — Records which files each stage needs and which files it produces.
* **Parameters** — Tracks configurable values used by the pipeline, such as `test_size` or `random_state`.
* **Reproducibility** — Allows the same pipeline to be recreated using the correct data, code, and parameters.
* **Remote data storage** — Stores large DVC-tracked files outside Git while Git keeps their metadata.

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
```

---

## 3. MLflow

### Main Role

MLflow answers:

> **Which experiment configuration produced this result?**

### MLflow manages

* **Experiment runs** — A single execution of a training workflow with a specific configuration.
* **Parameters** — Values used during a run, such as learning rate or batch size.
* **Metrics** — Numerical results used to evaluate a run, such as accuracy or F1-score.
* **Artifacts** — Files generated during a run, such as plots, reports, or model files.
* **Models** — Trained ML models that can be stored, registered, and managed.
* **Model versions** — Different versions of a registered model as it is updated over time.

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

## 4. DVC + MLflow Together

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

## 5. Simple Rule

> **DVC manages the data and pipeline.**
> **MLflow manages the experiments and model tracking.**

Using both gives you a clearer ML lifecycle:

```text
Version → Reproduce → Train → Track → Compare
   DVC       DVC        DVC    MLflow    MLflow
```
