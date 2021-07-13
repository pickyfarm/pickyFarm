import requests
import json


class BootpayApi:
    base_url = {
        'development': 'https://dev-api.bootpay.co.kr',
        'production': 'https://api.bootpay.co.kr'
    }

    def __init__(self, application_id, private_key, mode='production'):
        self.application_id = application_id
        self.pk = private_key
        self.mode = mode
        self.token = None

    def api_url(self, uri=None):
        if uri is None:
            uri = []
        return '/'.join([self.base_url[self.mode]] + uri)

    def get_access_token(self):
        data = {
            'application_id': self.application_id,
            'private_key': self.pk
        }
        response = requests.post(self.api_url(['request', 'token']), data=data)
        result = response.json()
        if result['status'] is 200:
            self.token = result['data']['token']
        return result

    def cancel(self, receipt_id, price=None, name=None, reason=None):
        payload = {'receipt_id': receipt_id,
                   'price': price,
                   'name': name,
                   'reason': reason}

        return requests.post(self.api_url(['cancel.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def verify(self, receipt_id):
        return requests.get(self.api_url(['receipt', receipt_id]), headers={
            'Authorization': self.token
        }).json()

    def subscribe_billing(self, billing_key, item_name, price, order_id, items=None, user_info=None, extra=None):
        if items is None:
            items = {}
        payload = {
            'billing_key': billing_key,
            'item_name': item_name,
            'price': price,
            'order_id': order_id,
            'items': items,
            'user_info': user_info,
            'extra': extra
        }
        return requests.post(self.api_url(['subscribe', 'billing.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    def subscribe_billing_reserve(self, billing_key, item_name, price, order_id, execute_at, feedback_url, items=None):
        if items is None:
            items = []
        payload = {
            'billing_key': billing_key,
            'item_name': item_name,
            'price': price,
            'order_id': order_id,
            'items': items,
            'scheduler_type': 'oneshot',
            'execute_at': execute_at,
            'feedback_url': feedback_url
        }
        return requests.post(self.api_url(['subscribe', 'billing', 'reserve.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    def subscribe_billing_reserve_cancel(self, reserve_id):
        return requests.delete(self.api_url(['subscribe', 'billing', 'reserve', reserve_id]), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    def get_subscribe_billing_key(self, pg, order_id, item_name, card_no, card_pw, expire_year, expire_month,
                                  identify_number, user_info=None, extra=None):
        if user_info is None:
            user_info = {}
        payload = {
            'order_id': order_id,
            'pg': pg,
            'item_name': item_name,
            'card_no': card_no,
            'card_pw': card_pw,
            'expire_year': expire_year,
            'expire_month': expire_month,
            'identify_number': identify_number,
            'user_info': user_info,
            'extra': extra
        }
        return requests.post(self.api_url(['request', 'card_rebill.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    def destroy_subscribe_billing_key(self, billing_key):
        return requests.delete(self.api_url(['subscribe', 'billing', billing_key]), headers={
            'Authorization': self.token
        }).json()

    def request_payment(self, payload={}):
        return requests.post(self.api_url(['request', 'payment.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def remote_link(self, payload={}, sms_payload=None):
        if sms_payload is None:
            sms_payload = {}
        payload['sms_payload'] = sms_payload
        return requests.post(self.api_url(['app', 'rest', 'remote_link.json']), data=payload).json()

    def remote_form(self, remoter_form, sms_payload=None):
        if sms_payload is None:
            sms_payload = {}
        payload = {
            'application_id': self.application_id,
            'remote_form': remoter_form,
            'sms_payload': sms_payload
        }
        return requests.post(self.api_url(['app', 'rest', 'remote_form.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def send_sms(self, receive_numbers, message, send_number=None, extra={}):
        payload = {
            'data': {
                'sp': send_number,
                'rps': receive_numbers,
                'msg': message,
                'm_id': extra['m_id'],
                'o_id': extra['o_id']
            }
        }
        return requests.post(self.api_url(['push', 'sms.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def send_lms(self, receive_numbers, message, subject, send_number=None, extra={}):
        payload = {
            'data': {
                'sp': send_number,
                'rps': receive_numbers,
                'msg': message,
                'sj': subject,
                'm_id': extra['m_id'],
                'o_id': extra['o_id']
            }
        }
        return requests.post(self.api_url(['push', 'lms.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def certificate(self, receipt_id):
        return requests.get(self.api_url(['certificate', receipt_id]), headers={
            'Authorization': self.token
        }).json()

    def submit(self, receipt_id):
        payload = {
            'receipt_id': receipt_id
        }
        return requests.post(self.api_url(['submit.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    def get_user_token(self, data={}):
        return requests.post(self.api_url(['request', 'user', 'token.json']), data=data, headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()