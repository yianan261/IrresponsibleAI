# IrresponsibleAI

IrresponsibleAI is a Python program designed for research purposes under the guidance of Dr. Guerra Gomez and Dr. Baeza-Yates. The script `aiid.py` is responsible for downloading AI Incident Database (AIID) data from a MongoDB cluster and outputting the information into CSV files for further analysis.
The script `news_content.py` is responsible for scraping news report urls of those incidents for OpenAI's gpt-4-turbo-preview model to interpret and summarize the list of categories and taxonomies we want. The API code is in `openai_api.py` located in the `api` directory.

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
To run `news_content.py`, ensure you have a valid OpenAI API key.
<br>
Execute the script with:

```sh
python3 aiid.py

```

or

```sh
python3 news_content.py

```

## News Content Processing

The `news_content.py` script aggregates news articles content of the same incident into one large string. It then instantiates an OpenaiAPI instance which processes the content of the aggregated article text by invoking the OpenAI() client. The `gpt-4-turbo-preview` model is used for this purpose.

The OpenaiAPI class and the prompt can be found in the `openai_api.py` file in the `api` directory. The taxonomies for our classification of the Irresponsible AI Atlas are defined in the `taxonomies.py` file, also located in the `api` directory, under the Taxonomies class. The prompt retrieves some of the taxonomic information from this file. The system is asked to adhere to the taxonomy we created as closely as possible, but if a field is not applicable, it can generate a more appropriate response.

# Data Analysis

IrresponsibleAI.ipynb file is used for data exploration. Current version can be found [here](https://colab.research.google.com/drive/1pJYpuXrnNFKJmI4L1h5VqWaYggeqosh5#scrollTo=GA770D6vuFyF)

# Data Visualization

Data processing and visualization can be found [here](https://observablehq.com/d/126c228131c034d7)

Interactive tree visualization of results of different prompting techniques can be found [here](https://observablehq.com/d/da2342040625eb8d)
