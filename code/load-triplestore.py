import requests
import os
import sys

GRAPHDB_URL = "http://localhost:7200"

DATASETS = [
    {
        "repo_id": "heritage-reification",
        "file_path": "data/contested-claims-reification.ttl",
        "content_type": "text/turtle"
    },
    {
        "repo_id": "heritage-named",
        "file_path": "data/contested-claims-named.trig",
        "content_type": "application/trig"
    },
    {
        "repo_id": "heritage-rdfstar",
        "file_path": "data/contested-claims-rdfstar.ttl",
        "content_type": "text/turtle"
    }
]

def clear_repository(repo_id):
    """
    Clears all data in the specified repository using SPARQL Update.
    """
    update_endpoint = f"{GRAPHDB_URL}/repositories/{repo_id}/statements"
    sparql_update = "DELETE { ?s ?p ?o } WHERE { ?s ?p ?o }"
    
    try:
        response = requests.post(
            update_endpoint, 
            data={'update': sparql_update},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if response.status_code == 204:
            print(f"  [✓] Repository '{repo_id}' cleared successfully.")
            return True
        elif response.status_code == 404:
             print(f"  [!] Error: Repository '{repo_id}' does not exist. Please create it manually in GraphDB first.")
             return False
        else:
            print(f"  [X] Failed to clear '{repo_id}'. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  [!] Connection Error: {e}")
        return False

def load_data(repo_id, file_path, content_type):
    """
    Loads a file into the specified repository via REST API.
    """
    if not os.path.exists(file_path):
        print(f"  [!] File not found: {file_path}")
        return False

    upload_endpoint = f"{GRAPHDB_URL}/repositories/{repo_id}/statements"
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
        print(f"  ... Uploading {os.path.basename(file_path)} ({len(data)} bytes) ...")
        
        response = requests.post(
            upload_endpoint,
            data=data,
            headers={'Content-Type': content_type}
        )
        
        if response.status_code == 204:
            print(f"  [✓] Success! Data loaded into '{repo_id}'.")
            return True
        else:
            print(f"  [X] Upload failed. Status: {response.status_code}")
            print(f"      Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  [!] Error during upload: {e}")
        return False

def get_statement_count(repo_id):
    """
    Gets the total number of statements (claims) in the repository.
    """
    size_endpoint = f"{GRAPHDB_URL}/repositories/{repo_id}/size"
    try:
        response = requests.get(size_endpoint)
        if response.status_code == 200:
            return response.text.strip() # Sunucudan dönen ham sayı
        else:
            return "Unknown"
    except:
        return "Error"

def main():
    print("=== GraphDB Data Loader & Counter ===")
    print(f"Target URL: {GRAPHDB_URL}\n")

    try:
        requests.get(f"{GRAPHDB_URL}/protocol")
    except:
        print(f"CRITICAL ERROR: Could not connect to GraphDB at {GRAPHDB_URL}")
        print("Please ensure GraphDB is running.")
        sys.exit(1)

    for ds in DATASETS:
        repo = ds['repo_id']
        file = ds['file_path']
        ctype = ds['content_type']
        
        print(f"Processing Repository: {repo}")
        
        if clear_repository(repo):
            if load_data(repo, file, ctype):
                count = get_statement_count(repo)
                print(f"  [#] Total Claims/Statements in Repo: {count}")
            
        print("-" * 40)

if __name__ == "__main__":
    main()