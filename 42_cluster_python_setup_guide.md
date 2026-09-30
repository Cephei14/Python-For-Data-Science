# 42 Cluster Python Environment Setup Guide

This guide provides the exact commands needed to set up, configure, and verify your Python development environment on 42 cluster computers using `goinfre` and `venv` without `sudo` access.

---

## 1. Setup & Installation Commands

Execute the following commands in your terminal to set up the virtual environment and install all necessary dependencies:

```bash
# 1. Navigate to your project inside goinfre
cd ~/goinfre/Python_for_Data_Science

# 2. Clean up any existing virtual environment folder
rm -rf .venv

# 3. Create a fresh virtual environment
python3 -m venv .venv

# 4. Activate the virtual environment
source .venv/bin/activate

# 5. Upgrade pip inside .venv
python -m pip install --upgrade pip

# 6. Install all required dependencies
pip install numpy pandas matplotlib seaborn pillow flake8 build setuptools wheel

# 7. Configure norminette alias for flake8
alias norminette=flake8

# 8. Ensure .venv is ignored by Git
echo ".venv/" >> .gitignore
```

---

## 2. Environment Verification

Run this verification block to test your Python version, environment path, package installations, and tools setup:

```bash
python - <<'EOF'
import sys, importlib
print(f"Python {sys.version.split()[0]}:", "OK" if sys.version_info >= (3, 10) else "TOO OLD (need >= 3.10)")
print("venv active:", "OK" if sys.prefix != sys.base_prefix else "NO, activate .venv")
print("venv location:", sys.prefix, "(should be inside goinfre)")
mods = {"numpy": "numpy", "pandas": "pandas", "matplotlib": "matplotlib",
        "seaborn": "seaborn", "PIL": "pillow", "flake8": "flake8",
        "build": "build", "setuptools": "setuptools", "wheel": "wheel",
        "tkinter": "sudo apt install python3-tk"}
for m, pkg in mods.items():
    try:
        mod = importlib.import_module(m)
        print(f"[OK]      {m} {getattr(mod, '__version__', '')}")
    except ImportError:
        print(f"[MISSING] {m}  ->  {pkg if ' ' in pkg else 'pip install ' + pkg}")
EOF
command -v git >/dev/null && echo "[OK]      git" || echo "[MISSING] git"
python -m flake8 --version | head -1
python -m build --version
type norminette 2>/dev/null || echo "[MISSING] norminette alias (add: alias norminette=flake8 to ~/.bashrc)"
```

---

## 3. Daily Workflow

Every time you log into a cluster computer or open a new terminal tab, reactivate your environment with:

```bash
cd ~/goinfre/Python_for_Data_Science
source .venv/bin/activate
```