# kmertools: DNA Vectorisation Tool

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Cargo tests](https://github.com/anuradhawick/kmertools/actions/workflows/rust_test.yml/badge.svg)](https://github.com/anuradhawick/kmertools/actions/workflows/rust_test.yml)
[![Clippy check](https://github.com/anuradhawick/kmertools/actions/workflows/clippy_check.yml/badge.svg)](https://github.com/anuradhawick/kmertools/actions/workflows/clippy_check.yml)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/kmertools/README.html)
[![Conda - Version](https://img.shields.io/conda/v/bioconda/kmertools)](https://anaconda.org/bioconda/kmertools)
[![Conda Downloads](https://img.shields.io/conda/dn/bioconda/kmertools)](https://anaconda.org/bioconda/kmertools)
[![PyPI Downloads](https://static.pepy.tech/badge/pykmertools)](https://pepy.tech/projects/pykmertools)
[![codecov](https://codecov.io/gh/anuradhawick/kmertools/graph/badge.svg?token=IDGRE54SSQ)](https://codecov.io/gh/anuradhawick/kmertools)
[![PyPI - Version](https://img.shields.io/pypi/v/pykmertools)](https://pypi.org/project/pykmertools/)

<div align="center">
<pre>
$$\   $$\                                   $$$$$$$$\                     $$\           
$$ | $$  |                                  \__$$  __|                    $$ |          
$$ |$$  / $$$$$$\$$$$\   $$$$$$\   $$$$$$\     $$ |    $$$$$$\   $$$$$$\  $$ | $$$$$$$\ 
$$$$$  /  $$  _$$  _$$\ $$  __$$\ $$  __$$\    $$ |   $$  __$$\ $$  __$$\ $$ |$$  _____|
$$  $$<   $$ / $$ / $$ |$$$$$$$$ |$$ |  \__|   $$ |   $$ /  $$ |$$ /  $$ |$$ |\$$$$$$\  
$$ |\$$\  $$ | $$ | $$ |$$   ____|$$ |         $$ |   $$ |  $$ |$$ |  $$ |$$ | \____$$\ 
$$ | \$$\ $$ | $$ | $$ |\$$$$$$$\ $$ |         $$ |   \$$$$$$  |\$$$$$$  |$$ |$$$$$$$  |
\__|  \__|\__| \__| \__| \_______|\__|         \__|    \______/  \______/ \__|\_______/ 
</pre>
</div>
                                                         
## Overview

`kmertools` is a k-mer based feature extraction tool designed to support metagenomics and other bioinformatics analytics. This tool leverages k-mer analysis to vectorize DNA sequences, facilitating the use of these vectors in various AI/ML applications.

<div align="center">
<a href="https://www.star-history.com/#anuradhawick/kmertools&Date">
  <img width="600px" src="https://api.star-history.com/svg?repos=anuradhawick/kmertools&type=Date" alt="Star History Chart">
</a>
</div>

## Features

- **Oligonucleotide Frequency Vectors:** Generate frequency vectors for oligonucleotides.
- **Minimiser Binning:** Efficiently bin sequences using minimisers to reduce data complexity.
- **Chaos Game Representation (CGR):** Compute CGR vectors for DNA sequences based on k-mers or whole sequence transformation.
- **Coverage Histograms:** Create coverage histograms to analyze the depth of sequencing reads.
- **Python Binding:** You can import kmertools functionality using `import pykmertools as kt`

## Installation

### Option 1: from bioconda (recommended)

You can install `kmertools` from Bioconda at https://anaconda.org/bioconda/kmertools. Make sure you have [conda](https://docs.conda.io/en/latest/) installed.

```bash
# create conda environment and install kmertools
conda create -n kmertools -c bioconda kmertools

# activate environment
conda activate kmertools
```

### Option 2: from PyPI

You can install `kmertools` from PyPI at https://pypi.org/project/pykmertools/.

```bash
pip install pykmertools
```

### Option 3: from sources

You can install `kmertools` directly from the source by cloning the repository and using Rust's package manager `cargo`.

```bash
git clone https://github.com/your-repository/kmertools.git
cd kmertools
cargo build --release
```

Now add the binary to path (you may modify `~/.bashrc` or `~/.zshrc`)

```sh
# to add to current terminal
export PATH=$PATH:$(pwd)/target/release/

# to save to ~/.bashrc
echo "export PATH=\$PATH:$(pwd)/target/release/" >> ~/.bashrc
source ~/.bashrc

# to save to ~/.zshrc for Mac
echo "export PATH=\$PATH:$(pwd)/target/release/" >> ~/.zshrc
source ~/.zshrc
```

To install the python bindings run the following commands. You can use either pip or conda directories for this.

```bash
# pip
cd pip
maturin build --release
# conda
cd conda
maturin build --release
```

Now move to parent directory using `cd ..` and run the following command.

```bash
pip install target/wheels/pykmertools-<VERSION>-cp39-abi3-manylinux_2_34_x86_64.whl
```

## Test the installation

After setting up, run the following command to print out the `kmertools` help message.

```bash
kmertools --help
```

## Help

Please read our comprehensive [Wiki](https://github.com/anuradhawick/kmertools/wiki).

## Authors

- Anuradha Wickramarachchi [https://anuradhawick.com](https://anuradhawick.com)
- Vijini Mallawaarachchi [https://vijinimallawaarachchi.com](https://vijinimallawaarachchi.com)

## Citation

If you use `kmertools` please cite as follows.

```bib
@software{Wickramarachchi_kmertools_DNA_Vectorisation,
  author = {Wickramarachchi, Anuradha and Mallawaarachchi, Vijini},
  title = {{kmertools: DNA Vectorisation Tool}},
  url = {https://github.com/anuradhawick/kmertools},
  version = {0.1.4}
}
```

Please refer to the [Wiki](https://github.com/anuradhawick/kmertools/wiki) for citations of relevant algorithms.

## Support and contributions

Please get in touch via author websites or GitHub issues. Thanks!

