# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:24:21 2022

@author: sride
"""

import sys
import googleapiclient.discovery

ZONE_NAME           = 'us-east1-b'                      # Zone name
PROJECT_NAME        = 'projects/clever-span-340206'            # Project name
IMAGE_NAME          = "ubuntu-1804-lts"                 # Image name
IMAGE_PROJECT_NAME  = "ubuntu-os-cloud"                 # Image project name
INSTANCE_TYPE       = "n1-standard-1"                   # Instance type
INSTANCE_NAME       = "demo_instance"                     # Name of the instance


def list_instances():
    """
    List all Compute Engine VM instances associated with an Google Cloud account
    """
    # Build and initialize the API
    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Listing VM instances ...')

    # Describe instances
    response = compute.instances().list(project=PROJECT_NAME, zone=ZONE_NAME).execute()
    print('Instances in project "%s" and zone "%s":' % (PROJECT_NAME, ZONE_NAME))
    if (response.get('items')):
        for instance in response['items']:
            print(' - Id:           ' + instance['id'])
            print('   Name:         ' + instance['name'])
            print('   Status:       ' + instance['status'])
            print('   Machine type: ' + instance['machineType'])
    else:
        print('NO instances')

    return


def create_instance():
    """
    Create a Compute Engine VM instance
    """
    # Build and initialize the API
    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Creating VM instance ...')

    # Get the latest image
    image_response = compute.images().getFromFamily(
                              project=IMAGE_PROJECT_NAME, family=IMAGE_NAME).execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    #machine_type = 'zones/' + ZONE_NAME + '/machineTypes/' + INSTANCE_TYPE
    machine_type = 'zones/%s/e2-medium/%s' % (ZONE_NAME, INSTANCE_TYPE)

    config = {
          'name': INSTANCE_NAME,
          'machineType': machine_type,

          # Specify the boot disk and the image to use as a source.
          'disks': [
              {
                  'boot': True,
                  'autoDelete': True,
                  'initializeParams': {
                      'sourceImage': source_disk_image,
                  }
              }
          ],

          # Specify a network interface with NAT to access the public
          # internet.
          #'networkInterfaces': [{
           #   'network': 'global/networks/default',
            ##     {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
              ##}],

          # Allow the instance to access cloud storage and logging.
          'serviceAccounts': [{
              'email': 'default',
              'scopes': [
                  'https://www.googleapis.com/auth/devstorage.read_write',
                  'https://www.googleapis.com/auth/logging.write',
                  'https://www.googleapis.com/auth/monitoring'
              ]
          }]
    }

    response = compute.instances().insert(project=PROJECT_NAME,
                              zone=ZONE_NAME,
                              body=config).execute()

    print('Instance Id: ' + response['targetId'])

    return response['targetId']


def list_instance(instance_id):
    """
    List a Compute Engine VM instance
    """
    # Build and initialize the API
    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Listing VM instance ...')
    print('Instance Id: ' + instance_id)

    # List the VM instance
    response = compute.instances().get(project=PROJECT_NAME, zone=ZONE_NAME, instance=INSTANCE_NAME).execute()

    print(' - Id:           ' + response['id'])
    print('   Name:         ' + response['name'])
    print('   Status:       ' + response['status'])
    print('   Machine type: ' + response['machineType'])

    return


