from huggingface_hub import HfApi, snapshot_download
import os
import torch
import argparse

def download_checkpoint(repo_id, save_path, repo_type="model"):
    """
    Download a model checkpoint from Hugging Face Hub to the specified local directory.
    
    Args:
        repo_id (str): The repository ID on Hugging Face Hub
        save_path (str): Local directory path to save the checkpoint
        repo_type (str): Type of repository (default: "model")
    """
    # Initialize Hugging Face API
    api = HfApi()
    
    # Create the directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Download the checkpoint
    print(f"Downloading {repo_id} to {save_path}...")
    snapshot_download(repo_id=repo_id, repo_type=repo_type, local_dir=save_path)
    print(f"Successfully downloaded {repo_id}")

def main(args):    
    # Define checkpoint configurations
    checkpoints = [
        {
            "repo_id": args.repo_id,
            "save_path": args.save_path,
            "repo_type": args.repo_type
        }
    ]
    
    # Add LoRA checkpoint if provided
    if args.lora_repo_id and args.lora_save_path:
        checkpoints.append({
            "repo_id": args.lora_repo_id,
            "save_path": args.lora_save_path,
            "repo_type": args.lora_repo_type
        })
    
    # Download each checkpoint
    for checkpoint in checkpoints:
        download_checkpoint(
            repo_id=checkpoint["repo_id"],
            save_path=checkpoint["save_path"],
            repo_type=checkpoint["repo_type"]
        )

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Download model checkpoints from Hugging Face Hub")
    parser.add_argument(
        "--repo_id",
        type=str,
        default="cerspense/zeroscope_v2_576w",
        help="Hugging Face repository ID for the checkpoint"
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="./ckpts/zeroscope_v2_576w",
        help="Local directory to save the checkpoint"
    )
    parser.add_argument(
        "--repo_type",
        type=str,
        default="model",
        help="Type of repository (e.g., model, dataset)"
    )
    parser.add_argument(
        "--lora_repo_id",
        type=str,
        default="danhtran2mind/zeroscope_v2_576w-Ghibli-LoRA",
        help="Hugging Face repository ID for the LoRA checkpoint"
    )
    parser.add_argument(
        "--lora_save_path",
        type=str,
        default="./ckpts/zeroscope_v2_576w-Ghibli-LoRA",
        help="Local directory to save the LoRA checkpoint"
    )
    parser.add_argument(
        "--lora_repo_type",
        type=str,
        default="model",
        help="Type of repository for the LoRA checkpoint (e.g., model, dataset)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call main with parsed arguments
    main(args)