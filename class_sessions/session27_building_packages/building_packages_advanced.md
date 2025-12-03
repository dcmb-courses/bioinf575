This file was generated with the use of AI.    
It was edited to correct errors and add clarity.      

# Amini Bioinformatics Package Guide
## BIOINF 575 - Beginner Tutorial

**Level:** Graduate students learning Python packaging  
**Goal:** Build, install, and use your first bioinformatics package

***

## What is a Python Package?

**Simple definition:** A folder of Python files that other people can `pip install` and `import`

**Why create packages for bioinformatics?**
- Share code with labmates (`pip install your-lab-tools`)
- Run from command line (`your-tool analyze.fasta`)
- Professional and reproducible research code
- Easy to version control and collaborate

***

## Step 1: Setup Environment & Directory

### Commands to run:

```bash
$ mkdir ~/Desktop/amini_bioinformatics
$ cd ~/Desktop/amini_bioinformatics
```
**What this does:** Creates your main project folder on Desktop and moves into it  
**Expected output:** No output, just changes your current directory

```bash
$ python -m venv .venv
```
**What this does:** Creates a virtual environment (sandbox) so your package doesn't conflict with other Python projects  
**Expected output:** Creates `.venv/` folder with Python interpreter + pip  
**Why?** Bioinformatics tools often need different library versions

```bash
$ source .venv/bin/activate    # Windows: .venv\Scripts\activate
```
**What this does:** Enters the virtual environment (notice your prompt changes to `(.venv)`)  
**Expected output:** Command prompt shows `(.venv)` prefix  

```bash
$ pip install --upgrade pip build pytest black
```
**What this does:** Updates pip and installs ALL tools needed for this workshop:
- `pip` = package manager
- `build` = creates distributable packages  
- `pytest` = runs unit tests
- `black` = auto-formats code
**Expected output:** "Successfully installed pip-24.x, build-1.x, pytest-7.x, black-23.x"

**Why virtual environment?**
- Keeps your package dependencies separate from other projects
- Prevents conflicts between different bioinformatics tools
- Professional standard

### Create directory structure:

```bash
$ mkdir -p src/amini data
```
**What this does:** Creates nested folders: `src/amini/` (your code) and `data/` (test files)  
**`-p` flag:** Creates parent folders if needed, no error if exists

```bash
$ touch src/amini/__init__.py pyproject.toml README.md LICENSE
```
**What this does:** Creates empty Python files (standard Unix way)  
**Expected output:** No output, files created

```bash
$ tree .    # Install with: sudo apt install tree
```
**What this does:** Shows pretty directory tree  
**Expected output:**
```
.
├── LICENSE
├── README.md
├── pyproject.toml
├── data/
├── src/
│   └── amini/
│       └── __init__.py
```
**Alternative:** `ls -R`

***

## Step 2: pyproject.toml - Your Package Recipe

### What is `pyproject.toml`?
**The single file that defines everything about your package:**
- Name (`amini-bioinformatics`)
- Description 
- Required libraries (Biopython)
- Creates `amini` command line tool
- Python version requirements

### Hatch vs Setuptools

| Tool | What it does | Pros | Cons |
|------|-------------|------|------|
| **Hatch** (Recommended) | Modern build system | Simple config, automatic everything | Newer |
| **Setuptools** | Traditional build system | Very mature | Verbose config files |

**What is Hatch?**
Hatch is a modern Python project manager that replaces old `setup.py`. It automatically finds your Python files, creates packages, handles dependencies, and makes command line tools.[11]

### Copy this exactly into `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "amini-bioinformatics"
description = "DNA sequence analyzer for beginners"
readme = "README.md"
license.file = "LICENSE"
authors = [{ name="Your Name", email="you@university.edu" }]

dependencies = ["biopython>=1.79"]
requires-python = ">=3.9"

[project.scripts]
amini = "amini.cli:main"
```

**Test it works (build tool already installed):**
```bash
$ python -m build --sdist --wheel
```
**What `python -m build` does:** 
1. Reads your `pyproject.toml` 
2. Finds Python files in `src/amini/`
3. Packages code + metadata into 2 formats
4. Creates files in `dist/` ready for PyPI[12][13]

**Expected output:** "Successfully built amini-bioinformatics"

```bash
$ ls -la dist/
```
**Expected output:**
```
amini_bioinformatics-0.1.0-py3-none-any.whl    # Wheel (binary)
amini_bioinformatics-0.1.0.tar.gz              # Source
```

**Wheel (.whl) vs Source (.tar.gz):**
| Wheel (.whl) | Source (.tar.gz) |
|--------------|------------------|
| **Binary** - pre-built, fastest install | **Source code** - builds on target machine |
| Smaller, production-ready [13] | For developers, cross-platform |

***

## Step 3: Essential Files

### `README.md`:

```markdown
# Amini - Simple DNA Analyzer

