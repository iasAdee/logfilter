import pytesseract
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import base64
import string
import io
import os
import time
import pandas as pd
import json

def extract_text_tesseract(image_input):
    """
    Extract text from image - accepts either file path or bytes
    """
    try:
        # If input is bytes, convert to PIL Image
        if isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input))
        # If input is string (file path)
        elif isinstance(image_input, str):
            image = Image.open(image_input)
        # If already a PIL Image
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            raise ValueError("Input must be file path, bytes, or PIL Image")
        
        # Configure for German and English
        custom_config = r'--oem 3 --psm 6 -l deu+eng'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        return text
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
    

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
        images = page.get_images(full=True) 
        
        if(len(charge)<1):
            if (page_number == len(doc)-1):
                multi_images.append(images_list)
                images_list = []   
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
        if(len(text) == 0):
            print(len(text), text_data, page_number)
            continue

        images = page.get_images(full=True) 

        images_sorted = sorted(images, key=lambda x: x[0])
        if(len(images_sorted)<4):
            continue
        else:
            print(f"{page_number} accepted: {text.split(':')[1].strip()}, {len(doc)}")

        for img_index, img in enumerate(images_sorted):

            xref = img[0]  
            if(img[3] <150):
                continue
                
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]  # e.g. 'png', 'jpeg'

            # Construct file name
            filename = f"{text}_{page_number}_{img_index}.{ext}"
            filename = filename.replace(" ", "_")  # avoid spaces
            

            base_image = doc.extract_image(xref)  
            image_bytes = base_image["image"]  
            
            if(img_index <=1):
                tesract_text = extract_text_tesseract(image_bytes)
                images_list.append((tesract_text, str(text+": "+str(page_number)+str(img_index))))
            else:
                images_list.append((image_bytes, str(text+": "+str(page_number)+str(img_index))))
                
        ref[text.split(":")[1].strip()] = [first_val, second_val]

        if(page_number > 2 and len(images_list) %20 == 0):
            print("Adding list for page: ", page_number)
            multi_images.append(images_list)
            images_list = []
        elif(page_number == len(doc)-1):
            print("Adding list for page: ", page_number)
            multi_images.append(images_list)
            images_list = []

        

    df_dict = pd.DataFrame.from_dict(ref, orient='index', columns=['Material', 'Quantity'])
    df_dict.index.name = 'Bild1_nummer'
    df_dict.reset_index(inplace=True)

    prompt_list =[]
    for multi_list in multi_images:
        prompt_parts = process_40_images(multi_list)
        prompt_list.append(prompt_parts)


    return prompt_list, df_dict


def process_40_images(image_bytes_list):
    if len(image_bytes_list) > 30:
        return {"error": "The image_bytes_list must contain less than 110 images."}

    prompt_parts = []
    for index, item in enumerate(image_bytes_list):  # Enumerate to get index
        try:
            
            content = item[0]
        
            if isinstance(content, bytes):
                # It's bytes: Process with BytesIO
                image = Image.open(BytesIO(content))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                prompt_parts.append(f"Image {item[1]}:")
                prompt_parts.append({
                    "mime_type": "image/jpeg",
                    "data": image_base64,
                }) 
            elif isinstance(content, str):
                # It's a string: Treat as a file path or URL
                prompt_parts.append(f"Image {item[1]}: {content}")
                
            
        except Exception as e:
            return {"error": f"Error processing image {index + 1}: {e}"}
        
    prompt_parts.append("""
    Two types of input contents are given to you with there indexs:
    
    TEXT Inputs :- TEXT with index ending in "00" or "01" → extract product label information.
    Image Inputs :- Images with index ending in "02" or "03" → extract numeric codes printed on round bottle bottoms.

    1. Only extract a value if you are 100% certain it is correct and explicitly present AND readable in the image.  
    2. If there is ANY doubt, noise, partial text, low clarity, or multiple possible interpretations, return an empty string ("") for that field.

    --------------------------------------------
    RULES FOR TEXT INPUTS INDEX ENDING WITH 0 / 1
    --------------------------------------------

    1) **Label**  
       - Must be the main product name printed clearly  
       - Example: “Sika® Paint Aktivator”

    2) **Batch No**  
       - Must match a numeric 
       - Examples:
            - “18467849391”

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
    Return the data as a RAW JSON LIST of objects. Do not include any conversational text, markdown formatting, or code blocks (like ```json). 

    Each object in the list must have these exact keys:
    "PO_Number", "lable 01", "ml 01", "best before 01", "artikel 01", "batch no 01", "lable 02", "ml 02", "best before 02", "artikel 02", "batch no 02", "10_digit_numeric_02", "10_digit_numeric_03"

    Do not guess. Do not infer. Do not hallucinate. If a value is not found, use an empty string""")



    return prompt_parts

