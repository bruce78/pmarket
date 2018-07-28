from flask import request, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse
from app import app
from app.models import HistoryData, CoinInfo, ExchangeInfo, User, Admin
import json
import ast

api = Api(app)

parser = reqparse.RequestParser()


def error(message):
    response = {
        'message': message,
        'status_code': 401
    }
    return jsonify(response)


def available():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        userId = User.decode_token(access_token)
        admin = Admin.query.filter_by(userId=userId).first()
        if request.method in ['DELETE', 'PUT', 'POST'] and not admin:
            return False
        return True
    else:
        return False


class UserApi(Resource):
    def get(self, userId):
        user = User.query.filter_by(userId=userId).first()
        response = {'id': user.id,
                    'userId': user.userId,
                    'email': user.email
                    }
        return jsonify(response)

    def delete(self, userId):
        user = User.query.filter_by(userId=userId).first()
        user.delete()
        return {
                   "message": "user {} deleted".format(user.id), "status_code": 200
               }

    def put(self, userId):
        user = User.query.filter_by(userId=userId).first()
        response = {
            'id': user.id
        }
        return jsonify(response)


class UserAddApi(Resource):
    def post(self):

        return jsonify({'code': 'OK', 'status_code': 201})


# api.add_resource(UserApi, '/profile/<int:userId>')
# api.add_resource(UserAddApi, '/profile')


class HisdataApi(Resource):
    def get(self, coin, type):
        data = HistoryData.query.filter_by(coin=coin, type=type).first()
        if data is not None:
            response = {'data': data.data,
                    'coin': data.coin,
                    'type': data.type
                    }

            return jsonify(response)
        else:
            return error("Error")


    def put(self, coin, type):
        data = HistoryData.query.filter_by(coin=coin, type=type).first()
        parser.add_argument('data', type=str, required=True)
        if data is not None:
            args = parser.parse_args()
            if args['data'] is None or len(args['data']) < 5:
                return error("Error")
            pointData = json.loads(args['data'])
            jsonObj = ast.literal_eval(data.data)
            array = jsonObj['market_cap_by_available_supply']
            array1 = jsonObj['price_usd']
            array2 = jsonObj['vol_usd']

            if len(pointData['market_cap_by_available_supply']) > 0:
                array.pop(0)
                array.append(pointData['market_cap_by_available_supply'][0])
            if len(pointData['price_btc']) > 0:
                array1.pop(0)
                array1.append(pointData['price_btc'][0])
            if len(pointData['vol_usd']) > 0:
                array2.pop(0)
                array2.append(pointData['vol_usd'][0])
            data.data = str(jsonObj)
            data.update()
            return jsonify({'id': data.id, 'status_code': 200})
        else:
            return error("Error")

    def delete(self, coin, type):
        data = HistoryData.query.filter_by(coin=coin, type=type).first()
        if data is not None:
            data.delete()
            return jsonify({'id': data.id, 'status_code': 200})
        else:
            return error("Error")


class HisdataAddApi(Resource):
    def post(self):
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('coin', type=str, required=True)
        parser.add_argument('data', type=str, required=True)
        parser.add_argument('step', type=int)
        args = parser.parse_args()
        data = HistoryData.query.filter_by(coin=args['coin'], type=args['type']).first()
        if data is not None:
            data.delete()

        hisData = HistoryData()
        hisData.data = args['data']
        hisData.type = args['type']
        hisData.coin = args['coin']
        hisData.step = args['step']
        hisData.save()
        return jsonify({'code': 'OK', 'status_code': 200})


api.add_resource(HisdataApi, '/hisdata/<string:coin>/<string:type>')
api.add_resource(HisdataAddApi, '/hisdata')


class CoinInfoApi(Resource):
    def get(self, coin):
        data = CoinInfo.query.filter_by(coin=coin).first()
        if data is not None:
            response = {'coin': data.coin,
                        'h24': data.h24,
                        'l24': data.l24,
                        'percentage': data.percentage,
                        'flowRate': data.flowRate,
                        'turnoverRate': data.turnoverRate,
                        'info': data.info
                        }
            return jsonify(response)
        else:
            return error("Error")

    def put(self, coin):
        data = CoinInfo.query.filter_by(coin=coin).first()

        parser.add_argument('coin', type=str, required=True)
        parser.add_argument('h24', type=str)
        parser.add_argument('l24', type=str)
        parser.add_argument('percentage', type=str)
        parser.add_argument('flowRate', type=str)
        parser.add_argument('turnoverRate', type=str)
        parser.add_argument('info', type=str)

        args = parser.parse_args()

        data.coin = args['coin']
        data.h24 = args['h24']
        data.l24 = args['l24']
        data.percentage = args['percentage']
        data.flowRate = args['flowRate']
        data.turnoverRate = args['turnoverRate']
        data.info = args['info']
        data.update()

        return jsonify({'id': data.id, 'status_code': 200})

    def delete(self, coin):
        data = HistoryData.query.filter_by(coin=coin).first()
        if data is not None:
            data.delete()
            return jsonify({'id': data.id, 'status_code': 200})
        else:
            return error("Error")


