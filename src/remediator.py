import os
from groq import Groq

def get_remediation(finding):
    """
    Uses AI (Groq) to generate remediation code for a security finding.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "AI Remediation skipped: No API key provided."

    client = Groq(api_key=api_key)
    
    # Constructing a prompt based on the finding type
    issue_description = str(finding)
    prompt = f"Provide a Terraform fix for the following security issue: {issue_description}. Return only the corrected HCL code snippet."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating remediation: {e}"
