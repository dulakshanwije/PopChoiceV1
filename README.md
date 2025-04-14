# PopChoice - Movie Suggestion AI

🎬 **PopChoiceV1** is an AI-powered movie recommendation system built using **ReactJS, Flask, OpenAI API, and Supabase**.

📺 Developed as part of the **Scrimba AI Engineering Course**.

## 📺 Demo Video

[![Watch the demo video](https://img.youtube.com/vi/SRNiffVd7Ss/maxresdefault.jpg)](https://www.youtube.com/watch?v=SRNiffVd7Ss)

## 🛠 Tech Stack

- **Frontend:** ReactJS
- **Backend:** Flask
- **API:** OpenAI API
- **Database:** Supabase

## 🔧 Features

- Movie details embedded using OpenAI's vector embedding API and stored in Supabase database as vectors
- Semantic search capabilities for movie recommendations
- User-friendly interface for discovering new films

## 🚀 Installation & Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/dulakshanwije/PopChoiceV1.git
   cd PopChoiceV1
   ```

2. **Backend Setup (Flask)**
   ```sh
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   flask run
   ```

3. **Frontend Setup**
   ```sh
   cd client
   npm install
   npm run dev
   ```

4. **Database Setup (Supabase)**
   - Create a Supabase Project and run the following SQL command to create the database:
   ```sql
   CREATE TABLE movies (
      id bigserial PRIMARY KEY,
      content text,
      embedding vector(1536) -- 1536 works for OpenAI embeddings
   );  
   ```

   - Create a function to search the movie table:
   ```sql
   CREATE OR REPLACE FUNCTION match_movies (
      query_embedding vector(1536),
      match_threshold float,
      match_count int
   )
   RETURNS TABLE (
      id bigint,
      content text,
      similarity float
   )
   LANGUAGE sql STABLE
   AS $$
      SELECT
         movies.id,
         movies.content,
         1 - (movies.embedding <=> query_embedding) AS similarity
      FROM movies
      WHERE 1 - (movies.embedding <=> query_embedding) > match_threshold
      ORDER BY similarity DESC
      LIMIT match_count;
   $$;
   ```

   - Run `create_table.py` to read `movies.txt` and upload data to Supabase.

## ⚠️ Disclaimer

**This project is for educational and demonstration purposes only.**

---

⭐ **Star this repo if you find it useful!** 😊
