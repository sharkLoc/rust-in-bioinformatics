[![Crates.io version](https://img.shields.io/crates/v/deacon?style=flat-square)](https://crates.io/crates/deacon)
[![Conda version](https://img.shields.io/conda/v/bioconda/deacon?style=flat-square&label=bioconda&color=blue)](https://anaconda.org/bioconda/deacon)
[![Crates.io downloads](https://img.shields.io/crates/d/deacon?color=orange&label=crates.io%20downloads&style=flat-square)](https://crates.io/crates/deacon)
[![Conda downloads](https://img.shields.io/conda/dn/bioconda/deacon.svg?style=flat-square&label=conda%20downloads&color=blue)](https://anaconda.org/bioconda/deacon)
[![biorXiv preprint](https://img.shields.io/badge/biorXiv-10.1101/2025.06.09.658732-red?&style=flat-square)](https://doi.org/10.1101/2025.06.09.658732)

<div align="center"><img src="deacon.png" width="180" alt="Logo"></div>

# Deacon

Deacon filters DNA sequences in FASTA/Q files and streams using SIMD-accelerated minimizer comparison with query sequence(s), emitting either matching sequences (**search mode**), or sequences without matches (**deplete mode**). Sequences match when they share enough distinct minimizers with the indexed query to exceed chosen absolute and relative thresholds. Query size has little impact on filtering speed, enabling ultrafast search and depletion with gene-, genome- and pangenome-scale queries using a laptop. Deacon filters uncompressed FASTA/Q at **gigabases per second** on recent AMD, Intel (`x86_64`), and Apple `arm64` systems. Built with panhuman host depletion in mind—yet broadly useful for searching large sequence collections—Deacon delivers [leading classification accuracy](https://doi.org/10.1101/2025.06.09.658732) for host depletion and unrivalled speed using 5GB of RAM.

Default parameters are carefully chosen but easily changed. Classification sensitivity, specificity and memory requirements may be tuned by varying *k*-mer length (`-k`), window size (`-w`), absolute match threshold (`-a`) and relative match threshold (`-r`) . Minimizer `k` and `w` are chosen at query index time, while the match thresholds can be chosen at filter time. Matching sequences are those that share enough distinct minimizers with the indexed query to exceed *both* the absolute threshold (`-a`, default 2 shared minimizers) and the relative threshold (`-r`, default 0.01 [1%] shared minimizers). For paired sequences, hits in either mate counts towards a single match threshold for the pair. Deacon reports filtering performance during execution and optionally writes a JSON `--summary` upon completion. Sequences can optionally be renamed using `--rename` for privacy and smaller file sizes. Deacon fully supports stdin, stdout and natively handles gz, zst and xz compression formats, detected by file extension.

Benchmarks for panhuman host depletion of complex microbial metagenomes are described in a [preprint](https://www.biorxiv.org/content/10.1101/2025.06.09.658732v1). Deacon with the `panhuman-1` (*k*=31, w=15) index exhibited the highest balanced accuracy for both long and short simulated reads. Deacon was less specific only than Hostile for short reads.

## Use cases

- Depletion of human or other host genome sequences in FASTQ reads or streams.
- Ultrafast binary classification of genes, genomes or pangenomes in terabase genome catalogues like [AllTheBacteria](https://allthebacteria.org/) without tedious pre-indexing.

## Install

### Conda/mamba/pixi  [![Conda version](https://img.shields.io/conda/v/bioconda/deacon?style=flat-square&label=bioconda&color=blue)](https://anaconda.org/bioconda/deacon)

```bash
conda install -c bioconda deacon
```

### Cargo [![Crates.io version](https://img.shields.io/crates/v/deacon?style=flat-square)](https://crates.io/crates/deacon)

```bash
RUSTFLAGS="-C target-cpu=native" cargo install deacon
```

> [!IMPORTANT]
> Cargo installation requires [Rust 1.88 or newer](https://rust-lang.org/tools/install/). Update using `rustup update`.

### Docker [![Crates.io version](https://img.shields.io/badge/install%20with-docker-important.svg?style=flat-square&logo=docker)](https://biocontainers.pro/tools/deacon)

Containers are available from the [BioContainers registry](https://biocontainers.pro/tools/deacon).

```bash
docker pull quay.io/biocontainers/deacon:0.13.2--h7ef3eeb_0
```

## Quickstart

### Ultrafast panhuman host depletion

```bash
# Download validated 3GB human pangenome index (version 0.13.0 or later)
deacon index fetch panhuman-1

# Deplete long reads
deacon filter -d panhuman-1.k31w15.idx reads.fq -o filt.fq

# Deplete short paired reads
deacon filter -d panhuman-1.k31w15.idx reads.r1.fq.gz reads.r2.fq.gz -o filt.r1.fq.gz -O filt.r2.fq.gz
```

### Ultrafast gene/genome/pangenome search

```bash
deacon index build amr-genes.fa > amr-genes.idx
deacon filter amr-genes.idx AllTheBacteria.fa.zst > hits.fa
```

*N.B. Indexing a 3Gbp human genome takes ~30s using 18GB of RAM with default parameters. Filtering uses 5GB.*

## Prebuilt indexes

Prebuilt pangenome indexes are provided for human and mouse host classification and depletion. These can be downloaded using the links below, or with `deacon index fetch <name>`.

|                          Name & URL                          |                         Composition                          | Minimizers  | Subtracted minimizers | Size  | Date    |
| :----------------------------------------------------------: | :----------------------------------------------------------: | ----------- | --------------------- | ----- | ------- |
| **`panhuman-1` (*k*=31, *w*=15)** [Cloud](https://objectstorage.uk-london-1.oraclecloud.com/n/lrbvkel2wjot/b/human-genome-bucket/o/deacon/3/panhuman-1.k31w15.idx), [Zenodo](https://zenodo.org/records/17288185) | [HPRC Year 1](https://github.com/human-pangenomics/HPP_Year1_Assemblies/blob/main/assembly_index/Year1_assemblies_v2_genbank.index) ∪ [`CHM13v2.0`](https://www.ncbi.nlm.nih.gov/assembly/11828891) ∪ [`GRCh38.p14`](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.40) - bacteria (FDA-ARGOS) - viruses (RefSeq) | 409,907,949 | 20,671 (**0.0050%**)  | 3.3GB | 2025-04 |
| **`panmouse-1` (*k*=31, *w*=15)** [Cloud](https://objectstorage.uk-london-1.oraclecloud.com/n/lrbvkel2wjot/b/human-genome-bucket/o/deacon/3/panmouse-1.k31w15.idx), [Zenodo](https://zenodo.org/records/17699167) | [`GRCm39`](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001635.27) ∪ [`PRJEB47108`](https://www.ebi.ac.uk/ena/browser/view/PRJEB47108?show=sequences) - bacteria (FDA-ARGOS) - viruses (RefSeq) | 551,041,865 | 9,866 (**0.0018%**)   | 4.4GB | 2025-11 |

> [!NOTE]
>
> **Index compatibility.** Deacon `0.11.0` and above uses index format version 3. Using version 3 indexes with older Deacon versions and vice versa triggers an error. Prebuilt indexes in legacy formats are archived in object storage and Zenodo to ensure  reproducibility. To download indexes in legacy formats, replace the `/3/` in any prebuilt index download URL with either `/2/` or `/1/`  accordingly.
>
> - Deacon **`0.11.0`** and above uses index format version **`3`**
> - Deacon **`0.7.0`** through to **`0.10.0`** used index format version **`2`**
> - Deacon **`0.1.0`** through to **`0.6.0`** used index format version **`1`**

## Usage

### Filtering

The main command `deacon filter` accepts an index path followed by up to two FASTA/FASTQ file paths, depending on whether input sequences originate from stdin, a single file, or paired input files. Indexes are built with `deacon index build`.  Paired queries are supported as either separate files or interleaved stdin, and written interleaved to either stdout or file, or else to separate paired output files. For paired reads, distinct minimizer hits originating from either mate are counted. By default, input sequences must meet both an absolute threshold of 2 minimizer hits (`-a 2`) and a relative threshold of 1% of minimizers (`-r 0.01`) to pass the filter. Filtering can be inverted for e.g. host depletion using the `--deplete` (`-d`) flag. Gzip, Zstandard, and xz compression formats are detected automatically by file extension.

#### Examples

```bash
# Keep only sequences matching a collection of genes
deacon index build genes.fa > genes.idx
deacon filter genes.idx sequences.fa.gz -o matches.fa.gz

# Host depletion using the panhuman-1 index
deacon filter -d panhuman-1.k31w15.idx reads.fq.gz -o filt.fq.gz

# High sensitivity host depletion with absolute threshold of 1 and no relative threshold
deacon filter -d -a 1 -r 0 panhuman-1.k31w15.idx reads.fq.gz -o filt.fq.gz

# High specificity 10% relative match threshold
deacon filter -d -r 0.1 panhuman-1.k31w15.idx reads.fq.gz > filt.fq.gz

# Stdin and stdout
zcat reads.fq.gz | deacon filter -d panhuman-1.k31w15.idx > filt.fq

# True multithreaded gzip decompression with rapidgzip
rapidgzip -dc reads.fq.gz | deacon filter -d panhuman-1.k31w15.idx > filt.fq

# Zstandard compression
deacon filter -d panhuman-1.k31w15.idx reads.fq.zst -o filt.fq.zst

# Paired reads
deacon filter -d panhuman-1.k31w15.idx r1.fq.gz r2.fq.gz > filt12.fq
deacon filter -d panhuman-1.k31w15.idx r1.fq.gz r2.fq.gz -o filt.r1.fq.gz -O filt.r2.fq.gz
zcat r12.fq.gz | deacon filter -d panhuman-1.k31w15.idx - - > filt12.fq

# Save summary JSON
deacon filter -d panhuman-1.k31w15.idx reads.fq.gz -o filt.fq.gz -s summary.json

# Replace read headers with incrementing integers
deacon filter -d -R panhuman-1.k31w15.idx reads.fq.gz > filt.fq

# Only look for minimizer hits inside the first 1000bp per record
deacon filter -d -p 1000 panhuman-1.k31w15.idx reads.fq.gz > filt.fq

# Debug mode: see sequences with minimizer hits in stderr
deacon filter -d --debug panhuman-1.k31w15.idx reads.fq.gz > filt.fq
```

> [!NOTE]
>
> `deacon filter` uses 8 threads by default. Using more threads (e.g.  `--threads 16`) can accelerate filtering given sufficient resources, especially with uncompressed sequences whose processing is not rate limited by decompression. Since version `0.13.0`, Deacon writes gzipped output files (e.g `-o out.fastq.gz`) in parallel, providing particular practical benefit for gzipped paired reads. If output file(s) ending in `.gz` are detected, total `--threads` are allocated 1:1 to compression and filtering tasks respectively. Gzip compression thread allocation can be overriden with `--compression-threads`.

### Indexing

```bash
# Index one FASTA/FASTQ file
deacon index build genome.fa.gz > genome.idx

# Index many FASTA/FASTQ files using stdin
zcat *.fa.gz | deacon index build - > genomes.idx
```

`deacon index build` accepts either a FASTA/FASTQ file or a stdin stream (`-`), enabling convenient indexing of compressed sequences in one or many files with a single step. Indexing a human genome takes a few seconds. Indexing uses 2-4x as much RAM as filtering. For indexing large collections approaching terabase scale—such as mammalian pangenomes—it may be practical to index genomes individually in parallel and later combine them using the `deacon index union` set operation, described below.

#### Set operations

A differentiating feature of Deacon is the ease of combining, subtracting and intersecting minimizer indexes. For example, `deacon index diff`can be used to subtract shared minimizers between target and host genomes when building custom indexes for host depletion.

- Use `deacon index union 1.idx 2.idx 3.idx… > 1+2+3.idx` to succinctly combine two or more indexes.
- Use `deacon index diff 1.idx 2.idx > 1-2.idx` to subtract minimizers in 2.idx from 1.idx. Useful for masking out shared minimizer content between e.g. target and host genomes.
  - `deacon index diff` also supports subtracting minimizers from an index using a fastx file or stream directly, e.g. `deacon index diff 1.idx 2.fa.gz > 1-2.idx` or `zcat *.fa.gz | deacon index diff 1.idx - > 1-2.idx`. This enables diffing with larger-than-memory sequence collections if desired.

- Use `deacon index intersect 1.idx 2.idx… > 1∩2.idx` to find the intersection of minimizers in two or more indexes.

#### Inspecting indexes

- Use `deacon index info 1.idx` to display index information including minimizer *k* and *w* parameters, number of minimizers, and index format version.
- Use `deacon index dump 1.idx > 1.fa` to dump a minimizer index to FASTA.

## Command line reference

### Filtering

```bash
$ deacon filter -h
Retain or deplete sequence records with sufficient minimizer hits to an indexed query

Usage: deacon filter [OPTIONS] <INDEX> [INPUT] [INPUT2]

Arguments:
  <INDEX>   Path to minimizer index file
  [INPUT]   Optional path to fastx file (or - for stdin) [default: -]
  [INPUT2]  Optional path to second paired fastx file (or - for interleaved stdin)

Options:
  -a, --abs-threshold <ABS_THRESHOLD>
          Minimum absolute number of minimizer hits for a match [default: 2]
  -r, --rel-threshold <REL_THRESHOLD>
          Minimum relative proportion (0.0-1.0) of minimizer hits for a match [default: 0.01]
  -p, --prefix-length <PREFIX_LENGTH>
          Search only the first N nucleotides per sequence (0 = entire sequence) [default: 0]
  -d, --deplete
          Discard matching sequences (invert filtering behaviour)
  -R, --rename
          Replace sequence headers with incrementing numbers
      --rename-random
          Replace sequence headers with incrementing numbers and random suffixes
  -o, --output <OUTPUT>
          Path to output fastx file (stdout if not specified; detects .gz and .zst)
  -O, --output2 <OUTPUT2>
          Optional path to second paired output fastx file (detects .gz and .zst)
  -s, --summary <SUMMARY>
          Path to JSON summary output file
  -t, --threads <THREADS>
          Number of threads (0 = auto) [default: 8]
      --compression-threads <COMPRESSION_THREADS>
          Number of threads used for output compression (0 = auto) [default: 0]
      --compression-level <COMPRESSION_LEVEL>
          Output compression level (1-9 for gz & xz; 1-22 for zstd) [default: 2]
      --debug
          Output sequences with minimizer hits to stderr
  -q, --quiet
          Suppress progress reporting
  -h, --help
          Print help
```

### Indexing

```bash
$ deacon index -h
Build, inspect, compose and fetch minimizer indexes

Usage: deacon index <COMMAND>

Commands:
  build      Index minimizers contained within a fastx file
  union      Combine multiple minimizer indexes (A ∪ B…)
  intersect  Intersect multiple minimizer indexes (A ∩ B…)
  diff       Subtract minimizers in one index from another (A - B)
  dump       Dump minimizer index to fasta
  info       Show index information
  fetch      Fetch a pre-built index from remote storage
  help       Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help

```

```bash
$ deacon index build -h
Index minimizers contained within a fastx file

Usage: deacon index build [OPTIONS] <INPUT>

Arguments:
  <INPUT>  Path to input fastx file (supports gz, zst and xz compression)

Options:
  -k <KMER_LENGTH>
          K-mer length used for indexing (k+w-1 must be <= 96 and odd) [default: 31]
  -w <WINDOW_SIZE>
          Minimizer window size used for indexing [default: 15]
  -o, --output <OUTPUT>
          Path to output file (stdout if not specified)
  -t, --threads <THREADS>
          Number of execution threads (0 = auto) [default: 8]
  -q, --quiet
          Suppress sequence header output
  -e, --entropy-threshold <ENTROPY_THRESHOLD>
          Minimum scaled entropy threshold for k-mer filtering (0.0-1.0) [default: 0.0]
  -h, --help
          Print help
```


## Filtering summary statistics

Use `-s summary.json` to save detailed filtering statistics:
```json
{
  "version": "deacon 0.9.0",
  "index": "panhuman-1.k31w15.idx",
  "input": "HG02334.1m.fastq.gz",
  "input2": null,
  "output": "-",
  "output2": null,
  "k": 31,
  "w": 15,
  "abs_threshold": 2,
  "rel_threshold": 0.01,
  "prefix_length": 0,
  "deplete": true,
  "rename": false,
  "seqs_in": 1000000,
  "seqs_out": 13452,
  "seqs_removed": 986548,
  "seqs_removed_proportion": 0.986548,
  "bp_in": 5477122928,
  "bp_out": 5710050,
  "bp_removed": 5471412878,
  "bp_removed_proportion": 0.9989574727324798,
  "time": 125.755103875,
  "seqs_per_second": 7951,
  "bp_per_second": 43553881
}
```

## Server mode

From version `0.11.0`, it is possible to eliminate index loading overhead at the start of each filter operation by preloading the index in the memory of a local server process. Subsequent filtering commands with `--use-server` are executed by the server process using a UNIX socket. Having started a server process, the index of the first filtering command it receives persists in memory for the life of that server process, enabling subsequent filter commands to be served rapidly without hash set construction overhead.

```bash
# Start the server
deacon server start

# The first filter command loads the index as usual
deacon --use-server filter ref.idx reads.fq > /dev/null

# Subsequent filter commands use the existing index stored in memory
deacon --use-server filter ref.idx reads.fq -o filt.fq -s summary.json

# Stop the server
deacon --use-server server stop
```

## Workflow manager integration

### Nextflow (nf-core)

- Modules [`deacon_index`](https://nf-co.re/modules/deacon_index) and [`deacon_filter`](https://nf-co.re/modules/deacon_filter)
- Subworkflow [`fastq_index_filter_deacon`](https://nf-co.re/subworkflows/fastq_index_filter_deacon/)

### Galaxy
Work in progress: https://github.com/galaxyproject/tools-iuc/pull/7473

## Citation

[![biorXiv preprint](https://img.shields.io/badge/biorXiv-10.1101/2025.06.09.658732-red?&style=flat-square)](https://doi.org/10.1101/2025.06.09.658732)

>  Bede Constantinides, John Lees, Derrick W Crook. "Deacon: fast sequence filtering and contaminant depletion" *bioRxiv* 2025.06.09.658732, https://doi.org/10.1101/2025.06.09.658732

Please also consider citing the SimdMinimizers paper:

> Ragnar Groot Koerkamp, Igor Martayan. "SimdMinimizers: Computing random minimizers, *fast*" *bioRxiv* 2025.01.27.634998, https://doi.org/10.1101/2025.01.27.634998


