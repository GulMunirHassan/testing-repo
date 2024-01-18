# # example.py

# def add_numbers(a, b):
#     return a + b

# def multiply_numbers(a, b):
#     return a * b

# def main():
#     num1 = 5
#     num2 = 3

#     result_sum = add_numbers(num1, num2)
#     result_product = multiply_numbers(num1, num2)

#     print(f"Sum: {result_sum}")
#     print(f"Product: {result_product}")

# if __name__ == "__main__":
#     main()

import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest ,HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm # Replace with your actual import path for the LoginForm
from django.views.decorators.csrf import csrf_exempt
import json 

from django.shortcuts import render
import requests
import json

import asyncio
import aiohttp




def access():     
    url = "https://api-staging.namipay.com.sa/client/get_token"
    payload = 'client_id=merchantapp&client_secret=r4vKbc17kVdKtC8R5jCvQZkgXyICRnW0&grant_type=client_credentials&scope=SCOPE_MERCHANTAPP'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    acces_token = response
    response_json = json.loads(acces_token.text)
    token = response_json.get("access_token")
    return token

"""
def sign_up(request):
    if request.method =='POST':
        username = request.POST.get('user_name')
        ID_number = request.POST.get('ID_Number')
        MobileNumber = request.POST.get('mob_number')
        IsOPT_Enabled = request.POST.get('OPT')
        Resident_Type_ID = request.POST.get('Resident_Type_ID') 
        Reseller_ID = request.POST.get('Reseller_ID')

        url = ""
        payload = json.dumps({
            "User_Name" : username,
            "ID_number" : ID_number,
            "MobileNumber" : MobileNumber,
            "IsOPT_Enabled" : IsOPT_Enabled,
            "Resident_Type_ID" : Resident_Type_ID,
            "Reseller_ID" : Reseller_ID,

        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization':f'Bearer {access()}',  # Replace with your actual access token
        }      
    
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
             print(response.json())
             user_data = response.json()
             return render(request, 'login.html', {'response_data': user_data})
        else:
            # Failed login, handle the error and display an appropriate message
            return render(request, 'error_template.html', {'error_message': 'Login failed'})
    else:
        # Render the login form
        return render(request, 'signup.html')

"""        
def logout_view(request):
    # Clear session data
    request.session.clear()
    # Redirect to the login page or any other desired page after logout
    return redirect('login') 

def sign (request):
    return render(request, 'register.html')


def forget (request):
    return render(request, 'register.html')

from asgiref.sync import sync_to_async
import json
from aiohttp import ClientSession

API_BASE_URL = "https://api-staging.namipay.com.sa/api/"

# Synchronous function that makes an API call
def make_sync_api_call(endpoint, payload):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access()}',  # Replace with your actual access token
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json() if response.status_code == 200 else None


@sync_to_async
def login_view(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        pin_password = request.POST.get('pin_password')

        # Make API call asynchronously
        url = "signuplogin/login"
        payload = json.dumps({
            "ID_Number": id_number,
            "PIN_Password": pin_password
        })
        user_data = make_sync_api_call(url, payload)

        customer_id = user_data.get('result', {}).get('CustomerID')
        request.session['CustomerID'] = customer_id
        if customer_id is None:
            error_message = 'User does not exist or Please Check Username & Password'
            return render(request, 'login.html', {'error_message': error_message})
     
        else:
            CR_Number = user_data.get('result', {}).get('CR_Number')
            request.session['CR_Number'] = CR_Number 
            print(CR_Number)
            Username = user_data.get('result', {}).get('Username')
            request.session['Username'] = Username

            MobileNumber = user_data.get('result', {}).get('MobileNumber')
            request.session['MobileNumber'] = MobileNumber

            api = "https://api-staging.namipay.com.sa/cr/verify"
            payload = json.dumps({
                "ID_Number": id_number,
                "CR_Number": CR_Number,
                "Mobile_Number":  MobileNumber
            })

            headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # Replace with your actual access token
            
            }

            responsev = requests.post(api, payload, headers=headers)

            verification_data = responsev.json()
            print(verification_data)
            request.session['isID_Verified'] = verification_data['result'][0]['isID_Verified']
            request.session['isCR_Verified'] = verification_data['result'][0]['isCR_Verified']
            request.session['isMobile_Verified'] = verification_data['result'][0]['isMobile_Verified']
            request.session['isCRNumber_MerchantAddress_Verified'] = verification_data['result'][0]['isCRNumber_MerchantAddress_Verified']
           

            is_cr_verified = verification_data.get('result', [{}])[0].get('isCR_Verified', False)

        

            if is_cr_verified:
                print(user_data)  # Print the response data to the console for debugging

       
                
                # Successful login, render welcome.html
                return render(request, 'welcom.html', {'response_data': user_data, 'username': Username })
            else:
                # Failed login, render error_template.html
                return render(request, 'errorvali.html', {'error_message': 'Login failed'})
    else:
        # Render the login form
        return render(request, 'login.html')