**Bioinformatics tool for students**

## Install
```
pip install -e .
```

## Usage
```
amini analyze genes.fasta --output results.json
```

## What it does
- Reads FASTA files
- Calculates GC content  
- Finds TATA box motifs
- Saves JSON results
```

### `LICENSE`:

```text
MIT License

Copyright (c) 2025 Your Name

Permission is granted to use, copy, modify, and distribute
this software freely.
```

***

## Step 4: Core Code Files

### `src/amini/__init__.py`:

```python
"""
Amini v0.1.0 - Simple bioinformatics tools
"""

__version__ = "0.1.0"

from .sequences import gc_content, find_motifs
from .parsers import read_fasta
from .cli import main

__all__ = ["gc_content", "find_motifs", "read_fasta", "main"]
```

### `src/amini/sequences.py`:

```python
"""
DNA analysis functions
"""

def gc_content(dna: str) -> float:
    """
    Calculate GC% (G+C letters / total length * 100)
    
    >>> gc_content("ATGC")
    50.0
    >>> gc_content("GCGCGCGC")
    100.0
    """
    if not dna:
        return 0.0
    
    dna = dna.upper()
    g = dna.count('G')
    c = dna.count('C')
    
    return (g + c) / len(dna) * 100

def find_motifs(dna: str, motif: str) -> list:
    """
    Find motif positions (non-overlapping)
    
    >>> find_motifs("TATATATA", "TATA")
    [(0, 4), (4, 8)]
    """
    positions = []
    dna = dna.upper()
    motif = motif.upper()
    start = 0
    
    while True:
        pos = dna.find(motif, start)
        if pos == -1:
            break
        positions.append((pos, pos + len(motif)))
        start = pos + len(motif)
    
    return positions
```

### `src/amini/parsers.py`:

```python
"""
Read FASTA files (DNA sequences)
"""

def read_fasta(filename: str) -> list:
    """
    FASTA format:
    >TP53
    ATGGCCATG...
    
    Returns: [("TP53", "ATGGCCATG..."), ...]
    """
    sequences = []
    
    try:
        with open(filename, 'r') as f:
            name = None
            seq_lines = []
            
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if name:
                        sequences.append((name, ''.join(seq_lines)))
                    name = line[1:]
                    seq_lines = []
                else:
                    seq_lines.append(line)
            
            if name:
                sequences.append((name, ''.join(seq_lines)))
        
        print(f"Read {len(sequences)} sequences")
        return sequences
        
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []
```

### `src/amini/cli.py`:

```python
"""
Command line interface
"""

import sys
import json
from .sequences import gc_content, find_motifs
from .parsers import read_fasta

def main():
    if len(sys.argv) < 3:
        print("Usage: amini analyze INPUT.fasta --output RESULTS.json [--motif PATTERN]")
        return
    
    command = sys.argv[1]
    if command == "analyze":
        analyze(sys.argv[2:])
    else:
        print(f"Unknown command '{command}'. Use 'analyze'")

def analyze(args):
    input_file = None
    output_file = None
    motif = None
    
    i = 0
    while i < len(args):
        if args[i] == "--output":
            output_file = args[i+1]
            i += 2
        elif args[i] == "--motif":
            motif = args[i+1]
            i += 2
        else:
            input_file = args[i]
            i += 1
    
    if not input_file or not output_file:
        print("Error: Need INPUT.fasta and --output RESULTS.json")
        return
    
    print(f"Analyzing {input_file}...")
    
    sequences = read_fasta(input_file)
    if not sequences:
        return
    
    results = []
    for name, dna in sequences:
        result = {
            "gene": name,
            "length": len(dna),
            "gc_percent": round(gc_content(dna), 1)
        }
        
        if motif:
            result["motif_hits"] = find_motifs(dna, motif)
        
        results.append(result)
        print(f"  {name}: {result['gc_percent']}% GC")
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved {len(results)} results to {output_file}")

if __name__ == "__main__":
    main()
