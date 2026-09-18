# DVC Practice — Commands & Concepts

## 1. Initialize Git

```bash
git init
```

Creates a Git repository for the project.

**Purpose:** Git will track our code and DVC metadata.

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
Git  → tracks dataset.dvc
DVC  → tracks the actual dataset
```

The `.dvc` file contains metadata such as the dataset's hash and size.

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

Moves/syncs DVC-tracked data from the local DVC cache to the DVC remote.

```text
LOCAL
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
LOCAL
```

### Difference from Git

```text
git push  → GitHub
dvc push  → DVC remote

git pull  → GitHub
dvc pull  → DVC remote
```

Git and DVC manage different things.

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

Our current pipeline is:

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

# Commands Learned So Far

| Command           | What it does             |
| ----------------- | ------------------------ |
| `git init`        | Initializes Git          |
| `dvc init`        | Initializes DVC          |
| `dvc add <file>`  | Tracks data with DVC     |
| `dvc status`      | Checks DVC state         |
| `dvc remote add`  | Adds a DVC remote        |
| `dvc remote list` | Lists DVC remotes        |
| `dvc push`        | Uploads DVC data         |
| `dvc pull`        | Downloads DVC data       |
| `dvc stage add`   | Creates a pipeline stage |

## The main idea

**Git tracks the project/code and DVC metadata.**

**DVC tracks the actual ML data and knows how to reproduce the data pipeline.**

So:

```text
Git
 └── code + DVC metadata
          │
          ▼
       GitHub


DVC
 └── datasets + pipeline outputs
          │
          ▼
      DVC Remote
```
