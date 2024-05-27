# fakit

🦀 a simple program for fasta file manipulation

## install latest version

```bash
cargo install --git https://github.com/sharkLoc/fakit.git
```

## install

```bash
cargo install fakit
```

## usage

```bash
Fakit: A simple program for fasta file manipulation

Version: 0.3.6

Authors: sharkLoc <mmtinfo@163.com>
Source code: https://github.com/sharkLoc/fakit.git

Fakit supports reading and writing gzip (.gz) format.
Bzip2 (.bz2) and xz (.xz) format is supported since v0.3.0.
Under the same compression level, xz has the highest compression ratio but consumes more time.

Compression level:
  format   range   default   crate
  gzip     1-9     6         https://crates.io/crates/flate2
  bzip2    1-9     6         https://crates.io/crates/bzip2
  xz       1-9     6         https://crates.io/crates/xz2


Usage: fakit [OPTIONS] <COMMAND>

Commands:
  topn     get first N records from fasta file [aliases: head]
  tail     get last N records from fasta file
  fa2fq    convert fasta to fastq file
  faidx    create index and random access to fasta files [aliases: fai]
  flatten  flatten fasta sequences [aliases: flat]
  range    print fasta records in a range
  rename   rename sequence id in fasta file
  reverse  get a reverse-complement of fasta file [aliases: rev]
  window   stat dna fasta gc content by sliding windows [aliases: slide]
  grep     grep fasta sequences by name/seq
  seq      convert all bases to lower/upper case, filter by length
  sort     sort fasta file by name/seq/gc/length
  search   search subsequences/motifs from fasta file
  shuffle  shuffle fasta sequences
  size     report fasta sequence base count
  subfa    subsample sequences from big fasta file
  split    split fasta file by sequence id
  split2   split fasta file by sequence number
  summ     simple summary for dna fasta files [aliases: stat]
  codon    show codon table and amino acid name
  help     Print this message or the help of the given subcommand(s)

Global Arguments:
  -w, --line-width <int>      line width when outputting fasta sequences, 0 for no wrap [default: 70]
      --compress-level <int>  set gzip/bzip2/xz compression level 1 (compress faster) - 9 (compress better) for gzip/bzip2/xz output file, just work with
                              option -o/--out [default: 6]
      --log <str>             if file name specified, write log message to this file, or write to stderr
  -v, --verbosity...          control verbosity of logging, [-v: Error, -vv: Warn, -vvv: Info, -vvvv: Debug, -vvvvv: Trace, defalut: Debug]

Global FLAGS:
  -q, --quiet    be quiet and do not show extra information
  -h, --help     prints help information
  -V, --version  prints version information

Use "fakit help [command]" for more information about a command

```

<br>
** any bugs please report issues **💖
