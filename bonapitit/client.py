from datetime import timedelta, date, datetime
from typing import List as _List

import requests

from bonapitit.base import BaseClient, BaseResponse, Error
import webbrowser


class OrderDetails:
    def __init__(self, data):
        self.content = data
        self.amount_paid: float = float(data.get('amountPaid'))
        self.amount_saved: float = float(data.get('amountSaved'))
        self.order_id: int = data.get('orderID')
        self.buyer_id: str = data.get('buyerUserID')
        self.buyer_name: str = data.get('buyerUserName')
        self.created_time: str = data.get('createdTime')
        self.item_array: list = data.get('itemArray')
        self.checkout_status: dict = data.get('checkoutStatus')
        self.buyer_checkout_message: str = data.get('buyerCheckoutMessage')
        self.shipping_address: str = data.get('shippingAddress')
        self.order_status: str = data.get('orderStatus')
        self.paid_time: str = data.get('paidTime')
        self.shipping_details: dict = data.get('shippingDetails')
        self.subtotal: float = float(data.get('subtotal'))
        self.tax_amount: float = float(data.get('taxAmount'))
        self.total: float = float(data.get('total'))
        self.transaction_array: dict = data.get('transactionArray')


class Order:
    def __init__(self, data):
        self.order: OrderDetails = OrderDetails(data.get('order'))


class OrderList(list, _List['Order']):
    def __init__(self, data):
        super().__init__([Order(datum) for datum in data])
        self.content = data


class GetOrdersResponse:
    def __init__(self, data):
        self.content = data
        self.error = None
        self.warning = None
        self.orders = None
        if 'errorMessage' in data:
            self.error: Error = Error(data['errorMessage'])
        if 'warnings' in data:
            self.warning: Warning = Warning(data['warnings'])
        if "getOrdersResponse" in data and "orderArray" in data["getOrdersResponse"]:
            self.orders: OrderList = OrderList(data["getOrdersResponse"]["orderArray"])


class UpdateInventory:
    def __init__(self, data, item_id):
        self.content = data
        self.result = False
        if item_id in data:
            self.result: bool = data[item_id]['success']


class UpdateInventoryResponse(BaseResponse):
    def __init__(self, data, item_id: str):
        super().__init__(data)
        self.details = None
        if 'updateInventoryResponse' in data:
            self.details: UpdateInventory = UpdateInventory(data['updateInventoryResponse'], item_id)


class AddFixedPriceItem:
    def __init__(self, data):
        self.content = data
        self.category_id: int = data.get('categoryId')
        self.item_id: int = data.get('itemId')
        self.message: str = data.get('message')
        self.selling_state: str = data.get('sellingState')


class AddFixedPriceItemResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        self.details = None
        if 'addFixedPriceItemResponse' in data:
            self.details: AddFixedPriceItem = AddFixedPriceItem(data['addFixedPriceItemResponse'])


class ReviseFixedPriceItemResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)


class EndFixedPriceItemResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        self.result: bool = False
        if 'itemsRemoved' in data and data['itemsRemoved'] > 0:
            self.result: bool = True


class Booth:
    def __init__(self, data):
        self.content = data
        self.custom_category: list = data.get('customCategory')
        self.activated: bool = data.get('activated')
        self.description: str = data.get('description')
        self.logo: list = data.get('logo')
        self.name: str = data.get('name')
        self.on_vacation: bool = data.get('onVacation')
        self.policies: str = data.get('policies')
        self.subscription_level: int = data.get('subscriptionLevel')
        self.syndicated: bool = data.get('syndicated')
        self.url: list = data.get('url')


class GetBoothResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        self.details: Booth = Booth(data['store']) if data.get('store') else None


class BoothItems:
    def __init__(self, data):
        self.content = data
        self.current_page: int = data.get('currentPage')
        self.size: int = data.get('size')
        self.total_entries: int = data.get('totalEntries')
        self.items: dict = data.get('items')


class GetBoothItemsResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        if 'getBoothItemsResponse' in data:
            self.details: BoothItems = BoothItems(data['getBoothItemsResponse'])


