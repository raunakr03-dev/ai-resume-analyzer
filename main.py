from google import genai
import time

client = genai.Client(api_key="AIzaSyCybBHUv-7_KJ25gv50evbR8nijfDQRp90")

print("="*50)
print("        AI RESUME ANALYZER 🚀")
print("="*50)

print("\nPaste your resume (type 'END' in new line to finish):")

lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)

resume_text = "\n".join(lines)

role = input("\nEnter target job role (optional): ")

prompt = f"""
Act as a professional resume reviewer.

Analyze the resume for the role: {role if role else "General"}.

Provide:
- Strengths
- Weaknesses
- Suggestions
- Score out of 10

Resume:
{resume_text}
"""

print("\nAnalyzing...\n")

# 🔁 Retry logic
for attempt in range(3):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        print("="*50)
        print("        RESULT 📊")
        print("="*50 + "\n")

        print(response.text)
        break

    except Exception as e:
        print(f"⚠️ Attempt {attempt+1} failed... Retrying...")
        time.sleep(2)

        if attempt == 2:
            print("\n❌ Failed after multiple attempts. Try again later.")