import os
import shutil
import sys
import re
from bs4 import BeautifulSoup
from typing import Callable
from html import escape

# Sigh... sorry about this
style_files = {
'load.php?debug=false&lang=en&modules=jquery.accessKeyLabel,client|mediawiki.RegExp,notify,util|mediawiki.legacy.wikibits&skin=vector&version=6281194730bd': True,
'load.php?debug=false&lang=en&modules=jquery|jquery.cookie|mediawiki.cookie,toc&skin=vector&version=085xbfw': True,
'load.php?debug=false&lang=en&modules=jquery|jquery.makeCollapsible&skin=vector&version=0e5dzdn': True,
'load.php?debug=false&lang=en&modules=jquery&skin=vector&version=0w5wrgy': True,
'load.php?debug=false&lang=en&modules=jquery.tabIndex,throttle-debounce|mediawiki.page.startup|skins.vector.js&skin=vector&version=4fe37926d110': True,
'load.php?debug=false&lang=en&modules=jquery.tablesorter|mediawiki.language.months&skin=vector&version=e2016b07e9c2': True,
'load.php?debug=false&lang=en&modules=mediawiki.action.view.categoryPage.styles|mediawiki.helplink,sectionAnchor|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?debug=false&lang=en&modules=mediawiki.action.view.filepage|mediawiki.legacy.commonPrint,shared|mediawiki.sectionAnchor|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?debug=false&lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.sectionAnchor|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?debug=false&lang=en&modules=site&only=styles&skin=vector': True,
'load.php?debug=false&lang=en&modules=site.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.action.view.categoryPage.styles|mediawiki.helplink|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.diff.styles|mediawiki.interface.helpers.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=jquery.makeCollapsible.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.action.view.categoryPage.styles|mediawiki.helplink|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=mediawiki.action.view.categoryPage.styles|mediawiki.helplink|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.action.view.filepage|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.action.view.redirectPage|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.diff.styles|mediawiki.interface.helpers.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.helplink|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.helplink,special|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.interface.helpers.styles|mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|mediawiki.toc.styles|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.skinning.interface|skins.vector.styles&only=styles&skin=vector': True,
'load.php?lang=en&modules=site.styles&only=styles&printable=1&skin=vector': True,
'load.php?lang=en&modules=site.styles&only=styles&skin=vector': True,
}

script_files = {
'load.php?debug=false&lang=en&modules=html5shiv&only=scripts&skin=vector&sync=1': True,
'load.php?debug=false&lang=en&modules=jquery,mediawiki&only=scripts&skin=vector&version=0kyhxuv': True,
'load.php?debug=false&lang=en&modules=jquery,mediawiki&only=scripts&skin=vector&version=0suxib7': True,
'load.php?debug=false&lang=en&modules=jquery,mediawiki&only=scripts&skin=vector&version=133tzap': True,
'load.php?debug=false&lang=en&modules=jquery,mediawiki&only=scripts&skin=vector&version=M1PPA2qs': True,
'load.php?debug=false&lang=en&modules=startup&only=scripts&skin=vector': True,
'load.php?lang=en&modules=html5shiv&only=scripts&skin=vector&sync=1': True,
'load.php?lang=en&modules=startup&only=scripts&printable=1&skin=vector': True,
'load.php?lang=en&modules=startup&only=scripts&safemode=1&skin=vector': True,
'load.php?lang=en&modules=startup&only=scripts&skin=vector': True,
}

deleted_files = 0
deleted_dirs = 0
renamed = 0

