# piscem

`piscem` is a rust wrapper for a next-generation index + mapper tool (still currently written in C++17).

Notes
=====

 - If you are primarily interested in simply *using* `piscem`, you can obtain pre-compiled binaries from the GitHub [releases](https://github.com/COMBINE-lab/piscem/releases/tag/v0.10.3) page
for linux x86-64, OSX x86-64, and OSX ARM. Likewise, `piscem` can be installed using [bioconda](https://bioconda.github.io/recipes/piscem/README.html).  The instructions below are 
primarily for those who need to *build* `piscem` from source.

 - **Please ensure that the user file handle limit is set to 2048**.  This may already be set (and should be fine already on OSX), but you can accomplish this by executing:

```
$ ulimit -n 2048
```

before running `piscem`.

- **The pre-compiled executables (including those installed via bioconda)** require that the underlying processor support [the BMI2 instruction set](https://en.wikipedia.org/wiki/X86_Bit_manipulation_instruction_set). If you are running on a CPU from ~2012 or earlier, these instructions may not be available and the pre-compiled executable may not work. In that case, you should compile from source using the `NO_BMI2` environement variable (i.e. `NO_BMI2=TRUE cargo build --release`).

Building
========

This repository currently pulls in (as submodules) `piscem-cpp` and `cuttlefish`, and then uses cargo + the cmake crate to build the C++ code.  It then calls out to the main C++ function from `main.rs`.  The idea is that in this framework, code can slowly be migrated from C++ -> Rust in a piecemeal fashion, while the overall top-level repo remains a "rust build".  Importantly, `piscem` unifies and simplifies the other tools, making them runnable via a single executable and providing an improved command line interface.

To build `piscem`, first check out this repository **with recursive dependencies**:

```
git clone --recursive https://github.com/COMBINE-lab/piscem.git
```

if you have accidentally checked out the repo without the `--recursive` flag, you can change into the top-level directory and run:

```
git submodule update --init --recursive
```

Once you have checked out the repository, you can build `piscem` with 

```
cargo build --release
```

It is worth noting that the build process respects the `CC` and `CXX` environment flags, so if you wish to use a specific C++ compiler, you can run:

```
CC=<path_to_c_compiler> CXX=<path_to_cxx_compiler> cargo build --release
```

Compling this code requires a C++17 capable compiler, so if your default compiler does not have these capabilities, please be sure to pass the appropriate 
flags along to `cargo build` with a sufficiently capable compiler.

Other details about building
----------------------------

The build process requries access to static libraries for both `zlib` and `libbz2`. If these are not in your standard path, you can provide them via the `RUSTFLAGS` option as:

```
RUSTFLAGS='-L <path_to_directory_with_libraries>' cargo build --release
```

Finally, on some systems, you may get a strange linking error related to relocatable symbols. In that case, you can pass the `NOPIE` option to the build process as follows:

```
NOPIE=TRUE cargo build --release
```

Note that the `CC`, `CXX`, `RUSTFLAGS` and `NOPIE` environment variables are all "stackable" and you can provide any subset of them that you need during build.

Usage
=====

```
Indexing and mapping to compacted colored de Bruijn graphs

Usage: piscem [OPTIONS] <COMMAND>

Commands:
  build     Index a reference sequence
  map-sc    map reads for single-cell processing
  map-bulk  map reads for bulk processing
  help      Print this message or the help of the given subcommand(s)

Options:
  -q, --quiet    be quiet (no effect yet for cDBG building phase of indexing)
  -h, --help     Print help
  -V, --version  Print version
```

`piscem` has several sub-commands; `build`, `map-sc` and `map-bulk` described below.

Info for different sub-commands


build
-----

> **Note**
> Since the build process makes use of [KMC3](https://github.com/refresh-bio/KMC) for a k-mer enumeration step, which, in turn, makes use of intermediate files to keep memory usage low, **you will likely need to increase the default number of file handles that can be open at once**.  Before running the `build` command, you can do this by running `ulimit -n 2048` in the terminal where you execute the `build` command.  You can also put this command in any script that you will use to run `piscem build`, or add it to your shell initalization scripts / profiles so that it is the default for new shells that you start

The build subcommand indexes one or more reference sequences, building a piscem index over them. The usage for the command is as so:

```
Index a reference sequence

Usage: piscem build [OPTIONS] --klen <KLEN> --mlen <MLEN> --threads <THREADS> --output <OUTPUT> <--ref-seqs <REF_SEQS>|--ref-lists <REF_LISTS>|--ref-dirs <REF_DIRS>>

Options:
  -s, --ref-seqs <REF_SEQS>    ',' separated list of reference FASTA files
  -l, --ref-lists <REF_LISTS>  ',' separated list of files (each listing input FASTA files)
  -d, --ref-dirs <REF_DIRS>    ',' separated list of directories (all FASTA files in each directory will be indexed, but not recursively)
  -k, --klen <KLEN>            length of k-mer to use
  -m, --mlen <MLEN>            length of minimizer to use
  -t, --threads <THREADS>      number of threads to use
  -o, --output <OUTPUT>        output file stem
      --keep-intermediate-dbg  retain the reduced format GFA files produced by cuttlefish that describe the reference cDBG (the default is to remove these)
  -w, --work-dir <WORK_DIR>    working directory where temporary files should be placed [default: .]
      --overwrite              overwite an existing index if the output path is the same
      --no-ec-table            skip the construction of the equivalence class lookup table when building the index
  -h, --help                   Print help
  -V, --version                Print version
```

The parameters should be reasonably self-expalanatory.  The `-k` parameter is the k-mer size for the underlying colored compacted de Bruijn graph, and the `-m` parameter is the minimizer size used to build the [`sshash`](https://github.com/jermp/sshash) data structure.  The quiet `-q` flag applies to the `sshash` indexing step (not yet the CdBG construction step) and will prevent extra output being written to `stderr`.

Finally, the `-r` argument takes a list of `FASTA` format files containing the references to be indexed.  Here, if there is more than one reference, they should be provided to `-r` in the form of a `,` separated list.  For example, if you wish to index `ref1.fa`, `ref2.fa`, `ref3.fa` then your invocation should include `-r ref1.fa,ref2.fa,ref3.fa`.  The references present within all of the `FASTA` files will be indexed by the `build` command.

> **Note**
> You should ensure that the `-t` parameter is less than the number of physical cores that you have on your system. _Specifically_, if you are running on an Apple silicon machine, it is highly recommended that you set `-t` to be less than or equal to the number of **high performance** cores that you have (rather than the total number of cores including efficiency cores), as using efficiency cores in the `piscem build` step has been observed to severely degrade performance.

map-sc
------

The `map-sc` command maps single-cell sequencing reads against a piscem index, and produces a RAD format output file that can be processed by [`alevin-fry`](https://github.com/COMBINE-lab/alevin-fry).  The usage is as so:

```
map reads for single-cell processing

Usage: piscem map-sc [OPTIONS] --index <INDEX> --geometry <GEOMETRY> --read1 <READ1> --read2 <READ2> --threads <THREADS> --output <OUTPUT>

Options:
  -i, --index <INDEX>              input index prefix
  -g, --geometry <GEOMETRY>        geometry of barcode, umi and read
  -1, --read1 <READ1>              path to list of read 1 files
  -2, --read2 <READ2>              path to list of read 2 files
  -t, --threads <THREADS>          number of threads to use
  -o, --output <OUTPUT>            path to output directory
      --check-ambig-hits           enable extra checking of the equivalence classes of k-mers that were too ambiguous to be included in chaining (may improve specificity, but could slow down
                                   mapping slightly)
  -m, --max-ec-card <MAX_EC_CARD>  determines the maximum cardinality equivalence class (number of (txp, orientation status) pairs) to examine if performing check-ambig-hits [default: 256]
  -h, --help                       Print help
  -V, --version                    Print version
```

Here, you can provide multiple files to `-1` and `-2` as a `,` separated list just like the `-r` argument to the `build` command. Of course, it is important to ensure that you provide that information in the same order to the `-1` and `-2` flags.  The `--geometry` flag specifies the geometry of the UMIs and cell barcodes for the reads; you can find a description [here](https://github.com/COMBINE-lab/piscem/blob/main/README.md#geometry).

map-bulk
--------

The `map-bulk` command maps bulk sequencing reads against a piscem index. The tool performs _non-spliced_ alignment, and therefore is applicable to e.g. metagenomic reads against a set of metagenomes, DNA-seq alignment against one or more references, or RNA-seq alignment against a transcriptome (but not a genome). The program and produces a bulk RAD format output file that can be processed by [`piscem-infer`](https://github.com/COMBINE-lab/piscem-infer) to estimate the abundances of all references in the index given the mapped reads.  The usage is as so:

```
map reads for bulk processing

Usage: piscem map-bulk --index <INDEX> --read1 <READ1> --read2 <READ2> --threads <THREADS> --output <OUTPUT>

Options:
  -i, --index <INDEX>      input index prefix
  -1, --read1 <READ1>      path to list of read 1 files
  -2, --read2 <READ2>      path to list of read 2 files
  -t, --threads <THREADS>  number of threads to use
  -o, --output <OUTPUT>    path to output directory
  -h, --help               Print help
  -V, --version            Print version
```

Here, you can provide multiple files to `-1` and `-2` as a `,` separated list just like the `-r` argument to the `build` command. Of course, it is important to ensure that you provide that information in the same order to the `-1` and `-2` flags.

geometry
--------

The geometry parameter `--geometry|-g` can take either a specific geometry name, or a generic specifier string.  The current valid names are `chromium_v2` and `chromium_v3` for 10x Genomics Chromium v2 and v3 protocols respectively. The custom format is as follows: you must specify the content of read 1 and read 2 in terms of the barcode, UMI, and mappable read sequence. A specification looks like this:

```
1{b[16]u[12]x:}2{r:}
```

In particular, this is how one would specify the 10x Chromium v3 geometry using the custom syntax.  The format string says that the read pair should be interpreted as read 1 `1{...}` followed by read 2 `2{...}`.  The syntax inside the `{}` says how the read should be interpreted.  Here `b[16]u[12]x:` means that the first 16 bases constitute the barcode, the next 12 constitute the UMI, and anything that comes after that (if it exists) until the end of read 1 should be discarded (`x`).  For read 2, we have `2{r:}`, meaning that we should interpret read 2, in it's full length, as biological sequence.

It is possible to have pieces of geometry repeated, in which case they will be extracted and concatenated together.  For example, `1{b[16]u[12]b[4]x:}` would mean that we should obtain the barcode by extracting bases 1-16 (1-based indexing) and 29-32 and concatenating them togehter to obtain the full barcode.  A specification that is followed by a specific length (i.e. a number in `[]` like `b[10]` or `x[4]` is said to be *bounded*).  The specification string can have many bounded pieces, but only one *unbounded* piece (and unbounded piece is a specifier like `r` or `x`, followed by `:`).  Likewise, since the `:` specifier means to extract this piece until the end of the string, the unbounded specifier must be the last specifier in the description of each read (_if it occurs_).

