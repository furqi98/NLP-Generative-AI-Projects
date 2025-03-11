# Fine-tuning Llama 3.2 3B Instruct with Unsloth on Psychotherapy Dataset

This repository contains the implementation of fine-tuning the `Llama 3.2 3B Instruct` model using the `Unsloth` library on a psychotherapy dataset. The goal is to enhance the model's performance in generating responses relevant to psychotherapy applications.

## Features

- Utilizes `Unsloth` for efficient fine-tuning.
- Leverages `Llama 3.2 3B Instruct` for natural language understanding.
- Trained on a psychotherapy dataset to generate insightful responses.
- Optimized for performance using LoRA (Low-Rank Adaptation).

## Installation

To set up the environment, install the required dependencies:

```bash
pip install torch transformers unsloth datasets accelerate peft bitsandbytes
```

## Usage

Run the Jupyter Notebook to fine-tune the model:

```bash
jupyter notebook
```

Open `unsloth_finetuning_of_Llama3_2_3B_Instruct_on_Psychotherapy_Dataset.ipynb` and execute the cells in order.

### Model Training Steps

1. Load `Llama 3.2 3B Instruct` with `Unsloth`.
2. Prepare the psychotherapy dataset.
3. Apply LoRA for parameter-efficient fine-tuning.
4. Train the model and evaluate performance.
5. Save and deploy the fine-tuned model.

## Dataset

The psychotherapy dataset used in this project contains conversations and responses relevant to therapy and counseling. The dataset is preprocessed before fine-tuning.

## Results

- The fine-tuned model demonstrates improved coherence and relevance in psychotherapy-based responses.
- LoRA-based tuning helps optimize performance with limited computational resources.

## Acknowledgments

This project is built using:

- [Unsloth](https://github.com/unslothai/unsloth)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)

##


