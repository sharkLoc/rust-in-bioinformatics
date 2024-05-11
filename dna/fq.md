# fq

[![CI status](https://github.com/stjude-rust-labs/fq/workflows/CI/badge.svg)](https://github.com/stjude-rust-labs/fq/actions)

**fq** filters, generates, subsamples, and validates [FASTQ] files.

[FASTQ]: https://en.wikipedia.org/wiki/FASTQ_format

## Install

There are different methods to install fq.

### Releases

[Precompiled binaries are built][releases] for modern Linux distributions
(`x86_64-unknown-linux-gnu`), macOS (`x86_64-apple-darwin`), and Windows
(`x86_64-pc-windows-msvc`). The Linux binaries require glibc 2.18+ (CentOS/RHEL
8+, Debian 8+, Ubuntu 14.04+, etc.).

[releases]: https://github.com/stjude-rust-labs/fq/releases

### Conda

fq is available via [Bioconda].

```
$ conda install fq=0.11.0
```

[Bioconda]: https://bioconda.github.io/recipes/fq/README.html

### Manual

Clone the repository and use [Cargo] to install fq.

```
$ git clone --depth 1 --branch v0.11.0 https://github.com/stjude-rust-labs/fq.git
$ cd fq
$ cargo install --locked --path .
```

[Cargo]: https://doc.rust-lang.org/cargo/getting-started/installation.html

### Container image

Container images are managed by Bioconda and available through [Quay.io], e.g.,
using [Docker]:

```
$ docker image pull quay.io/biocontainers/fq:<tag>
```

See [the repository tags] for the available tags.

Alternatively, build the development container image:

```
$ git clone --depth 1 --branch v0.11.0 https://github.com/stjude-rust-labs/fq.git
$ cd fq
$ docker image build --tag fq:0.11.0 .
```

[Quay.io]: https://quay.io/repository/biocontainers/fq
[the repository tags]: https://quay.io/repository/biocontainers/fq?tab=tags
[Docker]: https://www.docker.com/

## Usage

fq provides subcommands for filtering, generating, subsampling, and
validating FASTQ files.

### filter

**fq filter** filters a given FASTQ file by a set of names or a sequence
pattern. The result includes only the records that match the given options.

#### Usage

```
Filters a FASTQ file

Usage: fq filter [OPTIONS] --dsts <DSTS> [SRCS]...

Arguments:
  [SRCS]...  FASTQ sources

Options:
      --names <NAMES>
          Allowlist of record names
      --sequence-pattern <SEQUENCE_PATTERN>
          Keep records that have sequences that match the given regular expression
      --dsts <DSTS>
          Filtered FASTQ destinations
  -h, --help
          Print help
  -V, --version
          Print version
```

#### Examples

```sh
# Filters an input FASTQ using the given allowlist.
$ fq filter --names allowlist.txt --dsts /dev/stdout in.fastq

# Filters FASTQ files by matching a sequence pattern in the first input's
# records and applying the match to all inputs.
$ fq filter --sequence-pattern ^TC --dsts out.1.fq --dsts out.2.fq in.1.fq in.2.fq
```

### generate

**fq generate** is a FASTQ file pair generator. It creates two reads, formatting
names as [described by Illumina][1].

While _generate_ creates "valid" FASTQ reads, the content of the files are
completely random. The sequences do not align to any genome.

[1]: https://help.basespace.illumina.com/articles/descriptive/fastq-files/

#### Usage

```
Generates a random FASTQ file pair

Usage: fq generate [OPTIONS] <R1_DST> <R2_DST>

Arguments:
  <R1_DST>  Read 1 destination. Output will be gzipped if ends in `.gz`
  <R2_DST>  Read 2 destination. Output will be gzipped if ends in `.gz`

Options:
  -s, --seed <SEED>                  Seed to use for the random number generator
  -n, --record-count <RECORD_COUNT>  Number of records to generate [default: 10000]
      --read-length <READ_LENGTH>    Number of bases in the sequence [default: 101]
  -h, --help                         Print help
  -V, --version                      Print version
```

#### Examples

```sh
# Generates the default number of records, written to uncompressed files.
$ fq generate /tmp/r1.fastq /tmp/r2.fastq

# Generates FASTQ paired reads with 32 records, written to gzipped outputs.
$ fq generate --record-count 32 /tmp/r1.fastq.gz /tmp/r2.fastq.gz
```

### lint

**fq lint** is a FASTQ file pair validator.

#### Usage

```
Validates a FASTQ file pair

Usage: fq lint [OPTIONS] <R1_SRC> [R2_SRC]

Arguments:
  <R1_SRC>  Read 1 source. Accepts both raw and gzipped FASTQ inputs
  [R2_SRC]  Read 2 source. Accepts both raw and gzipped FASTQ inputs

Options:
      --lint-mode <LINT_MODE>
          Panic on first error or log all errors [default: panic] [possible values: panic, log]
      --single-read-validation-level <SINGLE_READ_VALIDATION_LEVEL>
          Only use single read validators up to a given level [default: high] [possible values: low, medium, high]
      --paired-read-validation-level <PAIRED_READ_VALIDATION_LEVEL>
          Only use paired read validators up to a given level [default: high] [possible values: low, medium, high]
      --disable-validator <DISABLE_VALIDATOR>
          Disable validators by code. Use multiple times to disable more than one
  -h, --help
          Print help
  -V, --version
          Print version
```

#### Validators

_validate_ includes a set of validators that run on single or paired records.
By default, records are validated with all rules, but validators can be
disabled using `--disable-validator CODE`, where `CODE` is one of validators
listed below.

##### Single

| Code | Level  | Name              | Validation
|------|--------|-------------------|------------
| S001 | low    | PlusLine          | Plus line starts with a "+".
| S002 | medium | Alphabet          | All characters in sequence line are one of "ACGTN", case-insensitive.
| S003 | high   | Name              | Name line starts with an "@".
| S004 | low    | Complete          | All four record lines (name, sequence, plus line, and quality) are present.
| S005 | high   | ConsistentSeqQual | Sequence and quality lengths are the same.
| S006 | medium | QualityString     | All characters in quality line are between "!" and "~" (ordinal values).
| S007 | high   | DuplicateName     | All record names are unique.

##### Paired

| Code | Level   | Name              | Validation
|------|---------|-------------------|------------
| P001 | medium  | Names             | Each paired read name is the same, excluding interleave.

#### Examples

```sh
# Validate both reads using all validators. Exits cleanly (0) if no validation
# errors occur.
$ fq lint r1.fastq r2.fastq

# Log errors instead of quitting on first error.
$ fq lint --lint-mode log r1.fastq r2.fastq

# Disable validators S004 and S007.
$ fq lint --disable-validator S004 --disable-validator S007 r1.fastq r2.fastq
```

### subsample

**fq subsample** outputs a subset of records from single or paired FASTQ files.

When using a probability (`-p, --probability`), each file is read through once,
and a subset of records is selected based on that chance. Given the randomness
used when sampling a uniform distribution, the output record count will not be
exact but (statistically) close.

When using a record count (`-n, --record-count`), the first input is read
twice, but it provides an exact number of records to be selected.

A seed (`-s, --seed`) can be provided to influence the results, e.g.,
for a deterministic subset of records.

For paired input, the sampling is applied to each pair.

#### Usage

```
Outputs a subset of records

Usage: fq subsample [OPTIONS] --r1-dst <R1_DST> <--probability <PROBABILITY>|--record-count <RECORD_COUNT>> <R1_SRC> [R2_SRC]

Arguments:
  <R1_SRC>  Read 1 source. Accepts both raw and gzipped FASTQ inputs
  [R2_SRC]  Read 2 source. Accepts both raw and gzipped FASTQ inputs

Options:
  -p, --probability <PROBABILITY>    The probability a record is kept, as a percentage (0.0, 1.0). Cannot be used with `record-count`
  -n, --record-count <RECORD_COUNT>  The exact number of records to keep. Cannot be used with `probability`
  -s, --seed <SEED>                  Seed to use for the random number generator
      --r1-dst <R1_DST>              Read 1 destination. Output will be gzipped if ends in `.gz`
      --r2-dst <R2_DST>              Read 2 destination. Output will be gzipped if ends in `.gz`
  -h, --help                         Print help
  -V, --version                      Print version
```

#### Examples

```sh
# Sample ~50% of records from a single FASTQ file
$ fq subsample --probability 0.5 --r1-dst r1.50pct.fastq r1.fastq

# Sample ~50% of records from a single FASTQ file and seed the RNG
$ fq subsample --probability --seed 13 --r1-dst r1.50pct.fastq r1.fastq

# Sample ~25% of records from paired FASTQ files
$ fq subsample --probability 0.25 --r1-dst r1.25pct.fastq --r2-dst r2.25pct.fastq r1.fastq r2.fastq

# Sample ~10% of records from a gzipped FASTQ file and compress output
$ fq subsample --probability 0.1 --r1-dst r1.10pct.fastq.gz r1.fastq.gz

# Sample exactly 10000 records from a single FASTQ file
$ fq subsample --record-count 10000 -r1-dst r1.10k.fastq r1.fastq
```