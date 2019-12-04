#### jaeger flask example 

##### reference
[https://github.com/opentracing-contrib/python-flask/tree/master/example](https://github.com/opentracing-contrib/python-flask/tree/master/example)

[https://github.com/jaegertracing/jaeger-client-python](https://github.com/jaegertracing/jaeger-client-python)

[https://www.jaegertracing.io/docs/1.15/getting-started/#all-in-one](https://www.jaegertracing.io/docs/1.15/getting-started/#all-in-one)

##### steps(env: linux)
- start jaeger
```
bash jaeger/start_jaeger_all_in_one.sh
# web url: http://$ip:16686
```
- run webapps
```
pip install -r requirements.txt
export JAEGER_HOST=$ip
python app/webapp_00.py
# in another terminal
python app/webapp_01.py
```
- client
```bash
python client/client.py
```

##### tips
install_all_patches patches requests, using grequests will split traces between services