async def make_api_calll(session, endpoint, customer_id):
    url = f"{API_BASE_URL}{endpoint}?Customer_ID={customer_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access()}',  # Replace with your actual access token
    }
    async with session.get(url, headers=headers) as response:
        return await response.json() if response.status == 200 else None

# Asynchronous view for the home page
async def home(request):
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
       return render(request, 'error_template.html')
    username = await sync_to_async(request.session.get)('Username')
    print('home',customer_id)
    async with aiohttp.ClientSession() as session:
        endpoints = [
            ("merchanttx/duessummary/getbycustomerid", "DUES_SUMMARY"),
            ("merchanttx/duetransactions/getbycustomerid", "Tran"),
            ("merchanttx/merchantdata/getbycustomerid", "MERCHANTDATA")
        ]

        data = {}
        tasks = []
        for endpoint, key in endpoints:
            tasks.append(make_api_calll(session, endpoint, customer_id))

        responses = await asyncio.gather(*tasks)

        for index, (_, key) in enumerate(endpoints):
            data[key] = responses[index] if responses[index] else None

    Tran = data.get('DUE_TRANSACTION_DETAILS')
         
        
    if data.get('DUES_SUMMARY'):
        due = data['DUES_SUMMARY']
        dues = due.get('result', {}).get('DUES_SUMMARY', [])
        if dues:
            Due_Tx = dues[0].get('Due_Tx')
            Due_Tx_Amount = dues[0].get('Due_Tx_Amount')
            Due_Adjustment_Amount = dues[0].get('Due_Adjustment_Amount')
            Due_Fees = dues[0].get('Due_Fees')
            fDue_Tx = '{:,.2f}'.format(Due_Tx)
            fDue_Tx_Amount = '{:,.2f}'.format(Due_Tx_Amount)
            fDue_Adjustment_Amount = '{:,.2f}'.format(Due_Adjustment_Amount)
            fDue_Fees = '{:,.2f}'.format(Due_Fees)
            print(fDue_Fees ,fDue_Tx, fDue_Tx_Amount, fDue_Adjustment_Amount)
    netduepr = 0
    trduepr = 0
    adjduepr = 0
    merchant_data = None
    due_transaction = None
    flast_settled_amount = None 
    fnet_due_amount = None
    tran = None 

    if data.get('MERCHANTDATA'):
        due = data['MERCHANTDATA']
        merchant  = due.get('result', {}).get('PAYMENT_INFO', [])
        print(merchant)
        if merchant:
            last_settled_amount =  merchant[0].get('Last_Settled_Amount')
            net_due_amount = merchant[0].get('Net_Due_Amount')
            last_settled_amount = int(last_settled_amount)
            fnet_due_amount = '{:,.2f}'.format(net_due_amount)
            Due_Adjustment_Amountp = abs(Due_Adjustment_Amount)
            print(Due_Adjustment_Amountp)
            total =  Due_Adjustment_Amountp + Due_Tx_Amount + net_due_amount
            adjduepr = (Due_Adjustment_Amountp/ total) * 100
            trduepr = ( Due_Tx_Amount  / total) * 100
            netduepr = (net_due_amount / total) * 100
            adjduepr = int(adjduepr)
            trduepr = int(trduepr)
            netduepr = int(netduepr)
            print(adjduepr,trduepr, netduepr)
            request.session['fnet_due_amountt'] = fnet_due_amount
            if 'fnet_due_amountt' in request.session:
    # The value is saved in the session
                saved_fnet_due_amount = request.session['fnet_due_amountt']
                print(f"The saved value of fnet_due_amount is: {saved_fnet_due_amount}")
            else:
                print('4')
            
           


    if data.get('Tran'):
        tran = data['Tran']

       
        return render(request, 'home.html', {
             'due_transaction':tran, 
             'netduepr':netduepr,
             'trduepr':  trduepr, 
             'adjduepr': adjduepr, 
             'merchant_data': merchant_data, 
             'customer_id': customer_id, 
             'Due_Tx':fDue_Tx, 
             'Due_Adjustment_Amount':fDue_Adjustment_Amount, 
             'last_settled_amount':flast_settled_amount, 
             'net_due_amount':fnet_due_amount,  
             'Due_Tx_Amount': fDue_Tx_Amount ,
             'Due_Fees':fDue_Fees,
             'username':username
             
        })














