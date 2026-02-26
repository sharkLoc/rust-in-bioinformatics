# squab

[![GitHub Actions status](https://github.com/zaeleus/squab/workflows/CI/badge.svg)](https://github.com/zaeleus/squab/actions)

**squab** performs gene expression quantification by counting the number of
aligned records that intersects a set of features. Output can be the raw counts
or normalized counts in TPM (transcripts per million) or FPKM (fragments per
kilobase per million mapped reads).

The original goal of this project is to provide a faster alternative to
[htseq-count]. It uses similar counting rules and outputs a compatible data
table.

[htseq-count]: https://htseq.readthedocs.io/en/master/count.html

## Installation

Install [Rust] and use `cargo` to install `squab`.

```
$ cargo install --locked --git https://github.com/zaeleus/squab.git
```

[Rust]: https://www.rust-lang.org/tools/install


## Usage

squab has two subcommands: `quantify` and `normalize`.

### `quantify`

`quantify` performs gene expression quantification by counting the number of
times aligned records intersect known gene annotations.

```
Gene expression quantification

Usage: squab quantify [OPTIONS] --annotations <ANNOTATIONS> <SRC>

Arguments:
  <SRC>  Input alignment file

Options:
      --with-secondary-records
          Count secondary records (BAM flag 0x100)
      --with-supplementary-records
          Count supplementary records (BAM flag 0x800)
      --with-nonunique-records
          Count nonunique records (BAM data tag NH > 1)
      --strand-specification <STRAND_SPECIFICATION>
          Strand specification [default: auto] [possible values: none, forward, reverse, auto]
  -t, --feature-type <FEATURE_TYPE>
          Feature type to count [default: exon]
  -i, --id <ID>
          Feature attribute to use as the feature identity [default: gene_id]
      --min-mapping-quality <MIN_MAPPING_QUALITY>
          [default: 10]
  -o, --output <OUTPUT>
          Output destination
  -a, --annotations <ANNOTATIONS>
          Input annotations file (GFF3)
      --threads <THREADS>
          Force a specific number of threads
  -h, --help
          Print help (see more with '--help')
```

The default output is a tab-delimited text file with two columns: the feature
identifier (string) and the number of reads (integer) from the input alignment
that overlap it. This file is compatible as output from htseq-count, meaning it
includes statistics in the trailer.

### `normalize`

`normalize` takes raw counts and normalizes them by gene length, meaning the
annotations used for quantification must be the same given here. Two
normalization methods are available: FPKM for single sample normalization and
TPM for across samples normalization (default).

Typically, this is only used when a sample was previously quanitifed, e.g.,
using `squab quantify` or `htseq-count`.

```
Normalize features counts

Usage: squab normalize [OPTIONS] --annotations <ANNOTATIONS> <SRC>

Arguments:
  <SRC>  Input counts file

Options:
  -t, --feature-type <FEATURE_TYPE>  Feature type to count [default: exon]
  -i, --id <ID>                      Feature attribute to use as the feature identity [default: gene_id]
  -a, --annotations <ANNOTATIONS>    Input annotations file (GFF3)
      --method <METHOD>              Quantification normalization method [default: tpm] [possible values: fpkm, tpm]
  -o, --output <OUTPUT>              Output destination
  -h, --help                         Print help (see more with '--help')
```

The output is a tab-delimited text file with two columns: the feature
identifier (string) and the normalized value (double).

## Examples

### Count features (exons by gene ID)

```
$ squab \
    quantify \
    --annotations annotations.gff3.gz \
    --output sample.counts.tsv \
    sample.bam
```

### Count featues (genes by gene name)

```
$ squab \
    quantify \
    --annotations annotations.gff3.gz \
    --feature-type gene \
    --id gene_name \
    --output sample.counts.tsv \
    sample.bam
```

### Normalize counts in FPKM (exons by gene ID)

```
$ squab \
    normalize \
    --method fpkm \
    --annotations annotations.gff3.gz \
    sample.counts.tsv \
    > sample.fpkm.tsv
```

## Limitations

  * Counts are taken only as the union of matched feature sets, i.e., reads that
    overlap any part of the feature is considered once.
  * For paired end alignments, a read that matches itself before a mate is
    found replaces the previously known record.

## References

  * S Anders, T P Pyl, W Huber. HTSeq – A Python framework to work with
    high-throughput sequencing data. _bioRxiv_ 2014.
    https://doi.org/10.1101/002824

  * Wagner, G.P., Kin, K. & Lynch, V.J. Measurement of mRNA abundance using
    RNA-seq data: RPKM measure is inconsistent among samples. _Theory Biosci_.
    **131**, 281–285 (2012). https://doi.org/10.1007/s12064-012-0162-3

