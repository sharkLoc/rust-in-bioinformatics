# Universal Single-Cell Genomics Preprocessing package

![PyPI](https://img.shields.io/pypi/v/precellar)
![PyPI - Downloads](https://img.shields.io/pypi/dm/precellar)
![Continuous integration](https://github.com/regulatory-genomics/precellar/workflows/test-python-package/badge.svg)
![GitHub Repo stars](https://img.shields.io/github/stars/regulatory-genomics/precellar?style=social)

This tool is an automated pipeline for preprocessing single-cell genomics data.
It is designed to take raw data (fastq files) from a variety of single-cell genomics
platforms and a seqspec file as input, and output a count matrix (RNA) or a fragment file (ATAC)
for downstream analysis. The seqspec files for common platforms can be found here: https://github.com/IGVF/seqspec.

## Installation

### Stable version

```
pip install precellar
```

### Development version

```
pip install 'git+https://github.com/regulatory-genomics/precellar.git#egg=precellar&subdirectory=python'
```

## Examples

Each example dataset below contains approximately 2.5 million fastq records.

> [!NOTE]
> You need to **change the paths to the reference genome** in the examples below.
> The reference genome should be downloaded and indexed before running the examples.
> STAR genome index for human and mouse can be downloaded from [here](https://www.10xgenomics.com/support/software/cell-ranger/downloads#reference-downloads).
> BWA genome index can be build using the `make_bwa_index` function.

### Gene Expression

<details>
<summary>10x scRNA-seq v3</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/10x_rna_v3.yaml')

data = precellar.examples.txg_rna_v3()
assay.add_illumina_reads('rna')
assay.update_read('rna-R1', fastq=data['R1'])
assay.update_read('rna-R2', fastq=data['R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCm39-2024-A"), 
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)
```

</details>


<details>
<summary>sci-RNA-seq3</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/sci_rna_seq3.yaml')

data = precellar.examples.sci_rna_seq3()
assay.update_read('R1', fastq=data['R1'])
assay.update_read('R2', fastq=data['R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCm39-2024-A"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)
```

</details>


<details>
<summary>MARS-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/mars_seq.yaml')

data = precellar.examples.mars_seq()
assay.add_illumina_reads(modality='rna')
assay.update_read('rna-R1', fastq=data['R1'])
assay.update_read('rna-R2', fastq=data['R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCm39-2024-A"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)
```

</details>

<details>
<summary>MGI DNBelab C4 scRNA-seq v1</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/dnbelabc4_rna_v1_dark.yaml')

data = precellar.examples.dnbelabc4_rna_v1()
assay.update_read('R1', fastq=data['R1'])
assay.update_read('R2', fastq=data['R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCh38-2024-A"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)
```

</details>

### Chromatin accessibility and protein-DNA interactions

<details>
<summary>10x scATAC-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/10x_atac.yaml')

data = precellar.examples.txg_atac()
assay.add_illumina_reads('atac', forward_strand_workflow=True)
assay.update_read('atac-I2', fastq=data['I2'])
assay.update_read('atac-R1', fastq=data['R1'])
assay.update_read('atac-R2', fastq=data['R2'])
atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCh38"),
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>

<details>
<summary>MGI DNBelab C4 scATAC-seq v1</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/dnbelabc4_atac_v1.yaml')

data = precellar.examples.dnbelabc4_atac_v1()
assay.update_read('R1', fastq=data['R1'])
assay.update_read('R2', fastq=data['R2'])

qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCh38"),
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(qc)
```

</details>


<details>
<summary>dscATAC-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/dscATAC.yaml')

data = precellar.examples.dsc_atac()
assay.update_read('R1', fastq=data['R1'])
assay.update_read('R2', fastq=data['R2'])

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCm39"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


<details>
<summary>scifi-ATAC-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/scifi_atac.yaml')

data = precellar.examples.scifi_atac()
assay.update_read('I2', fastq=data['I2'])
assay.update_read('R1', fastq=data['R1'])
assay.update_read('R2', fastq=data['R2'])

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("BWA_MEM2_index/Zea_mays"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


### Multi-Omics

<details>
<summary>10x single-cell multiome (Gene expression + ATAC)</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/10x_rna_atac.yaml')

data = precellar.examples.txg_multiome()
assay.add_illumina_reads('rna')
assay.update_read('rna-R1', fastq=data['rna-R1'])
assay.update_read('rna-R2', fastq=data['rna-R2'])

assay.add_illumina_reads('atac', forward_strand_workflow=True)
assay.update_read('atac-I2', fastq=data['atac-I2'])
assay.update_read('atac-R1', fastq=data['atac-R1'])
assay.update_read('atac-R2', fastq=data['atac-R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCm39-2024-A"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCm39"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


<details>
<summary>SHARE-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/share_seq.yaml')

data = precellar.examples.share_seq()
assay.update_read('rna-I1', fastq=data['rna-I1'])
assay.update_read('rna-R1', fastq=data['rna-R1'])
assay.update_read('rna-R2', fastq=data['rna-R2'], min_len=10, max_len=10)

assay.update_read('atac-I1', fastq=data['atac-I1'])
assay.update_read('atac-R1', fastq=data['atac-R1'])
assay.update_read('atac-R2', fastq=data['atac-R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("/data/Public/STAR_reference/refdata-gex-GRCh38-2024-A/star/"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCh38"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


<details>
<summary>SNARE-seq</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/snare_seq.yaml')

data = precellar.examples.snare_seq()
assay.update_read('rna-R1', fastq=data['rna-R1'])
assay.update_read('rna-R2', fastq=data['rna-R2'])

assay.update_read('atac-I1', fastq=data['atac-I1'])
assay.update_read('atac-R1', fastq=data['atac-R1'])
assay.update_read('atac-R2', fastq=data['atac-R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("/data/Public/STAR_reference/GRCm39/"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCm39"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


<details>
<summary>Droplet Paired-Tag</summary>

```python
import precellar

assay = precellar.Assay('https://raw.githubusercontent.com/regulatory-genomics/precellar/refs/heads/main/seqspec_templates/droplet_paired_tag.yaml')

data = precellar.examples.droplet_paired_tag()
assay.add_illumina_reads('rna')
assay.update_read('rna-R1', fastq=data['rna-R1'])
assay.update_read('rna-R2', fastq=data['rna-R2'])

assay.add_illumina_reads('atac')
assay.update_read('atac-I2', fastq=data['atac-I2'])
assay.update_read('atac-R1', fastq=data['atac-R1'])
assay.update_read('atac-R2', fastq=data['atac-R2'])

rna_qc = precellar.align(
    assay,
    precellar.aligners.STAR("STAR_reference/refdata-gex-GRCm39-2024-A"), 
    modality="rna",
    output="gene_matrix.h5ad",
    output_type="gene_quantification",
    num_threads=8,
)
print(rna_qc)

atac_qc = precellar.align(
    assay,
    precellar.aligners.BWAMEM2("/data/Public/BWA_MEM2_index/GRCm39"),
    modality="atac",
    output='fragments.tsv.zst',
    output_type='fragment',
    num_threads=8,
)
print(atac_qc)
```

</details>


For more information, please refer to the documentation: https://lab.kaizhang.org/precellar/.