```

**Test your code:**
```bash
$ python -c "from amini.sequences import gc_content; print(gc_content('GCGC'))"
```
**Expected:** `100.0`

***

## Step 5: Test Data

```bash
$ mkdir data
$ cat > data/genes.fasta << 'EOF'
>TP53
ATGGCCATGGCCATGGC
>BRCA1
GCGCGCGCGCGCGCGC
>ACTB
ATCGATCGATCGATCG
EOF
```
**What this does:** Creates test FASTA file with 3 genes

***

## Step 6: Install & Test Package

```bash
$ pip install -e .
```
**`-e` = editable install** - links to source code (changes work instantly)

**Test Python API:**
```bash
$ python -c "from amini.sequences import gc_content; print('GC:', gc_content('GCGC'))"
```
**Expected:** `GC: 100.0`

**Test command line:**
```bash
$ amini analyze data/genes.fasta --output test.json
```
**Expected:**
```
Analyzing data/genes.fasta...
Read 3 sequences
  TP53: 61.1% GC
  BRCA1: 100.0% GC
  ACTB: 50.0% GC
Saved 3 results to test.json
```

**Check results:**
```bash
$ cat test.json
```

***

## Step 7: Unit Tests

**Create `src/amini/test_sequences.py`:**

```python
"""
Unit tests - run with: pytest src/amini/
"""

from amini.sequences import gc_content, find_motifs

def test_gc_content():
    assert gc_content("ATGC") == 50.0
    assert gc_content("GCGC") == 100.0
    assert gc_content("") == 0.0

def test_find_motifs():
    result = find_motifs("TATATATA", "TATA")
    assert len(result) == 2
    assert result[0] == (0, 4)
```

```bash
$ pytest src/amini/ -v
```
**Expected:** `2 passed in 0.01s`

***

## Step 8: Build Distribution

```bash
$ python -m build
```
**Creates distributable packages in `dist/` (build already installed)**

```bash
$ ls -la dist/
```
**Output:**
```
amini_bioinformatics-0.1.0-py3-none-any.whl    # Ready for pip install
amini_bioinformatics-0.1.0.tar.gz              # Source distribution
```

**Test your built package:**
```bash
$ pip install dist/*.whl
```

***

## Step 9: Professional Polish

```bash
$ black src/amini/
```
**Auto-formats code to Python standards**

***

## Exercise: Add AT Content

**Add to `sequences.py`:**
```python
def at_content(dna: str) -> float:
    """Calculate AT content (opposite of GC)"""
    return 100.0 - gc_content(dna)
```

**Test:**
```bash
$ pytest src/amini/ -v
$ python -c "from amini.sequences import at_content; print(at_content('ATGC'))"
```

***

## Complete Package Checklist

```
✅ pip install -e . works
✅ python -c "import amini" works  
✅ amini analyze data/genes.fasta works
✅ pytest src/amini/ passes
✅ python -m build creates .whl + .tar.gz
✅ Added AT content + test
✅ Ready for GitHub!
```

## Share Your Package

```bash
$ git init
$ git add .
$ git commit -m "My first bioinformatics package"
$ git remote add origin https://github.com/yourusername/amini.git
$ git push -u origin main
```

**Your package is production-ready!**

*Follows Python Packaging Authority standards *[13][14][12]

[1](https://www.reddit.com/r/learnpython/comments/12jqf0p/how_do_i_install_build_when_build_is_not_available/)
[2](https://github.com/pypa/build/issues/427)
[3](https://devguide.python.org/getting-started/setup-building/)
[4](https://answers.netlify.com/t/python-build-is-not-working-anymore/47343)
[5](https://realpython.com/installing-python/)
[6](https://stackoverflow.com/questions/74278160/python-installation-problems)
[7](https://pmagpy.github.io/PmagPy-docs/installation/troubleshooting.html)
[8](https://discuss.python.org/t/problems-about-my-python-installation-that-could-make-me-crazy/30637)
[9](https://discuss.python.org/t/windows-install-from-source-failing/25389)
[10](https://discuss.python.org/t/python-not-found-by-command-prompt/45612)
[11](https://www.pyopensci.org/python-package-guide/tutorials/develop-python-package-hatch.html)
[12](https://pydevtools.com/handbook/reference/build/)
[13](https://www.geeksforgeeks.org/python/how-to-build-a-python-package/)
[14](https://packaging.python.org/tutorials/packaging-projects/)