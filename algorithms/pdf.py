import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import re
from tqdm import tqdm
import base64
import string
import pandas as pd
import io
import os

import os
import logging
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
# Silence standard python logging for the generativeai library
logging.getLogger('google.generativeai').setLevel(logging.ERROR)
import google.generativeai as genai
import time


def make_image_lists(doc):
    ref = {}
    multi_images = []
    images_list = []
    
    print("Total Pages", len(doc))
    for page_number in range(len(doc)):

        page = doc[page_number]
        text = page.get_text()
        text_data = text.split("\n")

        charge =[val.strip().lower() for val in text_data if len(val) > 1]
        #print(charge)

        images = page.get_images(full=True) 
        #print(len(images))

        #print(charge)
        if(len(charge)<1):
            if (page_number == len(doc)-1):
                multi_images.append(images_list)
                images_list = []   
                print(f"Adding image from lasat {page_number} total images = ", len(images_list))
            continue

        second_val = ""
        first_val = ""
        if("flaschennummer" in charge[-1]):
            second_val = charge[-1].split(" ")
            if(len(second_val) >=1):
                second_val = second_val[1]
            else:
                second_val = charge[charge.index("flaschennummer")+1]

        if("halb-charge" in charge):
            first_val = charge[charge.index("halb-charge")+1]


        text = ""
        artikle = ""

        for i, tex in enumerate(text_data):
            if(tex.startswith("PO")):
                text=tex

            if(tex.startswith("FERT-Artikel-Nummer")):
                artikle = text_data[i+1]


        images = page.get_images(full=True) 
        text_data = text.split(":")

        text = text.split('  ')[0].strip()
        #print(len(text))
        if(len(text) == 0):
            print(len(text), text_data, page_number)
            continue

        images = page.get_images(full=True) 

        images_sorted = sorted(images, key=lambda x: x[0])
        #print(images_sorted)
        if(len(images_sorted)<4):
            #print(f"{page_number} rejected: {text.split(':')[1].strip()}, {len(doc)}")
            continue
        #else:
        #    print(f"{page_number} accepted: {text.split(':')[1].strip()}, {len(doc)}")

        for img_index, img in enumerate(images_sorted):

            xref = img[0]  
            if(img[3] <150):
                #print(img_index, "Small Image")
                continue
   
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]  # e.g. 'png', 'jpeg'

            # Construct file name
            filename = f"{text}_{page_number}_{img_index}.{ext}"
            filename = filename.replace(" ", "_")  # avoid spaces


            base_image = doc.extract_image(xref)  
            image_bytes = base_image["image"]  

            images_list.append((image_bytes, str(text+": "+str(page_number)+str(img_index))))

            if(img_index>3):
                break

        ref[text.split(":")[1].strip()] = [first_val, second_val]

        if((page_number != 0 and page_number %4 == 0) or page_number == len(doc)-1):
            print(f"Adding image {page_number} total images = ", len(images_list))
            multi_images.append(images_list)
            
            images_list = []
            
    return ref, multi_images

import pandas 


