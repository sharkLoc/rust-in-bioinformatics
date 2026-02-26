<h1 align="center"><img width="300px" src="images/logo_HiPhase.svg"/></h1>

<h1 align="center">HiPhase</h1>

<p align="center">A tool for jointly phasing small, structural, and tandem repeat variants for PacBio sequencing data</p>

***

HiPhase will phase variant calls made from [PacBio HiFi](https://www.pacb.com/technology/hifi-sequencing/) datasets.
Key features relative to other phasing tools include:

* Joint phasing of small variants and structural variants
* Support for multi-allelic variation
* Creates [longer, correct phase blocks](docs/performance.md#summary-figure) relative to the current best practice
* No downsampling of the data
* [Novel algorithms](docs/methods.md): dual-mode allele assignment and core A* phasing algorithm
* Quality of life additions: innate multi-threading, simultaneous haplotagging and statistics generation

Authors: [Matt Holt](https://github.com/holtjma), [Chris Saunders](https://github.com/ctsa)

## Availability
* [Latest release with binary](https://github.com/PacificBiosciences/HiPhase/releases/latest)

## Documentation
* [Installation instructions](docs/install.md)
* [User guide with quickstart](docs/user_guide.md)
* [Output files](docs/user_guide.md#output-files)
* [Methods](docs/methods.md)
* [Performance](docs/performance.md)

## Citation
If you use HiPhase, please cite our publication:

[Holt, J. M., Saunders, C. T., Rowell, W. J., Kronenberg, Z., Wenger, A. M., & Eberle, M. (2024). HiPhase: Jointly phasing small, structural, and tandem repeat variants from HiFi sequencing. Bioinformatics, btae042.](https://doi.org/10.1093/bioinformatics/btae042)

Original BioRxiv pre-print:

[Holt, J. M., Saunders, C. T., Rowell, W. J., Kronenberg, Z., Wenger, A. M., & Eberle, M. (2023). HiPhase: Jointly phasing small and structural variants from HiFi sequencing. _bioRxiv_, 2023-05.](https://doi.org/10.1101/2023.05.03.539241)

## Need help?
If you notice any missing features, bugs, or need assistance with analyzing the output of HiPhase, 
please don't hesitate to open a GitHub issue.

## Support information
HiPhase is a pre-release software intended for research use only and not for use in diagnostic procedures. 
While efforts have been made to ensure that HiPhase lives up to the quality that PacBio strives for, we make no warranty regarding this software.

As HiPhase is not covered by any service level agreement or the like, please do not contact a PacBio Field Applications Scientists or PacBio Customer Service for assistance with any HiPhase release. 
Please report all issues through GitHub instead. 
We make no warranty that any such issue will be addressed, to any extent or within any time frame.

### DISCLAIMER
THIS WEBSITE AND CONTENT AND ALL SITE-RELATED SERVICES, INCLUDING ANY DATA, ARE PROVIDED "AS IS," WITH ALL FAULTS, WITH NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTIES OF MERCHANTABILITY, SATISFACTORY QUALITY, NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE. YOU ASSUME TOTAL RESPONSIBILITY AND RISK FOR YOUR USE OF THIS SITE, ALL SITE-RELATED SERVICES, AND ANY THIRD PARTY WEBSITES OR APPLICATIONS. NO ORAL OR WRITTEN INFORMATION OR ADVICE SHALL CREATE A WARRANTY OF ANY KIND. ANY REFERENCES TO SPECIFIC PRODUCTS OR SERVICES ON THE WEBSITES DO NOT CONSTITUTE OR IMPLY A RECOMMENDATION OR ENDORSEMENT BY PACIFIC BIOSCIENCES.

