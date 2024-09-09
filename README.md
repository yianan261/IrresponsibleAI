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

The `news_content.py` script is the entry-point of the program. It aggregates news articles content of the same incident into one large string. It then instantiates an OpenaiAPI instance which processes the content of the aggregated article text by invoking the OpenAI() client. The `gpt-3.5-turbo-0125` model is used for this purpose.
<br>
**Update 9/9/2024: As of July 2024, gpt-3.5 models should be replaced by the newest model `gpt-4o-mini`. For more information, please visit [here](https://platform.openai.com/docs/models/gpt-4o)**

Before scraping the article from the provided URLs, the program pre-processes the urls to check if they are valid.

The OpenaiAPI class and the prompt can be found in the `openai_api.py` file in the `api` directory. The taxonomies for our classification of the Irresponsible AI Atlas are defined in the `taxonomies.py` file, also located in the `api` directory, under the Taxonomies class. The prompt retrieves some of the taxonomic information from this file. The system is asked to adhere to the taxonomy we created as closely as possible, but if a field is not applicable, it can generate a more appropriate response.

### Running the `news_content.py` Program:

To run `news_content.py`, ensure you have a valid OpenAI API key in your `.env` file. The script scrapes news articles related to AI incidents, aggregates the content, and uses OpenAI's GPT-4 model to classify the data based on predefined taxonomies.

You can control the behavior of the script using the following arguments:

#### Example Command:

```sh
python3 news_content.py --start 0 --end 50 --prompt_type zero_shot
```

### Arguments:

- `--scrape_articles`: If set True, the script will scrape the articles from URLs. If not set, it will read from pre-downloaded articles. First-time users should set this value to True.
- `--double_check`: If set, the script will perform a double check of the processed results using an additional OpenAI prompt.
- `--start`: Defines the starting ID range (default is `0`).
- `--end`: Defines the ending ID range (default is `10`).
- `--prompt_type`: Specifies the prompt type to use for the OpenAI API call.

### Available Prompt Types:

You must specify the `prompt_type` argument when running the `news_content.py` script. The following prompt types are allowed:

- `taxonomy_string_formatted`: Uses a formatted string for the taxonomy.
- `taxonomy_string`: Uses a raw taxonomy string.
- `zero_shot`: Employs zero-shot learning for classification.
- `tree_of_thoughts`: Implements the "Tree of Thoughts" technique.
- `few_shots_cot_prompt`: Uses a few-shot learning approach with Chain of Thought (CoT) prompting.
- `few_shots`: Simple few-shot learning.
- `few_shots_cot_steps`: Uses a few-shot learning approach with CoT steps.
- `tot_cot`: Implements "Tree of Thoughts" with CoT.
- `cot_user_prompt`: Employs a user-defined CoT prompt.
- `tot_cot_multi_turn`: Uses a multi-turn CoT strategy with "Tree of Thoughts". This is used as the default prompt-type.
- `tot_cot_2`: A variation of the "Tree of Thoughts" with CoT.

# Data Analysis

IrresponsibleAI.ipynb file is used for data exploration. Current version can be found [here](https://colab.research.google.com/drive/1pJYpuXrnNFKJmI4L1h5VqWaYggeqosh5#scrollTo=GA770D6vuFyF)

# Data Visualization

Data processing and visualization can be found [here](https://observablehq.com/d/126c228131c034d7)

Interactive tree visualization of results of different prompting techniques can be found [here](https://observablehq.com/d/da2342040625eb8d)

# Prompt Results

Different prompting techniques are employed in this classification task. The aggregated results of different techniques are located in the `processed output` directory.
Individual JSON outputs are under the `processed_output_individual` directory

# File Structure

```plaintext
    IrresponsibleAI/
    ├── README.md <!-- Entry point documentation of the project -->
    ├── news_content.py <!-- Main application script -->
    ├── incident_data.py <!-- Utility functions used by news_content.py-->
    ├── api/ <!-- Main directory for LLM APIs -->
    │ ├── openai_api.py <!-- Main class for calling LLM APIs -->
    | ├── param_data.py <!--generates message arguments for openai_api-->
    │ ├── prompt_factory.py <!-- Contains all the prompts -->
    │ ├── results.py <!-- Examples -->
    | ├── search_request.py <!-- Calls Google Custom Search API -->
    │ └── taxonomies.py <!-- Taxonomic structure -->
    ├── check_urls.py <!-- Utility functions to pre-process urls -->
    ├── cut_text.py <!-- Utility function -->
    ├── format_checker.py <!-- Utility function -->
    ├── aiid.py <!-- Script that loads data to MongoDB -->
    ├── article_texts/ <!-- Contains the scraped articles of AIID -->
    ├── article_texts2/ <!-- This will be removed -->
    ├── processed_output/ <!-- Main directory of aggregated output -->
    ├── processed_output_individual/ <!-- Main directory of individual output -->
    ├── newsUrls.json <!-- JSON file of all news article URLs -->
    ├── ids_2023.json <!-- JSON file of all incident IDs of 2023-->
    └── IrresponsibleAI.ipynb <!-- Preliminary data exploration notebook-->
```
