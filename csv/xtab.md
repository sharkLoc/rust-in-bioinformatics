# xtab

🦀 CSV command line utilities

## install

##### setp1：install cargo first

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

##### step2:

```bash
cargo install xtab
# or

git clone https://github.com/sharkLoc/xtab.git
cd xtab
cargo b --release
# mv target/release/xtab to anywhere you want 
```

## usage

```bash
xtab -- CSV command line utilities
Version: 0.0.8

Authors: sharkLoc <mmtinfo@163.com>
Source code: https://github.com/sharkLoc/xtab.git

xtab supports reading and writing gzip/bzip2/xz format file.
Compression level:
  format   range   default   crate
  gzip     1-9     6         https://crates.io/crates/flate2
  bzip2    1-9     6         https://crates.io/crates/bzip2
  xz       1-9     6         https://crates.io/crates/xz2


Usage: xtab [OPTIONS] [CSV] <COMMAND>

Commands:
  addheader  Set new header for CSV file [aliases: ah]
  csv2xlsx   Convert CSV/TSV files to XLSX file [aliases: c2x]
  dim        Dimensions of CSV file
  drop       Drop or Select CSV fields by columns index
  flatten    flattened view of CSV records [aliases: flat]
  freq       Build frequency table of selected column in CSV data
  head       Print first N records from CSV file
  pretty     Convert CSV to a readable aligned table [aliases: prt]
  replace    Replace data of matched fields
  reverse    Reverses rows of CSV data [aliases: rev]
  sample     Randomly select rows from CSV file using reservoir sampling
  search     Applies the regex to each field individually and shows only matching rows
  slice      Slice rows from a part of a CSV file
  tail       Print last N records from CSV file
  transpose  Transpose CSV data [aliases: trans]
  uniq       Unique data with keys
  xlsx2csv   Convert XLSX to CSV format [aliases: x2c]
  view       Show CSV file content
  help       Print this message or the help of the given subcommand(s)

Global Arguments:
  -d, --delimiter <CHAR>      Set delimiter for input csv file, e.g., in linux -d $'\t' for tab, in powershell -d `t for tab [default: ,]
  -D, --out-delimite <CHAR>   Set delimiter for output CSV file, e.g., in linux -D $'\t' for tab, in powershell -D `t for tab [default: ,]
      --log <FILE>            If file name specified, write log message to this file, or write to stderr
      --compress-level <INT>  Set compression level 1 (compress faster) - 9 (compress better) for gzip/bzip2/xz output file, just work with option -o/--out [default: 6]
  -v, --verbosity...          control verbosity of logging, [-v: Error, -vv: Warn, -vvv: Info, -vvvv: Debug, -vvvvv: Trace, defalut: Debug]
  [CSV]                   Input CSV file name, if file not specified read data from stdin

Global FLAGS:
  -H, --no-header  If set, the first row is treated as a special header row, and the original header row excluded from output
  -q, --quiet      Be quiet and do not show any extra information
  -h, --help       prints help information
  -V, --version    prints version information

Use "xtab help [command]" for more information about a command
```
