# <img src="./docs/logo.webp" alt="logo" height="100"/> **DeepChopper** [![social](https://img.shields.io/github/stars/ylab-hi/DeepChopper?style=social)](https://github.com/ylab-hi/DeepChopper/stargazers)

[![pypi](https://img.shields.io/pypi/v/deepchopper.svg)](https://pypi.python.org/pypi/deepchopper)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/deepchopper)](https://pypi.org/project/deepchopper/#files)
[![license](https://img.shields.io/pypi/l/deepchopper.svg)](https://github.com/ylab-hi/DeepChopper/blob/main/LICENSE)
[![pypi version](https://img.shields.io/pypi/pyversions/deepchopper.svg)](https://pypi.python.org/pypi/deepbiop)
[![platform](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win-blue)](https://pypi.org/project/deepchopper/#files)
[![Actions status](https://github.com/ylab-hi/DeepChopper/actions/workflows/release-python.yml/badge.svg)](https://github.com/ylab-hi/DeepChopper/actions)
[![Space](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md.svg)](https://huggingface.co/spaces/yangliz5/deepchopper)

<!--toc:start-->

- [**DeepChopper**](#-deepchopper-)
  - [🚀 Quick Start: Try DeepChopper Online](#-quick-start-try-deepchopper-online)
  - [📦 Installation](#-installation)
    - [Compatibility and Support](#compatibility-and-support)
      - [PyPI Support](#pypi-support)
  - [🛠️ Usage](#%EF%B8%8F-usage)
    - [Command-Line Interface](#command-line-interface)
    - [Python Library](#python-library)
  - [📚 Cite](#-cite)
  - [🤝 Contribution](#-contribution)
    - [Build Environment](#build-environment)
  - [📬 Support](#-support)

<!--toc:end-->

🧬 DeepChopper leverages a language model to accurately detect and chop artificial sequences that may cause chimeric reads, ensuring higher quality and more reliable sequencing results.
By integrating seamlessly with existing workflows, DeepChopper provides a robust solution for researchers and bioinformaticians working with Nanopore direct-RNA sequencing data.

## ✨ What's New in v1.3.0

- **🚀 Direct FASTQ Processing**: No more encoding step! DeepChopper now works directly with FASTQ files
- **⚡ Simplified Workflow**: Go from raw data to results in just 2 commands (`predict` → `chop`)
- **📦 Auto-format Detection**: Automatically handles `.fastq`, `.fq`, `.fastq.gz`, and `.fq.gz` files
- **⚠️ Breaking Change**: The `encode` command has been removed - update your pipelines accordingly

[See full changelog →](./CHANGELOG.md)

📘 **FEATURED:** We provide a comprehensive tutorial that includes an example dataset in our [full documentation](https://ylab-hi.github.io/DeepChopper/latest/).

## 🚀 Quick Start: Try DeepChopper Online

Experience DeepChopper instantly through our user-friendly web interface. No installation required!
Simply click the button below to launch the web application and start exploring DeepChopper's capabilities:

[![Open in Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md.svg)](https://huggingface.co/spaces/yangliz5/deepchopper)

**What you can do online:**

- 📤 Upload your sequencing data
- 🔬 Run DeepChopper's analysis
- 📊 Visualize results
- 🎛️ Experiment with different parameters

Perfect for quick tests or demonstrations! However, for extensive analyses or custom workflows, we recommend installing DeepChopper locally.

> ⚠️ Note: The online version is limited to one FASTQ record at a time and may not be suitable for large-scale projects.

## 📦 Installation

DeepChopper can be installed using pip, the Python package installer.
Follow these steps to install:

1. Ensure you have Python 3.10 or later installed on your system.

2. Create a virtual environment (recommended):

   ```bash
   python -m venv deepchopper_env
   source deepchopper_env/bin/activate  # On Windows use `deepchopper_env\Scripts\activate`
   ```

3. Install DeepChopper:

   ```bash
   pip install deepchopper
   ```

4. Verify the installation:

   ```bash
   deepchopper --help
   ```

### Compatibility and Support

DeepChopper is designed to work across various platforms and Python versions.
Below are the compatibility matrices for PyPI installations:

#### [PyPI Support][pypi]

| Python Version | Linux x86_64 | macOS Intel | macOS Apple Silicon | Windows x86_64 |
| :------------: | :----------: | :---------: | :-----------------: | :------------: |
| 3.10 | ✅ | ✅ | ✅ | ✅ |
| 3.11 | ✅ | ✅ | ✅ | ✅ |
| 3.12 | ✅ | ✅ | ✅ | ✅ |

🆘 Trouble installing? Check our [Troubleshooting Guide](https://ylab-hi.github.io/DeepChopper/latest/tutorial/#troubleshooting) or [open an issue](https://github.com/ylab-hi/DeepChopper/issues).

## 🛠️ Usage

For a comprehensive guide, check out our [full tutorial](https://ylab-hi.github.io/DeepChopper/latest/tutorial/).
Here's a quick overview:

### Command-Line Interface

> **🎉 New in v1.3.0:** DeepChopper now works directly with FASTQ files! No encoding step required.

DeepChopper offers two main commands: `predict` and `chop`.

1. **Predict** chimera artifacts directly from FASTQ:

   ```bash
   deepchopper predict input.fastq --output predictions
   ```

   Using GPUs? Add the `--gpus` flag:

   ```bash
   deepchopper predict input.fastq --output predictions --gpus 2
   ```

   Supports all FASTQ formats: `.fastq`, `.fq`, `.fastq.gz`, `.fq.gz`

2. **Chop** chimera artifacts:

   ```bash
   deepchopper chop predictions/0 input.fastq
   ```

Want a GUI? Launch the web interface (note: limited to one FASTQ record at a time):

```bash
deepchopper web
```

### Python Library

Integrate DeepChopper into your Python scripts:

```python
import deepchopper

model = deepchopper.DeepChopper.from_pretrained("yangliz5/deepchopper")
# Your analysis code here
```

## 📚 Cite

If DeepChopper aids your research, please cite [our paper](https://www.nature.com/articles/s41467-026-68571-5):

```bibtex
@article{li2026genomic,
  title = {Genomic Language Model Mitigates Chimera Artifacts in Nanopore Direct {{RNA}} Sequencing},
  author = {Li, Yangyang and Wang, Ting-You and Guo, Qingxiang and Ren, Yanan and Lu, Xiaotong and Cao, Qi and Yang, Rendong},
  date = {2026-01-19},
  journaltitle = {Nature Communications},
  shortjournal = {Nat Commun},
  publisher = {Nature Publishing Group},
  issn = {2041-1723},
  doi = {10.1038/s41467-026-68571-5},
  url = {https://www.nature.com/articles/s41467-026-68571-5},
  urldate = {2026-01-20}
}
```

## 🤝 Contribution

We welcome contributions! Here's how to set up your development environment:

### Build Environment

Install [UV](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) and [Rust](https://www.rust-lang.org/tools/install)

```bash
git clone https://github.com/ylab-hi/DeepChopper.git
cd DeepChopper

# Install dependencies
uv sync

# Run DeepChopper
uv run deepchopper --help
```

🎉 Ready to contribute? Check out our [Contribution Guidelines](./CONTRIBUTING.md) to get started!

## 🔗 Related Projects

- **[ChimeraLM](https://ylab-hi.github.io/ChimeraLM/)** - Identify artificial chimeric reads from whole genome amplification (WGA) processes

## 📬 Support

Need help? Have questions?

- 📖 Check our [Documentation](./documentation/tutorial.md)
- 🐛 [Report issues](https://github.com/ylab-hi/DeepChopper/issues)

______________________________________________________________________

DeepChopper is developed with ❤️ by the YLab team.
Happy sequencing! 🧬🔬

[pypi]: https://pypi.python.org/pypi/deepchopper