class CoinInfoAddApi(Resource):
    def post(self):
        parser.add_argument('coin', type=str, required=True)
        parser.add_argument('h24', type=str)
        parser.add_argument('l24', type=str)
        parser.add_argument('percentage', type=str)
        parser.add_argument('flowRate', type=str)
        parser.add_argument('turnoverRate', type=str)
        parser.add_argument('info', type=str)

        args = parser.parse_args()
        data = CoinInfo.query.filter_by(coin=args['coin']).first()
        if data is not None:
            data.delete()

        coinInfo = CoinInfo()
        coinInfo.coin = args['coin']
        coinInfo.h24 = args['h24']
        coinInfo.l24 = args['l24']
        coinInfo.percentage = args['percentage']
        coinInfo.flowRate = args['flowRate']
        coinInfo.turnoverRate = args['turnoverRate']
        coinInfo.info = args['info']
        coinInfo.save()
        return jsonify({'code': 'OK', 'status_code': 200})


api.add_resource(CoinInfoApi, '/coininfo/<string:coin>')
api.add_resource(CoinInfoAddApi, '/coininfo')


class ExchangeInfoApi(Resource):
    def get(self, code):
        data = ExchangeInfo.query.filter_by(code=code).first()
        if data is not None:
            response = {'code': data.code,
                        'h24Volume': data.h24Volume,
                        'marketNum': data.marketNum,
                        'country': data.country,
                        'icon': data.icon,
                        'tradeTypes': data.tradeTypes,
                        'name': data.name,
                        'homeLink': data.homeLink,
                        'description': data.description
                        }
            return jsonify(response)
        else:
            return error("Error")

    def put(self, code):
        data = CoinInfo.query.filter_by(code=code).first()

        parser.add_argument('code', type=str, required=True)
        parser.add_argument('h24Volume', type=str)
        parser.add_argument('marketNum', type=str)
        parser.add_argument('country', type=str)
        parser.add_argument('icon', type=str)
        parser.add_argument('tradeTypes', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('homeLink', type=str)
        parser.add_argument('description', type=str)

        args = parser.parse_args()

        data.coin = args['code']
        data.h24Volume = args['h24Volume']
        data.marketNum = args['marketNum']
        data.country = args['country']
        data.icon = args['icon']
        data.tradeTypes = args['tradeTypes']
        data.name = args['name']
        data.homeLink = args['homeLink']
        data.description = args['description']

        data.update()

        return jsonify({'id': data.id, 'status_code': 200})

    def delete(self, code):
        data = HistoryData.query.filter_by(code=code).first()
        if data is not None:
            data.delete()
            return jsonify({'id': data.id, 'status_code': 200})
        else:
            return error("Error")


class ExchangeInfoAddApi(Resource):
    def post(self):
        parser.add_argument('code', type=str, required=True)
        parser.add_argument('h24Volume', type=str)
        parser.add_argument('marketNum', type=str)
        parser.add_argument('country', type=str)
        parser.add_argument('icon', type=str)
        parser.add_argument('tradeTypes', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('homeLink', type=str)
        parser.add_argument('description', type=str)

        args = parser.parse_args()
        data = ExchangeInfo.query.filter_by(code=args['code']).first()
        if data is not None:
            data.delete()

        exchangeInfo = ExchangeInfo()
        exchangeInfo.code = args['code']
        exchangeInfo.h24Volume = args['h24Volume']
        exchangeInfo.marketNum = args['marketNum']
        exchangeInfo.country = args['country']
        exchangeInfo.icon = args['icon']
        exchangeInfo.tradeTypes = args['tradeTypes']
        exchangeInfo.name = args['name']
        exchangeInfo.homeLink = args['homeLink']
        exchangeInfo.description = args['description']
        exchangeInfo.save()
        return jsonify({'code': 'OK', 'status_code': 200})


api.add_resource(ExchangeInfoApi, '/exchangeinfo/<string:code>')
api.add_resource(ExchangeInfoAddApi, '/exchangeinfo')

