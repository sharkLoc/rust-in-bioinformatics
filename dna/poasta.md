<h1 align="center">🍝 POASTA</h1>
<h2 align="center">Fast, gap-affine sequence-to-graph and partial order aligner</h2>

<p>&nbsp;</p>

POASTA is a fast and optimal partial order aligner that supports gap-affine alignment penalties. Inspired by
a recent [algorithm for pairwise alignment](https://github.com/smarco/WFA2-lib), it can exploit exact matches
between the query and the graph, greatly speeding up the alignment process.

<img src="doc/algo_intro.jpeg" width="800">

POASTA is based on the A* algorithm and accelerates alignment through three algorithmic innovations:

1. A novel heuristic for POA that prioritizes alignment states with a low minimum remaining gap cost (light-colored squares);
   i.e. states where the unaligned query sequence length is similar to the path lengths to the POA graph end node τ.
2. Reducing the number of computed alignment states by combining the A* algorithm with a depth-first search component,
   greedily aligning matches between the query and a path in the graph (black arrow). Adjacent insertion and deletion states are only queued when encountering a mismatch (squares with dashed borders).
3. Using knowledge about superbubble topology to prune states not part of the optimal solution. POASTA checks whether the
   best-case alignment paths (blue and green arrows) from a state under test (red square) can improve over the costs of implicitly
   opened gaps from prior reached bubble exits (bordered squares).

All examples use the linear gap cost model with $\Delta_m = 0, \Delta_x = 4$ and $\Delta_g = 2$.

POASTA is [published in Oxford Bioinformatics](https://academic.oup.com/bioinformatics/article/41/1/btae757/7942505)
and can be cited as:

> van Dijk, L. R., Manson, A. L., Earl, A. M., Garimella, K. V., & Abeel, T. (2025). Fast and exact gap-affine partial
> order alignment with POASTA. _Bioinformatics_, 41(1), btae757.

## Installation

### Conda

- Bioconda packages are still work in progress.

### Building POASTA from source

#### Rust compiler

POASTA is written in Rust, and to build and install it, you'll need a recent version of the Rust compiler. The
minimum supported Rust version is 1.70.

1. Download and install `rustup`: https://rustup.rs/
2. Run `rustup update`

#### Install from crates.io

POASTA is available on crates.io, and can be installed using `cargo`:

```bash
cargo install poasta
```
This command installs the executables `lasagna` and `poasta` that you can access from anywhere.

To use poasta as a dependency, use `cargo add`:

```bash
cargo add poasta
```

#### Install from git
Rust's build tool, `cargo` supports installing a cli tool straight from github. To do this, simply run the following command. Note that we set the rust compiler flags `-C` and `target-cpu=native` to ensure the compiler optimises the build for your CPU. If you wish to make the binary portable, then you can remove these flags.

```bash
RUSTFLAGS="-C target-cpu=native" cargo install --git https://github.com/broadinstitute/poasta
```
This command installs the executables `lasagna` and `poasta` that you can access from anywhere (the actual binaries are typically stored in `$HOME/.cargo/bin/poasta`)

#### Building POASTA

Alternatively, you can clone the repository and build `POASTA` that way.

1. Clone the repository.

   ```bash
   git clone https://github.com/broadinstitute/poasta
   ```

2. Move into the directory.

   ```bash
   cd poasta
   ```

3. Build using `cargo`. We enable a flag to ensure the compiler uses all features of your machine's CPU.
   To maximize portability of the binary, however, remove the `RUSTFLAGS="..."` part.

   ```bash
   RUSTFLAGS="-C target-cpu=native" cargo build --release
   ```

4. The built `poasta` executable will be available in the directory `target/release/`


## Usage

### Creating an alignment from scratch

To create a multiple sequence alignment from scratch, simply give it a FASTA. The FASTA file can be compressed
with gzip (filename should have a `.gz` extension).

```bash
poasta align -o graph.poasta sequences.fasta
```

This will output the graph to a binary file called `graph.poasta`. POASTA can reuse this file to later align
additional sequences to it.

### Re-using an earlier alignment

To align additional sequences to an earlier created partial order graph, specify the existing graph using the
`-g` option.

```bash
poasta align -g graph.poasta -o graph_updated.poasta new_sequences.fasta
```

This will import the graph stored in `graph.poasta`, then align the additional sequences in `new_sequences.fasta` to
this graph, and outputs the updated graph to `graph_updated.poasta`.

### Importing an existing multiple sequence alignment in FASTA format

POASTA can import an existing multiple sequence alignment stored in columnar FASTA format (e.g., those
created by other tools like `mafft` or `spoa`), create the equivalent partial order graph from the existing alignment,
and then align new sequences to it. To achieve this, specify the FASTA MSA with extension .fa, .fna, or .fasta with
the `-g` option (file is also allowed to be compressed with gzip if it has a `.gz` suffix).

```bash
poasta align -g msa.fasta -o graph_updated.poasta new_sequences.fasta
```

### Other output formats

The default output format is POASTA's binary file format storing the graph data structure.
This the recommended output because you can always convert this binary file
to other formats using `poasta view`.
If you don't need the binary file, however,
you can specify the output format with the `-O` option:

Other supported formats:

* DOT (GraphViz): Specify with `-O dot`
* FASTA MSA: Specify with `-O fasta`
* Graph GFA: Specify with `-O gfa`

For example, to visualize the graph directly with GraphViz:

```bash
poasta align -Odot sequences.fasta | dot -Tpng -o graph.png
```

Note that we did not specify an output file for `poasta align` (we did not use the `-o` option). If no output filename
is given, standard output will be used, so the output can be directly piped to `dot` to create the visualization.

### Using `poasta view` to convert between output formats

By default, POASTA stores the computed graph/MSA in its own binary file format.
To convert a previously computed MSA to other file formats, you can use `poasta view`.
The supported output formats are the same as described above, i.e.:

* DOT (GraphViz): Specify with `-O dot`
* FASTA MSA: Specify with `-O fasta`
* Graph GFA: Specify with `-O gfa`

Example:

```bash
# Convert to GFA
poasta view -Ogfa existing_msa.poasta > poa_graph.gfa

# Convert to FASTA MSA
poasta view -Ofasta existing_msa.poasta > poa_msa.fasta
```

## Gap penalty configuration

POASTA supports both standard affine gap penalties and two-piece affine gap penalties for more flexible gap modeling.

### Standard affine gap penalties

By default, POASTA uses standard affine gap penalties with the following defaults:
- Gap opening penalty: 6
- Gap extension penalty: 2
- Mismatch penalty: 4

You can customize these penalties:

```bash
poasta align -g 8 -e 3 -n 5 sequences.fasta
```

### Two-piece affine gap penalties

For more sophisticated gap modeling, POASTA supports two-piece affine gap penalties, which use different penalties for short and long gaps. This can better model biological insertion/deletion patterns.

To enable two-piece affine mode, provide comma-separated values for both gap opening and extension penalties:

```bash
# Two-piece affine: short gaps (8,2) and long gaps (24,1)
poasta align -g 8,24 -e 2,1 -n 5 sequences.fasta
```

The first values (8,2) apply to short gaps, while the second values (24,1) apply to longer gaps. The extension penalty for short gaps should be higher than for long gaps to properly model the two-piece behavior.

### Alignment modes

POASTA supports different alignment modes:
- `global`: End-to-end alignment (default)
- `semi-global`: Query aligned globally, but graph gaps are free at ends
- `ends-free`: Free gaps at sequence beginnings/ends for both query and graph

```bash
poasta align -m ends-free sequences.fasta
```

Note: Currently, `ends-free` and `semi-global` modes are only supported with `global` alignment.


## Related repositories

* [poa-bench](https://github.com/broadinstitute/poa-bench) - Benchmark POASTA against other POA tools
* [spoa-rs](https://github.com/broadinstitute/spoa-rs) - Rust bindings to SPOA

