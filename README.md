# Solar Thermal Platform

This repository contains a Streamlit application for solar thermal analysis.

## Setup

1. Create or activate the virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

2. Run the app:
   ```powershell
   & ".\.venv\Scripts\python.exe" -m streamlit run app.py
   ```

## Notes

- Keep the virtual environment folders (`.venv`, `venv`) out of version control.
- The `requirements.txt` file lists the dependencies used by the project.
- Use the `Solar analysis` folder for the data files and analysis inputs.

## Git Commands

### Initialize repository
```powershell
git init
```

### Basic workflow
```powershell
git status
git add .
git commit -m "Describe your changes"
```

### Branching
```powershell
git checkout -b feature/<name>
# make changes
git add .
git commit -m "Add feature <name>"
```

### Updating from main
```powershell
git checkout main
git pull origin main
git checkout feature/<name>
git merge main
```

### Preparing a pull request
```powershell
git push origin feature/<name>
```

### Helpful cleanup
```powershell
git log --oneline --graph --decorate
git diff --staged
git diff
```

### Restore ignored or generated files
```powershell
git restore --staged <file>
```
