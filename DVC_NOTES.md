# DVC Practice — Commands & Concepts

## 1. Initialize Git

```bash
git init
```

Creates a Git repository for the project.

**Purpose:** Git tracks our code and DVC metadata.

---

## 2. Initialize DVC

```bash
dvc init
```

Initializes DVC inside the Git repository.

**Purpose:** Enables DVC for managing datasets, models, and pipelines.

Creates files such as:

```text
.dvc/
.dvcignore
```

---

## 3. Add Dataset to DVC

```bash
dvc add data/dataset.csv
```

Tells DVC to track the dataset.

DVC creates:

```text
data/dataset.csv.dvc
data/.gitignore
```

**Important:**

```text
Git → tracks dataset.csv.dvc

DVC → tracks the actual dataset
```

The `.dvc` file contains metadata such as the dataset's hash and size.

The hash acts like a **fingerprint of the dataset's contents**. If the dataset changes, its hash changes.

---

## 4. Check DVC Status

```bash
dvc status
```

Checks whether DVC-tracked data and pipelines are up to date.

Example:

```text
Data and pipelines are up to date.
```

means DVC detects no changes that require action.

If a dependency or output has changed, DVC reports the change.

---

## 5. Configure a DVC Remote

```bash
dvc remote add -d local_storage C:\Users\lenovo\dvc-storage
```

Creates a DVC remote called `local_storage`.

**Purpose:** The remote is where DVC stores the actual tracked data.

For practice, we used a local folder.

---

## 6. See DVC Remotes

```bash
dvc remote list
```

Shows the DVC remotes configured for the project.

---

## 7. Upload Data to the DVC Remote

```bash
dvc push
```

Synchronizes DVC-tracked data from the local DVC cache to the DVC remote.

```text
LOCAL DVC CACHE
       │
       │ dvc push
       ▼
DVC REMOTE
```

---

## 8. Download Data from the DVC Remote

```bash
dvc pull
```

Gets missing DVC-tracked data from the remote and restores it locally.

```text
DVC REMOTE
       │
       │ dvc pull
       ▼
LOCAL DVC CACHE / WORKSPACE
```

### Difference from Git

```text
git push → GitHub
dvc push → DVC remote

git pull → GitHub
dvc pull → DVC remote
```

Git and DVC manage different parts of the project.

---

# DVC Pipeline

After learning dataset versioning, we created a small preprocessing pipeline.

```text
dataset.csv
     │
     ▼
prepare.py
     │
     ▼
processed.csv
```

Our `prepare.py` normalizes `hours_studied` between `0` and `1`.

---

## 9. Create a DVC Pipeline Stage

```bash
dvc stage add -n prepare -d src/prepare.py -d data/dataset.csv -o data/processed.csv python src/prepare.py
```

This tells DVC how the preprocessing step works.

### Command breakdown

```text
-n prepare
```

Names the stage `prepare`.

```text
-d src/prepare.py
-d data/dataset.csv
```

Defines the **dependencies**.

These are the files required to execute the stage.

```text
-o data/processed.csv
```

Defines the **output**.

```text
python src/prepare.py
```

Defines the command that performs the transformation.

---

## 10. `dvc.yaml`

The previous command automatically creates/updates:

```text
dvc.yaml
```

It describes the pipeline.

Our pipeline is:

```yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
    - data/dataset.csv
    - src/prepare.py
    outs:
    - data/processed.csv
```

Meaning:

```text
cmd  → what to run
deps → what the stage depends on
outs → what the stage produces
```

Think of `dvc.yaml` as the **recipe for the data pipeline**.

---

## 11. Reproduce the Pipeline

```bash
dvc repro
```

Runs the DVC pipeline stages that need to be executed.

DVC checks the dependencies of each stage and determines whether something has changed.

If nothing relevant changed:

```text
Stage 'prepare' is up to date
```

DVC can skip the stage.

If a dependency changes:

```text
dataset.csv
     │
     │ changed
     ▼
dvc repro
     │
     ▼
prepare.py runs again
     │
     ▼
processed.csv regenerated
```

For example, when we changed `data/dataset.csv`, DVC detected the modified dependency and reran the `prepare` stage.

---

## 12. `dvc.lock`

Running `dvc repro` creates or updates:

```text
dvc.lock
```

`dvc.lock` records the **exact state of the pipeline**, including the hashes of its dependencies and outputs.

The important distinction is:

```text
dvc.yaml
    │
    └── describes HOW to produce the data
        (pipeline recipe)


dvc.lock
    │
    └── records WHICH exact versions/hashes
        were used for a specific pipeline state
```

### Example

Suppose:

```text
dataset.csv
     │
     ▼
prepare.py
     │
     ▼
processed.csv
```

We modify one line in `dataset.csv`.

The pipeline structure has not changed, so:

```text
dvc.yaml → stays the same
```

But the dataset content has changed, so its hash changes:

```text
old dataset hash
       ↓
   dataset changed
       ↓
new dataset hash
```

After:

```bash
dvc repro
```

DVC updates the pipeline state in `dvc.lock`.

The tracked dataset metadata in:

```text
data/dataset.csv.dvc
```

can also be updated to reflect the new dataset hash.

### Key idea

