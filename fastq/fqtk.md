# fqtk

<p align="center">
  <a href="https://github.com/fulcrumgenomics/fqtk/actions?query=workflow%3ACheck"><img src="https://github.com/fulcrumgenomics/fqtk/actions/workflows/build_and_test.yml/badge.svg" alt="Build Status"></a>
  <img src="https://img.shields.io/crates/l/fqtk.svg" alt="license">
  <a href="https://crates.io/crates/fqtk"><img src="https://img.shields.io/crates/v/fqtk.svg?colorB=319e8c" alt="Version info"></a>
  <a href="http://bioconda.github.io/recipes/fqtk/README.html"><img src="https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat" alt="Install with bioconda"></a>
  <br>
</p>

A toolkit for working with FASTQ files, written in Rust.

Currently `fqtk` contains a single tool, `demux` for demultiplexing FASTQ files based on sample barcodes.
`fqtk demux` can be used to demultiplex one or more FASTQ files (e.g. a set of R1, R2 and I1 FASTQ files) with any number of sample barcodes at fixed locations within the reads.
It is highly efficient and multi-threaded for high performance.

Usage for `fqtk demux` follows:

```console
Performs sample demultiplexing on FASTQs.

The sample barcode for each sample in the metadata TSV will be compared against
the sample barcode bases extracted from the FASTQs, to assign each read to a
sample.  Reads that do not match any sample within the given error tolerance
will be placed in the ``unmatched_prefix`` file.

FASTQs and associated read structures for each sub-read should be given:

- a single fragment read (with inline index) should have one FASTQ and one read
  structure 
- paired end reads should have two FASTQs and two read structures 
- a dual-index sample with paired end reads should have four FASTQs and four read
  structures given: two for the two index reads, and two for the template reads.

If multiple FASTQs are present for each sub-read, then the FASTQs for each
sub-read should be concatenated together prior to running this tool (e.g. 
`zcat s_R1_L001.fq.gz s_R1_L002.fq.gz | bgzip -c > s_R1.fq.gz`).

Read structures are made up of `<number><operator>` pairs much like the `CIGAR`
string in BAM files. Four kinds of operators are recognized:

1. `T` identifies a template read
2. `B` identifies a sample barcode read
3. `M` identifies a unique molecular index read
4. `S` identifies a set of bases that should be skipped or ignored

The last `<number><operator>` pair may be specified using a `+` sign instead of
number to denote "all remaining bases". This is useful if, e.g., fastqs have
been trimmed and contain reads of varying length. Both reads must have template
bases.  Any molecular identifiers will be concatenated using the `-` delimiter
and placed in the given SAM record tag (`RX` by default).  Similarly, the sample
barcode bases from the given read will be placed in the `BC` tag.

Metadata about the samples should be given as a headered metadata TSV file with
two columns 1. `sample_id` - the id of the sample or library. 2. `barcode` - the
expected barcode sequence associated with the `sample_id`.

The read structures will be used to extract the observed sample barcode, template
bases, and molecular identifiers from each read.  The observed sample barcode
will be matched to the sample barcodes extracted from the bases in the sample
metadata and associated read structures.

An observed barcode matches an expected barcocde if all the following are true:

1. The number of mismatches (edits/substitutions) is less than or equal to the
   maximum mismatches (see --max-mismatches).
2. The difference between number of mismatches in the best and second best
   barcodes is greater than or equal to the minimum mismatch delta
   (`--min-mismatch-delta`). The expected barcode sequence may contains Ns,
   which are not counted as mismatches regardless of the observed base (e.g.
   the expected barcode `AAN` will have zero mismatches relative to both the
   observed barcodes `AAA` and `AAN`).

## Outputs

All outputs are generated in the provided `--output` directory.  For each sample
plus the unmatched reads, FASTQ files are written for each read segment
(specified in the read structures) of one of the types supplied to
`--output-types`.

FASTQ files have names of the format:

{sample_id}.{segment_type}{read_num}.fq.gz

where `segment_type` is one of `R`, `I`, and `U` (for template, barcode/index
and molecular barcode/UMI reads respectively) and `read_num` is a number starting
at 1 for each segment type.

In addition a `demux-metrics.txt` file is written that is a tab-delimited file
with counts of how many reads were assigned to each sample and derived metrics.

## Example Command Line

As an example, if the sequencing run was 2x100bp (paired end) with two 8bp index
reads both reading a sample barcode, as well as an in-line 8bp sample barcode in
read one, the command line would be:

fqtk demux \
  --inputs r1.fq.gz i1.fq.gz i2.fq.gz r2.fq.gz \
  --read-structures 8B92T 8B 8B 100T \
  --sample-metadata metadata.tsv \
  --output output_folder

Usage: fqtk demux [OPTIONS] --inputs <INPUTS>... --read-structures <READ_STRUCTURES>... --sample-metadata <SAMPLE_METADATA> --output <OUTPUT>

Options:
  -i, --inputs <INPUTS>...
          One or more input fastq files each corresponding to a sequencing (e.g. R1, I1)

  -r, --read-structures <READ_STRUCTURES>...
          The read structures, one per input FASTQ in the same order

  -b, --output-types <OUTPUT_TYPES>...
          The read structure types to write to their own files (Must be one of T, B,
          or M for template reads, sample barcode reads, and molecular barcode reads)

          Multiple output types may be specified as a space-delimited list.

          [default: T]

  -s, --sample-metadata <SAMPLE_METADATA>
          A file containing the metadata about the samples

  -o, --output <OUTPUT>
          The output directory into which to write per-sample FASTQs

  -u, --unmatched-prefix <UNMATCHED_PREFIX>
          Output prefix for FASTQ file(s) for reads that cannot be matched to a sample

          [default: unmatched]

      --max-mismatches <MAX_MISMATCHES>
          Maximum mismatches for a barcode to be considered a match

          [default: 1]

  -d, --min-mismatch-delta <MIN_MISMATCH_DELTA>
          Minimum difference between number of mismatches in the best and second best barcodes
          for a barcode to be considered a match

          [default: 2]

  -t, --threads <THREADS>
          The number of threads to use. Cannot be less than 3

          [default: 8]

  -c, --compression-level <COMPRESSION_LEVEL>
          The level of compression to use to compress outputs

          [default: 5]

  -S, --skip-reasons <SKIP_REASONS>
          Skip demultiplexing reads for any of the following reasons, otherwise panic.

          1. `too-few-bases`: there are too few bases or qualities to extract given the
             read structures.  For example, if a read is 8bp long but the read structure
             is `10B`, or if a read is empty and the read structure is `+T`.

  -h, --help
          Print help information (use `-h` for a summary)

  -V, --version
          Print version information
```

