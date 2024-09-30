import os
from Langchain_groq import ChatGrog 
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonutputParser 
from langchain_core.exceptions import OutputParserException 
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        
        self.llm = ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            ### INSTRUCTION:
            You are Vikas, a master's student at Sacramento State in your last semester, pursuing a Master of Computer Science with a GPA of 3.85. Over your experience, you have developed expertise in full-stack development, machine learning (ML), and generative AI. You've led projects from inception to deployment, achieving an 80% increase in user adoption and improving data processing efficiency by 50%.

            In your recent work, you built a Storm Water Analytics platform, enhanced a heart disease prediction model using K-Nearest Neighbors (KNN), and developed a social media application leveraging the MERN stack. Additionally, you have three years of industry experience as a backend developer at Tata Consultancy Services, where you optimized microservices and improved database efficiency. You are actively seeking a full-time role to apply your skills and drive impactful projects in software development and machine learning.

            Your job is to write a cold email to the employer regarding the job mentioned above description in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Vikas's portfolio: {link_list}
            Remember you are Vikas, master student at SAC State.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE) :
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke(input = {"job_description": str(job), "link_list": links})
        return res.content

res = chain_extract.invoke(input = {"page_data": page_data})

if __name__ == '__main__':
    print(os.getenv("GROQ_API_KEY"))