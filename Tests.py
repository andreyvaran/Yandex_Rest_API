from functional import client
def MyTest ():
    res = client.post('/orders' , json = {
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": [
                    "09:00-14:00"
                ]
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": [
                    "09:00-14:00"
                ]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": [
                    "09:00-12:00",
                    "16:00-21:30"
                ]
            },
            {
                "order_id": 4,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": [
                    "09:00-14:00"
                ]
            },
            {
                "order_id": 5,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": [
                    "09:00-18:00"
                ]
            },
            {
                "order_id": 6,
                "weight": 5,
                "region": 22,
                "delivery_hours": [
                    "09:00-18:00"
                ]
            },
            {
                "order_id": 7,
                "weight": 0.6,
                "region": 12,
                "delivery_hours": [
                    "09:00-14:00"
                ]
            },
            {
                "order_id": 8,
                "weight": 4.2,
                "region": 22,
                "delivery_hours": [
                    "09:00-18:00"
                ]
            }
        ]
    }
    )
    print('Orders' ,res.get_json())
    res = client.post('/orders', json={
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": [
                    "09:00-18:00"
                ]
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": [
                    "09:00-18:00"
                ]
            },
            {
                "order_id": 11,
                "weight": 50.23,
                "region": 22,
                "delivery_hours": [
                    "09:00-12:00",
                    "16:00-21:30"
                ]
            }

        ]
    })

    print('Bad data orders ' , res.get_json())
    res = client.post('/couriers' , json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 3,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": ["08:00-18:00"]
            }
        ]
    })
    print('Couriers POST' , res.get_json())
    res = client.post('/couriers' , json = {
        "data": [
            {
                "courier_id": 6,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "15:00-14:00"]
            },
            {
                "courier_id": 5,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 4,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": ["08:00-08:00"]
            }
        ]
    })

    print('Couriers with bad data ' , res.get_json())
    res = client.get('/couriers/1')
    print('Old data ' , res.get_json())
    res = client.patch('/couriers/1' , json = {
        "regions": [11, 22, 12],
        "courier_type" : "car",
        "working_hours": ['01:30-10:30' , '11:00-20:00']
    })
    print(res.get_json())
    res = client.get('/couriers/1')
    print('New data ' , res.get_json())

    res = client.post('/orders/assign' , json  = {
        "courier_id": 1
    })
    print('Orders to courier 1' , res.get_json())

    res = client.post('/orders/complete' , json = {
        "courier_id": 1,
        "order_id": 1,
        "complete_time": "2021-03-28T21:15:30.52Z"
    })
    res = client.post('/orders/complete' , json = {
        "courier_id": 1,
        "order_id": 3,
        "complete_time": "2021-03-28T21:30:30.52Z"
    })
    res = client.post('/orders/complete' , json = {
        "courier_id": 1,
        "order_id": 6,
        "complete_time": "2021-03-28T21:59:57.52Z"
    })
    res = client.post('/orders/complete' , json = {
        "courier_id": 1,
        "order_id": 7,
        "complete_time": "2021-03-28T22:59:57.52Z"
    })
    res = client.post('/orders/complete' , json = {
        "courier_id": 1,
        "order_id": 8,
        "complete_time": "2021-03-28T23:59:57.52Z"
    })
    print("Now let's delite 12 region in regions first courier where the last order [4,5]")
    res = client.patch('/couriers/1' , json = {
        "regions": [11, 22]
    })
    res = client.get('/couriers/1')
    print('New data after delivery ' , res.get_json())
# Sorry for this test . I have no time to do normal :(
#   But if u want my cool test delite # in line 202
#MyTest()