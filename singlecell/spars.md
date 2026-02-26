[![Rust](https://github.com/stuart-lab/spars/actions/workflows/rust.yml/badge.svg)](https://github.com/stuart-lab/spars/actions/workflows/rust.yml)

# 💥 spars: disk-based sparse matrix tools

`spars` is a memory-efficient tool for working with sparse matrices in the [Matrix Market](https://math.nist.gov/MatrixMarket/formats.html) format on-disk.

## Usage

Subset a matrix on-disk:

```
spars subset -i <matrix.mtx> --rows <row_index.txt> --cols <col_index.txt> -o <matrix_subset.mtx>
```

Compute matrix statistics (nonzero count, sum, mean, variance, standard deviation, min, max) for each row and column:

```
spars stats -i <matrix.mtx> -o <filename>
```

## Installation

### From cargo

```
cargo install spars
```

### From GitHub

To compile, clone the git repo and run `cargo install`:

```
git clone git@github.com:stuart-lab/spars.git
cd spars; cargo install --path .
```

Precompiled binaries are also available in the release

## Man Pages

The tool includes man pages (documentation) that can be generated and installed after installation:

```bash
# generate manpages
spars generate-manpages --outdir /tmp/spars-man

# install man pages (requires sudo)
# note that this path may be different on different systems
sudo cp /tmp/spars-man/*.1 /usr/local/share/man/man1/

# on linux, update the manual page cache by running mandb
sudo mandb
```

Once installed, you can view the documentation with:

```bash
man spars         # main command documentation
man spars-stats   # stats subcommand
man spars-subset  # subset subcommand
```

Alternatively, you can view the man pages directly without installation:

```bash
man /tmp/spars-man/spars.1
```
