from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarise_articles_text(raw_text):
    """
    Using OpenAI API to summarise text for better readability.
    """
    
    prompt = (
        "Based on the extracted text below, summarise it for WhatsApp. Give only the formatted summary, no intro "
        f"or explanation. Use the URL to search the web for better summary if possible.\n\n {raw_text}"
    )
    
    # print(prompt)
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content if response.choices else None

        if content:
            return content.strip()
        else:
            logging.warning("⚠️ No content returned from OpenAI response.")
            return "Summary unavailable at the moment."
        
    except Exception as e:
        logging.info(f"❌ OpenAI summarization failed: {e}")
        return "Summary unavailable at the moment."
    
    