import fitz
import numpy as np
import hashlib
from PIL import Image
import re
import requests
import io
import easyocr
from pdf2image import convert_from_bytes
import json

def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_text(bbox,reader,page_img):
    new = page_img.crop(bbox)
    bounds = reader.readtext(np.array(new), paragraph= True, x_ths = 2.0)
    lst = [bounds[i][1] for i in range(len(bounds))]
    return lst


def get_data(slug = "slugName"):
    url = "http://gallantrymedals.gov.in/IPSII/PDF/JH.pdf"
    res = requests.get(url)
    pdf_bytes = res.content
    states = ["Andaman and Nicobar", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
              "Chhattisgarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
              "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh",
              "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Puducherry", "Punjab", "Rajasthan", "Sikkim",
              "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
    pdf_image = convert_from_bytes(pdf_bytes)
    doc = fitz.open("pdf", stream=pdf_bytes)
    reader = easyocr.Reader(['en'])
    list_of_dict = []
    for i in range(len(pdf_image)):
        page_img = pdf_image[i]
        page_img_bbox = page_img.getbbox()  # get the bbox of whole pdf
        y_bottom_page = page_img_bbox[3]   # get the coordinate of y_bottom of page
        page_doc = doc[i]
        all_words = page_doc.get_text("words")    # extract all the words along with their bbox
        y_cor = []                              # collect all the y_cordinates to crop a particular row
        for w in all_words:
            if w[4] == "RR" or w[4] == "SPS":   # RR and SPS are used to get the y_cordinates
                y_cor.append(w[1] * 2.7779)        # multiplying a constant to comply with the change in dimension, when pdf is converted into image
        y_cor.append(y_bottom_page)
        print(i)
        for y in range(len(y_cor)-1):
            dict = {}
            bbox_name_education = (243, y_cor[y], 619.3, y_cor[y + 1])
            bbox_recrut_state = (619.3, y_cor[y], 793.8, y_cor[y + 1])
            bbox_dob = (793.8, y_cor[y], 1036.8, y_cor[y + 1])
            bbox_present_post = (1036.8, y_cor[y], 1355.0, y_cor[y + 1])
            bbox_medals = (1355.0, y_cor[y], 1653.0, y_cor[y + 1])
            name_edu = get_text(bbox_name_education, reader,page_img)    # calling get text function
            recrut_st = get_text(bbox_recrut_state, reader,page_img)    # calling get text function
            dob_doa = get_text(bbox_dob, reader,page_img)               # calling get text function
            pres_post = get_text(bbox_present_post, reader,page_img)     # calling get text function
            medals = get_text(bbox_medals, reader,page_img)             # calling get text function


            if len(name_edu) > 2:
                name = name_edu[1]
                dict["fullName"] = re.sub("\$","S", name)
                dict["educationInfo"] = name_edu[2]
            else:
                dict["fullName"] = name_edu[1]


            dict["additionalInfo"] = "Source of Recruitment: " + recrut_st[0]
            for word in recrut_st:
                if re.match("[0-9]+", word):
                    dict["additionalInfo"] += "; ID NO.: " + word
                elif word.strip() in states:
                    dict["state"] = word

            if len(dob_doa):
                dict["dob"] = dob_doa[0]
                if len(dob_doa) > 1:
                    if re.match("[0-9]+/[0-9]+/[0-9]+", dob_doa[1]):
                        dict["importantDates"] = "Date of Appointment to IPS: " + dob_doa[1]


            if len(pres_post):
                if re.match("^Level", pres_post[-1]):
                    dict["additionalInfo"] += " ; Pay Scale: " + pres_post.pop(-1)
                lop = ""
                for p in pres_post:
                    if not re.match("[0-9]+/[0-9]+/[0-9]+", p):
                        dopc = re.findall("[0-9]+/[0-9]+/[0-9]+", p)
                        if len(dopc):
                            dict["importantDates"] += " ; Date of Appointment to the Present Post: " + dopc[0]
                            lop += " " + re.sub(" [0-9]+/[0-9]+/[0-9]+", "", p)
                        else:
                            lop += p
                    else:
                        dict["importantDates"] += " ; Date of Appointment to the Present Post: " + p
                if len(lop):
                    dict["designation"] = lop

            if len(medals):
                dict["additionalInfo"] += " ; Medals: " + medals[0]


            attributes = list(dict.keys())
            hash_str = ""
            for attr in attributes:
                hash_str += dict[attr]
            dict["RawHtml"] = get_hash_of_html(hash_str)
            if len(dict["fullName"].split(" ")[0])>2:
                if "state" in list(dict.keys()) and "designation" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra, currently posted as {}. {} was born on {} in {}".format(dict["fullName"], dict["designation"], dict["fullName"].split(" ")[0], dict["dob"], dict["state"])
                elif "state" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra. {} was born on {} in {}".format(
                        dict["fullName"], dict["fullName"].split(" ")[0], dict["dob"], dict["state"])
                elif "designation" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra, currently posted as {}. {} was born on {}".format(
                        dict["fullName"], dict["designation"], dict["fullName"].split(" ")[0], dict["dob"])
                else:
                    dict["summary"] = "{} is an IPS officer in Maharashtra. {} was born on {}".format(
                        dict["fullName"], dict["fullName"].split(" ")[0], dict["dob"])
            else:
                if "state" in list(dict.keys()) and "designation" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra, currently posted as {}. {} was born on {} in {}".format(
                        dict["fullName"], dict["designation"], dict["fullName"], dict["dob"], dict["state"])
                elif "state" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra. {} was born on {} in {}".format(
                        dict["fullName"], dict["fullName"], dict["dob"], dict["state"])
                elif "designation" in list(dict.keys()):
                    dict["summary"] = "{} is an IPS officer in Maharashtra, currently posted as {}. {} was born on {}".format(
                        dict["fullName"], dict["designation"], dict["fullName"], dict["dob"])
                else:
                    dict["summary"] = "{} is an IPS officer in Maharashtra. {} was born on {}".format(
                        dict["fullName"], dict["fullName"], dict["dob"])

            dict["UpdationFlag"] = True
            list_of_dict.append(dict)

    return list_of_dict



def to_json(data):
    with open("judge.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()



if __name__ == "__main__":
    to_json(get_data())