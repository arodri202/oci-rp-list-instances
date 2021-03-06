# Resource Principle Function for Returning the Instances of the Calling Compartment.

  This function uses Resource Principals to securely receive information about the user's information from OCI and returns a list of all instances within the compartment that calls the function.

  Uses the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html) to create a client that receive user information when called in the OCI or a valid config file exists.

  As you make your way through this tutorial, look out for this icon. ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU) Whenever you see it, it's time for you to perform an action.


Pre-requisites:
---------------
  1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

  2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

### Switch to the correct context
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fn use context <your context name>
  ```
  Check using
  ```
  fn ls apps
  ```

### Create or Update your Dynamic Groups
  In order to use and retrieve information about other OCI Services you must grant access to your Function via a dynamic group. For information on how to create a dynamic group, click [here.](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To)

  When specifying a rule, consider the following examples:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  * If you want all functions in a compartment to be able to access a resource, enter a rule similar to the following that adds all functions in the compartment with the specified compartment OCID to the dynamic group:
  ```
  ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
  ```

  * If you want a specific function to be able to access a resource, enter a rule similar to the following that adds the function with the specified OCID to the dynamic group:
  ```
  resource.id = 'ocid1.fnfunc.oc1.iad.aaaaaaaaacq______dnya'
  ```

### Create or Update Policies
  Now that your dynamic group is created, create a new policy that allows your new dynamic group to inspect any resources you are interested in receiving information about, in this case we will grant access to `instance-family` in the functions related compartment.

  Your policy should look something like this:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  Allow dynamic-group <your dynamic group name> to inspect instance-family in compartment <your compartment name>
  ```

  e.g.

  ```
  Allow dynamic-group demo-func-dyn-group to inspect instance-family in compartment demo-func-compartment
  ```

  For more information on how to create policies, go [here.](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm)

Create application
------------------
  Get the python boilerplate by running:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fn init --runtime python <function-name>
  ```
  e.g.
  ```
  fn init --runtime python list-instances
  ```
  Enter the directory, create a new `__init__.py` file so the directory can be recognized as a package by Python.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  cd list-instances
  touch __init__.py
  ```

### Create an Application that is connected to Oracle Functions
  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]'
  ```
  You can find the subnet-ocid by logging on to [cloud.oracle.com](https://cloud.oracle.com/en_US/sign-in), navigating to Core Infrastructure > Networking > Virtual Cloud Networks. Make sure you are in the correct Region and Compartment, click on your VNC and select the subnet you wish to use.

  e.g.
  ```
  fn create app resource-principal --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]'
  ```

Writing the Function
------------------
### Requirements
  Update your requirements.txt file to contain the following:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fdk
  oci-cli
  oci>=2.2.18
  ```

### Open func.py
  Update the imports so that you contain the following.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```python
  import io
  import json
  from fdk import response

  import oci
  ```

### The Handler method
  This is what is called when the function is invoked by Oracle Functions, delete what is given from the boilerplate and update it to contain the following:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```python
  def handler(ctx, data: io.BytesIO=None):
      signer = oci.auth.signers.get_resource_principals_signer()
      resp = do(signer)
      return response.Response(
          ctx, response_data=json.dumps(resp),
          headers={"Content-Type": "application/json"}
      )
  ```

### The do method
  Create the following method.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```python
  def do(signer):
  ```
  This is where we'll put the bulk of our code that will connect to OCI and return the list of compartments in our tenancy.

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```python
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
  ```
  Here we are creating a [ComputeClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/client/oci.core.ComputeClient.html) from the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html), which allows us to connect to OCI with the resource principal's signer data, since resource principal is already pre-configured we do not need to pass in a valid config dictionary, we are now able to make a call to identity services for information on our compartments.

Test
----
### Deploy the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fn -v deploy --app <your app name>
  ```

  e.g.

  ```
  fn -v deploy --app resource-principal
  ```

### Invoke the function

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-rp-list-instances/master/images/userinput.png?token=AK4AYAUDF7AOJ42DOGGYO725BPUJU)
  ```
  fn invoke <your app name> <your function name>
  ```

  e.g.

  ```
  fn invoke resource-principal list-instances
  ```
  Upon success, you should see all of the instances in your compartment appear in your terminal.