class TokenStatus:
    def __init__(self, data):
        self.content = data
        self.verified: bool = data.get('verified')
        self.hard_expiration_time: datetime = data.get('hardExpirationTime')


class GetTokenStatusResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        if 'getTokenStatusResponse' in data:
            self.details: TokenStatus = TokenStatus(data['getTokenStatusResponse'])


class CompleteSale:
    def __init__(self, data):
        self.content = data
        self.skipped_processing: bool = data.get('skippedProcessing')
        self.processed_acceptance: bool = data.get('processedAcceptance')
        self.processed_deny: bool = data.get('processedDeny')


class CompleteSaleResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        if 'completeSaleResponse' in data:
            self.details: CompleteSale = CompleteSale(data['completeSaleResponse'])


class RegistrationAddress:
    def __init__(self, data):
        self.content = data


class SellerInfo:
    def __init__(self, data):
        self.content = data


class GetUserResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        self.user_id: int = data.get('userID')
        self.user_name: str = data.get('userName')
        self.avatar_url: str = data.get('avatarUrl')
        self.billing_email: str = data.get('billingEmail')
        self.bonanza_good_standing: bool = data.get('bonanzaGoodStanding')
        self.email: str = data.get('email')
        self.feedback_score: int = data.get('feedbackScore')
        self.postive_feedback_percentage: int = data.get('postiveFeedbackPercentage')
        if 'registrationAddress' in data:
            self.registration_address: RegistrationAddress = RegistrationAddress(data['registrationAddress'])
        if 'sellerInfo' in data:
            self.seller_info: SellerInfo = SellerInfo(data['sellerInfo'])


class Categories:
    def __init__(self, data):
        self.content = data
        self.category_brief_name: str = data.get('categoryBriefName')
        self.category_id: int = data.get('categoryId')
        self.category_level: int = data.get('categoryLevel')
        self.category_name: str = data.get('categoryName')
        self.trait_count: int = data.get('traitCount')


class CategoriesList(list, _List['Categories']):
    def __init__(self, data):
        super().__init__([Categories(datum) for datum in data])
        self.content = data


class GetCategoriesResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        if 'getCategoriesResponse' in data and "categoryArray" in data['getCategoriesResponse']:
            self.details: CategoriesList = CategoriesList(data['getCategoriesResponse']["categoryArray"])


class TraitArray:
    def __init__(self, data):
        self.content = data
        self.html_input_type: str = data.get('htmlInputType')
        self.id: int = data.get('id')
        self.label: str = data.get('label')
        self.parent_trait_id: int = data.get('parentTraitId')
        self.variations_enabled: bool = data.get('variationsEnabled')
        self.request_seller_input: bool = data.get('requestSellerInput')
        self.trait_values: dict = data.get('traitValues')


class CategoryTrait(list, _List['TraitArray']):
    def __init__(self, data):
        super().__init__([TraitArray(datum) for datum in data])
        self.content = data


class GetCategoryTraitsResponse:
    def __init__(self, data):
        self.content = data
        self.error = None
        self.warning = None
        self.category_traits = None
        if 'errorMessage' in data:
            self.error: Error = Error(data['errorMessage'])
        if 'warnings' in data:
            self.warning: Warning = Warning(data['warnings'])
        if 'getCategoryTraitsResponse' in data and 'traitArray' in data['getCategoryTraitsResponse']:
            self.category_traits = CategoryTrait(data['getCategoryTraitsResponse']['traitArray'])


class GetUnlistedItemResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)


class FetchToken:
    def __init__(self, data):
        self.content = data
        self.token: str = data.get("authToken")
        self.authentication_url: str = data.get("authenticationURL")

    def autoForward(self):
        return webbrowser.open(self.authentication_url)


class GetFetchTokenResponse(BaseResponse):
    def __init__(self, data):
        super().__init__(data)
        if "fetchTokenResponse" in data:
            self.details: FetchToken = FetchToken(data["fetchTokenResponse"])


