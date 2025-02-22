import razorpay
from decouple import config

def create_razorpay_order(amount):

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY'))
                                ).order.create({"amount": int(amount) * 100, 
                                            "currency": "INR", 
                                            "payment_capture": "1"})
    return payment

def verify_and_save_payment(order,res):

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = res.get('razorpay_order_id')
    raz_pay_id = res.get('razorpay_payment_id')
    raz_signature = res.get('razorpay_signature')


    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    client.utility.verify_payment_signature(data)
    
    # if payment is successful that means check is None then we will turn isPaid=True
    order.is_paid = True
    order.save()
