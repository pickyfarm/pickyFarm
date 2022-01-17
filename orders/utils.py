from core.slack_bot import send_message_to_slack
from .models import Order_Group
from django.utils import timezone

def payment_complete_notification(order_group_pk):
    order_group = Order_Group.objects.get(pk=order_group_pk)
    order_details = order_group.order_details.all()

    product_name = ''

    if order_details.count() == 1:
        product_name = order_details.first().product.title

    else:
        product_name = f'{order_details.first().product.title} 외 {order_details.count() -1}개'

    args = get_order_message_block(**{
        'time': order_group.create_at,
        'order_management_number': order_group.order_management_number,
        'products':product_name,
        'consumer': f'{order_group.consumer.user.nickname} ({order_group.consumer.user.account_name})',
        'price': f'{order_group.total_price}원',
        'payment_type': order_group.payment_type
    })

    send_message_to_slack('C02P6KGV19D', args)


def get_order_message_block(ptype='complete', **args):
    if ptype == 'cancel':
        pass
    
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*결제완료 알림*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*결제일시*\n{args['time']}"
				},
                {
					"type": "mrkdwn",
					"text": f"*주문번호*\n{args['order_management_number']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*상품명*\n{args['products']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*주문자*\n{args['consumer']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*결제 금액*\n{args['price']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*결제방법*\n{args['payment_type']}"
				}
			]
		}
	]




# order_group 주문 관리 번호 생성 function
def create_order_group_management_number(pk):


    

    
    



# order_detail 주문 관리 번호 생성 function
def create_order_detail_management_number(pk, farmer_id):

    now = timezone.localtime()
    year = now.year % 100
    print(year)

    month = now.month
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)

    print(month)
    day = now.day
    print(day)

    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    order_detail_management_number = str(year) + month + day + "_" + str(pk) + "_" + farmer_id
    return order_detail_management_number
