import os
import shutil
from markdown_helper_functions import *

public_path = "./public"
static_path = "./static"

def copy_static_to_public():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
        create_public_directory()
    else:
        os.mkdir(public_path)
        copy_files_from_static_to_public(static_path, public_path)

def create_public_directory():
        os.mkdir(public_path)
        copy_files_from_static_to_public(static_path, public_path)

def copy_files_from_static_to_public(path, destination):
    if os.path.exists(path):
         for item in os.listdir(path):

            item_path = path + "/" + item
            destination_path = destination + "/" + item

            if os.path.isdir(item_path):
                os.mkdir(destination_path)
                copy_files_from_static_to_public(item_path, destination_path)
            else:
                shutil.copy(item_path, destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}..")

    markdown_source = open(from_path, "r").read()
    template_source = open(template_path, "r").read()
    
    title = extract_title(markdown_source)
    html_source = convert_nested_elements(markdown_to_html_node(markdown_source).to_html())
    
    template_source = template_source.replace("{{ Title }}", title).replace("{{ Content }}", html_source)

    with open(dest_path, "w") as f:
        f.write(template_source)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}..")

    template_source = open(template_path, "r").read()
    directory_items = os.listdir(dir_path_content)
    
    for item in directory_items:
        print(item)
        item_path = dir_path_content + "/" + item
        destination_path = dest_dir_path + "/" + item

        if os.path.isdir(item_path):
            os.mkdir(destination_path)
            generate_pages_recursive(item_path, template_path, destination_path)

        elif item.endswith(".md"):
            print(f"found {item}, generating it into .html")
            markdown_source = open(item_path, "r").read()

            title = extract_title(markdown_source)
            html_source = convert_nested_elements(markdown_to_html_node(markdown_source).to_html())
    
            template_source = template_source.replace("{{ Title }}", title).replace("{{ Content }}", html_source)

            with open(f"{destination_path.split(".md")[0]}.html", "w") as f:
                f.write(template_source)
