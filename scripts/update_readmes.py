#!/usr/bin/env python3
import re
import os
import subprocess
import time

# List of categories to process
ALLOWED_CATEGORIES = {
    'bam', 'csv', 'dna', 'fastq', 'longreads', 'metagenomics', 
    'pangenomics', 'phylogenomics', 'proteomics', 'rna', 
    'singlecell', 'slurm', 'vcf'
}

def get_repo_readme(repo_url, output_path):
    """
    Fetches the README from a GitHub repository using the gh CLI.
    """
    # Extract owner/repo from URL
    match = re.search(r'github\.com/([^/]+/[^/]+)', repo_url)
    if not match:
        print(f"Skipping invalid GitHub URL: {repo_url}")
        return False
    
    repo_path = match.group(1)
    # clean repo path (remove trailing .git or fragments)
    repo_path = repo_path.replace('.git', '').split('#')[0]
    
    print(f"Fetching README for {repo_path} -> {output_path}...")
    
    try:
        # Run gh repo view to get the README content
        result = subprocess.run(
            ['gh', 'repo', 'view', repo_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True,
            text=True # decode output
        )
        
        content = result.stdout
        # gh repo view often outputs a header like:
        # name: owner/repo
        # description: ...
        # --
        # <README CONTENT>
        #
        # We try to strip this header by looking for the separator "\n--\n"
        if "\n--\n" in content:
            readme_content = content.split("\n--\n", 1)[1]
        else:
            readme_content = content

        with open(output_path, 'w') as f:
            f.write(readme_content)
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error fetching {repo_path}: {e.stderr}")
        return False

def main():
    # Assume script is run from project root or find README relative to script
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(project_root, 'README.md')
    
    if not os.path.exists(readme_path):
        print(f"Error: Could not find README.md at {readme_path}")
        return

    with open(readme_path, 'r') as f:
        lines = f.readlines()

    current_category = None
    
    # Regex to match category headers (##### name or #### name)
    category_re = re.compile(r'^#+\s+(\w+)')
    # Regex to match list items (- [name](url) : description)
    item_re = re.compile(r'^\-\s+\[([^\]]+)\]\(([^)]+)\)')

    for line in lines:
        line = line.strip()
        
        # Check for category change
        cat_match = category_re.match(line)
        if cat_match:
            cat_name = cat_match.group(1).lower()
            if cat_name in ALLOWED_CATEGORIES:
                current_category = cat_name
            else:
                current_category = None
            continue
            
        if current_category:
            item_match = item_re.match(line)
            if item_match:
                name = item_match.group(1)
                url = item_match.group(2)
                
                # Sanitize name for filename (keep simple, replace special chars with _)
                safe_name = re.sub(r'[^\w\-]', '_', name) + '.md'
                
                output_dir = os.path.join(project_root, current_category)
                output_path = os.path.join(output_dir, safe_name)
                
                # Ensure directory exists (though it should based on repo structure)
                os.makedirs(output_dir, exist_ok=True)
                
                # Fetch and overwrite existing files to keep them updated
                success = get_repo_readme(url, output_path)
                if success:
                    print(f"Updated: {safe_name}")
                    # Sleep briefly to avoid rate limiting
                    time.sleep(1) 

if __name__ == "__main__":
    main()
