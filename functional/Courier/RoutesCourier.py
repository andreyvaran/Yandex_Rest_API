from flask import Blueprint
from flask import jsonify, request, make_response

from functional import session
from functional.Models import Courier, Order
from functional.Schema import CourierSchema
from functional.Tools import CurierWeight, IntersectionTimes, Selary

couriers = Blueprint('couriers', __name__)


@couriers.route('/couriers', methods=['POST'])
def PostCouriers():
    global _courier
    id_list = []
    couriers_list = []
    res = request.json['data']

    cura = []
    badcura = []
    reslist = []

    for courier_ in res:
        try:
            _courier = CourierSchema.parse_obj(courier_)
            if session.query(Courier).get(_courier.courier_id):
                raise Exception
            courier = Courier(
                courier_id=_courier.courier_id,
                courier_type=_courier.courier_type,
                weight=CurierWeight(_courier.courier_type),
                regions=_courier.regions,
                working_hours=_courier.working_hours,
            )
            cura.append(courier)
            reslist.append({'id': _courier.courier_id})

        except Exception as e:
            badcura.append({'id': _courier.courier_id})


    if len(badcura) == 0:
        session.add_all(cura)
        session.commit()
        return make_response(jsonify({'success': 'HTTP 201 Created',
                                      "couriers": reslist
                                      }), 200)
    else:
        return make_response(jsonify({'error': 'HTTP 400 Bad Request',
                                      "validation_error": {
                                          "couriers": badcura
                                      }}), 400)


@couriers.route('/couriers/<int:courier_id>', methods=['PATCH'])
def PatchCourier(courier_id: int):

    try:
        res = request.json
        courier_ = session.query(Courier).filter(Courier.courier_id == courier_id).first()
        order_ = session.query(Order).filter(Order.id_courier == courier_id).all()
        oldarr = courier_.current_orders
        new_weight = 0
        if courier_:
            # Обновляем данные к рурьере по полученным данным
            if 'courier_type' in res and courier_.courier_type != res['courier_type']:
                new_weight = CurierWeight(res['courier_type'])
                courier_.courier_type = res['courier_type']
            if 'regions' in res and res['regions'] != courier_.regions:
                courier_.regions = res['regions']

            if 'working_hours' in res and res['working_hours'] != courier_.working_hours:
                courier_.working_hours = res['working_hours']
            # Загружаем их в схему для удобной загрузки в БД
            Schema = CourierSchema.parse_obj({
                'courier_id': courier_.courier_id,
                'courier_type': courier_.courier_type,
                'regions': courier_.regions,
                'working_hours': courier_.working_hours
            })
            free_weight = courier_.weight
            del_arr = []
            # Находим в del_arr только те ид которые не подощли по нашему новому запросу
            for i in oldarr:
                hit_order = session.query(Order).filter((Order.order_id == i), (Order.region.in_(Schema.regions)),
                                                        (Order.delivety_time == 0), (Order.weight < new_weight)).first()
                if hit_order:
                    if (IntersectionTimes(hit_order.delivery_hours,
                                          courier_.working_hours) and free_weight - hit_order.weight >= 0):
                        free_weight -= hit_order.weight
                    else:
                        del_arr.append(i)
                else:
                    del_arr.append(i)
            for i in del_arr:
                oldarr.remove(i)
                hit_order = session.query(Order).filter((Order.order_id == i)).update({
                    'id_courier': -1})
                session.commit()

            if oldarr:
                # Обновляем данные в базе данных если еще остались заказы у курьера
                session.query(Courier).filter(Courier.courier_id == courier_id).update({
                    'courier_type': Schema.courier_type,
                    'regions': Schema.regions,
                    'working_hours': Schema.working_hours,
                    'weight': new_weight,
                    'current_orders': oldarr

                })
            else:
                # Обновляем данные для курьера если не осталосб заказов
                new_dev = courier_.delivery
                new_str = courier_.selary_str
                if courier_.current_time != courier_.assign_time:
                    new_dev += 1
                else:
                    new_str = new_str[:-1]

                session.query(Courier).filter(Courier.courier_id == courier_id). \
                    update({
                    'courier_type': Schema.courier_type,
                    'regions': Schema.regions,
                    'working_hours': Schema.working_hours,
                    'weight': new_weight,
                    'delivery': new_dev,
                    'current_time': '',
                    'assign_time': '',
                    'current_orders': [],
                    'selary_str': new_str
                })
            session.commit()
        #     Получаем актуальные данные
        courier_ = session.query(Courier).filter(Courier.courier_id == courier_id).first()
        return make_response(jsonify({'success': 'HTTP 200 OK',
                                      "courier_id": courier_.courier_id,
                                      "co"
                                      "urier_type": courier_.courier_type,
                                      "regions": courier_.regions,
                                      "working_hours": courier_.working_hours
                                      }), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'HTTP 400 Bad Request'}), 400)

@couriers.route('/couriers/<int:courier_id>', methods=['GET'])
def GetInfo(courier_id):
    try:
        rating_orders  = session.query(Order).filter((Order.id_courier == courier_id)).all()
        courier_ = session.query(Courier).filter(Courier.courier_id == courier_id).first()
        #  dict { region_id : [ all time in region , count done order in region]
        # Очень спать уже хочу , так что плевать на красоту
        ratingmin = {}
        ratingcount = {}
        for order_ in rating_orders:
            if order_.region in ratingmin.items():
                ratingmin[order_.region] += order_.delivety_time
                ratingcount[order_.region] += 1

            else :
                ratingmin[order_.region] = order_.delivety_time
                ratingcount[order_.region]= 1
        arr = []
        for key, value in ratingmin.items():
            arr.append(value / ratingcount[key])
        arr.append(60 * 60)
        reting = (60 * 60 - min(arr)) / (60 * 60) * 5
        return make_response(jsonify({"courier_id": courier_id,
                                        "courier_type": courier_.courier_type,
                                        "regions": courier_.regions,
                                        "working_hours": courier_.working_hours,
                                        "rating": reting,
                                        "earnings": Selary(courier_.delivery , courier_.selary_str)}))
    except:
        return make_response(jsonify({'error ' : 'Courier not Found'} ),404)