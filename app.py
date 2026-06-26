import streamlit as st 
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client=genai.Client(

api_key=st.secrets("GEMINI_API_KEY")
)


st.title("📚 AI Study Buddy")
st.caption("Learn Smarter with AI😊")


uploaded_file=st.file_uploader(
   "Upload PDF",
   type=["pdf"]
)

text=""

if uploaded_file:

   st.success("PDF Uploaded")

   pdf=PdfReader(uploaded_file)


   for page in pdf.pages:


      page_text=page.extract_text()

      if page_text:
         text+=page_text + "\n"
st.write(text[:1000])


if st.button("Generate Summary"):

   if text.strip()=="":
      st.warning("Please upload a PDF first.")

   else:

     with st.spinner("Generating Summary..."):

       response=client.models.generate_content(
                  model="gemini-2.5-flash",
                  contents=f"""
you are an expert study assistant.

Summarize these notes in easy language.

{text[:12000]}
"""

      )

   summary =response.text

   st.subheader("Summary")

   st.write(summary)


   st.download_button("Download Summary",
      summary,
      file_name="summary.txt"
   )


st.divider()

st.subheader("💬 Ask Questions")

question = st.text_input(
    "Ask anything from the uploaded PDF"
)

if st.button("Get Answer"):

    if text.strip() == "":
        st.warning("Please upload a PDF first.")

    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
You are an AI Study Buddy.

Answer ONLY from the notes below.

If the answer is not available in the notes, reply:

"Sorry, this information is not available in the uploaded notes."

NOTES:

{text[:12000]}

QUESTION:

{question}
"""
            )

        answer = response.text

        st.subheader("Answer")

        st.write(answer)

        st.download_button(
            "Download Answer",
            answer,
            file_name="answer.txt"
        )


st.divider()

if st.button("Generate Quiz"):

    if text.strip() == "":
        st.warning("Please upload a PDF first.")

    else:

        with st.spinner("Creating Quiz..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Create 10 multiple-choice questions from these notes.

Format:

Question
A)
B)
C)
D)

Answer:

{text[:12000]}
"""
            )

        quiz = response.text

        st.subheader("Quiz")

        st.write(quiz)

        st.download_button(
            "Download Quiz",
            quiz,
            file_name="quiz.txt"
        )


st.divider()

if st.button("Generate Flashcards"):

    if text.strip() == "":
        st.warning("Please upload a PDF first.")

    else:

        with st.spinner("Generating Flashcards..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Create flashcards from these notes.

Format:

Q:
A:

{text[:12000]}
"""
            )

            flashcards = response.text

        
            st.subheader("Flashcards")
            st.write(flashcards)

            st.download_button(
               "Download Flashcards",
               data=flashcards,
               file_name="flashcards.txt"        
)



with st.sidebar:

   st.title("📚AI Study Buddy")

   st.markdown("---")

   st.write("### Features")

   st.write("✔️ PDF Uploaded")

   st.write("✔️ AI Summary")

   st.write("✔️ Ask Questions")

   st.write("✔️ Quiz Generator")

   st.write("✔️ Flashcards")

   st.markdown("---")

   st.info("Built with Google Gemini")

if uploaded_file:
   st.success(f"Uploaded:{uploaded_file.name}")


with st.expander("Preview Extracted Text"):
   st.write(text[:1500])



if not uploaded_file:
   st.warning("Please upload a PDF first.")
   st.stop()


st.markdown("---")









