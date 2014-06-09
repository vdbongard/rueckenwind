import pytest

import rw
import rw.routing


def generate_rule(route):
    return rw.routing.Rule(route, None)


def test_parse_rule():
    assert rw.routing.parse_rule('/asdf/') == [(None, None, '/asdf/')]
    rule = rw.routing.parse_rule('/foo/<name>/bar')
    assert rule[0] == (None, None, '/foo/')
    assert rule[1] == (rw.routing.converter_default, None, 'name')
    assert rule[2] == (None, None, '/bar')


def test_parse_rule_errors():
    with pytest.raises(ValueError):
        # the argument name "name" is used twice
        list(rw.routing.parse_rule('/<name>/<name>/asd'))

    with pytest.raises(ValueError):
        # missing > after name
        list(rw.routing.parse_rule('/<name/asd'))


def test_rule_compare():
    for rule_0, rule_1 in (
        (generate_rule('/name'), generate_rule('/<something>')),
        (generate_rule('/name'), generate_rule('/na<something>')),
        (generate_rule('/name<something>'), generate_rule('/na<something>')),
    ):
        assert rule_0 < rule_1
        assert rule_1 > rule_0


def test_rule_eq():
    assert generate_rule('/') == generate_rule('/')
    assert generate_rule('/foo') == generate_rule('/foo')
    assert generate_rule('/name/<name>/photo') == generate_rule('/name/<name>/photo')
    assert generate_rule('/name/<name>/photo/<num:int>') == generate_rule('/name/<name>/photo/<num:int>')

    assert generate_rule('/') != generate_rule('/foo')
    assert generate_rule('/name/<name>/photo/<num>') != generate_rule('/name/<name>/photo/<num:int>')


def test_rule_sorting():
    rules = [
        generate_rule('/name'),
        generate_rule('/'),
        generate_rule('/name/<name>/photo'),
        generate_rule('/name/<else>'),
        generate_rule('/<something>'),
    ]
    rules2 = rules[:]
    rules2.sort()
    assert rules == rules2

    rules3 = rules[:]
    rules3.reverse()
    rules3.sort()
    assert rules == rules3


def test_reverse_path():
    assert generate_rule('/').get_path() == '/'
    assert generate_rule('/somewhere').get_path() == '/somewhere'
    assert generate_rule('/user/<user>').get_path({'user': 'dino'}) == '/user/dino'


def test_converter_default():
    assert (3, 'foo') == rw.routing.converter_default('foo')
    assert (3, 'foo') == rw.routing.converter_default('foo/bar')


def test_convert_int():
    assert rw.routing.converter_int('123') == (3, 123)
    assert rw.routing.converter_int('4321Hello World') == (4, 4321)
    assert rw.routing.converter_int('-1431') == (5, -1431)
    with pytest.raises(rw.routing.NoMatchError):
        rw.routing.converter_int('foo')


def test_convert_uint():
    assert rw.routing.converter_uint('123') == (3, 123)
    assert rw.routing.converter_uint('4321Hello World') == (4, 4321)

    with pytest.raises(rw.routing.NoMatchError):
        assert rw.routing.converter_uint('-1431') == (5, -1431)

# class HandlerA(rw.www.RequestHandler):
#     @rw.www.post('/post')
#     def post(self):
#         pass
#
#
# class HandlerB(rw.www.RequestHandler):
#     @rw.www.post('/bost')
#     def postB(self):
#         pass
#
#
# class Handler2(HandlerA, HandlerB):
#     @rw.www.get('/get')
#     def get_(self):
#         pass
#
#
# def gen_handler(handler_cls, method, path):
#     req = httpserver.HTTPRequest(method, path, remote_ip='127.0.0.1')
#     return handler_cls(web.Application(), req)
#
#
# def test_inheritance():
#     routes = rw.www.generate_routing(Handler2)
#     assert len(routes['get']) == 1
#     assert len(routes['post']) == 2
#     # assert gen_handler(Handler2, 'GET', '/get')._execute([])
#     # assert gen_handler(Handler2, 'POST', '/post')._handle_request()
#     # assert gen_handler(Handler2, 'POST', '/bost')._handle_request()
#     # assert not gen_handler(Handler2, 'POST', '/get')._handle_request()
#     # assert not gen_handler(Handler2, 'GET', '/post')._handle_request()
#
#
# class TestHandler(rw.www.RequestHandler):
#     last_invoced = None
#
#     @rw.www.get('/')
#     def index(self):
#         TestHandler.last_invoced = 'index'
#
#     @rw.www.get('/<name>')
#     def page(self, name):
#         TestHandler.last_invoced = 'page:' + name


# def test_minimum_consume():
#     gen_handler(TestHandler, 'GET', '/')._handle_request()
#     assert TestHandler.last_invoced == 'index'
#     gen_handler(TestHandler, 'GET', '/asd')._handle_request()
#     assert TestHandler.last_invoced == 'page:asd'
#     gen_handler(TestHandler, 'GET', '/')._handle_request()
#     assert TestHandler.last_invoced == 'index'

#def test_converter():
#    a = generate_rule('/a/<x:int>/<y:int>')
#    class Req(object):
#        def __init__(self, path, type):
#            self.path = path
#            self.type = type
#    assert a.match(None, Req('/a/1/2'))