def process_200_images(image_bytes_list):
    if len(image_bytes_list) > 80:
        return {"error": "The image_bytes_list must contain less than 110 images."}

    prompt_parts = []
    for index, image_bytes in enumerate(image_bytes_list):  # Enumerate to get index
        try:
            image = Image.open(BytesIO(image_bytes[0]))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            prompt_parts.append(f"Image {image_bytes[1]}:")
            prompt_parts.append({
                "mime_type": "image/jpeg",
                "data": image_base64,
            })
            
            
        except Exception as e:
            return {"error": f"Error processing image {index + 1}: {e}"}

    
    prompt_parts.append("""
    For each image:

    1. Only extract a value if you are 100% certain it is correct and explicitly present AND readable in the image.  
    2. If there is ANY doubt, noise, partial text, low clarity, or multiple possible interpretations, return an empty string ("") for that field.

    Image categories:
    - Images with index ending in "00" or "01" → extract product label information.
    - Images with index ending in "02" or "03" → extract numeric codes printed on round bottle bottoms.

    --------------------------------------------
    RULES FOR IMAGES ENDING WITH 0 / 1
    --------------------------------------------
    Extract the following ONLY if fully visible, readable, and unambiguous:

    1) **Label**  
       - Must be the main product name printed clearly  
       - Example: “Sika® Paint Aktivator”

    2) **Batch No**  
       - Must match a numeric 
       - Examples:
            - “18467849391”
       - Reject if:
            - cropped
            - unclear
            - partly blocked
            - multiple candidates seen

    3) **Best before date**  
       - Must be in clear format:
            - MM/YYYY
            - MM/YY
       - Reject if missing or unclear.

    4) **ml Value**  
       - Must be a number followed by “ml”  
       - Extract only the number  
       - Example:
            - “250ml” → “250”

    5) **Article number**  
       - Numeric only  
       - Length 4–6 digits  
       - Must appear as a standalone number  
       - Reject if attached to text or symbols.

    --------------------------------------------
    RULES FOR IMAGES ENDING WITH 2 / 3
    --------------------------------------------
    - Extract 10 digit long numeric number on round bottle top make sure you are 100% confidant.
    - Do not predict text of image ending with 3 based on text of image ending with 2
    - Return empty ("") if it is not 100% correct and not readable
    - Extract only if:
        - Fully readable and 100% sure correct
        - Not cut or obstructed 
        - Only one valid candidate appears
    

    If multiple candidates exist, or clarity < 100% → return "".

    --------------------------------------------
    OUTPUT FORMAT
    --------------------------------------------

    **Image PO: <PO_NUMBER>: <INDEX>**
    1) <Label or "">
    2) <Batch No or "">
    3) <Best before or "">
    4) <ml or "">
    5) <Artikel or "">

    For images 02 and 03:
    **Image PO: <PO_NUMBER>: <INDEX>**
    <10 digit long numeric number written on round bottle top or "">

    Do not guess. Do not infer. Do not hallucinate. Only extract values that are 100% certain.""")
    return prompt_parts



import pandas as pd
import re
import numpy as np


def parse_po_responses(responses):
    # Combine all responses into one string
    if isinstance(responses, list):
        text = "\n".join(responses)
    else:
        text = responses

    columns = [
        "Bild1_label", "BatchNO1", "Bild1_Date", "Bild1 ML", "Artikel NO Bild1",
        "Bild2_label", "BatchNO2", "Bild2_Date", "Bild ML", "Artikel NO Bild2", "BottleInfo1", "BottleInfo2"
    ]

    # Split text by PO blocks
    po_blocks = re.findall(r"\*\*Image PO: (\d+): (\d+)\*\*(.*?)((?=\*\*Image PO)|$)", text, re.DOTALL)

    rows = []
    current_po = None
    po_values = []

    for po_num, sub_num, content, _ in po_blocks:
        if current_po is None:
            current_po = po_num

        # If PO changes, save the previous PO row
        if po_num != current_po:
            # pad/truncate to 13 values
            po_values += [np.nan] * (13 - len(po_values))
            po_values = po_values[:13]
            row = {"Bild1_nummer": current_po}
            row.update(dict(zip(columns, po_values)))
            rows.append(row)

            # start new PO
            current_po = po_num
            po_values = []

        # Extract numbered entries
        values = re.findall(r"^\s*\d+\)\s*(.+)$", content, re.MULTILINE)
        if not values:
            # fallback for single-line entries
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            values = lines if lines else [np.nan]

        po_values.extend(values)
    

    # Add the last PO
    if po_values:
        po_values += [np.nan] * (13 - len(po_values))
        po_values = po_values[:13]
        row = {"Bild1_nummer": current_po}
        row.update(dict(zip(columns, po_values)))
        rows.append(row)

    df = pd.DataFrame(rows, columns=["Bild1_nummer"] + columns)
    return df


