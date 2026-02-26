# DNA palindrome finder
This tool is designed to identify and extract palindromic sequences and data from a DNA sequence. 

A palindrome or inverted repeat in DNA is a sequence of nucleotides that is followed by its complement sequence.
This command-line tool uses fast sequence alignment algorithms coded in rust to locate such palindromes within a sequence.

It also contains a few scripts that are useful for analyzing the output data.

## Getting started
### Installation
Download the binary in the releases that match your OS and architecture.

This tool only contains binaries for windows and linux. To generate a binary for another system,
install [Rust](https://www.rust-lang.org/tools/install) and clone the repository.
From the terminal, run 
```
cargo build --release
```
Inside the 'target/release' folder, there will be an executable which you can run.


## Algorithm
This tool has two algorithms:

### Fixed mismatch
This is the most common type of algorithm found on the internet for palindrome search.
It scans the sequence base by base, and upon finding a complement it extends outwards in both directions, sometimes allowing a fixed number of mismatches.
This does not account for indels or gaps, and is also slower. However, it is useful for comparing this program with existing tools

```
./palindrome-finder fixed-mismatch --input input.fasta --fa --output results.tsv --length 10 --gap 5 --mismatch 4
```
This will allow for 4 mismatches total within the palindrome
Run with `-h` for more details

### WFA
The better alternative utilizes the wave-finding algorithm, a very fast sequence alignment algorithm.
It accounts for indels and mismatches, uses multiple pruning methods, and is much faster.

### Example usage
```
./palindrome-finder wfa --input input.fastq --fq --output results.tsv --length 10 --gap 5  --match-bonus 1 --mismatch-penalty 1 --x-drop 25 --mismatch-proportion 0.05
```
This will allow for 5% mismatches within the palindrome. The scoring mechanism and X-drop factor allow for further pruning. Run with `-h` for more details

## Output
The output is a TSV file containing the palindromes found, containing the following 8 statistics
```
Start  End  Arm-Length  Gap  Length  Mismatches  Seq-name  Sequence
...
```
Note that the arm and gap lengths are approximated


## Scripts
This tool contains a few scripts for data analysis and processing. 

### Adapter script
This is a script for aligning adapter sequences to help filter out bad nanopore reads which often contain adapter sequences in the middle. It uses the [block-aligner](https://github.com/Daniel-Liu-c0deb0t/block-aligner) library to align a file of adapter sequences and identify them and their location.

It also allows the user to filter out real adapter sequences present at the beginning of the the read

#### Example usage 
```
./palindrome-finder adapters --input input.fq --output results.tsv --fq --adapters-file-path adapters.fa --longest-adapter 100 --score-cutoff 11 --remove-t
```
The addition of `--remove-t` applies the filter described above
Run with `-h` for more details

### Python scripts

Three python scripts have been implemented for data analysis. 

1. plot_graph -- Plots a graph with statistics from the output file
2. print_statistic -- Prints a desired statistic, for example longest palindrome
3. filter_output -- Filters the output to only include certain palindromes, for example repeat masking the outputq

#### Example usage
```
python plot_graph.py --input results.tsv --length
```
This will plot a graph of length to frequency using the output from the algorithm

## Fine tuning the inputs 
The tool is may not be able to find all desired palindromes, and requires some fine tuning of the input values to the algorithm. 

Generally speaking, increasing the X-drop threshold will allow for more consecutive mismatches, and increasing the mismatch proportion allows for more overall mismatches. The default values should be sufficient for most cases.

A [paper](https://figshare.com/articles/journal_contribution/A_NOVEL_ALGORITHMFOR_DETECTION_OF_PALINDROME_DNA/27897300?file=50772369) has been published which details the algorithm, process, and input variables much more thoroughly.

