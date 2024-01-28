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

# snippet-start:[python.example_code.rekognition.image_detection_imports]
import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os

from rekognition_objects import (
    RekognitionFace,
    RekognitionLabel,
    RekognitionText,
    show_bounding_boxes,
)

logger = logging.getLogger(__name__)

# snippet-end:[python.example_code.rekognition.image_detection_imports]
# labels = street_scene_image.detect_labels(100)

# snippet-start:[python.example_code.rekognition.RekognitionImage]
class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """

    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    # snippet-end:[python.example_code.rekognition.RekognitionImage]

    # snippet-start:[python.example_code.rekognition.RekognitionImage.from_file]
    @classmethod
    def from_file(cls, image_file_name, rekognition_client, image_name=None):
        """
        Creates a RekognitionImage object from a local file.

        :param image_file_name: The file name of the image. The file is opened and its
                                bytes are read.
        :param rekognition_client: A Boto3 Rekognition client.
        :param image_name: The name of the image. If this is not specified, the
                           file name is used as the image name.
        :return: The RekognitionImage object, initialized with image bytes from the
                 file.
        """
        with open(image_file_name, "rb") as img_file:
            image = {"Bytes": img_file.read()}
        name = image_file_name if image_name is None else image_name
        return cls(image, name, rekognition_client)

    # snippet-end:[python.example_code.rekognition.RekognitionImage.from_file]

    # snippet-start:[python.example_code.rekognition.DetectFaces]
    # TODO: Plan to identify face in case of NO HELMET
    def detect_faces(self):
        """
        Detects faces in the image.

        :return: The list of faces found in the image.
        """
        try:
            response = self.rekognition_client.detect_faces(
                Image=self.image, Attributes=["ALL"]
            )
            faces = [RekognitionFace(face) for face in response["FaceDetails"]]
            logger.info("Detected %s faces.", len(faces))
        except ClientError:
            logger.exception("Couldn't detect faces in %s.", self.image_name)
            raise
        else:
            return faces

    # snippet-end:[python.example_code.rekognition.DetectFaces]

    # snippet-start:[python.example_code.rekognition.DetectLabels]
    def detect_labels(self, max_labels):
        """
        Detects labels in the image. Labels are objects and people.

        :param max_labels: The maximum number of labels to return.
        :return: The list of labels detected in the image.
        """
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels
            )
            labels = [RekognitionLabel(label) for label in response["Labels"]]
            logger.info("Found %s labels in %s.", len(labels), self.image_name)
        except ClientError:
            logger.info("Couldn't detect labels in %s.", self.image_name)
            raise
        else:
            return labels

    # snippet-end:[python.example_code.rekognition.DetectLabels]

    # snippet-start:[python.example_code.rekognition.DetectText]
    # TODO: Plan to identify license plate in case of NO HELMET
    def detect_text(self):
        """
        Detects text in the image.

        :return The list of text elements found in the image.
        """
        try:
            response = self.rekognition_client.detect_text(Image=self.image)
            texts = [RekognitionText(text) for text in response["TextDetections"]]
            logger.info("Found %s texts in %s.", len(texts), self.image_name)
        except ClientError:
            logger.exception("Couldn't detect text in %s.", self.image_name)
            raise
        else:
            return texts

    # snippet-end:[python.example_code.rekognition.DetectText]

def display_vehicle_in_a_box(labels, img_scene):
    names = []
    box_sets = []
    colors = ["aqua", "red", "white", "blue", "yellow", "green"]
    for label in labels:
        if label.instances:
            # print("Has instance:", label.name)
            if label.name not in ("Vehicle", "Moped", "Motor Scooter", "Motorcycle"):
                continue
            names.append(label.name)
            box_sets.append([inst["BoundingBox"] for inst in label.instances])
    if len(names):
        print(f"Showing bounding boxes for {names} in {colors[:len(names)]}.")
        show_bounding_boxes(
            img_scene.image["Bytes"], box_sets, colors[: len(names)]
        )

# snippet-end:[python.example_code.rekognition.Usage_ImageDetection]

def display_helmet_in_a_box(labels, img_scene):
    names = []
    box_sets = []
    colors = ["aqua", "red", "white", "blue", "yellow", "green"]
    for label in labels:
        if label.instances:
            # print("Has instance:", label.name)
            # if label.name not in ("helmet", "Helmet", "Crash Helmet", "Motorcycle"):
            #     continue
            names.append(label.name)
            box_sets.append([inst["BoundingBox"] for inst in label.instances])
    if len(names):
        print(f"Showing bounding boxes for {names} in {colors[:len(names)]}.")
        show_bounding_boxes(
            img_scene.image["Bytes"], box_sets, colors[: len(names)]
        )


def check_if_helmet(img_file_name):
    # print("-" * 88)
    # print("Welcome to the Amazon Rekognition image detection demo!")
    # print("-" * 88)

    # logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    rekognition_client = boto3.client("rekognition",                  
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                    aws_secret_access_key =os.environ.get('AWS_SECRET_KEY'),
                    region_name=os.environ.get('AWS_DEFAULT_REGION'))

    street_scene_image = RekognitionImage.from_file(
        img_file_name, rekognition_client
    ) 

    # print(f"Detecting labels in {street_scene_image.image_name}...")
    labels = street_scene_image.detect_labels(100)
    
    # print(f"Found {len(labels)} labels.")
    is_2_wheeler = False
    is_helmet = False
    
    for label in labels:
        detected_obj = label.to_dict()
        pprint(detected_obj)
        if detected_obj["name"] in ["Motorcycle", "Motor Scooter", "Moped"] and detected_obj["confidence"] > 50:
            is_2_wheeler = True
        if detected_obj["name"] in ["Helmet", "helmet"] and detected_obj["confidence"] > 50:
            is_helmet = True

    if is_2_wheeler and is_helmet:
        return (True, street_scene_image, labels) 
    elif not is_2_wheeler:
        return (True, street_scene_image, labels)

    return (False, street_scene_image, labels)

if __name__ == "__main__":
    # usage_demo()
    img_files = [ ".media/istockphoto-1189505927-612x612.jpg",
        ".media/without-helmet.jpeg",
    ]

    for img_file_name in img_files:
        (helmet_detected, img_scene, labels) = check_if_helmet(img_file_name)
        if helmet_detected:
            print("Helmet detected in", img_file_name)
            display_helmet_in_a_box(labels, img_scene)
        else:
            print("Helmet is not detected in", img_file_name)
            # TODO: Show face 
            # TODO: Show license plate
            display_vehicle_in_a_box(labels, img_scene)
        print("")
        user_input_continue=input("Press to continue")