```text
dvc.yaml → What should happen?

dvc.lock → What exact data/state was used?

dvc repro → Make the pipeline reach that state.
```

---

# Git + DVC Together

The overall idea is:

```text
                    PROJECT
                       │
             ┌─────────┴─────────┐
             │                   │
            GIT                 DVC
             │                   │
      Code + metadata       Data + pipeline
             │                   │
          GitHub             DVC Remote
```

For example:

```bash
git add .
git commit -m "..."
git push
```

→ sends Git-tracked files to GitHub.

```bash
dvc push
```

→ sends DVC-tracked data to the DVC remote.

---

# Dataset Change Experiment

We also performed a small experiment to understand DVC's version tracking.

### Step 1 — Change the dataset

We modified a value in:

```text
data/dataset.csv
```

### Step 2 — Check the status

```bash
dvc status
```

DVC detected that the dataset dependency had changed.

It also detected that the tracked dataset's hash no longer matched the recorded version.

### Step 3 — Reproduce the pipeline

```bash
dvc repro
```

DVC:

```text
Detected dataset change
        │
        ▼
Reran prepare stage
        │
        ▼
Regenerated processed.csv
        │
        ▼
Updated dvc.lock
```

### What we learned

Changing the data does **not** change the pipeline recipe.

```text
dataset.csv changed
       │
       ├── dvc.yaml → unchanged
       │
       ├── dataset.csv.dvc → new dataset hash
       │
       └── dvc.lock → updated pipeline state
```

This demonstrates the difference between the **pipeline definition** and the **pipeline state**.

---

# Inspecting Previous Versions with Git

Because Git tracks files such as:

```text
dvc.yaml
dvc.lock
data/dataset.csv.dvc
```

we can inspect their previous versions.

Show the file from the current commit:

```bash
git show HEAD:data/dataset.csv.dvc
```

Show the file from the previous commit:

```bash
git show HEAD~1:data/dataset.csv.dvc
```

Show the file from two commits before:

```bash
git show HEAD~2:data/dataset.csv.dvc
```

The meaning is:

```text
HEAD~2       HEAD~1        HEAD
   │            │            │
   ▼            ▼            ▼
Commit A  →  Commit B  →  Commit C
```

This allows us to compare the dataset hashes recorded in different Git commits.

---

# Git vs DVC

```text
                    PROJECT
                       │
             ┌─────────┴─────────┐
             │                   │
            GIT                 DVC
             │                   │
             ▼                   ▼
      Code + metadata          Data
      dvc.yaml                 Dataset
      dvc.lock                 Models
      *.dvc files              Pipeline outputs
             │                   │
             ▼                   ▼
          GitHub             DVC Remote
```

Git and DVC work together:

```text
Git
 │
 ├── tracks code
 ├── tracks dvc.yaml
 ├── tracks dvc.lock
 └── tracks .dvc metadata
             │
             ▼
       identifies versions
             │
             ▼
DVC
 │
 ├── stores datasets
 ├── stores models
 ├── stores pipeline outputs
 └── reproduces pipelines
```

---

# Commands Learned So Far

| Command                  | What it does                             |
| ------------------------ | ---------------------------------------- |
| `git init`               | Initializes Git                          |
| `dvc init`               | Initializes DVC                          |
| `dvc add <file>`         | Tracks data with DVC                     |
| `dvc status`             | Checks DVC state                         |
| `dvc remote add`         | Adds a DVC remote                        |
| `dvc remote list`        | Lists DVC remotes                        |
| `dvc push`               | Uploads DVC data to the remote           |
| `dvc pull`               | Downloads DVC data from the remote       |
| `dvc stage add`          | Creates a pipeline stage                 |
| `dvc repro`              | Reproduces pipeline stages when needed   |
| `git show HEAD:<file>`   | Shows a file from the current Git commit |
| `git show HEAD~1:<file>` | Shows a file from the previous commit    |
| `git show HEAD~2:<file>` | Shows a file from two commits before     |

---

# The Main Idea

**Git tracks the project/code and DVC metadata.**

**DVC tracks the actual ML data and knows how to reproduce the data pipeline.**

The core workflow is:

```text
             CODE + PIPELINE DEFINITION
                       │
                       ▼
                  Git / GitHub
                       │
                       │
DATA ────────► DVC tracks hashes
                       │
                       ▼
                  DVC Remote
                       │
                       │
                       ▼
                 dvc repro
                       │
                       ▼
              Reproduce the pipeline
```

The three most important concepts learned are:

```text
dvc.yaml
   ↓
Defines the pipeline
"HOW should the data be produced?"


dvc.lock
   ↓
Records the exact pipeline state
"WHICH versions/hashes were used?"


dvc repro
   ↓
Reproduces the pipeline
"RUN the necessary stages again."
```

## Mental Model

Think of DVC as combining **data versioning + pipeline tracking + reproducibility**:

```text
              DVC
               │
       ┌───────┼────────┐
       │       │        │
       ▼       ▼        ▼
     DATA   PIPELINE  STATE
       │       │        │
   dvc add  dvc.yaml  dvc.lock
       │       │        │
       └───────┼────────┘
               │
               ▼
           dvc repro
               │
               ▼
        Reproducible ML
```
