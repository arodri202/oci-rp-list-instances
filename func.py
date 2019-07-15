# Copyright (c) 2016, 2018, Oracle and/or its affiliates.  All rights reserved.
import io
import json
import sys
from fdk import response

import oci.core

sys.path.append(".")
import rp

def handler(ctx, data: io.BytesIO=None):
    provider = rp.ResourcePrincipalProvider()
    resp = do(provider)
    return response.Response(
        ctx, response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )


def do(provider):
    # List instances (in IAD) --------------------------------------------------------------------------------
    client = oci.core.ComputeClient(provider.config, signer=provider.signer)
    # Use this API to manage resources such as virtual cloud networks (VCNs), compute instances, and block storage volumes.
    try:
        inst = client.list_instances(provider.compartment)

        inst = [[i.id, i.display_name] for i in inst.data]
    except Exception as e:
        inst = str(e)

    resp = {
             "instances": inst,
            }

    return resp

def main():
    # If run from the command-line, fake up the provider by using stock user credentials
    provider = rp.MockResourcePrincipalProvider()
    resp = do(provider)
    print((resp))
    print(json.dumps(resp))


if __name__ == '__main__':
    main()
