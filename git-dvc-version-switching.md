# Git + DVC Version Switching

One of the most useful features of using **Git and DVC together** is the ability to switch to an older project version and restore the data and pipeline state that belong to that version.

## The Problem

Git tracks things such as:

* Code
* `dvc.yaml`
* `dvc.lock`
* `params.yaml`

But Git does not directly store large DVC-managed files such as datasets and models.

So when switching to an older Git commit, the workspace can temporarily contain newer DVC outputs.

## The Solution

Use Git and DVC together:

```text
git checkout <old-commit>

        ↓
Restore old code + DVC metadata
        ↓
dvc checkout
        ↓
Restore matching DVC data and outputs
```

For example:

```bash
git checkout dc92202
dvc checkout
```

After `dvc checkout`, files such as:

```text
data/test.csv
models/model.pkl
```

are restored to the versions recorded for that Git commit.

## Why This Is Useful

Suppose the project evolved like this:

```text
Commit A
  dataset v1
  pipeline v1
  model v1

      ↓

Commit B
  dataset v2
  pipeline v2
  model v2
```

We can return to Commit A:

```bash
git checkout <commit-A>
dvc checkout
```

Now the code, pipeline definition, parameters, data, and DVC outputs correspond to that older project state.

## Important Distinction

`git checkout` and `dvc checkout` have different roles:

```text
git checkout
    ↓
changes Git-tracked project files

dvc checkout
    ↓
restores DVC-tracked data and outputs
```

Together:

```text
Git commit
     ↓
old project state
     ↓
DVC lock information
     ↓
matching data + model
```

## Reproducibility

This makes it possible to ask:

> **What data, code, parameters, pipeline, and model were associated with this project version?**

After restoring the version, `dvc repro` can also be used when we want to reproduce the pipeline computation from that state.

### Simple Mental Model

> **Git chooses the project version. DVC restores the data and artifacts belonging to that version.**
