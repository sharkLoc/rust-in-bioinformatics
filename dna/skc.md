# skc

`skc` is a simple tool for finding shared k-mer content between two genomes.

## Installation

### Prebuilt binary

```
curl -sSL skc.mbh.sh | sh
# or with wget
wget -nv -O - skc.mbh.sh | sh
```

You can also pass options to the script like so

```text
$ curl -sSL skc.mbh.sh | sh -s -- --help
install.sh [option]

Fetch and install the latest version of skc, if skc is already
installed it will be updated to the latest version.

Options
        -V, --verbose
                Enable verbose output for the installer

        -f, -y, --force, --yes
                Skip the confirmation prompt during installation

        -p, --platform
                Override the platform identified by the installer

        -b, --bin-dir
                Override the bin installation directory [default: /usr/local/bin]

        -a, --arch
                Override the architecture identified by the installer [default: x86_64]

        -B, --base-url
                Override the base URL used for downloading releases [default: https://github.com/mbhall88/skc/releases]

        -h, --help
                Display this help message

```

### Cargo

```text
cargo install skc
```

### Conda

```text
conda install skc
```

### Local

```text
cargo build --release
./target/release/skc --help
```

## Usage

Check for shared 16-mers between the [HIV-1 genome](https://www.ncbi.nlm.nih.gov/nuccore/NC_001802.1) and the [
*Mycobacterium tuberculosis* genome](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3).

```text
$ skc -k 16 NC_001802.1.fa NC_000962.3.fa
[2023-06-20T01:46:36Z INFO ] 9079 unique k-mers in target
[2023-06-20T01:46:38Z INFO ] 2 shared k-mers between target and query
>4233642782 tcount=1 qcount=1 tpos=NC_001802.1:739 qpos=NC_000962.3:4008106
TGCAGAACATCCAGGG
>4237062597 tcount=1 qcount=1 tpos=NC_001802.1:8415 qpos=NC_000962.3:629482
CCAGCAGCAGATAGGG
```

So we can see there are two shared 16-mers between the genomes. By default, the shared k-mers are written to stdout -
use the `-o` option to write them to file.

### Fasta description

Example: `>4233642782 tcount=1 qcount=1 tpos=NC_001802.1:739 qpos=NC_000962.3:4008106`

The ID (`4233642782`) is the 64-bit integer representation of the k-mer's value in bit-space (
see [Daniel Liu's brilliant ][cute] for more information). `tcount` and `qcount` are the
number of times the k-mer is present in the target and query genomes, respectively. `tpos` and `qpos` are the (1-based)
k-mer starting position(s) within the target and query contigs - these will be comma-seperated if the k-mer occurs
multiple times.

### Usage help

```text
$ skc --help
Shared k-mer content between two genomes

Usage: skc [OPTIONS] <TARGET> <QUERY>

Arguments:
  <TARGET>
          Target sequence

          Can be compressed with gzip, bzip2, xz, or zstd

  <QUERY>
          Query sequence

          Can be compressed with gzip, bzip2, xz, or zstd

Options:
  -k, --kmer <KMER>
          Size of k-mers (max. 32)

          [default: 21]

  -o, --output <OUTPUT>
          Output filepath(s); stdout if not present

  -O, --output-type <u|b|g|l|z>
          u: uncompressed; b: Bzip2; g: Gzip; l: Lzma; z: Zstd

          Output compression format is automatically guessed from the filename extension. This option is used to override that

          [default: u]

  -l, --compress-level <INT>
          Compression level to use if compressing output

          [default: 6]

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

### Caveats

- Make the first genome passed (`<TARGET>`) the smallest genome. This is to reduce memory usage as all unique k-mers (
  well their `u64` value) for this genome will be held in memory.
- We do not use canonical k-mers
- 32 is the largest k-mer size that can be used. This is basically a (lazy) implementation decision, but also helps to
  keep the memory footprint as low as possible. If you want larger k-mer values, I would suggest checking out some of
  the [similar tools](#alternate-tools).

## Alternate tools

`skc` does not claim to be the fastest or most memory-efficient tool to find shared k-mer content. I basically wrote it
as I either struggled to install some alternate tools, they were clunky/verbose, or it was laborious to get shared
k-mers out of the results (e.g. can only search one k-mer at a time or have to run many different subcommands). Here is
a (non-exhaustive) list of other tools that can be used to get shared k-mer content

- [unikmer](https://github.com/shenwei356/unikmer) - this was brought to my attention *after* I wrote `skc`. Had I known
  about it beforehand, I probably wouldn't have written `skc`. So I would recommend unikmer for almost all use
  cases - [Wei Shen](https://github.com/shenwei356) writes awesome tools
- [Jellyfish](https://github.com/gmarcais/Jellyfish)
- [REINDEER](https://github.com/kamimrcht/REINDEER)
- [kmer-db](https://github.com/refresh-bio/kmer-db)
- [GGCAT](https://github.com/algbio/ggcat)
- [KAT](https://github.com/TGAC/KAT)

## Acknowledgements

[Daniel Liu's brilliant ][cute] is used to (rapidly) convert k-mers into 64-bit integers.


[cute]: https://github.com/Daniel-Liu-c0deb0t/cute-nucleotides
