# RAxTax - `raxtax` Accelerates Taxonomic Classification

`raxtax` is a fast and efficient k-mer-based non-Bayesian taxonomic classifier for barcoding DNA sequences.
A preprint of our manuscript is available at [BioRxiv](https://www.biorxiv.org/content/10.1101/2025.03.11.642618v1).
This project is heavily inspired by the SINTAX algorithm [[1]](#1).

## Installation

### Precompiled Binaries

Precompiled binaries are available from the [Github Release page](https://github.com/noahares/raxtax/releases/) for Linux, Windows and macOS (Intel and Apple Silicon).

### [crates.io](https://crates.io/crates/raxtax)

`raxtax` can be installed via:
```sh
cargo install raxtax
```

### Build From Source

To install from source (with maximum performance):
```sh
git clone https://github.com/noahares/raxtax.git
cargo build --profile=ultra
```

## Usage

```sh
Usage: raxtax [OPTIONS] --database-path <DATABASE_PATH> --query-file <QUERY_FILE>

Options:
  -d, --database-path <DATABASE_PATH>  Path to the database fasta or bin file
  -i, --query-file <QUERY_FILE>        Path to the query file
      --skip-exact-matches             If used for mislabling analysis, you want to skip exact sequence matches
      --tsv                            Output primary result file in tsv format
      --only-db                        Create binary database and exit
      --skip-db                        Don't create the binary database for the reference sequences
  -c, --clean                          Remove binary database and checkpoint files after a successful run
      --raw-confidence                 Don't adjust confidence values for 1 exact match
  -t, --threads <THREADS>              Number of threads
                                       If 0, uses all available threads [default: 0]
  -o, --prefix <PREFIX>                Output prefix [default: raxtax]
      --redo                           Force override of existing output files
      --pin                            Use thread pinning
  -v, --verbose...                     Increase logging verbosity
  -q, --quiet...                       Decrease logging verbosity
  -h, --help                           Print help
  -V, --version                        Print version
```

### Simple Example

See [`example/`](https://github.com/noahares/raxtax/tree/main/example) for example data to run `raxrax`.

The files `example/diptera_references.fasta` and `example/diptera_queries.fasta` contain *Diptera* sequences for a quick example run of `raxtax`.
**If you did not clone this repository to acquire the `raxtax` executable, you may have to download these files from GitHub (via cloning the repository or manual download).**

From the project root (otherwise adjust the paths) run:
```sh
# with raxtax installed
<path/to/raxtax> -d example/diptera_references.fasta -i example/diptera_queries.fasta -o example/example_run

# from source
cargo run --profile=ultra -- -d example/diptera_references.fasta -i example/diptera_queries.fasta -o example/example_run
```

This creates a new folder `example/example_run` with the taxonomic assignments and confidence values for each query in `raxtax.out` and various log messages (including exact sequence matches) in `raxtax.log`.

### Input Database (`-d`)

The input format for the database file is FASTA.
It is possible to provide the file as a Gzip archive (`.gzip` or `.gz`).

Sequence identifier should have the form `tax=<lineage>;`.
Everything after `tax=` is parsed as a comma-separated list of lineage nodes and is terminated by a semicolon.
Lineages may have different depth, the only requirement is that they can be parsed into a multi-furcating tree.
We use phylum to sequence for the examples in this README to aid readability.
For example, an entry may look like this:

```sh
# example sequence
>metadata;tax=Arthropoda,Insecta,Diptera,Muscidae,Musca,Musca_domestica;
ACTCGATAC
```

### Input Query (`-i`)

The format for query sequences is also FASTA (again, Gzip archives are supported), but more relaxed than the database format:

```sh
# example sequence
>query1
ACTCGATAC
```

### Output (`-o`)

`raxtax` will produce 2 primary output files under the prefix specified with `-o` (defaults to `raxtax/`).

1. `<PREFIX>/raxtax.out` is the full result of the analysis. It contains for each query sequence a line for each database sequence where the confidence value is above 0.01 (confidence values are between 0 and 1).
**If no database sequence fulfills this criterion, a single line containing the best match is printed**.
In this case, values are rounded up to 0.01.
The format is (tab separated):

```sh
query1    Arthropoda,Insecta,Diptera,Muscidae,Musca,Musca_domestica    1.0,1.0,0.8,0.68,0.52,0.31  0.67456  0.71234
```

The first part is simply the query label.
The second part is the taxonomic lineage of the respective database sequence.
The third part contains the confidence values for each level of the taxonomic lineage.
**It is important to understand that these values are always relative to the sequences in the database and therefore should be interpreted carefully.**
To this end, we include a fourth and fifth value indicating the confidence in the reported lineage (local signal) and confidence in the confidence values themselves on sequence level (global signal).
These are again between 0 and 1, where 1 indicates high confidence.
For more information, see the manuscript.

2. `<PREFIX>/raxtax.log` is the log file where more or less useful information accumulates.
With the default command line parameters, only warnings and errors will be collected.
With `-v` additional information about runtime and the size of the database are printed.
With `-vv` debug messages are also included.
Generally, if a warning or error occurs, the program will inform you through `stderr` and refer you to the log file if needed.
This file also contains information about exact matches and inconsistent lineages (possible mislabeling).

4. (_optional_ via `--tsv`) `<PREFIX>/raxtax.tsv` is pretty much the same as the first output file but slightly more convenient for viewing in your favorite spreadsheet editor.
In this file, the taxonomic lineage and confidence values are interleaved, and the query sequence is also printed at the end:

```sh
query1  Arthropoda  1.0 Insecta 1.0 Diptera 0.8 Muscidae    0.68    Musca   0.52    Musca_domestica 0.31    0.67456 0.71234 ACTCGATAC
```

### Other Options

`--skip-exact-matches` may be useful when running the database against itself to identify mislabeled sequences. Per default, `raxtax` skips over exact sequences matches if there is **exactly one match** and outputs a confidence of 1.0 for the exact match.
This option makes it so that any exact match is not considered for the analysis of a query sequence.

`--only-db` can be used if you just want to create a binary database for the reference sequences and then run `raxtax` for many different query files.
If the reference database is large this will save significant time on repeat execution.
This option does not require `-i` to be specified and `raxtax` will terminate after creating the binary database.

`--skip-db` will skip the creation of the binary database.
This is only recommended if you run with that database only once or it is very small.

`--clean` will remove the binary database and checkpoint files (`raxtax.json` and `raxtax.ckp`) after a successful run. This is mainly intended for long runs that might get interrupted, but the binary database is not needed afterwards.

`--raw-confidence` will output the real confidence values if there is 1 exact match instead of setting the confidence to 1.0.
This is mostly a debugging option, but might come in handy for specific usecases.

`--threads` may be omitted most of the time and `raxtax` will use as many cores as your system has available. Because the analysis is _embarrassingly parallel_, this is a sensible default.
However, if you experience problems due to hyper-threading, you might want to reduce the number of threads, to increase parallel efficiency.

`--redo` will enable overwriting of existing output files. **Use at your own risk!**

`--pin` enables thread-pinning. On Linux, this will try to avoid hyper-threading and crossing sockets whenever possible. On other platforms, threads will still be pinned but in order of their IDs **which might affect performance negatively.**

## Important Implementation Details

We suggest a threshold of 0.01 for confidence values to be considered (`F64_OUTPUT_ACCURACY` also in `src/utils.rs`).
For technical reasons this is the number of digits after the decimal point, so currently this is 2.

If the database contains duplicate sequences that have different lineages above the lowest taxonomic level a warning will be emitted.

## Gigantic Databases

Per default, `raxtax` uses 32-bit indices for indexing reference sequences.
This makes things a lot faster, but trying to run it with more than $2^{32}$ (~4 Billion) reference sequences will fail.
In this case, compile it with `--features huge_db` to use 64-bit indices (on 64-bit systems).
An error message will be displayed if too many reference sequences are used with the 32-bit indices version.

## Checkpointing

Since v.1.3.0 `raxtax` comes with default checkpointing to prevent data loss in case of unforeseen crashes (i.e. terminated by the OS scheduler). `raxtax` will create a binary database of the reference sequences in the output directory for faster loading on subsequent runs (disable this with `--skip-db`). Then, every time a query finishes, it will be written to the output files.
To restart from the latest checkpoint, run `raxtax` with the same options for `--raw_confidence <bool> --skip_exact_matches <bool> --tsv <bool> --prefix <path>`.
The database path will be recovered from the checkpoint file.
The log file and result files will be appended to in subsequent runs.

**Caution**: Running with `--redo` will override any checkpoints!

**Advanced usage**: Checkpoint information is saved in `<prefix>/raxtax.json` in JSON format and therefore can be manually adjusted to make the checkpoint cooperate if e.g. the database file was moved.
The list of already processed queries is kept in `<prefix>/raxtax.ckp` and can be adjusted if some queries need to be re-run.
**Do this at your own risk!**

## References
<a id="1">[1]</a>
Edgar, Robert C. "SINTAX: a simple non-Bayesian taxonomy classifier for 16S and ITS sequences." biorxiv (2016): 074161.

## Copyright
 This work is licensed under CC BY-NC-SA 4.0.
 To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

