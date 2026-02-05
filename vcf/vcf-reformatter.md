# VCF Reformatter: What is it?

Did it ever happen that you had VCF files and you wanted to have a look at the data as you would do with a normal table? `VCF Reformatter` is here for your rescue!

A Rust command-line tool for parsing and reformatting VCF (Variant Call Format) files, with support for VEP (Variant Effect Predictor) and SnpEff annotations. This tool flattens complex VCF files into tab-separated values (TSV) format for easier downstream analysis.
Also incredibly useful for quick checks to your data!

# VCF Reformatter

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Rust](https://img.shields.io/badge/rust-1.70+-blue.svg)](https://www.rust-lang.org)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Performance](https://img.shields.io/badge/performance-10k--30k%20variants%2Fsec-green.svg)]()
[![Release](https://img.shields.io/github/v/release/flalom/vcf-reformatter)](https://github.com/flalom/vcf-reformatter/releases)

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-purple.svg?style=flat)](https://anaconda.org/bioconda/vcf-reformatter)
[![Conda](https://anaconda.org/bioconda/vcf-reformatter/badges/version.svg)](https://anaconda.org/bioconda/vcf-reformatter)

**Transform complex VCF files into clean, analyzable tables with ease**

*A high-performance Rust tool for flattening VCF files with intelligent VEP and SnpEff annotation handling*

</div>

---

## 🚀 Quick Start

```` bash
# Download binary from releases (easiest! You download and use it)
wget https://github.com/flalom/vcf-reformatter/releases/latest/download/vcf-reformatter-v0.3.0-linux-x86_64
chmod +x vcf-reformatter-v0.3.0-linux-x86_64

# Transform your VCF file  
./vcf-reformatter-v0.3.0-linux-x86_64 sample.vcf.gz

# Generate MAF output ⚠️ (in beta!)
./vcf-reformatter-v0.3.0-linux-x86_64 sample.vcf.gz --output-format maf
````
OR Via Bioconda
```bash
conda install -c bioconda vcf-reformatter
# or
# mamba install vcf-reformatter -c bioconda
```
OR install from [crates.io](https://crates.io/crates/vcf-reformatter):
```bash
cargo install vcf-reformatter
```
OR build from source (you need Rust toolchain):
```` bash
git clone https://github.com/flalom/vcf-reformatter.git
cd vcf-reformatter
cargo build --release
./target/release/vcf-reformatter sample.vcf.gz
````
## ⚠️ Experimental MAF support
**MAF output is currently in beta testing (v0.3.0). Known limitations:**

- VAF calculation needs refinement for some genotype patterns
- Multi-sample handling requires validation
- Use with caution in production workflows

**Memory considerations for MAF:**
- Files >100K variants: Monitor memory usage
- Files >1M variants: Ensure adequate RAM (16GB+)


## 🎯 Why VCF Reformatter?

**The Problem:** VCF files are notoriously difficult to analyze. Complex nested annotations, semicolon-separated INFO fields, and multi-transcript VEP annotations make downstream analysis a nightmare.

**The Solution:** VCF Reformatter flattens everything into clean, readable TSV format that works seamlessly with Excel, R, Python, and any analysis tool (⚠️ beware Excel auto-correction!).

### Before & After

**Before (Raw VCF):**
```
chr1  69511  .  A  G  1294.53  .  DP=65;AF=1;CSQ=G|missense_variant|MODERATE|OR4F5|ENSG00000186092...
```
**After (Reformatted TSV):**
```
CHROM  POS    REF  ALT  QUAL     INFO_DP  INFO_AF  CSQ_Allele  CSQ_Consequence      CSQ_SYMBOL
chr1   69511  A    G    1294.53  65       1        G           missense_variant     OR4F5
```

## ✨ Key Features

| Feature                                 | Description                                      | Benefit                                              |
|-----------------------------------------|--------------------------------------------------|------------------------------------------------------|
| 🧬 **VEP/SnpEff Annotation Parsing**    | Intelligent handling of CSQ/ANN annotations      | No more manual parsing of complex VEP/SnpEff output  |
| 👀 **Automatic Annotation Recognition** | Automatic detection of CSQ/ANN annotations       | Saving even more time now for both VEP and SnpEff    |
| 🔀 **Smart Transcript Handling**        | Most severe, first only, or split transcripts    | Choose the analysis approach that fits your needs    |
| 🚀 **Parallel Processing**              | Multi-threaded processing up to 30k variants/sec | Process large cohorts in minutes, not hours          |
| 📁 **Native Compression**               | Direct `.vcf.gz` reading & gzip output           | Seamless workflow with compressed/uncompressed files |
| 🎯 **Production Ready**                 | Comprehensive error handling & logging           | Reliable for automated pipelines                     |
| 🐳 **Container Support**                | Docker & Singularity ready                       | Deploy anywhere, from laptops to HPC clusters        |

---

## 📦 Installation

### Option 1: Download Pre-compiled Binaries (Easiest!)
**No Rust installation required** - just download and run:

1. **Go to [Releases](https://github.com/flalom/vcf-reformatter/releases/latest)**
2. **Download the binary for your platform:**
    - `vcf-reformatter-v0.3.0-linux-x86_64` → **Linux** (most users)
    - `vcf-reformatter-v0.3.0-linux-x86_64-static` → **HPC clusters** (works everywhere)
    - `vcf-reformatter-v0.3.0-windows-x86_64.exe` → **Windows**
    - `vcf-reformatter-v0.3.0-macos-x86_64` → **Intel Mac**
    - `vcf-reformatter-v0.3.0-macos-arm64` → **Apple Silicon Mac** (M1/M2/M3/M4)

3. **Make executable and run:**
````bash
# Linux/Mac
chmod +x vcf-reformatter-*
./vcf-reformatter-* --help

# Windows
# Just double-click or run from command prompt
# C++ might be required, if not already installed
````

### Option 2: **Build from Source**
````bash
git clone https://github.com/flalom/vcf-reformatter.git
cd vcf-reformatter
cargo build --release
````

### Option 3: Docker
```shell script
# Build the container
docker build -t vcf-reformatter .

# Run with your data
docker run --rm -v $(pwd):/data vcf-reformatter /data/sample.vcf.gz
```
### Option 4: Singularity
```shell script
# Build Singularity image
singularity build vcf-reformatter.sif Singularity

# Run on HPC cluster
singularity run --bind $PWD:/data vcf-reformatter.sif /data/sample.vcf.gz -j 16
```

## 🛠️ Usage

### Basic Usage
```shell script
# Simple conversion
vcf-reformatter input.vcf.gz

# Most severe consequence only (recommended for analysis)
vcf-reformatter input.vcf.gz -t most-severe

# All transcripts in separate rows (comprehensive)
vcf-reformatter input.vcf.gz -t split
```
### Annotation Type Detection
```shell script
# Auto-detect annotation type (recommended)
vcf-reformatter input.vcf.gz -a auto

# Force VEP processing
vcf-reformatter vep_annotated.vcf.gz -a vep -t most-severe

# Force SnpEff processing  
vcf-reformatter snpeff_annotated.vcf.gz -a snpeff -t most-severe
```
### Advanced Usage
```shell script
# High-performance processing with compression
vcf-reformatter large_cohort.vcf.gz \
  --transcript-handling most-severe \
  --threads 0 \
  --compress \
  --output-dir results/ \
  --prefix my_analysis \
  --verbose

# Optimized for HPC environments
vcf-reformatter huge_dataset.vcf.gz -t most-severe -j 32 -o /scratch/results/ -c -v
```
### Complete Options
```
Usage: vcf-reformatter [OPTIONS] <INPUT_FILE>

Arguments:
  <INPUT_FILE>  Input VCF file (supports .vcf.gz)

Options:
  --output-format <FORMAT>     Output format [default: tsv] 
                               [values: tsv, maf]
  --center <CENTER>            Sequencing center for MAF output  
  --ncbi-build <BUILD>         Genome build 
                               [default: GRCh38]
  --sample-barcode <BARCODE>   Sample identifier for MAF output
  -t, --transcript-handling <MODE>  How to handle multiple transcripts
                                   [default: first]
                                   [values: most-severe, first, split]
  -a, --annotation-type <N>        Which annotations to parse VEP/SnpEff
                                   [default: auto]
                                   [values: snpeff, vep, auto]
  -j, --threads <N>                Thread count (0 = auto-detect) [default: 1]
  -o, --output-dir <DIR>           Output directory [default: current]
  -p, --prefix <PREFIX>            Output file prefix [default: input filename]
  -c, --compress                   Compress output with gzip
  -v, --verbose                    Detailed performance statistics
  -h, --help                       Show help
  -V, --version                    Show version
```

## 🧬 Transcript Handling Modes

VCF files with VEP annotations often contain multiple transcript annotations per variant. Choose the strategy that fits your analysis:

### 🎯 Most Severe (`--transcript-handling most-severe`)
**Best for:** Clinical analysis, variant prioritization
```shell script
vcf-reformatter input.vcf.gz -t most-severe

# for maf output
vcf-reformatter input.vcf.gz -t most-severe --output-format maf
```
Selects the transcript with the most severe consequence (stop_gained > missense_variant > synonymous, etc.)

### ⚡ First Only (`--transcript-handling first`) *[Default]*
**Best for:** Quick analysis, performance-critical workflows
```shell script
vcf-reformatter input.vcf.gz  # Uses first transcript by default
```

Processes only the first transcript annotation (fastest option)

### 📊 Split All (`--transcript-handling split`)
**Best for:** Comprehensive analysis, transcript-level studies
```shell script
vcf-reformatter input.vcf.gz -t split
```
Creates separate rows for each transcript (most detailed output)

## 📈 Performance

### Benchmarks
- **Small files** (< 1K variants): ~5,000 variants/sec
- **Medium files** (1K-10K variants): ~15,000 variants/sec
- **Large files** (10K+ variants): ~30,000 variants/sec

### Optimization Tips
```shell script
# Auto-detect optimal thread count
vcf-reformatter input.vcf.gz -j 0

# For files > 10K variants, use parallel processing
vcf-reformatter input.vcf.gz -t most-severe -j 0 -v

# Combine with compression for large outputs
vcf-reformatter input.vcf.gz -t split -j 0 -c -v
```

## 📊 Output Format

### File Structure
VCF Reformatter generates two files:
- `{prefix}_header.txt` - Original VCF header and metadata
- `{prefix}_reformatted.tsv` - Flattened tabular data

### Column Types
1. **Standard VCF**: `CHROM`, `POS`, `ID`, `REF`, `ALT`, `QUAL`, `FILTER`
2. **INFO Fields**: `INFO_DP`, `INFO_AF`, `INFO_AC`, etc.
3. **VEP Annotations**: `CSQ_Allele`, `CSQ_Consequence`, `CSQ_SYMBOL`, `CSQ_Gene`, etc.
3. **SnpEff Annotations**: `ANN_Allele`, `ANN_Annotation_Impact`, `ANN_Gene_Name`, `ANN_Distance`, etc.
4. **Sample Data**: `SAMPLE1_GT`, `SAMPLE1_DP`, `SAMPLE1_AD`, etc.

### Example Output VEP
```
CHROM  POS    ID     REF  ALT  QUAL     FILTER  INFO_DP  CSQ_Consequence      CSQ_SYMBOL  SAMPLE1_GT
chr1   69511  .      A    G    1294.53  PASS    65       missense_variant     OR4F5       1/1
chr1   69761  rs123  C    T    892.15   PASS    42       synonymous_variant   OR4F5       0/1
```

### Example Output SnpEff
```
CHROM  POS    ID     REF  ALT  QUAL     FILTER  INFO_DP  ANN_Annotation          ANN_Gene_Name  SAMPLE1_GT
chr1   69761  rs587   C    T  730  PASS   .     214      synonymous_variant      OR4F5          0/1
chr1   924024  .      A    G  53   PASS   .     409      5_prime_UTR_variant     SAMD11         1/1
```

## 🔧 Integration Examples

### With R
```textmate
# Read compressed output directly
library(data.table)
data <- fread("output_reformatted.tsv.gz")

# Quick variant summary
summary(data$CSQ_Consequence)
```

### With Python
```textmate
import pandas as pd

# Load and analyze
df = pd.read_csv("output_reformatted.tsv.gz", sep="\t", compression="gzip")
df['CSQ_Consequence'].value_counts()
```

### In Workflows
```shell script
# Nextflow pipeline
vcf-reformatter ${vcf} -t most-severe -j ${task.cpus} -o results/ -c

# Snakemake rule
shell: "vcf-reformatter {input.vcf} -t most-severe -j {threads} -o {params.outdir} -c"
```

## 🐳 Container Usage

### Docker
```shell script
# Build once
docker build -t vcf-reformatter .

# Run anywhere
docker run --rm \
  -v $(pwd):/data \
  vcf-reformatter \
  /data/input.vcf.gz \
  -t most-severe -j 4 -o /data/results/ -c
```

### Singularity (HPC)
```shell script
# On HPC cluster
singularity run \
  --bind $PWD:/data \
  --bind /scratch:/scratch \
  vcf-reformatter.sif \
  /data/large_cohort.vcf.gz \
  -t most-severe -j 16 -o /scratch/results/ -c -v
```
## 🧪 Use Cases

| Use Case | Command | Why It Works |
|----------|---------|--------------|
| **Clinical Variant Review** | `vcf-reformatter variants.vcf.gz -t most-severe` | Prioritizes clinically relevant consequences |
| **Population Analysis** | `vcf-reformatter cohort.vcf.gz -t first -j 0 -c` | Fast processing of large cohorts |
| **Transcript Studies** | `vcf-reformatter genes.vcf.gz -t split -v` | Comprehensive transcript-level analysis |
| **Quick Data Exploration** | `vcf-reformatter sample.vcf.gz` | Simple, fast conversion for immediate analysis |
| **HPC Batch Processing** | `vcf-reformatter huge.vcf.gz -t most-severe -j 32 -c` | Optimized for high-performance computing |

## 🚀 What's New in v0.3.0
- ✅ **MAF Output Support (in Beta⚠️)** - Direct conversion to Mutation Annotation Format
- ✅ **Auto-metadata Detection (in Beta⚠️)** - Extracts center/sample info from VCF headers for MAF
- ✅ **Memory-Efficient Processing (streaming)** - Chunked streaming for large files (>>100K variants)
- ✅ **Enhanced Error Handling** - Better processing of malformed files
- ✅ **Comprehensive Testing** - 70+ test cases ensure reliability

## Previous Releases
### 🚀 What's New in v0.2.0
- ✅ **SnpEff Support** - Full ANN field parsing with intelligent detection
- ✅ **Smart Auto-Detection** - Automatically identifies VEP vs SnpEff annotations
- ✅ **Enhanced Error Handling** - Better processing of malformed or headerless files

## TODOs
- ~~Add SnpEff support✅~~
- ~~Output MAF format option✅~~
- Add `stdin` to combine with other tools, such as `bcftools`
- Support for multi-sample VCF files in MAF output

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Add tests** for new functionality
4. **Commit** your changes: `git commit -am 'Add feature'`
5. **Push** to the branch: `git push origin feature-name`
6. **Submit** a pull request

### Development Setup
```shell script
git clone https://github.com/flalom/vcf-reformatter.git
cd vcf-reformatter
cargo test  # Run the test suite
cargo run -- data/sample.vcf.gz -v  # Test with sample data
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **VCF Format Contributors** - For the standard that enables genomic data sharing
- **VEP Team** - For the powerful variant annotation framework
- **Rust Community** - For the incredible ecosystem that makes this possible
- **Bioinformatics Community** - For feedback and feature requests

---

## Frequently Asked Questions

### Q: Which transcript handling mode should I use?
- **Clinical analysis**: `--transcript-handling most-severe`
- **Quick exploration**: `--transcript-handling first`
- **Comprehensive analysis**: `--transcript-handling split`

### Q: How does this compare to other VCF tools?
VCF Reformatter is specifically designed for:
- Converting complex VEP/SnpEff annotations to tabular format
- Handling multiple transcripts intelligently
- High-performance parallel processing
- Easy integration with R/Python workflows

### Q: Can I use this in production pipelines?
Yes! VCF Reformatter is designed for production use with:
- Comprehensive error handling
- Docker/Singularity support
- Automated testing
- Stable CLI interface

### Q: What's the difference between TSV and MAF output?
- **TSV**: Direct flattening of VCF fields (default)
- **MAF (beta)**: Standardized cancer genomics format for downstream tools

### Q: What if I get out-of-memory errors?
- Use TSV format instead of MAF: `vcf-reformatter file.vcf.gz -j 0 -c`
- Enable verbose mode to monitor: `vcf-reformatter file.vcf.gz -v`

___

## 📞 Support

- **📋 Issues**: [GitHub Issues](https://github.com/flalom/vcf-reformatter/issues)
- **📧 Email**: [fl@flaviolombardo.site](mailto:fl@flaviolombardo.site)

---

<div align="center">

**⭐ Star this repo if VCF Reformatter helps your research!**

Made with ❤️ by [Flavio Lombardo](https://github.com/flalom)

</div>