async def profile(request):
     
    # Retrieve user data from the session asynchronously
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    username = await sync_to_async(request.session.get)('Username')
    mobile_number = await sync_to_async(request.session.get)('MobileNumber')
    cr_number = await sync_to_async(request.session.get)('CR_Number')
    fnet_due_amount = request.session.get('fnet_due_amount')
 
    if customer_id is None:
       return render(request, 'error_template.html')

    # Create a dictionary with retrieved data
    user_data = {
        "customer_id": customer_id,
        "Username": username,
        "MobileNumber": mobile_number,
        "CR_Number": cr_number,
        # Add other relevant data fields as needed
    }

    # Access and use the retrieved data as required
    print(fnet_due_amount)
    is_ID_verified = request.session.get('isID_Verified')
    is_CR_verified = request.session.get('isCR_Verified')
    is_mobile_verified = request.session.get('isMobile_Verified')
    isCRNumber_MerchantAddress_Verified = request.session.get('isCRNumber_MerchantAddress_Verified')
    print(is_ID_verified, is_CR_verified, is_mobile_verified, isCRNumber_MerchantAddress_Verified)   # For demonstration, printing user_data

    return render(request, 'profile.html', {'Net_Amount':fnet_due_amount, 'isCRNumber_MerchantAddress_Verified':isCRNumber_MerchantAddress_Verified,'mob':is_mobile_verified,'cr':is_CR_verified,'id':is_ID_verified,'user_data':user_data, 'username':username})



async def password (request):
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    print('here')
    

    return render(request, 'password1.html')


import requests
from django.shortcuts import HttpResponse, redirect

def change(request):
    if request.method == 'POST':
        ID_Number = request.POST.get('ID_Number')
        Old_Password = request.POST.get('Old_Password')
        New_Password = request.POST.get('New_Password')
        print(ID_Number, Old_Password, New_Password)

        url = "https://api-staging.namipay.com.sa/api/signuplogin/resetpassword"
        payload = {
            'ID_Number': ID_Number,
            'Old_Password': Old_Password,
            'New_Password': New_Password
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            merchant_data = response.json()
            print(merchant_data)
            if merchant_data.get("success"):
                 error_message = 'Passsword Changed! Successfully'
            return render(request, 'change2.html', {'eerror_message': error_message}) # Redirect on successful password change

    # If it's not a POST request or if the password change fails, return an HttpResponse or appropriate response.
    return HttpResponse("Failed to change password. Please try again.")  # Modify this response as needed

    
async def forgot (request):
   
    

    return render(request, 'forgetpass.html')





def recover(request):
    if request.method == 'POST':
        ID_Number = request.POST.get('ID_Number')
        CR_Number = request.POST.get('CR_Number')
        MobileNumber = request.POST.get('MobileNumber')
        New_Password = request.POST.get('New_Password')

        print(ID_Number, CR_Number, New_Password)

        url = "https://api-staging.namipay.com.sa/api/signuplogin/forgetpassword"
        payload = {
            'ID_Number': ID_Number,
            'CR_Number':  CR_Number,   
            'MobileNumber': MobileNumber,
            'New_Password': New_Password,
        }


        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            merchant_data = response.json()
            print(merchant_data)
            if merchant_data.get("success"):
                 error_message = 'Passsword Recoverd! Successfully'
            return render(request, 'change2.html', {'eerror_message': error_message}) # Redirect on successful password change

    # If it's not a POST request or if the password change fails, return an HttpResponse or appropriate response.
    return HttpResponse("Failed to change password. Please try again.") 






    

def wel (request):
    return render(request, 'welcome.html')




 









async def marchant(request):
        username = await sync_to_async(request.session.get)('Username')
        # Retrieve the customer_id from the session
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
            
            

                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'marchant/marchant.html', {'merchant_data': merchant_data, 'customer_id': customer_id, 'username': username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

    
    

async def marchant_branch (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)

                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'marchant/marchant_branch.html', {'merchant_data': merchant_data, 'customer_id': customer_id, 'username': username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})


async def marchant_account (request): 
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)

                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'marchant/marchant_account.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})


     

