import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import re
import requests

def is_image_url(url):
    """Check if the URL points to an image."""
    try:
        response = requests.head(url)
        return response.headers.get('content-type', '').startswith('image')
    except:
        return False

def download_image(url, save_dir='media'):
    """Download image from URL and save it to the specified directory."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Download the file
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download {url}")
            return False
            
        # Verify it's an image using PIL
        try:
            img = Image.open(BytesIO(response.content))
            # Get the file extension from the actual image format
            ext = img.format.lower() if img.format else 'jpg'
            
            # Generate filename from URL
            filename = os.path.join(save_dir, f"image_{len(os.listdir(save_dir))+1}.{ext}")
            
            # Save the image
            img.save(filename)
            print(f"Successfully downloaded: {filename}")
            return True
        except:
            print(f"Invalid image format: {url}")
            return False
            
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def download_images_from_list(urls):
    """Download multiple images from a list of URLs."""
    successful = 0
    failed = 0
    
    for url in urls:
        if is_image_url(url):
            if download_image(url):
                successful += 1
            else:
                failed += 1
        else:
            print(f"Not an image URL: {url}")
            failed += 1
    
    print(f"\nDownload complete!\nSuccessful: {successful}\nFailed: {failed}")

def get_steam_workshop_images(url):
    """Extract images from Steam Workshop page."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print("Failed to access Steam Workshop page")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        print("HTML Content length:", len(response.text))
        
        # Find all images
        images = []
        
        # Search for all images in the guide
        guide_images = soup.find_all('img')
        print(f"Found {len(guide_images)} images")
        
        for img in guide_images:
            if 'src' in img.attrs:
                img_url = img['src']
                # Make relative URLs absolute
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                if img_url not in images:  # avoid duplicates
                    images.append(img_url)
                    print(f"Found image: {img_url}")

        return images
    except Exception as e:
        print(f"Error parsing Steam Workshop page: {str(e)}")
        return []

# Example usage:
if __name__ == "__main__":
    steam_workshop_url = "https://steamcommunity.com/sharedfiles/filedetails/?id=3356916602"
    images = get_steam_workshop_images(steam_workshop_url)
    if images:
        print(f"\nFound {len(images)} images. Starting download...")
        download_images_from_list(images)
    else:
        print("No images found.")
