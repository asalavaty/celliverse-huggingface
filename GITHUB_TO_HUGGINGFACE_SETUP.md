# GitHub → Hugging Face automatic deployment setup

This repository can be used as the source of truth for the CelliVerse Hugging Face Space.

## Recommended repository names

GitHub repository:

```text
celliverse-huggingface
```

Hugging Face Space:

```text
celliverse
```

or, if unavailable:

```text
celliverse-clustocell-demo
```

## Step 1: Create the GitHub repository

Create a new GitHub repository, for example:

```text
asalavaty/celliverse-huggingface
```

Keep it public if you want the Space code to be fully visible. Private is also fine if you prefer.

## Step 2: Add the files

Add all files from this template to the GitHub repository, including:

```text
app.py
requirements.txt
README.md
assets/celliverse_logo.png
data/
scripts/
.github/workflows/sync-to-huggingface.yml
```

## Step 3: Create the Hugging Face Space

Create a Hugging Face Space using:

```text
SDK: Gradio
Visibility: Public
License: GPL-3.0
Hardware: CPU basic
```

## Step 4: Create a Hugging Face access token

In Hugging Face:

```text
Settings → Access Tokens → Create new token
```

Create a token with write access to the target Space.

## Step 5: Add the token to GitHub

In GitHub:

```text
Repository → Settings → Secrets and variables → Actions → New repository secret
```

Name the secret exactly:

```text
HF_TOKEN
```

Paste your Hugging Face token as the value.

## Step 6: Edit the workflow file

Open:

```text
.github/workflows/sync-to-huggingface.yml
```

Replace this line:

```yaml
huggingface_repo_id: YOUR_HF_USERNAME/YOUR_SPACE_NAME
```

with your real Hugging Face Space ID, for example:

```yaml
huggingface_repo_id: asalavaty/celliverse
```

or:

```yaml
huggingface_repo_id: asalavaty/celliverse-clustocell-demo
```

## Step 7: Push to GitHub

```bash
git add .
git commit -m "Initial CelliVerse Hugging Face Space"
git push origin main
```

The GitHub Action should then sync the repository contents to your Hugging Face Space.

## Notes

- The Hugging Face Hub itself is also Git-based and version-controlled.
- GitHub Actions syncing is useful if you prefer GitHub as your main development home.
- Files larger than 10 MB may need Git LFS.
- The official Hugging Face sync action mirrors files from GitHub to the Hub. It is not a true git-to-git sync.
