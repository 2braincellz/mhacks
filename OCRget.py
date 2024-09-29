import os
from google.cloud import vision
from groq import Groq
import base64
import streamlit as st
from io import BytesIO

os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./handwriting-437018-cdcb9caaa04e.json"

def detect_document(path):
    """Detects document features in an image."""

    output = open("rawtext.txt", "w");

    client = vision.ImageAnnotatorClient.from_service_account_json("./handwriting-437018-cdcb9caaa04e.json")

    with open(path, "rb") as image_file:
        content = image_file.read()
    # image_file = BytesIO(path.read())
    # content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image, image_context={"language_hints": ["en"]})

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                # print("Paragraph confidence: {}".format(paragraph.confidence))
                # output.write("Paragraph confidence: {}".format(paragraph.confidence)+"\n")

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    # print(
                    #     "Word text: {} (confidence: {})".format(
                    #         word_text, word.confidence
                    #     )
                    # )
                    output.write(word_text+" ")

                    # for symbol in word.symbols:
                    #     print(
                    #         "\tSymbol: {} (confidence: {})".format(
                    #             symbol.text, symbol.confidence
                    #         )
                    #     )


    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def spell_check(filePath):
    with open(filePath, "r") as f:
        fileContent = f.read()
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{
            "role" : "user",
            "content" : "Given this string of text: "+ fileContent + "fix misspelled English words and remove unnecessary whitespace. Do not make additional comments. Do not change the arrangements of words."
        }]
    )
    with open(filePath, "w") as f:
        f.write(completion.choices[0].message.content)


def cross_reference(filePath, imagePath):
    with open(filePath, "r") as f:
        fileContent = f.read()
    client = Groq()
    with open(imagePath, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode('utf-8')
    # bytes_data = imagePath.getvalue()
    # base64_img = base64.b64encode(bytes_data).decode('utf-8')
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Format the following string: "+fileContent+"\n based on the structure of the text in the image, including proper line breaks. Do not change the spelling of any word. Separate each paragraph and do not bold or italicize. Do not comment"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_img}",
                    },
                    }
                ]
            },
        ]
      )
    with open(filePath, "w") as f:
        f.write(completion.choices[0].message.content) 
    # print(completion.choices[0].message.content)


def readImage(filePath):
    detect_document(filePath)
    spell_check("rawtext.txt")
    cross_reference("rawtext.txt", filePath)



# readImage("./test4.webp")