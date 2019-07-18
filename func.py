# Copyright (c) 2016, 2018, Oracle and/or its affiliates.  All rights reserved.
import io
import json
from fdk import response

import oci

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = do(signer)
    return response.Response(
        ctx, response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def do(signer):
    # List instances (in IAD) --------------------------------------------------------------------------------
    client = oci.core.ComputeClient(config={}, signer=signer)
    # Use this API to manage resources such as virtual cloud networks (VCNs), compute instances, and block storage volumes.
    try:
        inst = client.list_instances(signer.compartment_id)

        inst = [[i.id, i.display_name] for i in inst.data]
    except Exception as e:
        inst = str(e)

    resp = {
             "instances": inst,
            }

    return resp
