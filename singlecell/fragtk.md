[![Rust](https://github.com/stuart-lab/fragtk/actions/workflows/rust.yml/badge.svg)](https://github.com/stuart-lab/fragtk/actions/workflows/rust.yml)

# fragtk: fragment file toolkit

`fragtk` is a fast and efficient toolkit implemented in Rust for working with fragment files.

To install `fragtk`, please see the [installation](#installation) section below.

## Usage

### Create region x cell matrix

A region x cell matrix can be created from a fragment file and a peak file:

```
fragtk matrix -f <fragments.tsv.gz> -b <peaks.bed> -c <cells.txt> -o <output>
```

### Count fragments per cell barcode

Select cell barcodes from the fragment file according to their total count:

```
fragtk count -f <fragments.tsv.gz> -o <barcode_counts.tsv> -t <threshold> > barcodes.txt
```

### Filter fragments

Filter fragments according to the cell barcodes:

```
fragtk filter -f <fragments.tsv.gz> -c <barcodes.txt> | bgzip -c > filtered.tsv.gz
```

### Compute QC metrics

Compute scATAC-seq quality control metrics per cell:

```
fragtk qc -f <fragments.tsv.gz> -o <outfile.tsv.gz> <--gff <genes.gff3.gz> |--bed <tss.bed.gz>>
```

## Installation

### Using cargo

```
cargo install fragtk
```

### From GitHub

```
git clone git@github.com:stuart-lab/fragtk.git
cd fragtk; cargo install --path .
```

Pre-compiled binaries are also available in the release.

## Man Pages

The tool includes man pages (documentation) that can be generated and installed after installation:

```bash
# generate manpages
fragtk generate-manpages --outdir /tmp/fragtk-man

# install man pages (requires sudo)
# note that this path may be different on different systems
sudo cp /tmp/fragtk-man/*.1 /usr/local/share/man/man1/

# on linux, update the manual page cache by running mandb
sudo mandb
```

Once installed, you can view the documentation with:

```bash
man fragtk # main command documentation
man fragtk-matrix # matrix subcommand documentation
man fragtk-count # count subcommand documentation
man fragtk-filter # filter subcommand documentation
```

Alternatively, you can view the man pages directly without installation:

```bash
man /tmp/fragtk-man/fragtk.1
```
