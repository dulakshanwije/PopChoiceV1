from openai import OpenAI
from supabase import create_client, Client
from dotenv import dotenv_values
import re

config = dotenv_values('.env')

openai = OpenAI(
    api_key = config['OPENAI_API_KEY']
)

supabase : Client = create_client(config['SUPABASE_URL'],config['SUPABASE_KEY'])

def search_movie(query):
    try:
        embedding = create_embedding(query)
        match = find_nearest_match(embedding)
        return get_chat_completion(match,query)
    except Exception as e:
        print("ERROR:: ", e)
        return {
            "success":False,
            "error": e
        } 
    
def create_embedding(query):
    
    content = f'{query['1']['answer']} {query['2']['answer']} {query['3']['answer']}'
    
    search_embedding =  openai.embeddings.create(
        model="text-embedding-ada-002",
        input=content,
        encoding_format="float"
    )
    return search_embedding.data[0].embedding

def find_nearest_match(embedding):
    response = supabase.rpc("match_movies", {
        "query_embedding": embedding, 
        "match_threshold": 0.5, 
        "match_count": 4, 
    }).execute()
    
    match = ""
    for data in response.data:
        match += data['content'] + "\n"
    return match

chatMessages = [{
    "role": 'system',
    "content": 'You are an enthusiastic movie expert who loves recommending movies to people. You will be given two infromation sets one is three set of questions and answers each include, a question and a answer from and the second part is a context about sugessted movies. Your main job is to formulate a short answer with a movie suggestion. Please wrap the movie name and the released year with three hashtags, eg: ###The Super Mario Bros. Movie (2023)###. If you are unsure and cannot find the answer, say, "Sorry, I don\'t know the answer." Please do not make up the answer. Always speak as if you were chatting to a friend.'
}]

def get_chat_completion(match,query):
    chatMessages.append({
        "role":"user",
        "content":f"Context: {match} Question and Answers Set: {query}"
    })
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=chatMessages,
        temperature = 0.65,
        frequency_penalty = 0.5
    )
    
    content = completion.choices[0].message.content

    match = re.search(r"###(.*?)###", content)    
    movie_name = ""
    
    if not match:
        return {
            "success":False,
            "error": "Unable to fetch movie name."
        }
        
    movie_name = match.group(1)
    
    formatted_content = content.replace("###",'')
    
    return {
        "success":True,
        "name":movie_name,
        "description":formatted_content
    } 
    