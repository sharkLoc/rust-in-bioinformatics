[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/mapad/README.html)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15268295.svg)](https://doi.org/10.5281/zenodo.15268295)

# mapAD

This is another attempt to write a _fast enough_ experimental ancient DNA damage aware short read mapper.
This work depends on the [rust-bio](https://rust-bio.github.io/) crate
([Köster, 2016](https://doi.org/10.1093/bioinformatics/btv573)).

mapAD uses pure backtracking on top of the bidirectional
FMD-index ([Li, 2012](https://doi.org/10.1093/bioinformatics/bts280)).
Central algorithmic ideas are inspired by
BWA-backtrack ([Li & Durbin, 2009](https://doi.org/10.1093/bioinformatics/btp324)).
Improved algorithms and error models will be incorporated step by step as needed.

Ancient DNA damage models can be included via the `SequenceDifferenceModel` trait.
The default (and only) impl is based on Udo Stenzel's ANFO/r-candy.

## Build and Install

Besides Rust, no additional dependencies are needed to compile.

0. Install/update Rust (locally, to the current user's home directory):

   `curl https://sh.rustup.rs -sSf | sh`

1. Git clone mapAD or simply download a release zip file:

   `git clone https://github.com/mpieva/mapAD.git && cd mapAD`

3. Build:

   `cargo build --release`

   The resulting binary file `mapad` is now in the subfolder `target/release/`.

4. Run!

   `cd target/release/`

   `./mapad index --reference /path/to/reference/hg19.fasta`

###### Optional

- For increased performance on modern CPUs the compiler can make use of advanced SIMD instructions if you enable AVX2
  and FMA like this (recommended).
  Please note that the resulting binary will not run on CPUs that don't support these features.

`RUSTFLAGS="-C target-feature=+avx2,+fma" cargo build --release`

or this (not recommended; reduced portability)

`RUSTFLAGS="-C target-cpu=native" cargo build --release`

Please note that the resulting binary is not necessarily portable between different CPU architectures.

- The number of `v`s passed to the program determines the level of verbosity:

`mapad -vv index ...` or `mapad -vv map ...`

- `mapAD` can be built as a fully static binary with `musl` libc:
    1. Install target platform requirements: `rustup target add x86_64-unknown-linux-musl`
    2. Install `musl-gcc` on the building system (Ubuntu: `sudo apt install musl-tools`)
    3.
  Build: `RUSTFLAGS="-C target-feature=+crt-static -C link-self-contained=yes" cargo build --release --target x86_64-unknown-linux-musl`

## Usage

The subprograms `mapad index` and `mapad map` will index the reference and map reads to it, respectively.
Adding the ` --help` flag will print a list of available and required command line options.

### Indexing Reference Genomes

`./mapad index --reference /path/to/reference/hg19.fasta` will store six index files in the directory of the input
FASTA (`/path/to/reference/hg19.fasta{.tbw, .tle, .toc, .tpi, .trt, .tsa}`).

### Mapping

#### Damage Parameters

##### Scoring Model

The scoring model is derived from Udo
Stenzel's [ANFO/r-candy](https://bitbucket.org/ustenzel/r-candy) ([Green et al., 2010](https://doi.org/10.1126/science.1188021)
; SOM3).
The symbols $f$ (5'-overhang parameter),
$t$ (3'-overhang parameter),
$d$ (double-stranded deamination rate),
$s$ (single-stranded deamination rate),
$D$ (divergence / base error rate), and
$i$ (indel rate) correspond to command line options.

Double-stranded library preparation: The probability of a
position $i \in [0 .. l - 1]$
being inside an overhang is
$p_{\text{fwd}} = f^{i + 1}$ and
$p_{\text{rev}} = t^{l - i}$, respectively.
Single-stranded library
preparation: $p_{\text{fwd}} = f^{i + 1} + t^{l - 1} - f^{i + 1} t^{l - 1}$
,
$p_{\text{rev}} = 0$.

Effective deamination
probabilities: $p_C = s p_{\text{fwd}} + d(1 - p_{\text{fwd}})$
,
$p_G = s p_{\text{rev}} + d(1 - p_{\text{rev}})$

Sequencing errors and evolution ($q$ denotes the
PHRED-scaled base quality):
$\epsilon = \frac{10^{-q / 10}}{3} + \frac{D}{3} - \frac{10^{-q / 10}}{3} \frac{D}{3}$

|     |  A  |  C  |  G  |  T  |
|:---:|:---:|:---:|:---:|:---:|
|  A  | $1 - 3 \epsilon$ | $\epsilon$ | $\epsilon + p_G - 4 \epsilon p_G$ | $\epsilon$ |
|  C  | $\epsilon$ | $1 - 3 \epsilon - p_C + 4 \epsilon p_C$ | $\epsilon$ | $\epsilon$ |
|  G  | $\epsilon$ | $\epsilon$ | $1 - 3 \epsilon - p_G + 4 \epsilon p_G$ | $\epsilon$ |
|  T  | $\epsilon$ | $\epsilon + p_C - 4 \epsilon p_C$ | $\epsilon$ | $1 - 3 \epsilon$ |

All of the above probabilities are $\log_2$ transformed.
The optimal penalty given the base in the read, its quality, and its position is subtracted from the penalty. During
alignment the resulting per-base scores are summed up to form alignment scores. We use affine gap-costs with a gap
opening penalty of
$\log_2(i)$ (InDel rate). The gap extension penalty is
currently fixed to a "representative mismatch" penalty (the score of a virtual "ordinary" mismatch not caused by
deamination or poor base quality).

#### Examples

Tests have shown that we can achieve good sensitivity and specificity allowing `-p 0.03` mismatches and relatively high
deamination parameters (see "50% Deamination Parameters" below).

**Over-specification of damage parameters does not seem to have a significant negative impact on alignment accuracy.**

##### 1) 50% Deamination Parameters

The following example aligns reads to an existing index of the hg19 reference. These damage settings cause C -> T
mismatches on both 5'- and 3'-ends to be free (no penalty). The penalties for those substitutions of course increase as
the center of a read is approached.

###### Local Mapping (One Computer)

```bash
./mapad -vv map \
--threads 32                                               `# Number of threads to use (runs on all available cores when set to 0).` \
--library single_stranded                                  `# Library preparation protocol (single- or double-stranded)` \
-p 0.03                                                    `# Allowed mismatches under `-D` base error rate (similar to BWA backtrack)` \
-f 0.5                                                     `# Five-prime overhang parameter` (generic overhang parameter when "--library" is set to "double_stranded") \
-t 0.5                                                     `# Three-prime overhang parameter` (not used if "--library" is set to "double_stranded") \
-d 0.02                                                    `# Deamination rate in double-stranded parts` \
-s 1.0                                                     `# Deamination rate in single-stranded overhangs` \
-i 0.001                                                   `# InDel rate (corresponds to gap open penalty)` \
-x 0.5                                                     `# Gap extension penalty as a fraction of the repr. mismatch penalty` \
--reads "${input_bam}" \
--reference "/path/to/reference/hg19.fasta"                `# Prefix of index files` \
--output "${output_bam}"
```

###### Distributed Mapping (Many Computers Over Network)

The following example starts a dispatcher node and then spawns multi-threaded workers on SGE cluster nodes that have
more than 30GB of free RAM.
Start the dispatcher:

   ```bash
   ./mapad -v map \
   --dispatcher \
   # ... (see local example)
   ```

Spawn workers:

   ```bash
   qsub -N "mapAD_worker" -pe "smp" 1-32 -t 1-128 -l "h_vmem=30G,s_vmem=30G,virtual_free=30G,mem_free=30G,class=*" -j "y" -R "y" -b "y" ./mapad -vv worker --threads 8 --host $(hostname)
   ```

## Mapping Quality

Mapping qualities are comparable with those produced by `BWA`. However, an alignment that maps equally well to two
positions in the genome would be assigned a MAPQ of 3 by `mapAD`, whereas `BWA` would assign a MAPQ of 0. To filter out
reads mapping to multiple positions a MAPQ threshold of > 5-10 roughly corresponds to a `BWA`-specific threshold of > 0.

Here, $AS_\text{best}$ and
$AS_\text{subopt}$ refer to the non-log-transformed
alignment scores ($2^\text{AS}$) of the best and a
suboptimal alignment, respectively. $|\text{alignment}|$
refers to the number of position an alignment maps to.

- Unique (best alignment maps to one position): $1$
- Pseudo-unique (best alignment maps to one position, but, with worse score, also to
  others): $\frac{\text{AS}_\text{best}}{\text{AS}_\text{best} + \sum{\text{AS}_\text{subopt} |\text{subopt}|}}$
- Non-unique (best alignment maps to multiple
  positions): $\frac{1}{|\text{best}|}$

Mapping quality is defined as the PHRED-scaled probability that an alignment is incorrect. Hence the above probabilities
are PHRED-scaled, and, for better compatibility with `BWA`, confined to the interval
$[0..37]$.

A recommended equivalent to a mapping quality threshold of 25 for BWA mapped data is 20 for mapAD output.

## BAM Output

mapAD uses BAM auxiliary data fields to report suboptimal alignments in a `bwa aln`-like fashion. `X0`: Number of best
hits (multi-mapped alignment), `X1`: Number of suboptimal alignments, `XA`: 5 best suboptimal alignments in the format
`chr,(+|-)pos,cigar,MD,NM,num_of_hits,AS`, `XT`: Type of mapping (`(N|U|R)`), `XS`: Best suboptimal alignment score.

<!--- FIXME: Needs to be updated with current numbers
## Hardware Requirements

- The standalone program needs ~100GB RAM when running on 32 cores to align against the human reference genome `hg19`. 
  The mapping speed is roughly comparable to `bwa aln` using "ancient parameters" (`-l 16500 -o 2 -n 0.01`). 
  To parallelize alignments, `mapAD` will use all idle CPU cores on the machine it is run on (this behaviour can be 
  controlled via `--threads`).
  
- When using the distributed mapping feature (dispatcher/workers), each worker needs around 
  `(10 + 0.5 * |threads|)` GB of RAM while the dispatcher node uses around 70GB RAM since it keeps the suffix array in memory.
 
- Indexing `hg19`, however, needs around 160GB of RAM. This will be improved in future versions.
-->

## Known Issues

- Memory consumption of both mapping and indexing (see [Hardware Requirements](#hardware-requirements))
- No awareness of paired-end sequencing (pairs need to be merged before mapping)
- No seeding (it's not very effective for short reads, but could easily be implemented for longer ones. Probably
  with less negative impact on (aDNA-)sensitivity than seeding in `BWA`).

