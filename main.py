#Importing  the necessary modules
from flask import Flask, request, jsonify
import boto3
import logging
import datetime
import requests

AWS_sts = boto3.client("sts")
assumed_role_credentials =  AWS_sts.assume_role(
                                       RoleArn="arn:aws:iam::130159455024:role/Bibin_Role",
                                       RoleSessionName="Readingroute53data", DurationSeconds=3600)['Credentials']

session = boto3.Session(aws_access_key_id=assumed_role_credentials["AccessKeyId"],
                                                 aws_secret_access_key=assumed_role_credentials["SecretAccessKey"],
                                                 aws_session_token=assumed_role_credentials['SessionToken'],
                                                 region_name='us-east-1')
#rt= session.client("route53")
AWS_ACCESS_KEY_ID = assumed_role_credentials["AccessKeyId"]
AWS_SECRET_KEY = assumed_role_credentials["SecretAccessKey"]
AWS_SESSION_TOKEN = assumed_role_credentials["SessionToken"]

#AWS_SECURITY_TOKEN = assumed_role_credentials["SessionToken"]




# Creating client 
rt=boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
app= Flask(__name__)
#creating end-points
@app.route('/', methods=['GET', 'POST'])
#creationg function to get hostedzones
def get_hostedzone():
    response=rt.list_hosted_zones()
    response1=response['HostedZones'][0]
    return jsonify(response1)
#creating end-points
@app.route('/record_create', methods=['POST'])

#function to create recordset under "qdatalabs.com"
def create_recordset():
    name=request.json["name"]
    ip=request.json["ip"]
    rt=boto3.client('route53')
    response=rt.list_hosted_zones_by_name(DNSName='qdatalabs.com')
    response1=response['HostedZones'][0]['Id']
    rt.change_resource_record_sets(
    HostedZoneId=response1,
      ChangeBatch={
        'Changes': [
            {                                                       
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': name,
                    'Type': 'A',
                    'TTL': 123,
                    'ResourceRecords': [
                        {
                            'Value': ip                         }
                    ]
                     }}]})
    return("success")

   
#creating end-point
@app.route('/record_delete', methods=['POST'])
#function to delete recordset under "qdatalabs.com"
def delete_recordset():
    name=request.json["name"]
    ip=request.json["ip"]
    rt=boto3.client('route53')
    response=rt.list_hosted_zones_by_name(DNSName='qdatalabs.com.')
    response1=response['HostedZones'][0]['Id']
    rt.change_resource_record_sets(
    HostedZoneId=response1,
      ChangeBatch={
        'Changes': [
            {                                                       
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': name,
                    'Type': 'A',
                    'TTL': 123,
                    'ResourceRecords': [
                        {
                            'Value': ip
                         }
                    ]
                     }}]})
    return  "Record has been successfully Deleted"
                    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
  


