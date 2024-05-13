[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/nextpolish2/README.html)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/nextpolish2/badges/version.svg)](https://anaconda.org/bioconda/nextpolish2)
# NextPolish2

Telomere-to-telomere (T2T) genome has been emerging as a new hotspot in the field of genomics. Typically, we obtain a T2T genome with datasets including both high-accuracy PacBio HiFi long reads and Oxford Nanopore Technologies (ONT) ultra-long reads. Although genomes obtained using HiFi long reads have considerably higher qualities, however, they still contain a handful of assembly errors in regions where HiFi long reads stumble as well, such as homopolymer or low-complexity microsatellite regions. Additionally, a typical gap-filling step is accomplished using ONT ultra long reads which contain a certain amount of errors. Hence, the current T2T genomes assembled still require further improvement in terms of consensus accuracy. NextPolish2 can be used to fix these errors (SNV/Indel) in a high quality assembly. Through the built-in phasing module, it can only correct the error bases while maintaining the original haplotype consistency. Therefore, even in the regions with complex repeat elements, NextPolish2 will still not produce overcorrections. In fact, in some cases it can reduce switching errors in the heterozygous region. NextPolish2 is not an upgraded version of NextPolish, but an additional supplement for the pursuit of extremely-high-quality genome assemblies.

## Table of Contents

- [Installation](#install)
- [General usage](#usage)
- [Getting help](#help)
- [Citation](#cite)
- [License](#license)
- [Limitations](#limit)
- [Benchmarking](#benchmark)
- [FAQ](./doc/faq.md)

### <a name="install"></a>Installation

#### Installing from bioconda
```sh
conda install nextpolish2
```
#### Installing from source
##### Dependencies

`NextPolish2` is written in rust, try below commands (no root required) or refer [here](https://www.rust-lang.org/tools/install) to install `Rust` first.
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

##### Download and install

```sh
git clone --recursive git@github.com:Nextomics/NextPolish2.git
cd NextPolish2 && cargo build --release
```

##### Test

```sh
cd test && bash hh.sh
```

### <a name="usage"></a>General usage

NextPolish2 takes a genome assembly file, a HiFi mapping file and one or more k-mer dataset files from short reads as input and generates the polished genome.

1. Prepare HiFi mapping file ([winnowmap](https://github.com/marbl/Winnowmap) or [minimap2](https://github.com/lh3/minimap2/)).

```sh
meryl count k=15 output merylDB asm.fa.gz
meryl print greater-than distinct=0.9998 merylDB > repetitive_k15.txt
winnowmap -t 5 -W repetitive_k15.txt -ax map-pb asm.fa.gz hifi.fasta.gz|samtools sort -o hifi.map.sort.bam -

# or mapping using minimap2
# minimap2 -ax map-hifi -t 5 asm.fa.gz hifi.fasta.gz|samtools sort -o hifi.map.sort.bam -

# indexing
samtools index hifi.map.sort.bam
```

2. Prepare k-mer dataset files ([yak](https://github.com/lh3/yak)). Here we only produce 21-mer and 31-mer datasets, you can produce more k-mer datasets with different k-mer size.

```sh
# produce a 21-mer dataset, remove -b 37 if you want to count singletons
./yak/yak count -o k21.yak -k 21 -b 37 <(zcat sr.R*.fastq.gz) <(zcat sr.R*.fastq.gz)

# produce a 31-mer dataset, remove -b 37 if you want to count singletons
./yak/yak count -o k31.yak -k 31 -b 37 <(zcat sr.R*.fastq.gz) <(zcat sr.R*.fastq.gz) 
```

3. Run NextPolish2.

```sh
./target/release/nextPolish2 -t 5 hifi.map.sort.bam asm.fa.gz k21.yak k31.yak > asm.np2.fa

# or try with -r
# ./target/release/nextPolish2 -r -t 5 hifi.map.sort.bam asm.fa.gz k21.yak k31.yak > asm.np2.fa
```

***Optional:*** If your genome is assembled via **trio binning**. You can discard reads that have different haplotype with the reference before the mapping procedure, see [here](./doc/benchmark3.md) for an example.

#### More options

Use `./target/release/nextPolish2 -h` to see options.

### <a name="help"></a>Getting help

#### Help

   Feel free to raise an issue at the [issue page](https://github.com/Nextomics/NextPolish2/issues/new).

   ***Note:*** Please ask questions on the issue page first. They are also helpful to other users.
#### Contact
   
   For additional help, please send an email to huj\_at\_grandomics\_dot\_com.

### <a name="cite"></a>Citation

Jiang Hu, Zhuo Wang, Fan Liang, Shan-Lin Liu, Kai Ye, De-Peng Wang, NextPolish2: A Repeat-aware Polishing Tool for Genomes Assembled Using HiFi Long Reads, Genomics, Proteomics & Bioinformatics, 2024;, qzad009, https://doi.org/10.1093/gpbjnl/qzad009

### <a name="license"></a>License

NextPolish2 is only freely available for academic use and other non-commercial use.

### <a name="limit"></a>Limitations

1. NextPolish2 can only correct the regions that are mapped by HiFi reads. For regions without HiFi reads mapping (usually cause by high error rate), you can try to adjust mapping parameters.
2. The performance of NextPolish2 relies heavily on the quality of short reads.
3. NextPolish2 can only fix some structural misassemblies.

### <a name="benchmark"></a>Benchmarking

| Source                                           | Software           | QV      | Switch error rate (‱) |
| :----------------------------------------------: | ------------------ | :-----: | :---------------------: |
| [*A. thaliana*](./doc/benchmark1.md)             | Hifiasm  (primary) | 47.67   | 1.99                    |
|^(simulated data, primary contigs)^               | NextPolish2        |**65.42**| **0.35**                |
| [*A. thaliana*](./doc/benchmark2.md)             | Hifiasm  (primary) | 58.03   |                         |
| ^(Col-XJTU, primary contigs)^                    | NextPolish2        |**64.26**|                         |
| [*H. sapiens*](./doc/benchmark3.md)              | Hifiasm  (primary) | 60.25   | 0.15                    |
| ^(HG002, primary contigs)^                       | NextPolish2        |**62.87**| **0.14**                |
| [*H. sapiens*](./doc/benchmark3.md)              | Hifiasm  (trio)    | 59.77   | 0.21                    |
|^(HG002, paternal contigs)^                       | NextPolish2        |**63.49**| **0.20**                |
| [*H. sapiens*](./doc/benchmark3.md)              | Hifiasm  (trio)    | 59.78   | 0.33                    |
|^(HG002, maternal contigs)^                       | NextPolish2        |**63.29**| **0.30**                |

### Star
You can track updates by tab the **Star** button on the upper-right corner at the [github page](https://github.com/Nextomics/NextPolish2).