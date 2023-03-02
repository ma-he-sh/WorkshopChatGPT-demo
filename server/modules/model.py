from pathlib import Path
import openai

class ModelGPT:
    # maximum number of tokens per chunk
    max_tokens_per_chunk = 1024
    max_chunk_size = 1024
    model_engine = "text-ada-001"

    def __init__( self, session, api_key ):
        self.session = session
        openai.api_key = api_key

    def get_message(self, user_prompt, content):
        chunks = [content[i:i+self.max_chunk_size] for i in range(0, len(content), self.max_chunk_size)]

        # Generate a summary for each chunk using the OpenAI API
        summary = []
        for chunk in chunks:
            prompt = (f"{user_prompt}:\n\n{chunk}\n\nOutput:")
            response = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            rep_summary = response.choices[0].text.strip()
            summary.append(rep_summary)
        
        message = "NO RESPONSE RECIEVED"
        # extract the summary from the response
        if len(summary) > 0:
            message = " ".join(summary)
        
        return message
    