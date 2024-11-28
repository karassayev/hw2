import csv
import random
from elasticsearch import Elasticsearch
import warnings
from elasticsearch import ElasticsearchWarning
warnings.filterwarnings("ignore", category=ElasticsearchWarning)


# Initialize Elasticsearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Function to generate random data and save it to a CSV file
def generate_random_data(filename, num_records=100):
    departments = ['Engineering', 'Marketing', 'Finance', 'HR', 'Science']
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'department', 'threat_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user_id in range(1, num_records + 1):
            writer.writerow({
                'user_id': f'user_{user_id}',
                'department': random.choice(departments),
                'threat_score': round(random.uniform(0, 100), 2)
            })
    print(f"Random data saved to '{filename}'")

# Function to create Elasticsearch index with mappings
def create_index(index_name):
    mappings = {
        "mappings": {
            "properties": {
                "user_id": {"type": "keyword"},
                "department": {"type": "keyword"},
                "threat_score": {"type": "float"}
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mappings)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

# Function to bulk upload data from CSV to Elasticsearch
def bulk_upload_to_elasticsearch(csv_file, index_name):
    actions = []
    
    # Read data from CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Add the action metadata
            action = {"index": {"_index": index_name}}
            # Add the actual document
            document = {
                "user_id": row["user_id"],
                "department": row["department"],
                "threat_score": float(row["threat_score"])  # Convert threat_score to float
            }
            actions.append(action)
            actions.append(document)
    
    # Bulk upload to Elasticsearch
    response = es.bulk(body=actions)
    
    if response['errors']:
        print(f"Errors occurred during bulk upload: {response['items']}")
    else:
        print("Bulk upload completed successfully")

# Function to fetch data from Elasticsearch
def fetch_data_from_elasticsearch(index_name):
    query = {"size":1000,
        "query": {"match_all": {}}}
    result = es.search(index=index_name, body=query)
    data = result['hits']['hits']
    for record in data:
        print(record['_source'])

# Main workflow
if __name__ == "__main__":
    #Generate random data and save to CSV
    csv_filename = 'threat_data.csv'
    generate_random_data(csv_filename, num_records=100)

    # Create Elasticsearch index
    index_name = 'threat_data'
    create_index(index_name)

    # Bulk upload data to Elasticsearch
    bulk_upload_to_elasticsearch(csv_filename, index_name)

    #Fetch and print data from Elasticsearch
    fetch_data_from_elasticsearch(index_name)
