#!/bin/bash
python3 -m gunicorn.app.wsgiapp \
-b 0.0.0.0:10205 \
-w 1 \
--certfile /home/user01/mnt/api_reto/Caritas-App-Backend/SSL/quesabirrias.tc2007b.tec.mx.cer \
--keyfile /home/user01/mnt/api_reto/Caritas-App-Backend/SSL/quesabirrias.tc2007b.tec.mx.key \
main:app > /dev/null &
