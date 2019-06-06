from flask import Flask, render_template, url_for, flash, redirect, request
from forms import dnscreate, dnsdelete, dns_service, record_list
import boto3
outputnew=[]
app = Flask(__name__)
app.config["SECRET_KEY"]= "1525a1793a7e68be967c47fe6cd5eedd"

@app.route("/dnscreate", methods=['GET', 'POST'])
def create():
    form=dnscreate() 
    if form.validate_on_submit():
      a=form.name.data
      b=form.value.data
      rt=boto3.client('route53') 
      response=rt.list_hosted_zones_by_name(DNSName='qdatalabs.com.') 
      response1=response['HostedZones'][0]['Id']
      rt.change_resource_record_sets(
      HostedZoneId=response1,
      ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': a,
                    'Type': 'A', 
                    'TTL': 123,                                
                    'ResourceRecords': [
                        {
                            'Value': b
                         }
                    ]
                     }}]})
                     
                 
                    
                
 
       
    return render_template('dnscreate.html', title="create", form=form)
@app.route("/dnsdelete", methods=['GET', 'POST'])
def delete():
    form=dnsdelete()  
    if form.validate_on_submit():
      a=form.name.data
      b=form.value.data
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
                    'Name': a,
                    'Type': 'A', 
                    'TTL': 123,                                
                    'ResourceRecords': [
                        {
                            'Value': b
                         }
                    ]}}]})    
     
    return render_template('dnsdelete.html', title="DELETE", form=form)

@app.route("/", methods=['GET', 'POST'])
def service():
    form=dns_service()
    rt=boto3.client('route53') 
    response=rt.list_hosted_zones() 
    response1=response['HostedZones'][0]
    output=response1['Name']
        
    return render_template('dns_sevice.html', title="Home", form=form, response=output)

@app.route("/record_list",methods=['GET', 'POST'])
def list():
    form=record_list()
    rt=boto3.client('route53') 
    response=rt.list_hosted_zones_by_name(DNSName='qdatalabs.com.')  
    response1=response['HostedZones'][0]['Id']
    record=rt.list_resource_record_sets(HostedZoneId=response1)
    split=record['ResourceRecordSets']
    print(split)
    form.listing_record.data=split
    return render_template('record_list.html', title="List", form=form)
    

if __name__== "__main__":
    app.run(debug=True, host='0.0.0.0')