def create_match_column(df):

    df = df.copy()

    df['Match'] = 'nicht übereinstimmend'

    def is_valid(series):
        return (
            series.notna() & 
            (series.astype(str).str.strip() != '') & 
            (series.astype(str).str.strip() != 'nan') &
            (series.astype(str).str.strip() != 'None')
        )

    mask = (
        is_valid(df['Bild1_label']) & is_valid(df['Bild2_label']) &
        (df['Bild1_label'] == df['Bild2_label']) &

        is_valid(df['Bild1 ML']) & is_valid(df['Bild ML']) &
        (df['Bild1 ML'] == df['Bild ML']) &

        is_valid(df['BatchNO1']) & is_valid(df['BatchNO2']) &
        (df['BatchNO1'] == df['BatchNO2']) &

        is_valid(df['BottleInfo1']) & is_valid(df['BottleInfo2']) &
        (df['BottleInfo1'] == df['BottleInfo2']) &

        is_valid(df['Bild1_Date']) & is_valid(df['Bild2_Date']) &
        (df['Bild1_Date'] == df['Bild2_Date']) &

        is_valid(df['Material']) & is_valid(df['BottleInfo2']) &
        (
            df['Material'].astype(str).str.strip() ==
            df['BottleInfo2'].astype(str).str.strip()
        ) &

        is_valid(df['Artikel NO Bild1']) & is_valid(df['Artikel NO Bild2']) &
        (
            df['Artikel NO Bild1'].astype(str).str.strip() ==
            df['Artikel NO Bild2'].astype(str).str.strip()
        )
    )

    df.loc[mask, 'Match'] = 'übereinstimmend'

    return df

import google.generativeai as genai
import re

def get_results(doc, api_key=""):
    
    os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"]) 
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt_list,df_dict = make_image_lists(doc)
    
    
    #calling LLM model gemini
    responses= []
    print(f"Total Responses {len(prompt_list)}")
    for i, prompt_parts in enumerate(prompt_list):
        try:
            response = model.generate_content(prompt_parts)
            responses.append(response)
            print(f"response {i+1}: completed") 
            #if(i>=1):
            #    break
        except Exception as e:
            print(e)
    print("All responses completed")
    
    # checking for only 1 
    data_list = []
    for response in responses:
        raw_content = response.text
        raw_content = raw_content.replace("```json", "").replace("```", "").strip()
        data_list.extend(json.loads(raw_content))
        
    # 3. Create the DataFrame
    df = pd.DataFrame(data_list)
    columns = [
        "Bild1_nummer","Bild1_label", "Bild1 ML", "Bild1_Date", "Artikel NO Bild1", "BatchNO1",
        "Bild2_label", "Bild ML", "Bild2_Date", "Artikel NO Bild2", "BatchNO2", "BottleInfo1", "BottleInfo2"
    ]
    
    df.columns = columns
    df_merged = df.merge(df_dict, on='Bild1_nummer', how='inner')

    def extract_main_id(text):
        """
        Extract the 10-digit main ID from BottleInfo string.
        If multiple numbers exist, take the first 10-digit number.
        """
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


    for col in df_merged.columns:
        df_merged[col] = (
            df_merged[col]
            .astype(str)              # ensure string type
            .str.strip()              # remove leading/trailing spaces
            .str.replace('\u00A0', '', regex=False)  # remove non-breaking spaces
            .str.replace('\s+', ' ', regex=True)     # normalize multiple spaces
        )
    df_merged = create_match_column(df_merged)

    return df_merged


    

    