## Installing

### Installing with `conda`

To install with conda you must first [install conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#installation).
Then, in your command line (and with the environment you wish to install fqtk into active) run:

```console
conda install -c bioconda fqtk
```

### Installing with `cargo`

To install with cargo you must first [install rust](https://doc.rust-lang.org/cargo/getting-started/installation.html).
Which (On Mac OS and Linux) can be done with the command:

```console
curl https://sh.rustup.rs -sSf | sh
```

Then, to install `fqtk` run:

```console
cargo install fqtk
```

### Building From Source

First, clone the git repo:

```console
git clone https://github.com/fulcrumgenomics/fqtk.git
```

Secondly, if you do not already have rust development tools installed, install via [rustup](https://rustup.rs/):

```console
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Then build the toolkit in release mode:

```console
cd fqtk
cargo build --release
./target/release/fqtk --help
```

## Developing

fqtk is developed in Rust and follows the conventions of using `rustfmt` and `clippy` to ensure both code quality and standardized formatting.
When working on fqtk, before pushing any commits, please first run `./ci/check.sh` and resolve any issues that are reported.

## Releasing a New Version

### Pre-requisites

Install 

```console
cargo install cargo-release
```

### Prior to Any Release

Create a release that will not try to push to `crates.io` and verify the command:

```console
cargo release [major,minor,patch,release,rc...] --no-publish
```

Note: "dry-run" is the default for cargo release.

See the [ reference documentation][cargo-release-docs-link] for more information

### Semantic Versioning

This tool follows [Semantic Versioning](https://semver.org/).  In brief:

* MAJOR version when you make incompatible API changes,
* MINOR version when you add functionality in a backwards compatible manner, and
* PATCH version when you make backwards compatible bug fixes.

### Major Release

To create a major release:

```console
cargo release major --execute
```

This will remove any pre-release extension, create a new tag and push it to github, and push the release to creates.io.

Upon success, move the version to the [next candidate release](#release-candidate).

Finally, make sure to [create a new release][new-release-link] on GitHub.

### Minor and Patch Release

To create a _minor_ (_patch_) release, follow the [Major Release](#major-release) instructions substituting `major` with `minor` (`patch`):

```console
cargo release minor --execute
```

### Release Candidate

To move to the next release candidate:

```console
cargo release rc --no-tag --no-publish --execute
```

This will create or bump the pre-release version and push the changes to the main branch on github.
This will not tag and publish the release candidate.
If you would like to tag the release candidate on github, remove `--no-tag` to create a new tag and push it to github.

[cargo-release-link]: https://github.com/crate-ci/cargo-release
[cargo-release-docs-link]: https://github.com/crate-ci/cargo-release/blob/master/docs/reference.md

[new-release-link]: https://github.com/fulcrumgenomics/fqtk/releases/new
