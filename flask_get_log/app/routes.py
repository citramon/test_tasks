from app import app
from flask import request, jsonify
from app.models import Log, People
from sqlalchemy.sql import and_
import re


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    __page = request.args.get('page', 1, type=int)
    __from = request.args.get('from', 0, type=int)
    __to = request.args.get('to', 0, type=int)
    __items = request.args.get('items', 20, type=int)

    logs = Log.query.filter(
        and_(Log.dt <= __to, Log.dt >= __from)
        ).paginate(__page, __items, False).items

    peoples = {}
    result = []
    for log in logs:

        event = log.event
        for i in re.findall(re.compile('<p=[0-9]*>'), log.event):
            num = int(i[3:-1])

            if num not in peoples:
                res = People.query.filter(People.id == num).first()
                peoples[num] = '{} {}'.format(res.first_name, res.last_name)

            event = event.replace('<p={}>'.format(num), peoples[num])

        result.append({'date': log.dt, 'event': event})

    del peoples
    del logs

    return jsonify(result)
