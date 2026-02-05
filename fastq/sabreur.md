# sabreur

<p align="center">
  <a href="https://github.com/Ebedthan/sabreur/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/Ebedthan/sabreur/actions/workflows/ci.yml/badge.svg">
  </a>
  <a href="https://codecov.io/gh/Ebedthan/sabreur">
    <img alt="Coverage" src="https://codecov.io/gh/Ebedthan/sabreur/branch/main/graph/badge.svg">
  </a>
  <a href="https://github.com/Ebedthan/sabreur">
    <img alt="Rust version" src="https://img.shields.io/badge/rust-1.78.0%2B-blue.svg?maxAge=3600">
  </a>
  <a href="https://github.com/Ebedthan/sabreur/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-blue?style=flat">
  </a>
</p>

<p align="center">
  <img src="img/sabreur.png" alt="sabreur logo" width="150">
</p>

## 🔎 About

**sabreur** is a command-line tool designed to **demultiplex barcoded sequencing reads** into separate files. It supports:

- **FASTA** and **FASTQ** formats
- **Compressed inputs and outputs**: `gzip`, `bzip2`, `xz`, and `zstd`
- **Paired-end** and **Single-end** reads

It uses a barcode file to match reads and dispatches each to the corresponding output. Reads with unknown barcodes go into a separate file.

Powered by [niffler](https://github.com/luizirber/niffler) for seamless compression support.

## 🚀 Usage

### ▶️ Paired-end mode

```bash
sabreur barcode.txt input_R1.fq.gz input_R2.fq.gz
```
### ▶️ Single-end mode
```bash
sabreur barcode.txt input.fq
```

sabreur automatically detects the format and compression. Just provide the inputs!

## ⚙️ Command-Line Options
```
USAGE:
    sabreur [options] <BARCODE> <FORWARD FILE> [<REVERSE FILE>]

ARGS:
    <BARCODE>    input barcode file
    <FORWARD>    input forward fastx file
    <REVERSE>    input reverse fastx file

OPTIONS:
    -m, --mismatch <INT>    maximum number of mismatches [default: 0]
    -o, --out <DIR>         ouput directory [default: sabreur_out]
    -f, --format <STR>      output files compression format
    -l, --level <INT>       compression level [default: 1]
        --force             force reuse of output directory
    -q, --quiet             decrease program verbosity
    -h, --help              Print help information
    -V, --version           Print version information

```

## 📦 Installation

### Requirements
- [Rust](https://rust-lang.org) in stable channel
- libgz for gz file support
- liblzma for xz file support
- libbzip2 for bzip2 file support
- zstd for zstd file support

### 🛠️ From Source (via Cargo)

```bash
git clone https://github.com/Ebedthan/sabreur.git
cd sabreur
cargo install --path . --root ~/.cargo
sabreur --help
```

### 📁 Prebuilt Binaries

Download binaries for your platform from the [releases page](https://github.com/Ebedthan/sabreur/releases):

* macOS (Apple Silicon): [Download](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-aarch64-apple-darwin.tar.xz) • [Checksum](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-aarch64-apple-darwin.tar.xz.sh256)
* macOS (Intel): [Download](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-apple-darwin.tar.xz) • [Checksum](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-apple-darwin.tar.xz.sha256)
* Linux (x86\_64): [Download](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-unknown-linux-gnu.tar.xz) • [Checksum](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-unknown-linux-gnu.tar.xz.sha256)
* Windows (x86\_64): [Download](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-pc-windows-msvc.zip) • [Checksum](https://github.com/Ebedthan/sabreur/releases/download/v0.7.0/sabreur-v0.7.0-x86_64-pc-windows-msvc.zip.sha256)

## Benchmark

Benchmarked with [hyperfine](https://github.com/sharkdp/hyperfine) [dataset](https://figshare.com/articles/dataset/Paired-end_fastq_files_for_demultiplexing/14701629).


| Tool  | Single-end uncompressed output | Single-end compressed output | Paired-end uncompressed output | Paired-end compressed output |
| :---  |             :----:             |             :----:           |              :----:           |              :----:           |
| [idemp](https://github.com/yhwu/idemp) | - | 211.571 ± 3.718 | -      | 366.247 ± 10.482  |
| [sabre](https://github.com/najoshi/sabre) | 32.911 ± 2.411 | - | 109.470 ± 49.909 | -     |
| **sabreur** | 10.843 ± 0.531| 93.840 ± 0.446    | 40.878 ± 13.743     | 187.533 ± 0.572   |


### 🗜️ Compression format performance

A simple benchmark of the different compression format (`sabreur tests/bc_pe_fq.txt tests/input_R1.fastq.gz tests/input_R2.fastq.gz`), zst being the fastest.

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `--format zst` | 43.096 ± 1.547 | 41.179 | 46.878 | 1.00 |
| `--format bz2` | 94.049 ± 4.762 | 87.984 | 101.140 | 2.18 ± 0.14 |
| `--format gz` | 123.107 ± 1.748 | 120.529 | 125.166 | 2.86 ± 0.11 |
| `--format xz` | 285.692 ± 18.625 | 264.960 | 325.750 | 6.63 ± 0.49 |


## 📄 Barcode File Format

The barcode file must be tab-delimited in the format:

```
barcode1    barcode1_file1.fq   barcode1_file2.fq
barcode2    barcode2_file1.fq   barcode2_file2.fq
...
```

Output filenames must be unique. You can use .fq, .fastq, .fa, or .fasta as extensions.

### Minimum supported Rust version
`sabreur` minimum [Rust](https://www.rust-lang.org/) version is 1.78.0.

## 🤝 Contributing

- Contributions are welcome under the [Contributor Code of Conduct](https://github.com/Ebedthan/sabreur/blob/main/CODE_OF_CONDUCT.md).
- Please open an [issue or pull request on GitHub](https://github.com/Ebedthan/sabreur/issues).

## 🐛 Bugs & Support

Found a bug or have a feature request? → [Open an issue](https://github.com/Ebedthan/sabreur/issues).

## 📜 License
This project is licensed under the MIT License.

