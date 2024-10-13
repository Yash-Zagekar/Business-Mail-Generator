
import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        # Ensure skills is formatted as a list of strings
        if isinstance(skills, list) and all(isinstance(skill, str) for skill in skills):
            print(f"Querying links for skills: {skills}")  # Debugging line
            # Join skills into a single string or keep as list depending on your implementation
            results = self.collection.query(query_texts=skills, n_results=2)

            # Check if results have any metadatas
            if 'metadatas' in results:
                return [meta['links'] for meta in results['metadatas']]
            else:
                print("No metadata found in results")  # Debugging line
                return []
        else:
            print("Skills input is not a valid list of strings")  # Debugging line
            return []
