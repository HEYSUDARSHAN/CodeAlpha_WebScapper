import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, folder='images'):
    # Create a directory for the downloaded images if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")
    
    # Fetch the HTML content from the given URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags in the HTML
    img_tags = soup.find_all('img')
    if not img_tags:
        print("No images found on this page.")
        return

    print(f"Found {len(img_tags)} image(s). Downloading...")

    for img in img_tags:
        # Get the image URL from the 'src' attribute
        img_url = img.get('src')
        if not img_url:
            continue  # Skip if no src attribute found

        # Convert relative URLs to absolute URLs
        img_url = urljoin(url, img_url)

        # Create a valid filename from the image URL
        img_name = os.path.basename(img_url.split("?")[0])  # Remove any query parameters
        if not img_name:  # Fallback in case the URL doesn't end with a file name
            img_name = "downloaded_image.jpg"
        
        img_path = os.path.join(folder, img_name)

        try:
            # Download the image data
            img_data = requests.get(img_url)
            img_data.raise_for_status()
            
            # Write the image data to a file in binary mode
            with open(img_path, 'wb') as f:
                f.write(img_data.content)
            print(f"Downloaded: {img_url} -> {img_path}")
        except requests.RequestException as e:
            print(f"Failed to download {img_url}. Error: {e}")

if __name__ == '__main__':
    target_url = input("Enter the URL of the website: ").strip()
    download_images(target_url)
