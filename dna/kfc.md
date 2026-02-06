# KFC

![tests](https://github.com/lrobidou/KFC/workflows/tests/badge.svg)
[![license](https://img.shields.io/badge/license-AGPL-purple)](https://github.com/lrobidou/KFC//blob/main/LICENSE)

<p align="center"><img src="https://github.com/user-attachments/assets/b56db9a5-e755-4af9-a28d-6a787c71b3a9" width="180" alt="KFC logo"></p>

KFC (**K**-mer **F**ast **C**ounter) is a fast and space-efficient *k*-mer counter based on hyper-*k*-mers.

It is particularly well-suited for counting large *k*-mers (with *k* ≥ 63) from long reads with a low error-rate.

It can also filter *k*-mers based on their count and only retrieve the *k*-mers above a certain threshold.

## Install

If you have not installed Rust yet, please visit [rustup.rs](https://rustup.rs/) to install it.

Then clone this repository and build KFC using:
```sh
git clone https://github.com/lrobidou/KFC
cd KFC
RUSTFLAGS="-C target-cpu=native" cargo +nightly build --release -F nightly
```
Make sure to set `RUSTFLAGS="-C target-cpu=native"` to use the fastest instructions available on your architecture.

If you cannot use Rust nightly, you can also build KFC in stable mode (which may be slightly slower):
```sh
RUSTFLAGS="-C target-cpu=native" cargo build --release
```
This will create a binary located at `target/release/kfc`.

## Run

The KFC binary provides two main subcommands: `build` (to count *k*-mers from a FASTA/Q file) and `dump` (to extract the *k*-mers contained in a KFC index).
You can view the detailed usage of each subcommand using:
```sh
./kfc <subcommand> -h
```

### Building a KFC index

The first step to any KFC usage is to build a KFC index.
```sh
./kfc build -k <k> -i <FASTA/Q> -o <index>.kfc
```

### Dumping a KFC index to text

Once the KFC index is computed, it is possible to dump it to text. The *k*-mers are *not* ordered.
```sh
./kfc dump -t <threshold> -i <index>.kfc --output-text <kmers>.txt
```

### Dumping a KFC index to KFF (*k*-mer file format)

KFC supports the *k*-mer file format (see [Dufresne et al, The K-mer File Format: a standardized and compact disk representation of sets of *k*-mers](https://doi.org/10.1093/bioinformatics/btac528)).
As such, it is possible to dump a KFC index into a KFF file.
The count of each *k*-mer is encoded in the KFF file.
```sh
./kfc dump --input-index <index>.kfc --output-kff <index>.kff
```

### Dumping a KFF to text

**Warning:** KFC only handles KFF files built by KFC.

Reading the KFF file produced by KFC should be possible with any implementation supporting KFF, but we recommend relying on KFC for this task.
Indeed, a KFF built by KFC respects some assumptions on the count of *k*-mers, which can be used to dump the KFF file with a lower memory consumption.
This also means that files not respecting these assumptions would produce invalid count if dumped by KFC.
```sh
./kfc kff-dump --input-kff <index>.kff --output-text <index>.txt
```

