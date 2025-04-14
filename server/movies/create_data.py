from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import dotenv_values
from openai import OpenAI
from supabase import create_client, Client

config = dotenv_values('.env')

openai = OpenAI(
    api_key = config['OPENAI_API_KEY']
)

supabase : Client = create_client(config['SUPABASE_URL'],config['SUPABASE_KEY'])

def split_document(file_path):
    print("DEBUG::Reading file...")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            file.close()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=250,
                chunk_overlap=35,
            )
            
            print("DEBUG::Splitting content...")
            
            splitted_content = text_splitter.create_documents([content])
            
            return splitted_content
            
    except FileNotFoundError as file_e:
        print("ERROR::File not found. ", file_e)
        return None
    except Exception as e:
        print("ERROR::Something went wrong. ", e)
        return None

def create_store_embeddings(splitted_content):
    print("DEBUG::Creating embeddings...")
    embeddings = []
    for content in splitted_content:
        content_value = content.page_content
        embedding_response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=content_value,
            encoding_format="float"
        )
        embeddings.append({
            "content":content_value,
            "embedding" : embedding_response.data[0].embedding
        })
    
    print("DEBUG::Storing embeddings...")
    data = supabase.table("movies").insert(embeddings).execute()

    if(len(data.data) > 0):
        print("DEBUG::Database updated successfully")

if __name__ == "__main__":
    try:
        splitted_content = split_document('movies.txt')
        if split_document:
            create_store_embeddings(splitted_content)
    except Exception as e:
        print("ERROR:: ", e)