class TokenClient:
    def __init__(self, dev_name, cert_name):
        self.__url = 'https://api.bonanza.com/api_requests/secure_request'
        self.__headers = {
            'X-BONANZLE-API-DEV-NAME': dev_name,
            'X-BONANZLE-API-CERT-NAME': cert_name,
        }

    # 获取用户令牌
    def getFetchTonken(self):
        request_name = 'fetchTokenRequest'
        response = requests.post(url=self.__url, data=request_name, headers=self.__headers)

        return GetFetchTokenResponse(response.json())

    # 获取用户令牌的当前状态
    def getTokenStatus(self, fetch_token):
        payload = {
            'getTokenStatusRequest': {
                'requesterCredentials': {
                    'bonanzleAuthToken': fetch_token
                }
            }
        }
        response = requests.post(url=self.__url, json=payload, headers=self.__headers)

        return GetTokenStatusResponse(response.json())


class BonanzaClient(BaseClient):
    def __init__(self, dev_name, cert_name, fetch_token):
        super().__init__(dev_name, cert_name)
        self._requester_credentials = {'bonanzleAuthToken': fetch_token}

    # 获取相关用户的详细信息。
    def getUser(self):
        payload = {'getUserRequest': {'requesterCredentials': self._requester_credentials}}
        response = self._request(path='secure_request', json=payload)

        return GetUserResponse(response.json())

    def getOrders(
            self,
            soldtime_from: date = date.today() - timedelta(days=1),
            soldtime_to: date = date.today(),
            item_num: 'int > 0' = 100,
            **kwargs
    ):
        """
        获取买方或卖方的待处理、出售和发货订单(暂时限制卖方)，如果想获取买方的你可以在kwargs传入seller="buyer"
        :param soldtime_from: 开始时间
        :param soldtime_to: 结束时间
        :param item_num: 订单数量
        :param kwargs: 更多的可选操作，具体请查看https://api.bonanza.com/docs/reference/get_orders
        :return:GetOrdersResponse
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'orderRole': 'seller',
            'soldTimeFrom': str(soldtime_from),
            'soldTimeTo': str(soldtime_to),
            'paginationInput': {
                'entriesPerPage': item_num
            }
        }
        if kwargs: input_dictionary.update(kwargs)
        payload = {'getOrdersRequest': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return GetOrdersResponse(response.json())

    def updateInventory(self, items: _List[dict]):
        """
        更新一个或者多个商品的价格和数量(暂时只支持更新一个的判断),传值的时候传列表类型里面放一个数据就行了
        :param items:[{'itemId01': {'price': 12.3,'quantity': 100,}},{'itemId02': {'price': 15.0,'quantity': 10,}}]
        :return: UpdateInventoryResponse
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'updates': items
        }
        payload = {'updateInventoryRequest': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return UpdateInventoryResponse(response.json(), items[0]['itemId'])

    def addFixedPriceItem(self, **item):
        """
        将商品添加到卖家的展位
        https://api.bonanza.com/docs/reference/add_fixed_price_item
        :param item:由于太过复杂，不作注释模板，自行查阅Bonanza官方文档
        :return:AddFixedPriceItemResponse
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'item': item
        }
        payload = {'addFixedPriceItemRequest': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return AddFixedPriceItemResponse(response.json())

    def reviseFixedPriceItem(self, item_id: int, item: dict, discard_old_variations: bool = None):
        """
        编辑卖家展位中的项目
        :param item_id:修改的项目id
        :param item:参照addFixedPriceItem中的参数item值
        :param discard_old_variations:默认为False，当为True时，会去除当前项目的有数据，相当于新建addFixedPriceItem功能
        :return:ReviseFixedPriceItemResponse
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'itemId': item_id,
            'item': item
        }
        if discard_old_variations: input_dictionary['discardOldVariations'] = discard_old_variations
        payload = {'reviseFixedPriceItemRequest': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return ReviseFixedPriceItemResponse(response.json())

    # 从卖家的展位中移除一个商品。
    def endFixedPriceItem(self, item_id: int):
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'itemID': item_id,
        }
        payload = {'endFixedPriceItemRequest': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return EndFixedPriceItemResponse(response.json())

    def getBooth(self, **kwargs: str):
        """
        该方法获取 Bonanza 展位的所有可用数据
        最多可接收三个可用参数 "boothId" "storeId" "storeId"三个中至少有一个
        所有参数都为可选参数并且都为str类型
        :param kwargs:{'boothId': str,'storId': str,'userId': str}
        :return:GetBoothResponse
        """
        input_dictionary = {}
        if kwargs: input_dictionary.update(kwargs)
        payload = {'getBoothRequest': input_dictionary}

        response = self._request(path='standard_request', json=payload)

        return GetBoothResponse(response.json())

    def getBoothItems(self, booth_id, order: bool, **kwargs):
        """
        获取一组指定状态的项目
        :param booth_id:整形或者字符型都可以
        :param order:是否排序选填True或False
        :param kwargs:{"boothId":123456,"itemStatus":[Default:"for_sale",],"itemsPerPage":Default:20,"page":Default:1}
        :return:
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'boothId': booth_id,
        }
        if kwargs: input_dictionary.update(kwargs)
        if order: input_dictionary['order'] = "newest"
        payload = {'getBoothItemsRequest': input_dictionary}
        response = self._request(path='secure_request', json=payload)

        return GetBoothItemsResponse(response.json())

    def updateBooth(self):
        """
        请求更新给定卖家的展位。这会将处于“准备出售（待售）”状态的所有商品更改为“出售”状态。
        请注意，由于展位更新是异步进行的，因此可能需要等待 1-10 分钟（对于拥有数千件物品的展位，时间更长），直到所有物品都被激活。
        另请注意，如果展位尚未完成其初始激活过程 - 卖方提供其销售详细信息并同意 Bonanza 服务条款 - 则此呼叫不会失败
        :return: 成功返回True，失败返回False。
        """
        payload = {'updateBoothRequest': {'requesterCredentials': self._requester_credentials}}

        response = self._request(path='secure_request', json=payload)
        data = response.json()

        if 'updateBoothResponse' in data:
            return data['updateBoothResponse']['success']
        else:
            return BaseResponse(data)

    def completeSale(self, transaction_id: int, **kwargs):
        """
        向已完成的订单追加反馈和运输/跟踪信息。
        "shippingCarrierUsed"可选"usps"、"ups"、"fedex"、"other"
        :param transaction_id:订单编号
        :param kwargs:{
            "accept": bool,
            "deny": bool,
            "feedbackInfo": {
                "commentText": str,
                "commentTypeCode": str,
                "targetUser": str
            },
            "shipment": {
                "notes": str,
                "privateNote": str,
                "shippingTrackingNumber": str,
                "shippingCarrierUsed": str,
            },
            "shipped": bool
        }
        :return:CompleteSaleResponse
        """
        input_dictionary = {
            'requesterCredentials': self._requester_credentials,
            'transactionID': transaction_id,
        }
        if kwargs: input_dictionary.update(kwargs)
        payload = {'completeSale': input_dictionary}

        response = self._request(path='secure_request', json=payload)

        return CompleteSaleResponse(response.json())

    def getCategories(self, category_parent: int):
        """
        获取您传入的类别ID 的所有子类别的详细信息
        如果您想获得 Bonanza 的所有基本级别类别，请传入类别 ID“0”。
        如果您需要所有类别的完整数据库转储，请登录并单击右上角的“我的帐户”，然后单击“下载类别”。
        :param category_parent:想要获取的类别ID
        :return:所有子集详细信息
        """
        payload = {'getCategoriesRequest': {'categoryParent': category_parent}}
        response = self._request(path='standard_request', json=payload)

        return GetCategoriesResponse(response.json())

    def getCategoryTraits(self, category_id: int):
        payload = {'getCategoryTraitsRequest': {'categoryId': category_id}}
        response = self._request(path='standard_request', json=payload)

        return GetCategoryTraitsResponse(response.json())

    def getUnlistedItem(self, item_id: int):
        """
        获取尚未发布出售的商品的详细信息
        :param item_id: 项目id
        :return:GetUnlistedItemResponse
        """
        payload = {'getUnlistedItemRequest': {'itemId': item_id}}
        response = self._request(path='standard_request', json=payload)

        return GetUnlistedItemResponse(response.json())
