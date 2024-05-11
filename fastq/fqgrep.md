# fqgrep

<p align="center">
  <a href="https://github.com/fulcrumgenomics/fqgrep/actions?query=workflow%3ACheck"><img src="https://github.com/fulcrumgenomics/fqgrep/workflows/Check/badge.svg" alt="Build Status"></a>
  <img src="https://img.shields.io/crates/l/fqgrep.svg" alt="license">
  <a href="https://crates.io/crates/fqgrep"><img src="https://img.shields.io/crates/v/fqgrep.svg?colorB=319e8c" alt="Version info"></a>
  <a href="http://bioconda.github.io/recipes/fqgrep/README.html"><img src="https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat" alt="Install with bioconda"></a>
  <br>
  Grep for FASTQ files.
</p>

Search a pair of fastq files for reads that match a given ref or alt sequence.

## Install

### From bioconda

```console
conda install -c bioconda fqgrep
```

### From Source

```console
git clone ... && cd fqgrep
cargo install --path .
```

## Usage

```console
fqgrep -r 'GACGAGATTA' -a 'GACGTGATTA' --r1-fastq /data/testR1.fastq.gz  --r2-fastq /data/testR2.fastq.gz -o ./test_out -t 28
```

## Help

See the following for usage:

```console
fqgrep -h
```
