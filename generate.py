import os
import random
from PIL import Image
import json

# Directories for your layers and the outputted image and json files
layers_dir = 'layers/'
nfts_dir = 'nfts/'
if not os.path.exists(nfts_dir):
    os.makedirs(nfts_dir)

# Load layers
layers = {layer: [os.path.join(layers_dir, layer, f) for f in os.listdir(os.path.join(layers_dir, layer)) if not f.startswith('.')] for layer in os.listdir(layers_dir) if os.path.isdir(os.path.join(layers_dir, layer))}

# Layer order, customize this to match your layer folder names
layer_order = ['1 Background', '2 Fur', '3 Patch', '4 Ear', '5 Body', '6 Eyes', '7 Mouth', '8 Nose', '9 Head', '10 Item', '11 Hand']

# Initialize dictionaries for trait frequencies and rarity scores
trait_frequencies = {}
trait_rarity_scores = {}

# Generate NFT
def generate_nft(nft_id):
    attributes = []
    base_image = Image.new('RGBA', Image.open(layers[layer_order[0]][0]).size)
    for layer in layer_order:
        choice = random.choice(layers[layer])
        layer_image = Image.open(choice)
        base_image = Image.alpha_composite(base_image.convert('RGBA'), layer_image.convert('RGBA'))
        trait_type = layer.split(' ', 1)[1]
        trait_value = os.path.basename(choice).split('.')[0]
        attributes.append({"trait_type": trait_type, "value": trait_value})
    
    # Save the NFT image
    composite_file = os.path.join(nfts_dir, f'nft_{nft_id}.png')
    base_image.save(composite_file)

    return attributes

# Calculate frequencies of each trait to calculate score
def calculate_trait_frequencies(nfts_attributes):
    for attributes in nfts_attributes:
        for attribute in attributes:
            trait_key = (attribute["trait_type"], attribute["value"])
            if trait_key not in trait_frequencies:
                trait_frequencies[trait_key] = 0
            trait_frequencies[trait_key] += 1

# Calculate rarity scores
def calculate_rarity_scores():
    total_nfts = sum(trait_frequencies.values()) / len(layer_order)  # Total NFTs is the total counts divided by number of traits per NFT
    for key, frequency in trait_frequencies.items():
        trait_rarity_scores[key] = 1 / (frequency / total_nfts)

# Update NFT metadata with rarity scores and calculate overall rarity rank
def update_nft_metadata_with_rarity(nft_id, attributes):
    rarity_rank = 0
    for attribute in attributes:
        trait_key = (attribute["trait_type"], attribute["value"])
        rarity_score = trait_rarity_scores[trait_key]
        attribute["rarity_score"] = round(rarity_score, 2)
        rarity_rank += rarity_score

    # Construct metadata including rarity scores and rank
    nft_metadata = {
        "name": f"Collection Name #{nft_id}",
        "description": "A dope collection of..",
        "image": f"https://ipfs.io/path/to/nft_{nft_id}.png",
        "external_url": "https://myCoolSite.com",
        "background_color": "000000",
        "attributes": attributes,
        "rarity_rank": rarity_rank
    }

    # Save the updated metadata
    metadata_file_path = os.path.join(nfts_dir, f'nft_{nft_id}.json')
    with open(metadata_file_path, 'w') as f:
        json.dump(nft_metadata, f, indent=4)

# Generate NFTs and collect attributes for rarity calculation
nfts_attributes = [generate_nft(i) for i in range(10)]

# Calculate trait frequencies and rarity scores
calculate_trait_frequencies(nfts_attributes)
calculate_rarity_scores()

# Update metadata for each NFT with rarity scores and overall rarity rank
for i, attributes in enumerate(nfts_attributes):
    update_nft_metadata_with_rarity(i, attributes)
