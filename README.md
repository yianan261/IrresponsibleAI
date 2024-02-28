# IrresponsibleAI

IrresponsibleAI is a Python program designed for research purposes under the guidance of Dr. Guerra Gomez and Dr. Baeza-Yates. The script `aiid.py` is responsible for downloading AI Incident Database (AIID) data from a MongoDB cluster and outputting the information into CSV files for further analysis.
The script `newsContent.py` is responsible for scraping news report urls of those incidents for OpenAI's gpt-4-turbo-preview model to interpret and summarize the list of categories and taxonomies we want.

## Installation

Before running the script, you need to install the required Python packages listed in `requirements.txt`.

To set up your environment, follow these steps:

1. Clone the repository:

```sh
git clone https://github.com/yianan261/IrresponsibleAI.git
cd IrresponsibleAI
```

2. It's recommended to create a virtual environment:

```sh
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install the required packages:

```sh
pip install -r requirements.txt
```

# Usage

To run the `aiid.py` program, ensure your MongoDB cluster is accessible and that you have the necessary credentials.
To run `newsContent.py`, ensure you have a valid OpenAI API key.
<br>
Execute the script with:

```sh
python aiid.py

```

or

```sh
python newsContent.py

```

# Data Analysis

IrresponsibleAI.ipynb file is used for data exploration. Current version can be found [here](https://colab.research.google.com/drive/1pJYpuXrnNFKJmI4L1h5VqWaYggeqosh5#scrollTo=GA770D6vuFyF)

# Data Visualization

Data processing and visualization can be found [here](https://observablehq.com/d/126c228131c034d7)
