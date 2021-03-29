from flask import Blueprint
from flask import jsonify, request, make_response

from functional import session
from functional.Models import Order, Courier
from functional.Schema import OrderSchema, CompleteOrderSchema
from functional.Tools import DeltaSecondRFC_3339, IntersectionTimes, NowRFC_3339

orders = Blueprint('orders', __name__)


@orders.route('/orders', methods=['POST'])
def post_orders():
    id_list = []
    res = request.json['data']
    for i in res:
        id_list.append({'id': i['order_id']})
    try:
        ordera = []
        for odrer_ in res:
            _order = OrderSchema.parse_obj(odrer_)
            if _order.weight > 50 or _order.weight < 0.01:
                return make_response(jsonify({'error': 'HTTP 400 Bad Request',
                                              "validation_error": {
                                                  "orders": id_list
                                              }}), 400)
            order = Order(
                order_id=_order.order_id,
                weight=_order.weight,
                region=_order.region,
                delivery_hours=_order.delivery_hours
            )
            ordera.append(order)
        session.add_all(ordera)
        session.commit()
        return make_response(jsonify({'success': 'HTTP 201 Created',
                                      "orders": id_list
                                      }), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'HTTP 400 Bad Request',
                                      "validation_error": {
                                          "orders": id_list
                                      }}), 400)


@orders.route('/orders/assign', methods=['POST'])
def AssignOrder():
    global new_str
    res = request.json
    try:
        courier_ = session.query(Courier).get(res["courier_id"])
    except:
        return make_response(jsonify({'error': 'Courier not found'}), 400)
    # print(courier_.current_orders)
    if len(courier_.current_orders ) == 0  :
        free_weight = courier_.weight
        deliv_arr = []
        order_ = session.query(Order).filter((Order.region.in_(courier_.regions)), (Order.delivety_time == 0),
                                             (Order.weight < courier_.weight), (Order.id_courier == -1 )).all()

        for ord in order_:
            if (IntersectionTimes(ord.delivery_hours, courier_.working_hours) and free_weight - ord.weight >= 0):
                deliv_arr.append(ord.order_id)
                session.query(Order).filter(Order.order_id == ord.order_id).update({
                    'id_courier': courier_.courier_id
                })
                free_weight -= ord.weight
        session.commit()
        if len(deliv_arr) != 0:
                now_time = NowRFC_3339()
                if courier_.courier_type == 'foot':
                    new_str = courier_.selary_str + 'F'
                elif courier_.courier_type == 'bike':
                    new_str = courier_.selary_str + 'B'
                elif courier_.courier_type == 'car':
                    new_str = courier_.selary_str + 'C'
                session.query(Courier).filter(Courier.courier_id == res['courier_id']). \
                    update({
                    'current_time': now_time,
                    'assign_time': now_time,
                    'current_orders': deliv_arr,
                    'selary_str': new_str
                })
                session.commit()
                resarr = []
                for i in deliv_arr:
                    resarr.append({"id": i})
                return make_response(jsonify({'success': 'HTTP 200 OK'}, {
                    "order_id": resarr}, {
                                                 'assign_time': now_time
                                             }), 200)
        else:
                return make_response(jsonify({'success': 'HTTP 200 OK'}, {
                    "order_id": deliv_arr}), 200)
    else:
        resarr = []
        for i in courier_.current_orders:
            resarr.append({"id": i})
        return make_response(jsonify({'success': 'HTTP 200 OK'}, {
            "order_id": resarr}, {'assign_time': courier_.assign_time}), 200)


@orders.route('/orders/complete', methods=['POST'])
def complete_order():
    res = request.json

    try:
        res = CompleteOrderSchema.parse_obj(res)
        courier_ = session.query(Courier).get(res.courier_id)
        order_ = session.query(Order).filter((Order.order_id == res.order_id), (Order.id_courier == res.courier_id),
                                             (Order.delivety_time == 0)).first()

        if not order_ or not courier_:
            return make_response(jsonify({'error': 'HTTP 400 Bad Request'}), 400)

        # if courier_.current_time:
        order_.second = DeltaSecondRFC_3339(courier_.current_time,
                                            res.complete_time)

        check = courier_.current_orders

        check.remove(res.order_id)
        if len(check) == 0:
            new_dev = courier_.delivery + 1
            session.query(Courier).filter(Courier.courier_id == res.courier_id). \
                update({
                'delivery': new_dev,
                'current_time': '',
                'assign_time': '',
                'current_orders': [],

            })
        else:
            done_time = res.complete_time
            session.query(Order).filter(Order.order_id == res.order_id). \
                update({
                'delivety_time': DeltaSecondRFC_3339(courier_.current_time,
                                                     res.complete_time)
            })
            session.query(Courier).filter(Courier.courier_id == res.courier_id). \
                update({
                'current_time': done_time,
                'current_orders': check
            })

        session.commit()
        return make_response(jsonify({'success': 'HTTP 200 OK'}, {
            "order_id": res.order_id
        }), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'HTTP 400 Bad Request'}), 400)
