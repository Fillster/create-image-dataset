from duckduckgo_search import DDGS
import requests
import argparse
import os

def image_search(term, max_images):
    list_of_images = []
    with DDGS() as ddgs:
        keywords = term
        ddgs_images_gen = ddgs.images(
        keywords,
        region="wt-wt",
        safesearch="off",
        size=None,
        type_image=None,
        layout=None,
        license_image=None,
        max_results=max_images,
        )
        for r in ddgs_images_gen:
            print(r["image"])
            list_of_images.append(r["image"])
    return list_of_images


def folder_exists(folder_path):
    return os.path.exists(folder_path) and os.path.isdir(folder_path)


def create_folder(folder_path):
    if not folder_exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def download_image(url, save_folder, file_name):
    response = requests.get(url)
    
    if response.status_code == 200:
        save_path = os.path.join(save_folder, file_name)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("query", help="Search term for images")
    parser.add_argument("folder", help="Folder to download images")
    parser.add_argument("--count", type=int, default=5, help="Numer of images (default is 5)")

    args = parser.parse_args()

    query= args.query
    folder = args.folder
    count = args.count

    current_folder = os.getcwd()
    new_folder = current_folder+"/"+folder
    create_folder(new_folder)
    
    list_of_images = image_search(query, count)
    
    name_inc = 1
    for i in list_of_images:
        file_extension = ""
        if ".jpg" in i:
            file_extension = ".jpg"
        elif ".png" in i:
            file_extension = ".png"

        file_name = query+str(name_inc)+file_extension
        download_image(i, new_folder, file_name)
        name_inc+=1