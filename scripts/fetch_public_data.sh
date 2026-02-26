#!/bin/bash
set -e

# Directories
DATA_DIR="test_data"
DNA_DIR="$DATA_DIR/dna"
VCF_DIR="$DATA_DIR/vcf"
PROT_DIR="$DATA_DIR/proteomics"
BAM_DIR="$DATA_DIR/bam"

mkdir -p "$DNA_DIR" "$VCF_DIR" "$PROT_DIR" "$BAM_DIR"

echo "Fetching public datasets..."

# 1. SARS-CoV-2 Genome (FASTA)
# NCBI RefSeq NC_045512.2
SARS_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895/GCF_009858895.2_ASM985889v3/GCF_009858895.2_ASM985889v3_genomic.fna.gz"
echo "Downloading SARS-CoV-2 genome..."
curl -s -o "$DNA_DIR/sars_cov_2.fna.gz" "$SARS_URL"
# Keep it compressed as many tools handle gz

# 2. Small VCF from bcftools test suite
VCF_URL="https://raw.githubusercontent.com/samtools/bcftools/develop/test/view.vcf"
echo "Downloading example VCF..."
curl -s -o "$VCF_DIR/example.vcf" "$VCF_URL"

# 3. Small PDB Structure (1CRN - Crambin, small protein)
PDB_URL="https://files.rcsb.org/download/1CRN.pdb"
echo "Downloading small PDB structure (1CRN)..."
curl -s -o "$PROT_DIR/1CRN.pdb" "$PDB_URL"

# 4. PhiX Genome (for metagenomics/mock community)
# NCBI RefSeq NC_001422.1
PHIX_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/819/615/GCF_000819615.1_ViralProj14015/GCF_000819615.1_ViralProj14015_genomic.fna.gz"
echo "Downloading PhiX genome..."
curl -s -o "$DNA_DIR/phix.fna.gz" "$PHIX_URL"

# Create a mock metagenome (SARS-CoV-2 + PhiX)
META_DIR="$DATA_DIR/metagenomics"
mkdir -p "$META_DIR"
echo "Creating mock metagenome (SARS-CoV-2 + PhiX)..."
# Decompress temporarily to concat
gunzip -c "$DNA_DIR/sars_cov_2.fna.gz" > "$META_DIR/temp_sars.fna"
gunzip -c "$DNA_DIR/phix.fna.gz" > "$META_DIR/temp_phix.fna"
cat "$META_DIR/temp_sars.fna" "$META_DIR/temp_phix.fna" > "$META_DIR/mock_community.fna"
rm "$META_DIR/temp_sars.fna" "$META_DIR/temp_phix.fna"

# 5. Try to fetch a small BAM if possible, otherwise rely on synthetic SAM
# Using a specific commit or stable link if found, otherwise skipping.
# I'll skip BAM download to avoid 404s and rely on synthetic SAM in generate_test_data.py

echo "Public data fetch complete."
