# isONclust3

isONclust3 is a tool for clustering either PacBio Iso-Seq reads, or Oxford Nanopore reads into clusters, where each cluster represents all reads that came from a gene family. Output is a tsv file with each read assigned to a cluster-ID and a folder 'fastq' containing one fastq file per cluster generated. Detailed information is available in the [isONclust3 paper](https://doi.org/10.1093/bioinformatics/btaf207).

# Table of contents
1. [Installation](#installation)
2. [Output](#output)
3. [Running isONclust3](#Running)
4. [Contact](#contact)
5. [Credits](#credits)

# Installation <a name="installation"></a>
The installation of isONclust3 requires users to install the Rust programming language onto their system.

## Installing Rust <a name="installingrust"></a>
You can install rust via<br />

`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` (for macOS and Linux or other Unix-based OS). For Windows please follow the instructions on the following site: https://forge.rust-lang.org/infra/other-installation-methods.html .<br />

## Installing isONclust3

You can install isONclust3 from the cargo package manager or from source.

### From Cargo package manager <a name="installation cargo"></a>
When you have installed Rust run  `cargo install isONclust3` to install the binary globally.

### From GitHub source <a name="installation source"></a>
```
git clone https://github.com/aljpetri/isONclust3.git
cd isONclust3
cargo build --release
```
The executable is then located in folder `target/release`.

### Testing the installation <a name="installation"></a>
Run `target/release/isONclust3 --fastq example_data/test_data.fastq --mode ont --outfolder example_out --seeding minimizer --post-cluster`.

This generates an output directory in the repository folder. The fastq_files folder inside clustering should now contain 94 fastq files(each representing one cluster).

# Running isONclust3 <a name="Running"></a>
IsONclust3 can be used on either Pacbio data or ONT data.

```
isONclust3 --fastq {input.fastq} --mode ont  --outfolder {outfolder}         # Oxford Nanopore reads
isONclust3 --fastq {input.fastq} --mode pacbio  --outfolder {outfolder}      # PacBio reads

```

The `--mode ont` argument means setting `--k 13 --w 21`. The `--mode pacbio` argument is equal to setting `--k 15 --w 51`.

# Output <a name="output"></a>

### Clustering information
The output consists of a tsv file `final_clusters.tsv` present in the specified output folder. In this file, the first column is the cluster ID and the second column is the read accession. For example:
```
0 read_X_acc
0 read_Y_acc
...
n read_Z_acc
```
if there are n reads there will be n rows. Some reads might be singletons.
### Clusters
IsONclust outputs the reads in .fastq file format with each file containing the reads for the respective cluster. The .fastq files are located in the `fastq_files` directory that is created in the given outfolder.

## Contact <a name="contact"></a>
If you encounter any problems, please raise an issue on the issues page, you can also contact the developer of this repository via:
alexander.petri[at]math.su.se


## Credits <a name="credits"></a>

Please cite this study when using isONclust3:

Alexander J Petri, Kristoffer Sahlin, De novo clustering of large long-read transcriptome datasets with isONclust3, Bioinformatics, 2025;, btaf207, [https://doi.org/10.1093/bioinformatics/btaf207](https://doi.org/10.1093/bioinformatics/btaf207).

