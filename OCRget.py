import os
from google.cloud import vision
from groq import Groq
import base64

def detect_document(path):
    """Detects document features in an image."""

    output = open("rawtext.txt", "w");

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

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

def cross_reference(filePath, imagePath):
    with open(filePath, "r") as f:
        fileContent = f.read()
    client = Groq()
    with open(imagePath, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode('utf-8')
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Format the following string: "+fileContent+"based on the structure of the text in the image. Do not change the spelling of any word. Make no comments."
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
    print(completion.choices[0].message.content)




imagePath = "./test.webp"
detect_document(imagePath)
cross_reference("rawtext.txt", imagePath)