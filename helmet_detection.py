#!/usr/local/bin/python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Rekognition to
recognize people, objects, and text in images.

The usage demo in this file uses images in the .media folder. If you run this code
without cloning the GitHub repository, you must first download the image files from
    https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/python/example_code/rekognition/.media
"""
import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import numpy as np 
import cv2
import os
import glob
from rekognition_objects import (
    RekognitionLabel,
    RekognitionText,
)

logger = logging.getLogger(__name__)

rekognition_client = boto3.client("rekognition",
    aws_access_key_id="", #Enter your own aws key id for AWS
    aws_secret_access_key = "", #Enter your own access key for AWS
    region_name="us-east-1")

class RekognitionImage:
    def __init__(self, image, image_name, rekognition_client):
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client
    @classmethod
    def from_file(cls, image_file_name, rekognition_client, image_name=None):
        with open(image_file_name, "rb") as img_file:
            image = {"Bytes": img_file.read()}
        name = image_file_name if image_name is None else image_name
        return cls(image, name, rekognition_client)
    def detect_labels(self, max_labels):
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels
            )
            labels = np.array([RekognitionLabel(label) for label in response["Labels"]])
            logger.info("Found %s labels in %s.", len(labels), self.image_name)
        except ClientError:
            logger.info("Couldn't detect labels in %s.", self.image_name)
            raise
        else:
            return labels

    def detect_text(self):
        try:
            response = self.rekognition_client.detect_text(Image=self.image)
            texts = [RekognitionText(text) for text in response["TextDetections"]]
            logger.info("Found %s texts in %s.", len(texts), self.image_name)
        except ClientError:
            logger.exception("Couldn't detect text in %s.", self.image_name)
            raise
        else:
            return texts
def check_if_helmet(img_file_name):
    street_scene_image = RekognitionImage.from_file(
        img_file_name, rekognition_client
    )  
    # print(f"Detecting labels in {street_scene_image.image_name}...")
    labels = street_scene_image.detect_labels(20)
    # print(f"Found {len(labels)} labels.")
    is_2_wheeler = False
    is_helmet = False
    labels = np.array(labels)
    for label in labels:
        detected_obj = label.to_dict()
        if detected_obj["name"] in ["Motorcycle", "Motor Scooter", "Moped"] and detected_obj["confidence"] > 50:
            is_2_wheeler = True
        if detected_obj["name"] in ["Helmet", "helmet"] and detected_obj["confidence"] > 50:
            is_helmet = True
        if (is_2_wheeler==True) and (is_helmet==True):
            return (True, street_scene_image) 

    if is_2_wheeler and is_helmet:
        return (True, street_scene_image) 
    elif not is_2_wheeler:
        return (True, street_scene_image)
    return (False, street_scene_image)       

def check_if_exists():
    img_files = [".media/without-helmet.jpeg"]
    for img_file_name in img_files:
        (helmet_detected) = check_if_helmet(img_file_name)
        print(helmet_detected)
        if helmet_detected[0]:
            print("Helmet detected in", img_file_name)
        else:
            print("Helmet is not detected in", img_file_name)


check_if_exists()