def select_model(api_key, model = "gem25"):
    if(model == "gem25"):
        os.environ["GEMINI_API_KEY"] = api_key
        genai.configure(api_key=os.environ["GEMINI_API_KEY"]) 
        model = genai.GenerativeModel("gemini-2.5-flash")
        return model
    else:
        key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-3.1-pro-preview")
        return model
    

def calculate_pdf_scores(doc, selected_model,  api_key=""):

    ref, multi_images = make_image_lists(doc)

    df_dict = pd.DataFrame.from_dict(ref, orient='index', columns=['Material', 'Quantity'])
    df_dict.index.name = 'Bild1_nummer'
    df_dict.reset_index(inplace=True)

    print("Slected ",selected_model)
    print(api_key)
    model = select_model(api_key, model = selected_model)

    prompt_list =[]
    for bulk in multi_images:

        prompt_parts = process_200_images(bulk)
        prompt_list.append(prompt_parts)

    responses = []
    print("Waiting 5s to stabilize connection...")
    time.sleep(5)

    for i, prompt_parts in enumerate(prompt_list):
        success = False
        while not success:
            try:
                response = model.generate_content(prompt_parts)
                responses.append(response)
                print(f"Prompt {i+1}: Success")
                
                success = True # This breaks the 'while' loop and moves to the next 'for' item
                time.sleep(10) # Your standard 10s safety delay
                
            except Exception as e:
                if "429" in str(e) or "Quota" in str(e):
                    print(f"Quota hit on prompt {i+1}. Sleeping 30s before retrying same prompt...")
                    time.sleep(30)
                else:
                    print(f"Different error occurred: {e}")
                    break # Stops retrying this specific prompt if the error isn't about quota

    responses_text = [res.text for res in responses]
    data=parse_po_responses(responses_text)


    df_merged = data.merge(df_dict, on='Bild1_nummer', how='inner')


    def extract_main_id(text):
        if pd.isna(text):
            return None
        # Find all sequences of digits
        nums = re.findall(r'\d+', str(text))
        # Return the first one with length >= 10 (or adjust based on ID length)
        for n in nums:
            if len(n) >= 10:
                return n
        # Fallback: return first number
        return nums[0] if nums else None

    # Apply to both columns
    df_merged['BottleInfo1'] = df_merged['BottleInfo1'].apply(extract_main_id)
    df_merged['BottleInfo2'] = df_merged['BottleInfo2'].apply(extract_main_id)
    
    def create_match_column(df):
        #df['Artikel NO Bild1'] = df['Artikel NO Bild1'].astype(str).str.strip()
        #df['Artikel NO Bild2'] = df['Artikel NO Bild2'].astype(str).str.strip()
        df['Match'] = 'nicht übereinstimmend'
        df.loc[
            (df['Bild1_label'] == df['Bild2_label']) &
            (df['Bild1 ML'] == df['Bild ML']) &
            (df['BatchNO1'] == df['BatchNO2']) &
            (df['BottleInfo1'] == df['BottleInfo2']) &
            (df['Bild1_Date'] == df['Bild2_Date']) &
            (df['Material'].astype(str).str.strip() == df['BottleInfo2'].astype(str).str.strip()) &
            (df['Artikel NO Bild1'] == df['Artikel NO Bild2']),
            'Match'
        ] = 'übereinstimmend'
        return df

    punct_cols = ['BottleInfo1', 'BottleInfo2']

    for col in df_merged.columns:
        # Base cleaning for all columns
        cleaned = (
            df_merged[col]
            .astype(str)                              # ensure string type
            .str.strip()                              # remove leading/trailing spaces
            .str.replace('\u00A0', '', regex=False)   # remove non-breaking spaces
            .str.replace('\s+', ' ', regex=True)      # normalize multiple spaces
        )
        
        # Remove punctuation only for specific columns
        if col in punct_cols:
            cleaned = cleaned.str.replace(f"[{string.punctuation}]", "", regex=True)
        df_merged[col] = cleaned

    df_merged = create_match_column(df_merged)
    return df_merged



