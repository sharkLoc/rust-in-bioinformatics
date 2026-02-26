# cedar

[![CI](https://github.com/Ebedthan/cedar/actions/workflows/ci.yml/badge.svg)](https://github.com/Ebedthan/cedar/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Ebedthan/cedar/graph/badge.svg?token=S3OLFFHF4X)](https://codecov.io/gh/Ebedthan/cedar)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](https://github.com/Ebedthan/cedar/blob/main/LICENSE)


## 🗺️ Overview

`cedar` is a fast tool to build (rapid) neighbor-joining trees bases on mash distance.
It takes as input the sequences (FASTA and FASTQ files are welcomed, compressed or not), compute the sketches and output a newick file of the tree.

The main advantages of cedar over others tools are:
- It uses the innovative approach of sketching algorithm [finch](https://github.com/onecodex/finch-rs) which is fast, have adaptive, count-based filtering (for FASTQs) and strandedness filtering.
- Reliable and fast neighbor-joining tree estimation using [speedytree](https://docs.rs/speedytree/latest/speedytree/).

`cedar` outputs the tree in newick format.

## 🔧 Installing

```
git clone https://github.com/Ebedthan/cedar.git
cd cedar

# if default Rust install directory is ~/.cargo
cargo install --path . --root ~/.cargo
cedar -h
```

## 💡 Examples

```
# Compute rapid neighbor-joining tree of all files in a directory
cedar dir/*

# Compute rapid NJ tree using specific files
cedar file1.fa.gz file2.fq.xz file3.fna.bz2

# Compute canonical neighbor-joining tree
cedar -c dir/*
```
Full help is available from `cedar --help`;

### Minimum supported Rust version
`cedar` minimum [Rust](https://www.rust-lang.org/) version is 1.74.1.

### Semver
`cedar` is following [Semantic Versioning 2.0](https://semver.org/).

### Licence
`cedar` is distributed under the terms of the MIT license.
See [LICENSE-MIT](https://github.com/Ebedthan/cedar/blob/main/LICENSE-MIT) for details.