async def marchant_terminal (request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    if customer_id:
        # Perform actions using the customer_id
        # Example: Fetch merchant data from an API using the customer_id
        url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            merchant_data = response.json()
            print(merchant_data)
            # Render the 'marchant.html' template with the merchant data and customer_id
            return render(request, 'marchant/marchant_terminal.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
        else:
            # Handle the error in your own way
            return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
    else:
        print("Errorr coming from Nonwe")
        # The customer_id is not available in the session, handle this case as needed
        return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})


async def marchant_payment (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                payment_info = merchant_data.get('result', {}).get('PAYMENT_INFO', [])
                if payment_info:
                    last_settled_amount = payment_info[0].get('Last_Settled_Amount')
                    net_due_amount = payment_info[0].get('Net_Due_Amount')

                    request.session['net_due_amount'] = net_due_amount
            

                    # Printing the values
                    print("Last Settled Amount:", last_settled_amount)
                    print("Net Due Amount:", net_due_amount)
                else:
                    print("No payment information available in the response.")
                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'marchant/marchant_payment.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})
#1
async   def payment_summary (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/settlementsummary/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'payment/payment_summary.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})
        

async def paymentsummary(request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/paymentdetails/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'payment/payment_summary1.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

        
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # You can use WeasyPrint or ReportLab as well




async def generate_pdf(request):
    # Replace this URL with the endpoint providing the required data
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
        url = f"https://api-staging.namipay.com.sa/api/merchanttx/paymentdetails/getbycustomerid?Customer_ID={customer_id}"
        headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            # Extract data from the API response (adjust this based on your API response structure)
            api_data = response.json()
            print(api_data)
            
            # Create a context dictionary using the API data
            context = {
                'merchant_data': api_data,
                # Add more variables as needed based on the data structure
            }

            # Load the Django template file
            template = get_template('my_template.html')

            # Render the template by passing the context data
            rendered_template = template.render(context)

            # Create a PDF file
            response_pdf = HttpResponse(content_type='application/pdf')
            response_pdf['Content-Disposition'] = 'attachment; filename="my_pdf.pdf"'

            # Generate PDF file from rendered HTML content
            pisa_status = pisa.CreatePDF(rendered_template, dest=response_pdf)

            # Check if PDF generation encountered any errors
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + rendered_template + '</pre>')

            # Return the PDF file as an HTTP response
            return response_pdf
        else:
            return HttpResponse('Failed to fetch data from the API')


#2

async def due_summary (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
          
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/duessummary/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                return render(request, 'payment/due_summary.html', {'merchant_data': merchant_data, 'customer_id': customer_id, 'username':username})
            else:
         
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

#3
async def due_transaction (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/duetransactions/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'payment/due_transaction.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

#4
async def due_adjustment (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/dueadjustments/getbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
              
                return render(request, 'payment/due_adjustment.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

async  def ad_adjustment (request):
        username = await sync_to_async(request.session.get)('Username')
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        if customer_id:
            # Perform actions using the customer_id
            # Example: Fetch merchant data from an API using the customer_id
            url = f"https://api-staging.namipay.com.sa/api/merchanttx/settledadjustments/getallbycustomerid?Customer_ID={customer_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                # Render the 'marchant.html' template with the merchant data and customer_id
                return render(request, 'Adjustment/adjustment.html', {'merchant_data': merchant_data, 'customer_id': customer_id,'username':username})
            else:
                # Handle the error in your own way
                return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
        else:
            print("Errorr coming from Nonwe")
            # The customer_id is not available in the session, handle this case as needed
            return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

async def ad_due (request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    if customer_id:
        # Perform actions using the customer_id
        # Example: Fetch merchant data from an API using the customer_id
        url = f"https://api-staging.namipay.com.sa/api/merchanttx/settledadjustments/getallbycustomerid?Customer_ID={customer_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            merchant_data = response.json()
            print(merchant_data)
            # Render the 'marchant.html' template with the merchant data and customer_id
            return render(request, 'Adjustment/due.html', {'merchant_data': merchant_data, 'customer_id': customer_id, 'username':username})
        else:
            # Handle the error in your own way
            return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})
    else:
        print("Errorr coming from Nonwe")
        # The customer_id is not available in the session, handle this case as needed
        return render(request, 'error_template.html', {'error_message': 'Customer ID not found'})

import datetime
async def find (request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    if request.method == 'POST':
        from_date = request.POST.get('from_date', '1-1-1')
        to_date = request.POST.get('to_date')
        terminal_id = request.POST.get('terminal_id')
        reference_number = request.POST.get('reference_number')
        approval_code = request.POST.get('approval_code')
        amount = request.POST.get('amount')
        print(from_date, to_date, terminal_id, reference_number, approval_code, amount)

        base_url = "https://api-staging.namipay.com.sa/api/merchanttx/searchtransaction/getbycustomerid"
        params = {
            'Customer_ID': customer_id,
            'Terminal_ID': terminal_id,
            'Tx_Ref_No': reference_number,
            'Approval_Code': approval_code,
            'Tx_Amount': amount
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }

        response = requests.get(base_url, headers=headers, params=params)
     
    if response.status_code == 200:
        response_data = response.json()
        response_code = response_data.get("response_code") 
        print(response)
        if response_code == 2:
            error_message = 'No Transcations Found'
            return render(request, 'search_results.html', {'error_message': error_message})


        elif 'result' in response_data and 'SEARCHED_TRANSACTION_DETAILS' in response_data['result']:
            merchant_data = response_data['result']['SEARCHED_TRANSACTION_DETAILS']
            
            if not from_date:
                from_date = '0001-01-01'  # Default value if from_date is empty

            if not to_date:
                to_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Default value if to_date is empty

            start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()

            filtered_transactions = [transaction for transaction in merchant_data if
                                     start_date <= datetime.datetime.strptime(transaction['Transaction_Date'],
                                                                               "%Y-%m-%dT%H:%M:%S").date() <= end_date]

            return render(request, 'search_results.html', {
                'merchant_data': filtered_transactions,
                'customer_id': customer_id,
                'username': username,
                'from_date': from_date,
                'to_date': to_date,
            })
        else:
            # Handle missing keys in API response
            return render(request, 'error_template.html', {'error_message': 'Data format in response is incorrect'})
    else:
        # Handle API error
        return render(request, 'error_template.html', {'error_message': f'API call failed with status code {response.status_code}'})

import httpx

async def ticket(request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')

    if customer_id is None:
        return render(request, 'error_template.html')

    if customer_id:
        urlstatus = 'https://api-staging.namipay.com.sa/api/ticket/merchantticketstatus/get'
        url = f"https://api-staging.namipay.com.sa/api/ticket/getbycustomerid?customerId={customer_id}"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }
        
        async with httpx.AsyncClient() as client:
            statusresponse = await client.get(urlstatus, headers=headers)
            if statusresponse.status_code == 200:
                statusdata = statusresponse.json()
                print(statusdata)
                # You might want to process 'statusdata' here
                
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
                print(merchant_data)
                return render(request, 'ticket.html', {'terminal': statusdata, 'merchant_data': merchant_data, 'customer_id': customer_id, 'username': username})

    # Handle other cases or errors here


from django.http import JsonResponse

import requests
from django.shortcuts import render

"""
def create_ticket(request):
    if request.method == 'GET':
        # Make API call to get activities
        activities_api_url = "https://api-staging.namipay.com.sa/api/ticket/activities/get"
        
        activities_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
        }


        activities_response = requests.get(activities_api_url, headers=activities_headers)
        token = access()

        if activities_response.status_code == 200:
            regions = activities_response.json().get('activities', [])
       

            # Pass activities data to the template
            return render(request, 'create_ticket.html', {'activities': regions, 'token': token})
        else:
            # Handle the case when the activities API call fails
            error_message = 'Failed to retrieve activities data'
            return render(request, 'error_template.html', {'error_message': error_message})
        
"""


async def complain_ticket(request):
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    username = await sync_to_async(request.session.get)('Username')
    mobile_number = await sync_to_async(request.session.get)('MobileNumber')
    cr_number = await sync_to_async(request.session.get)('CR_Number')
    if request.method == 'POST':
        #selected_activity = request.POST.get('selected_activity')
        selected_fault_category = request.POST.get('selected_fault_category_key')
        selected_sub_category = request.POST.get('selected_fault_category_value')
        #selected_region = request.POST.get('selected_region')
        #selected_vendor = request.POST.get('selected_vendor')
        terminal_id = request.POST.get('terminal_id')
        if True:
            print('in side of Try')
            url = "https://api-staging.namipay.com.sa/api/ticket/createcomplainbycustomer"
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
                }
            iterminal_id = int(terminal_id)
            iselected_fault_category = int(selected_fault_category)
            UserId = "ABB8229E-7EA5-4B9A-A343-8D431373762B"
            params = {
                    'CustomerId': customer_id,
                    'TerminalId': iterminal_id,
                    'FaultCategoryId': iselected_fault_category,
                    "FaultReported": selected_sub_category, 
                    "UserName":username,
                    'UserId':UserId,
                }
            print(type(customer_id), type(iterminal_id), type(iselected_fault_category), iselected_fault_category, type(selected_sub_category), type(username))

                
            response = requests.post(url, headers=headers, data=json.dumps(params))
            print(response)
            
            if response.status_code == 200:
                response_data = response.json()
                response_code = response_data.get("statusCode")
                response_code2 = response_data.get("message")
                response_code3 = response_data.get("ticketId")
 
                print(response_code)
                print(response_code2)
                print(response_code3)
                error_message =  f"Message : {response_code2}"

                return render(request, 'ticketinfo.html', {'error_message': error_message})
        else:
            print('notworking')
    if request.method == 'GET':
        try:
            regions_api_url = "https://api-staging.namipay.com.sa/api/ticket/Regions/get"
            activities_api_url = "https://api-staging.namipay.com.sa/api/ticket/activities/get"
            vender = "https://api-staging.namipay.com.sa/api/ticket/Vendors/get"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',
                'appid': '2'  # You may need to obtain a new access token here
            }

            

            # Get regions data
            regions_response = requests.get(regions_api_url, headers=headers)
            if regions_response.status_code == 200:
                regions = regions_response.json().get('regions', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve regions data'})

            # Get activities data
            activities_response = requests.get(activities_api_url, headers=headers)
            if activities_response.status_code == 200:
                activities = activities_response.json().get('activities', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve activities data'})

            # Get fault categories data
            vender = requests.get(vender, headers=headers)
            if vender.status_code == 200:
               vender = vender.json().get('vendors', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve fault categories data'})

            
            return render(request, 'complainticket.html', {
                'regions': regions,
                'activities': activities,
                'vender': vender,
                'username':username,
                
                 
            })

        except requests.RequestException as e:
            return render(request, 'error_template.html', {'error_message': f'Error: {e}'})

    else:
        return render(request, 'error_template.html', {'error_message': 'Invalid request method'})
async def create_ticket(request):
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    username = await sync_to_async(request.session.get)('Username')
    mobile_number = await sync_to_async(request.session.get)('MobileNumber')
    cr_number = await sync_to_async(request.session.get)('CR_Number')
    if request.method == 'POST':
        #selected_activity = request.POST.get('selected_activity')
        selected_fault_category = request.POST.get('selected_fault_category_key')
        selected_sub_category = request.POST.get('selected_fault_category_value')
        #selected_region = request.POST.get('selected_region')
        #selected_vendor = request.POST.get('selected_vendor')
        terminal_id = request.POST.get('terminal_id')
        if True:
            print('in side of Try')
            url = "https://api-staging.namipay.com.sa/api/ticket/createticketbycustomer"
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access()}', 
                      # You may need to obtain a new access token here
                }
            iterminal_id = int(terminal_id)
            iselected_fault_category = int(selected_fault_category)
            UserId = "ABB8229E-7EA5-4B9A-A343-8D431373762B"
            params = {
                    'CustomerId': customer_id,
                    'TerminalId': iterminal_id,
                    'FaultCategoryId': 19,
                    "FaultReported": selected_sub_category, 
                    "UserName":username,
                    'UserId':UserId,
                }
            print(type(customer_id), type(iterminal_id), type(iselected_fault_category), iselected_fault_category, type(selected_sub_category), type(username))

                
            response = requests.post(url, headers=headers, data=json.dumps(params))
            print(response)
            
            if response.status_code == 200:
                response_data = response.json()
                response_code = response_data.get("statusCode")
                response_code2 = response_data.get("message")
                response_code3 = response_data.get("ticketId")
 
                print(response_code)
                print(response_code2)
                print(response_code3)
                error_message =  f"Message : {response_code2}"

                return render(request, 'ticketinfo.html', {'error_message': error_message})
        else:
            print('notworking')
    if request.method == 'GET':
        try:
            regions_api_url = "https://api-staging.namipay.com.sa/api/ticket/Regions/get"
            activities_api_url = "https://api-staging.namipay.com.sa/api/ticket/activities/get"
            vender = "https://api-staging.namipay.com.sa/api/ticket/Vendors/get"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',
                'appid': '2'  # You may need to obtain a new access token here
            }




            url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantdata/getbycustomerid?Customer_ID={customer_id}"
          
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merchant_data = response.json()
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve regions data'})
            

            # Get regions data
            regions_response = requests.get(regions_api_url, headers=headers)
            if regions_response.status_code == 200:
                regions = regions_response.json().get('regions', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve regions data'})

            # Get activities data
            activities_response = requests.get(activities_api_url, headers=headers)
            if activities_response.status_code == 200:
                activities = activities_response.json().get('activities', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve activities data'})

            # Get fault categories data
            vender = requests.get(vender, headers=headers)
            if vender.status_code == 200:
               vender = vender.json().get('vendors', [])
            else:
                return render(request, 'error_template.html', {'error_message': 'Failed to retrieve fault categories data'})

            
            return render(request, 'create_ticket.html', {
                'regions': regions,
                'activities': activities,
                'vender': vender,
                'username':username,
                'merchant_data':merchant_data
                
                 
            })

        except requests.RequestException as e:
            return render(request, 'error_template.html', {'error_message': f'Error: {e}'})

    else:
        return render(request, 'error_template.html', {'error_message': 'Invalid request method'})
   


def fetch_fault_categories(request):
    if request.method == 'POST':
        selected_key = request.POST.get('selectedKey')
        print(selected_key)  

        fault_categories_api_url = f"https://api-staging.namipay.com.sa/api/ticket/faultcategory/getbyactivityid?activityId={selected_key}"
        sub_activity_api_url = f"https://api-staging.namipay.com.sa/api/ticket/subactivityremarks/get?activityId={selected_key}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  
        }

        fault_categories_response = requests.get(fault_categories_api_url, headers=headers)
        sub_activity_response = requests.get(sub_activity_api_url, headers=headers)

        if fault_categories_response.status_code == 200 and sub_activity_response.status_code == 200:
            fault_categories_data = fault_categories_response.json().get('faultcategory', [])
            sub_activity_data = sub_activity_response.json().get('subActivityRemarks', [])
            
            return JsonResponse({
                'fault_categories': fault_categories_data,
                'sub_activity_data': sub_activity_data
            })
        else:
            return JsonResponse({'error': 'Failed to retrieve data'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

   

async def search (request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    return render(request, 'search.html',{ 'username':username})


import aiohttp

async def doc(request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')

    api_url = f"https://api-staging.namipay.com.sa/api/merchanttx/MerchantDocuments/Get?MerchantId={customer_id}"

    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  
        }
    

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url,  headers=headers) as response:
                if response.status == 200:
                    merchant_documents = await response.json()
                 
                    return render(request, 'docs.html', {'merchant_documents': merchant_documents['result'], 'username':username})
                else:
                    return render(request, 'error_template.html', {'error_message': f'Failed to fetch merchant documents. Status code: {response.status}'})
    except aiohttp.ClientError as e:
        return render(request, 'error_template.html', {'error_message': f'Error: {str(e)}'})
    
    
from django.http import FileResponse
import os

def download_document(request, file_name):
    file_path = f'D:\\AhsankhanLogs\\OPS-Aggregator\\DProTarget\\ClassifiedDocuments\\1010200776\\Doc-11603145-R-1-1.jpg'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:

        return HttpResponse("File not found", status=404)
    
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt








import base64
@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
            uploaded_image = request.FILES.get('img')
            print(uploaded_image)
            if uploaded_image:
                image_data = uploaded_image.read()  # Read the image data from BytesIO
                encoded_image = base64.b64encode(image_data).decode('utf-8')  
                print(encoded_image)
                response_data = {
                    'image_base64': encoded_image,
                    'other_info': 'other data related to the API response'
                }
                
                return JsonResponse(response_data)
    
def upload(request):
    if request.method == 'POST':
        merchant_id = request.session.get('CustomerID')
        user_id = "ABB8229E-7EA5-4B9A-A343-8D431373762B"
        selected_doc_type = request.POST.get('selectedDocType')
        uploaded_image = request.FILES.get('img')
        image_data = uploaded_image.read()
        File_Name = uploaded_image.name
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        print(merchant_id, user_id, selected_doc_type, uploaded_image.name)

        # Validate if necessary data exists in the session
        if None in [merchant_id, user_id, selected_doc_type, uploaded_image]:
            return JsonResponse({'success': False, 'error': 'Missing session data'}, status=400)

        # Construct the payload
        payload = {
            "DocTypeId": selected_doc_type,
            "MerchantId": merchant_id,
            "FileName": File_Name,
            "DocData":  encoded_image,  # Read the image data
            "UserId": user_id
        }

        upload_api_url = 'https://api-staging.namipay.com.sa/api/merchanttx/MerchantDocuments/Upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',
        }

        response = requests.post(upload_api_url, json=payload, headers=headers)

           
        if response.status_code == 200:
           
            # Print the API response content in the terminal
            response_json = response.json()
            print(response_json)

            error_message = 'User does not exist or Please Check Username & Password'
            return JsonResponse({'success': True, 'error_message': error_message})

            
            
        else:
            return JsonResponse({'success': False, 'error': 'Failed to upload document and image'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
          
            



def fetch_document_types(request):
    api_url = 'https://api-staging.namipay.com.sa/api/merchanttx/MerchantDocTypes/Get'
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',  
            }
    response = requests.get(api_url, headers=headers)
    try:
        data = response.json()
        print('Hello',data)
        return JsonResponse(data, safe=False)  # Return the fetched data as JSON response
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)})  # Handle error if API request fails










# views.py

def mark_notification_as_seen(request):
    print('printed')
    if request.method == 'POST':
        notification_id = request.POST.get('notificationID')  # assuming 'notificationID' is sent from the frontend
        print(notification_id)
        api_url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantnotifications/update?NotificationId={notification_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}',
        }
        response = requests.post(api_url, headers=headers)
        data = response.json()
        print('api succesfully',data)
        if data.get('success'):
            print("Notification status updated successfully.")
            
            return redirect('display_notifications')

        else:
            print("Failed to update notification status.")
  

        # After successfully marking the notification as seen, send the updated count back to the frontend
        new_notification_count = 1  # replace with the actual count
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

async def display_notifications(request):
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        api_url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantnotifications/Get?MerchantId={customer_id}"
        headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }

        try:
            response = requests.get(api_url, headers=headers)
            notifications = response.json()
            
            return JsonResponse(notifications)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
async def notifications(request):
        customer_id = await sync_to_async(request.session.get)('CustomerID')
        if customer_id is None:
            return render(request, 'error_template.html')
        username = await sync_to_async(request.session.get)('Username')
        api_url = f"https://api-staging.namipay.com.sa/api/merchanttx/merchantnotifications/Get?MerchantId={customer_id}"
        headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access()}',  # You may need to obtain a new access token here
            }

        if True:
            response = requests.get(api_url, headers=headers)
            notifications = response.json()
            print(notifications)
            
            return render(request, 'notifaction.html', {'merchant_documents': notifications, 'username':username}) 