def add_html_extension_to_links(directory):
    """
    Traverse the given directory and its subdirectories to find all HTML files.
    
    For each HTML file, this function searches for all <a> tags and appends 
    '.html' to the end of the 'href' attribute value if it doesn't already 
    end with '.html'. The modified content is then written back to the same file.
    
    Parameters:
    directory (str): The path to the directory to search for HTML files.

    Returns:
    None: This function modifies the files in place and does not return a value.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.htm')):
                file_path = os.path.join(root, file)
                
                # Read the file contents
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the HTML content
                soup = BeautifulSoup(content, 'html.parser')

                # Find all <a> tags
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    # Check if the href does not already end with .html
                    if not href.endswith('.html'):
                        a_tag['href'] += '.html'

                # Write the modified content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

def replace_string_in_files(directory, old_string, new_string):
    """
    Replaces all occurrences of the old_string with the new_string in all files within the given directory.

    Args:
        directory (str): The path to the directory to search.
        old_string (str): The string to be replaced.
        new_string (str): The replacement string.
    """

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Construct the full path to the file
            file_path = os.path.join(root, file)

            try:
                # Open the file in read mode
                with open(file_path, 'r') as f:
                    content = f.read()

                # Replace all occurrences of old_string with new_string
                new_content = content.replace(old_string, new_string)

                # Open the file again in write mode and replace the content
                with open(file_path, 'w') as f:
                    f.write(new_content)
            except Exception as e:
                continue
                #print(f"Error processing {file}: {e}")

def parse_get_query(query):
    """
    Parse a URL query string into a dictionary.

    Args:
        query (str): The URL query string,.

    Returns:
        dict: A dictionary containing key-value pairs from the query string,
              where keys and values are decoded to replace '+' with spaces.
    """
    # Remove leading '?' if present
    if query.startswith('?'):
        query = query[1:]

    # Regular expression to match key-value pairs
    pattern = r'([^&=]+)=([^&]*)'
    
    # Create a dictionary to store the parameters
    params = {}
    
    # Find all matches and populate the dictionary
    for match in re.findall(pattern, query):
        key = match[0]
        value = match[1]
        params[key] = value
    
    return params

def rename_get_query_files(directory, keyword):
    """
    Search all files in a given directory that start with a certain keyword
    and renames them.

    Args:
        directory (str): The path to the directory you want to search.
        keyword (str): The keyword to look for at the beginning of each filename.
    """
    global renamed
    global script_files
    global style_files

    for item in os.listdir(directory):
        if item.startswith(keyword):
            old_path = os.path.join(directory, item)
            new_name = "_".join(list(parse_get_query(item).values()))
            
            extension = ""
            if(script_files.get(item,False)):
                extension = ".js"
            if(style_files.get(item,False)):
                extension = ".css"
            new_name = new_name+extension

            new_path = os.path.join(directory, new_name)
            shutil.move(old_path, new_path)
            renamed += 1

            #print("Replacing: ", item, " with: ", new_name, " escaped: ", escape(item).replace('|', '%7C'))
            replace_string_in_files(directory, escape(item).replace('|', '%7C').replace(',', '%2C'), new_name)

def remove_by_condition(base_path: str, condition: Callable[[str], bool]) -> None:
    """
    Recursively removes files and directories from the given base path
    based on a provided condition.

    Args:
        base_path (str): The root directory to start searching from.
        condition (Callable[[str], bool]): A function that takes a string
            representing a file or directory name and returns True if it
            should be removed, False otherwise.
    """
    global deleted_files
    global deleted_dirs
    # Check all items in the current directory
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            # Recur into the directory
            remove_by_condition(item_path, condition)
            # After recursion, check if the directory should be deleted
            if condition(item):
                shutil.rmtree(item_path)
                deleted_dirs += 1
        elif os.path.isfile(item_path) and condition(item):
            os.remove(item_path)
            deleted_files += 1

def remove_empty_dirs(base_path: str) -> None:
    """
    Recursively removes empty directories from the given base path.

    Args:
        base_path (str): The root directory to start searching from.
    """
    global deleted_dirs
    # Check all items in the current directory
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            # Recur into the directory
            remove_empty_dirs(item_path)
            # After recursion, check if the directory is empty
            if not os.listdir(item_path):  # Check if directory is empty
                os.rmdir(item_path)
                deleted_dirs += 1

def rename_and_move_index_files(base_path: str) -> None:
    """
    Renames index.html files in subdirectories to the parent directory name
    and moves them outside.

    Args:
        base_path (str): The root directory to start searching from.
    """
    global renamed
    # Traverse all items in the current directory
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            # Recur into the directory
            rename_and_move_index_files(item_path)
            # Check if index.html exists in the current directory
            index_file_path = os.path.join(item_path, "index.html")
            if os.path.isfile(index_file_path):
                # Rename to the parent directory name and move it outside
                parent_dir_name = os.path.basename(item_path)
                new_file_name = os.path.join(base_path, f"{parent_dir_name}.html")
                shutil.move(index_file_path, new_file_name)
                renamed += 1
                

def rename_title_files_and_dirs(base_path: str) -> None:
    """
    Renames files and directories containing "title=" to have a new name.

    Args:
        base_path (str): The root directory to start searching from.
    """
    global renamed
    # Traverse all items in the current directory
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if "title=" in item:
            # Extract the new name after "title="
            new_name = item.split("title=", 1)[1]
            new_name = new_name.strip()  # Remove any leading/trailing whitespace
            
            # Determine if it's a file or directory
            if os.path.isdir(item_path):
                new_item_path = os.path.join(base_path, new_name)
                os.rename(item_path, new_item_path)
            elif os.path.isfile(item_path):
                new_item_path = os.path.join(base_path, f"{new_name}.html")
                os.rename(item_path, new_item_path)
                renamed += 1

        # Recur into directories
        if os.path.isdir(item_path):
            rename_title_files_and_dirs(item_path)

def rename_non_html_files(base_path: str) -> None:
    """
    Renames non-HTML files in cdda_wiki to have a new name.

    Args:
        base_path (str): The root directory to start searching from.
    """
    global renamed
    cdda_wiki_path = os.path.join(base_path, "cdda_wiki/index.php")
    if not os.path.isdir(cdda_wiki_path):
        print(f"Directory {cdda_wiki_path} does not exist.")
        return

    # Traverse all items in the cdda_wiki/index.php directory
    for item in os.listdir(cdda_wiki_path):
        item_path = os.path.join(cdda_wiki_path, item)
        if os.path.isfile(item_path) and not item.endswith('.html'):
            new_item_path = item_path + '.html'
            os.rename(item_path, new_item_path)
            renamed +=1

def move_contents(source_path: str, destination_path: str) -> None:
    """
    Moves contents of cdda_wiki to the parent directory.

    Args:
        cdda_wiki_path (str): The path to the cdda_wiki directory.
        parent_dir (str): The parent directory to move the contents to.
    """
    global renamed

    if not os.path.isdir(source_path):
        print(f"Directory {source_path} does not exist.")
        return

    for item in os.listdir(source_path):
        item_path = os.path.join(source_path, item)
        moveto = os.path.join(destination_path, item)

        if os.path.isdir(item_path):
            if(not os.path.exists(moveto)):
                os.makedirs(moveto)
            move_contents(item_path, moveto)
            continue

        #TODO: check if the destination file exits and decide with one is the newest using the "Cached time" value inside them

        try:
            #NOTE: If we use the full path where we want to move it and not only destination folder it will overwrite
            shutil.move(item_path, moveto)
            renamed += 1

        except Exception as e:
            print("An exception occurred:", item_path, moveto)
            print(e)



def remove_unwanted_files_and_dirs(base_path: str) -> None:
    """
    Removes unwanted files and directories from the given base path.

    Args:
        base_path (str): The root directory to start searching from.
    """
    global deleted_dirs
    global deleted_files

    # Delete unwanted root folders
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and 'cdda_wiki' not in item:
            shutil.rmtree(item_path)
            deleted_dirs += 1

    # Define conditions for file deletions
    conditions = [
        lambda file: 'action=' in file,
        lambda file: 'oldid=' in file,
        lambda file: 'printable=' in file,
        lambda file: 'Special:' in file and 'Special:Categories' not in file,
        lambda dir_name: dir_name.startswith("doc"),
    ]

    # Apply the conditions using the generic function
    for condition in conditions:
        remove_by_condition(base_path, condition)
    
    # Rename and move index.html files
    rename_and_move_index_files(base_path)

    # Remove empty directories
    remove_empty_dirs(base_path)

    # Rename files and directories containing "title="
    rename_title_files_and_dirs(base_path)

    # Rename non-HTML files in cdda_wiki
    rename_non_html_files(base_path)

    # Move contents of cdda_wiki to the parent directory
    move_contents(os.path.join(base_path, 'cdda_wiki/index.php'), os.path.join(base_path, "cdda_wiki"))

    # Remove empty directories again
    remove_empty_dirs(base_path)

    # Modify the links to be local friendly
    replace_string_in_files(os.path.join(base_path, "cdda_wiki"),'="/cdda_wiki/index.php/','="./')
    replace_string_in_files(os.path.join(base_path, "cdda_wiki"),'="/cdda_wiki/','="./')

    # Add .html extension to all the html links
    add_html_extension_to_links(os.path.join(base_path, "cdda_wiki"))

    # Rename the files that have a get query name
    rename_get_query_files(os.path.join(base_path, "cdda_wiki"), "load.php?")
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleaning.py <directory_path>")
        sys.exit(1)

    base_path = sys.argv[1]
    remove_unwanted_files_and_dirs(base_path)

    print("Deleted dirs: ", deleted_dirs)
    print("Deleted files: ", deleted_files)
    print("Renamed files: ", renamed)
