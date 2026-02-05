# HyperEx 🔬🧬

[![CI Status](https://img.shields.io/github/actions/workflow/status/Ebedthan/hyperex/ci.yml?style=flat&logo=github)](https://github.com/Ebedthan/hyperex/actions)
[![Crates.io](https://img.shields.io/crates/v/hyperex?logo=rust)](https://crates.io/crates/hyperex)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![Code Coverage](https://codecov.io/gh/Ebedthan/hyperex/branch/main/graph/badge.svg)](https://codecov.io/gh/Ebedthan/hyperex)

<p align="center">
  <img src="img/hyperex.png" width="300" alt="HyperEx Logo">
</p>

**HyperEx** (Hypervariable region Extractor) is a high-performance tool for precise extraction of 16S rRNA hypervariable regions using primer-based approaches. Built in Rust for speed and reliability.

## Features ✨

- 🧬 Built-in universal 16S primer sequences
- 🔍 Supports IUPAC ambiguity codes in primers
- ⚡ Multi-threaded processing for large datasets
- 📁 Handles compressed inputs (gzip, xz, bzip2)
- 📊 Generates both FASTA and GFF3 outputs
- 🎯 Configurable mismatch tolerance

## Installation 📦

### Quick Install (via Cargo)

```bash
cargo install hyperex
```

### Prebuilt Binaries
Download from our Releases Page

### Download from Source

```bash
git clone https://github.com/Ebedthan/hyperex.git
cd hyperex
cargo install --path .
```

## Usage 🚀
### Basic Extraction

```bash
hyperex input.fasta
```

### Extract Specific Regions
```bash
hyperex --region v3v4 --region v4v5 input.fasta
```

### Custom Primers
```bash
hyperex -f CCTACGGGNGGCWGCAG -r GGACTACHVGGGTWTCTAAT input.fasta
```

### With Mismatches
```bash
hyperex --region v1v2 --mismatch 2 input.fasta
```

## Advanced Options ⚙️

| Option | Description |
|--------|-------------|
| **-f, --forward-primer** |	Forward primer sequence (IUPAC supported) |
| **-r, --reverse-primer** |	Reverse primer sequence (IUPAC supported) |
| **--region** | 	Predefined region (v1v2, v3v4, etc.) or primer file |
| **-m, --mismatch** |	Allowed mismatches (default: 0) |
| **-p, --prefix** |	Output file prefix (default: hyperex_out) |
| **--force**	| Overwrite existing files |
| **-q, --quiet** |	Reduce verbosity |


## Primer File Format 📝

Create a CSV file with primer pairs:

```
FORWARD_1,REVERSE_1
FORWARD_2,REVERSE_2
...
```
## Examples 🧪

Multiple regions from compressed input:

```bash
xzcat big_file.fa.xz | hyperex --region v1v2 --region v3v4 -p results
```
Custom primers with 1 mismatch:

```bash
hyperex -f ATCG -r GGCC -m 1 input.fasta
```

## Requirements ✅
 - Rust 1.60+ (for source builds)
 - Compression libraries (optional for compressed inputs):
 - libz (gzip)
 - liblzma (xz)
 - libbz2 (bzip2)


## Support 🆘
Found an issue? File it on our Issue Tracker.

