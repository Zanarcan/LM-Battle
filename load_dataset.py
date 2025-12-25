#!/usr/bin/env python3
"""
Script to load and explore the Pliny_HackAPrompt_Dataset from Hugging Face.
This dataset contains adversarial prompts for testing LLM security systems.
"""

from datasets import load_dataset
import json

def load_pliny_dataset():
    """
    Load the Pliny_HackAPrompt_Dataset from Hugging Face.
    """
    print("Loading Pliny_HackAPrompt_Dataset...")
    try:
        dataset = load_dataset("hackaprompt/Pliny_HackAPrompt_Dataset")
        print("Dataset loaded successfully!")
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def explore_dataset(dataset):
    """
    Explore the structure and content of the dataset.
    """
    if dataset is None:
        return

    print("\n=== Dataset Structure ===")
    print(f"Dataset splits: {list(dataset.keys())}")

    # Assume 'train' split exists
    if 'train' in dataset:
        train_data = dataset['train']
        print(f"\nTrain split size: {len(train_data)}")
        print(f"Features: {train_data.features}")
        print(f"Column names: {train_data.column_names}")

        # Show first few examples
        print("\n=== First 3 Examples ===")
        for i in range(min(3, len(train_data))):
            example = train_data[i]
            print(f"\nExample {i+1}:")
            for key, value in example.items():
                print(f"  {key}: {value}")
    else:
        print("No 'train' split found.")

def save_sample_to_json(dataset, filename="pliny_sample.json", num_samples=10):
    """
    Save a sample of the dataset to a JSON file for inspection.
    """
    if dataset is None or 'train' not in dataset:
        return

    train_data = dataset['train']
    samples = []

    for i in range(min(num_samples, len(train_data))):
        sample = {key: str(value) for key, value in train_data[i].items()}
        samples.append(sample)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(samples)} samples to {filename}")

if __name__ == "__main__":
    dataset = load_pliny_dataset()
    explore_dataset(dataset)
    save_sample_to_json(dataset)
