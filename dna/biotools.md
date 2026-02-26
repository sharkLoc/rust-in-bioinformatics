# Biotools

These are just trivial bioinformatics tools that are convenient to have available on the command line.

![Build](https://github.com/jimrybarski/biotools/actions/workflows/build.yml/badge.svg) ![Tests](https://github.com/jimrybarski/biotools/actions/workflows/tests.yml/badge.svg)

#### Installation

`cargo install biotools`  

#### Build

`git clone git@github.com:jimrybarski/biotools.git && cd biotools && cargo build --release`  

#### Test

`cargo test`

#### Coordinate system

Coordinates are given in zero-based, half-open intervals (i.e. the same as Python, C, Rust, etc.).

#### Commands 

You can add `--help` after any subcommand for subcommand-specific options.  

```
Simple bioinformatics tools for sequence analysis and manipulation

Usage: biotools <COMMAND>

Subcommands:
  reverse-complement   Converts a nucleic acid sequence to its reverse complement.
  length               Computes the length of a sequence.
  gc-content           Computes the GC content of a nucleic acid sequence.
  pairwise-local       Performs a local pairwise alignment of two sequences.
  pairwise-semiglobal  Performs a semiglobal pairwise alignment of two sequences.
  pairwise-global      Performs a global pairwise alignment of two sequences.
  help                 Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

### Reverse complement

There are no options. Spaces and dashes are allowed to permit usage with gap-containing pairwise alignments.

```bash
$ biotools reverse-complement GATTACA
TGTAATC
$ biotools reverse-complement GATT ACA-TTGA
TCAA-TGT AATC
```

### Length

There are no options. Spaces and dashes are allowed to permit usage with gap-containing pairwise alignments.
```
$ biotools length GATTACA
7
$ biotools length GAT  C   TACA
8
$ biotools length GAT-CTACA
8
```

### GC content

There are no options. Spaces and dashes are allowed to permit usage with gap-containing pairwise alignments.
```
$ biotools gc-content GGG GAA-TA
0.5000000000000000
```

### Pairwise alignment

There are three pairwise alignment commands, for local, semiglobal and global alignments. We use the aligner from ![rust-bio](https://github.com/rust-bio/rust-bio), which ultimately uses an implementation of Smith-Waterman.

```
$ biotools pairwise-local ACAGT ACGT
4 GT 5
  ||
3 GT 4

$ biotools pairwise-semiglobal ACAGT ACGT
1 ACAGT 5
  || ||
1 AC-GT 4

$ biotools pairwise-global GGGGCCCCGGGGACAGT ACGT
1 GGGGCCCCGGGGACAGT 17
              || ||
1 ------------AC-GT 4
```

Coordinates can be disabled:

```
$ biotools pairwise-semiglobal ACAGT ACGT --hide-coords
ACAGT
|| ||
AC-GT
```

Lines wrap once the alignment string exceeds 60 characters (this does not include the characters from the coordinates). You can adjust the limit:

```
$ biotools pairwise-semiglobal --line-width 30 ATTAGATCATCCGGGCAGACAGAGGTATCCCACGTTCCGTCTACCTGCTGAAGGTAATCT ATTAGTCATCCGCGCTTACAGAGGTATCCCACGTTCCGTCTACCTGCTGAAGGTAATCT
 1 ATTAGATCATCCGGGCAGACAGAGGTATCC 30
   ||||| |||||||.||..||||||||||||
 1 ATTAG-TCATCCGCGCTTACAGAGGTATCC 29

31 CACGTTCCGTCTACCTGCTGAAGGTAATCT 60
   ||||||||||||||||||||||||||||||
30 CACGTTCCGTCTACCTGCTGAAGGTAATCT 59
```
You can have biotools try both the forward sequence and reverse complement and then pick the one with the best alignment score. If the reverse complement is superior, the coordinates will be inverted for the top sequence:

```
$ biotools pairwise-semiglobal TGTAATC GGCGATTACAATGACA
1 TGTAATC 7
  |..|||.
7 TACAATG 13

$ biotools pairwise-semiglobal TGTAATC GGCGATTACAATGACA --try-rc
7 GATTACA 1
  |||||||
4 GATTACA 10
```

You can adjust the gap penalties (substitutions are always penalized a value of 1). These are given as positive numbers.
Defaults: gap open penalty: 2, gap extend penalty: 1.

```
$ biotools pairwise-semiglobal ACGT ACAAAAGT --gap-open 5 --gap-extend 5
1 ACGT 4
  |.||
5 AAGT 8

$ biotools pairwise-semiglobal ACGT ACAAAAGT --gap-open 0 --gap-extend 0
1 AC----GT 4
  ||    ||
1 ACAAAAGT 8
```

By default, 1-based inclusive coordinates are used. You can switch to 0-based, half-open coordinates (so the range you would use in Python or Rust to select the substring) with `--use-0-based-coords`:

```
biotools pairwise-semiglobal --use-0-based-coords ACAGT ACGT
0 ACAGT 5
  || ||
0 AC-GT 4

biotools pairwise-semiglobal --try-rc --use-0-based-coords TGTAATC GGCGATTACAATGACA
7 GATTACA 0
  |||||||
3 GATTACA 10
```

### Suggested aliases

The subcommands are deliberately verbose to give clarity to new users. You may prefer aliases such as these:

```
alias rc='biotools reverse-complement'
alias len='biotools length'
alias gc='biotools gc-content'
alias pw='biotools pairwise-semiglobal --try-rc'
alias pwl='biotools pairwise-local --try-rc'
alias pwg='biotools pairwise-global --try-rc'
```

