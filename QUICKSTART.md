# Quickstart

## Clone the Repository

```bash
git clone https://github.com/trewise/paraview-dynamic-attractor-explorer.git
cd paraview-dynamic-attractor-explorer
```

## Linux/macOS Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Windows PowerShell Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Generate Data

```bash
python scripts/build/generate_all.py
```

## Verify Outputs

```bash
python tools/validate_dataset.py
```
