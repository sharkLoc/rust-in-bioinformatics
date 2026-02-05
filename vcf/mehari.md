[![Crates.io](https://img.shields.io/crates/d/mehari.svg)](https://crates.io/crates/mehari)
[![Crates.io](https://img.shields.io/crates/v/mehari.svg)](https://crates.io/crates/mehari)
[![Crates.io](https://img.shields.io/crates/l/mehari.svg)](https://crates.io/crates/mehari)
[![CI](https://github.com/varfish-org/mehari/actions/workflows/rust.yml/badge.svg)](https://github.com/varfish-org/mehari/actions/workflows/rust.yml)
[![codecov](https://codecov.io/gh/varfish-org/mehari/branch/main/graph/badge.svg?token=B1dfb7N2n8)](https://codecov.io/gh/varfish-org/mehari)
[![DOI](https://zenodo.org/badge/609124150.svg)](https://zenodo.org/badge/latestdoi/609124150)

# Mehari

<img style="float: right" width="200" height="200" src="misc/camel.jpeg" alt="a camel">

Mehari is a software package for annotating VCF files with variant effect/consequence.
The program uses [hgvs-rs](https://crates.io/crates/hgvs) for projecting genomic variants to transcripts and proteins and thus has high prediction quality.

Other popular tools offering variant effect/consequence prediction include:

- [SnpEff](http://pcingola.github.io/SnpEff/)
- [VEP (Variant Effect Predictor)](https://www.ensembl.org/info/docs/tools/vep/index.html)

Mehari offers HGVS predictions that aim to mirror VariantValidator, the gold standard for HGVS variant descriptions, and consequence predictions compatible with VEP.
Further, it is written in the Rust programming language and can be used as a library for users' Rust software.

## Usage
To annotate variant consequences, gnomAD frequencies and clinVar information for sequence variants:
```sh
    mehari annotate seqvars \
      --transcripts resources/transcript_db \
      --frequencies resources/gnomad_db \
      --clinvar resources/clinvar_db \
      --path-input-vcf input.vcf \
      --path-output-vcf output.vcf
```
The corresponding database builds can be obtained from:
 - transcripts: [github.com/varfish-org/mehari-data-tx/releases](https://github.com/varfish-org/mehari-data-tx/releases)
 - gnomAD frequencies: TODO
 - clinVar: [github.com/varfish-org/annonars-data-clinvar/releases](https://github.com/varfish-org/annonars-data-clinvar/releases)

See [Getting Started](docs/getting_started.md) for more information on usage, and [Development Setup](docs/development.md) for more information on how to build mehari and its databases from scratch.

