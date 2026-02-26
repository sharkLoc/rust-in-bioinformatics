![Build](https://github.com/fulcrumgenomics/fgumi/actions/workflows/check.yml/badge.svg)
[![Latest release](https://img.shields.io/github/downloads-pre/fulcrumgenomics/fgumi/latest/total)](https://github.com/fulcrumgenomics/fgumi/releases)
[![Version at crates.io](https://img.shields.io/crates/v/fgumi)](https://crates.io/crates/fgumi)
[![Documentation at docs.rs](https://img.shields.io/docsrs/fgumi)](https://docs.rs/fgumi)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/fulcrumgenomics/fgumi/blob/main/LICENSE)

# fgumi

**⚠️ ALPHA SOFTWARE - USE AT YOUR OWN RISK**

This software is currently in **ALPHA**. While we have extensively tested these
tools across a wide variety of vendor-provided data, **no guarantees are made**
regarding correctness or stability.

We are targeting **June 1, 2026** to recommend fgumi over
[fgbio](https://github.com/fulcrumgenomics/fgbio) for production use.

Fulcrum Genomics Unique Molecular Indexing (UMI) Tools - a suite of high-performance tools for working with UMI-tagged sequencing data.

<p>
<a href="https://fulcrumgenomics.com"><img src="https://raw.githubusercontent.com/fulcrumgenomics/fgumi/main/.github/logos/fulcrumgenomics.svg" alt="Fulcrum Genomics" height="100"/></a>
</p>

<a href="mailto:contact@fulcrumgenomics.com?subject=[GitHub inquiry]"><img src="https://img.shields.io/badge/Email_us-brightgreen.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>
<a href="https://www.fulcrumgenomics.com"><img src="https://img.shields.io/badge/Visit_Us-blue.svg?&style=for-the-badge&logo=wordpress&logoColor=white"/></a>

## Overview

fgumi provides comprehensive functionality for:
- **UMI extraction** from FASTQ files
- **Read grouping** by UMI with multiple assignment strategies
- **UMI-aware deduplication** for marking/removing PCR duplicates
- **Consensus calling** (simplex, duplex, and vanilla)
- **Quality filtering** of consensus reads
- **Read clipping** for overlapping pairs
- **Metrics collection** for QC and analysis

## Pipeline Overview

<p align="center">
  <img src="https://raw.githubusercontent.com/fulcrumgenomics/fgumi/main/docs/images/fgumi_subway.png" alt="fgumi Pipeline" width="800"/>
</p>

The diagram shows the workflow from FASTQ files to filtered consensus reads:
- **Red**: Simplex (single-strand) consensus
- **Blue**: Duplex (double-strand) consensus
- **Green**: CODEC consensus
- **Orange**: Optional UMI correction for fixed UMI sets

## Resources

* [Documentation](https://docs.rs/fgumi)
* [Best Practice Pipeline](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/best-practice-consensus-pipeline.md): Recommended workflow from FASTQ to consensus
* [Snakemake Pipeline](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/FastqToConsensus-RnD.smk): Reference implementation
* [Metrics](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/metrics.md): Output metrics documentation
* [Developing](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/DEVELOPING.md): Developer guide
* [Compare CLI](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/compare-cli.md): Compare command documentation (feature-gated)
* [Simulate CLI](https://github.com/fulcrumgenomics/fgumi/blob/main/docs/simulate-cli.md): Simulate command documentation (feature-gated)
* [Releases](https://github.com/fulcrumgenomics/fgumi/releases)
* [Issues](https://github.com/fulcrumgenomics/fgumi/issues): Report a bug or request a feature
* [Pull requests](https://github.com/fulcrumgenomics/fgumi/pulls): Submit a patch or new feature
* [Discussions](https://github.com/fulcrumgenomics/fgumi/discussions): Ask a question
* [Contributors guide](https://github.com/fulcrumgenomics/fgumi/blob/main/CONTRIBUTING.md)
* [License](https://github.com/fulcrumgenomics/fgumi/blob/main/LICENSE): Released under the MIT license

## Installation

### Downloading a pre-built binary

Pre-built binaries for the most common operating systems and CPU architectures are attached to each [release](https://github.com/fulcrumgenomics/fgumi/releases/latest) for this project.

### Installing with Cargo

```
cargo install fgumi
```

### Building from source

Clone the repository:

```
git clone https://github.com/fulcrumgenomics/fgumi
```

Build the `release` version:

```
cd fgumi
cargo build --release
```

### Optional Features

| Feature | Description |
|---------|-------------|
| `compare` | Developer tools for comparing BAMs and metrics |
| `simulate` | Commands for generating synthetic test data |
| `profile-adjacency` | Enable profiling output for adjacency UMI assigner |
| `isal` | Use ISA-L/igzip for BGZF compression (benchmarking) |

Enable with: `cargo build --release --features <feature>`

**Note:** The `isal` feature requires the vendored submodule. Clone with submodules:

```
git clone --recursive https://github.com/fulcrumgenomics/fgumi
```

Or initialize after cloning: `git submodule update --init`

## Available Tools

| Command | Description | Equivalent Tool(s) |
|---------|-------------|------------------|
| `extract` | Extract UMIs from FASTQ files | `fgbio ExtractUmisFromBam` |
| `correct` | Correct UMIs based on sequence similarity | `fgbio CorrectUmis` |
| `zipper` | Restore original FASTQ from unaligned BAM | `fgbio ZipperBams`, `picard MergeBamAlignment` |
| `fastq` | Convert BAM to FASTQ format | `samtools fastq` |
| `sort` | Sort BAM by coordinate/queryname/template | `samtools sort` |
| `group` | Group reads by UMI | `fgbio GroupReadsByUmi` |
| `dedup` | Mark/remove UMI-aware duplicates | `gatk UmiAwareMarkDuplicatesWithMateCigar`, `umi-tools dedup` |
| `simplex` | Call single-strand consensus reads | `fgbio CallMolecularConsensusReads` |
| `duplex` | Call duplex consensus reads | `fgbio CallDuplexConsensusReads` |
| `codec` | Call CODEC consensus | `fgbio CallCodecConsensusReads` |
| `filter` | Filter consensus reads | `fgbio FilterConsensusReads` |
| `clip` | Clip overlapping read pairs | `fgbio ClipBam` |
| `duplex-metrics` | Collect duplex metrics | `fgbio CollectDuplexSeqMetrics` |
| `review` | Review consensus variants | `fgbio ReviewConsensusVariants` |
| `downsample` | Downsample BAM by UMI family | N/A |
| `compare <cmd>` | Compare files (feature-gated) | N/A |
| `simulate <cmd>` | Generate test data (feature-gated) | N/A |

## Usage

For detailed usage of each command, run:
```bash
fgumi <command> --help
```

### Basic Workflow

1. **Extract UMIs** from FASTQ:
```bash
fgumi extract \
  --inputs R1.fastq.gz R2.fastq.gz \
  --read-structures +T +M \
  --output unaligned.bam
```

2. **(Optional) Correct UMIs** for fixed UMI sets:
```bash
fgumi correct \
  --input unaligned.bam \
  --output corrected.bam \
  --includelist umis.txt
```

3. **Align and sort** reads using fgumi fastq + zipper + sort pipeline:
```bash
fgumi fastq --input unaligned.bam \
  | bwa mem -p ref.fa - \
  | fgumi zipper --unmapped unaligned.bam \
  | fgumi sort --output sorted.bam --order template-coordinate
```

4. **Group** reads by UMI:
```bash
fgumi group \
  --input sorted.bam \
  --output grouped.bam \
  --strategy paired   # for duplex workflows
  # or --strategy adjacency for simplex/codec workflows
```

5. **Call consensus** reads:
```bash
# Simplex consensus
fgumi simplex \
  --input grouped.bam \
  --output consensus.bam

# Or duplex consensus
fgumi duplex \
  --input grouped.bam \
  --output duplex.bam

# Or codec consensus
fgumi codec \
  --input grouped.bam \
  --output codec_consensus.bam
```

6. **(Optional) Collect duplex metrics**:
```bash
fgumi duplex-metrics \
  --input duplex.bam \
  --output metrics.txt
```

7. **Filter** consensus reads:
```bash
fgumi filter \
  --input consensus.bam \
  --output filtered.bam \
  --reference ref.fa
```

## Threading Options

fgumi supports multi-threading for parallel processing:

- `--threads 0` or `--threads 1` or omitted → single-threaded
- `--threads N` where N > 1 → multi-threaded with N threads

Thread distribution is optimized per-command based on workload profiling.

| Scenario | Recommendation |
|----------|----------------|
| SLURM job with 8 CPUs allocated | `--threads 8` |
| Dedicated 16-core workstation | `--threads 16` |
| Shared login node | `--threads 2` (or avoid heavy jobs) |
| Snakemake/Nextflow with resource limits | `--threads {threads}` |

## Performance

fgumi is written in Rust for maximum performance.

### Command-Level Optimizations

| Command | Key Optimizations |
|---------|-------------------|
| `extract` | Work-stealing thread pool, streaming I/O |
| `correct` | N-gram indexing with pigeonhole principle, BK-tree for k>1 |
| `group` | 2-bit UMI encoding, N-gram/BK-tree indexing, directed adjacency graph |
| `simplex` | Fast-path for unanimous consensus, parallel processing |
| `duplex` | Parallel duplex calling, efficient strand matching |
| `codec` | Parallel CODEC consensus |
| `filter` | Streaming filter with parallel processing |
| `clip` | Parallel overlap detection and clipping |
| `sort` | External merge sort, configurable memory limit |

### General Optimizations

- **2-bit DNA encoding**: 4 bases in 1 byte, 32 bases in u64
- **CPU intrinsics**: XOR + popcount for Hamming distance
- **Work-stealing scheduler**: Unified pipeline with dynamic load balancing
- **libdeflate**: Fast BGZF compression (optional ISA-L)

## Acknowledgements

fgumi's UMI grouping algorithms are inspired by:

- [UMI-tools](https://github.com/CGATOxford/UMI-tools) (Smith et al. 2017) - The directed adjacency
  method for UMI deduplication with count gradient constraints.
- [UMICollapse](https://github.com/Daniel-Liu-c0deb0t/UMICollapse) (Liu 2019) - N-gram and BK-tree
  indexing strategies for efficient similarity search in UMI deduplication.

## Authors

- [Nils Homer](https://github.com/nh13)
- [Tim Fennell](https://github.com/tfenne)

## Sponsors

Development of fgumi is supported by [Fulcrum Genomics](https://www.fulcrumgenomics.com).

[Become a sponsor](https://github.com/sponsors/fulcrumgenomics)

## Disclaimer

This software is under active development.
While we make a best effort to test this software and to fix issues as they are reported, this software is provided as-is without any warranty (see the [license](https://github.com/fulcrumgenomics/fgumi/blob/main/LICENSE) for details).
Please submit an [issue](https://github.com/fulcrumgenomics/fgumi/issues), and better yet a [pull request](https://github.com/fulcrumgenomics/fgumi/pulls) as well, if you discover a bug or identify a missing feature.
Please contact [Fulcrum Genomics](https://www.fulcrumgenomics.com) if you are considering using this software or are interested in sponsoring its development.

