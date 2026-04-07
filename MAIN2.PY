from google import genai
import time
import re

# 🔑 API key
client = genai.Client(api_key="AIzaSyCybBHUv-7_KJ25gv50evbR8nijfDQRp90")

print("="*50)
print("        AI RESUME ANALYZER 🚀")
print("="*50)

print("\nPaste your resume (type 'END' in new line to finish):")

# 📥 Multi-line input
lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)

resume_text = "\n".join(lines)

# 🎯 Optional role input
role = input("\nEnter target job role (optional): ")

# 🧠 Prompt
prompt = f"""
Act as a professional resume reviewer.

Analyze the resume for the role: {role if role else "General"}.

Provide:
1. Strengths (bullet points)
2. Weaknesses (bullet points)
3. Suggestions (actionable)
4. Overall score out of 10 (with reasoning)

Keep response clear and structured.

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

        # 🎨 Output formatting
        print("="*50)
        print("        RESULT 📊")
        print("="*50 + "\n")

        print(response.text)

        # 📁 Save result to file
        with open("analysis.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        print("\n📁 Saved as analysis.txt")

        # 🎯 Extract score
        score_match = re.search(r'(\d+(\.\d+)?)/10', response.text)
        if score_match:
            print(f"\n🎯 Extracted Score: {score_match.group()}")

        break

    except Exception as e:
        print(f"⚠️ Attempt {attempt+1} failed... Retrying...")
        time.sleep(2)

        if attempt == 2:
            print("\n❌ Failed after multiple attempts.")
            print("Error:", e)