def custom_404_page(request, exception):
    return render(request, '404.html', status=404)


async def pp(request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    
    return render(request, 'privacy_policy.html',{'username':username})

async def tm(request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    
    return render(request, 'Terms.html',{'username':username})


async def validateform(request):
    return render(request, 'validate.html')

async def validate(request):
    username = await sync_to_async(request.session.get)('Username')
    customer_id = await sync_to_async(request.session.get)('CustomerID')
    if customer_id is None:
        return render(request, 'error_template.html')
    if request.method == 'POST':
        ID_Number = request.POST.get('ID_Number')
        CR_Number = request.POST.get('CR_Number')
        MobileNumber = request.POST.get('MobileNumber')
   

        api = "https://api-staging.namipay.com.sa/cr/verify"
        payload = json.dumps({
            "ID_Number": ID_Number,
            "CR_Number": CR_Number,
            "Mobile_Number":  MobileNumber
        })

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access()}',  # Replace with your actual access token
        
        }

        responsev = requests.post(api, payload, headers=headers)
        verification_data = responsev.json()
        print(verification_data)
        return render(request, 'validate.html',{'data':'Data Sent Successfully'})
    return render(request, 'profile.html')


async def history(request):
    return render(request, 'history.html')




async def postatus(request):
    username = await sync_to_async(request.session.get)('Username')
    merchantId = await sync_to_async(request.session.get)('CustomerID')

    if merchantId is None:
        return render(request, 'error_template.html')

    if request.method == 'POST':
        ticketId = request.POST.get('ticketId')
        merchantTicketStatusId = request.POST.get('merchantTicketStatusId')

        api = "https://api-staging.namipay.com.sa/api/ticket/merchantapprovedticket/Update"
        params = {
            "merchantId": merchantId,
            "ticketId": ticketId,
            "merchantTicketStatusId": merchantTicketStatusId
        }

        print(merchantId, ticketId, merchantTicketStatusId)

        

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access()}', 
        }

        responsev = requests.post(api, params=params, headers=headers)
        verification_data = responsev.json()

        print('Response:', verification_data)
        return JsonResponse({'data':'Status Update Successfully'})

    return render(request, 'profile.html')

