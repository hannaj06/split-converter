from split_converter import *
from split_converter.single_val_converter import single_val_converter
from split_converter.multiple_val_converter import multiple_val_converter

templateLoader = FileSystemLoader( searchpath = 'templates')
templateEnv = Environment(loader = templateLoader)
home_page = templateEnv.get_template('home.html')

single_process=True 

class home(tornado.web.RequestHandler):
    def get(self):
        html_output = home_page.render()
        self.write(html_output)

    def post(self):
        unit = self.get_argument('unit', '')
        
        if unit == 'mph' or unit == 'kmh':
            val = self.get_argument('val', '')
        else:
            mins = self.get_argument('min', '')
            secs = self.get_argument('sec', '')


        if unit == 'kmh':
            converter = single_val_converter(val)
            results = [converter.kmh_to_split(),
            val,
            converter.kmh_to_mph(),
            converter.kmh_to_msplit()]


        elif unit == 'mph':
            converter = single_val_converter(val)

            results = [converter.mph_to_split(),
            converter.mph_to_kmh(),
            val,
            converter.mph_to_msplit()
            ] 

        elif unit == 'sec/500m':
            converter = multiple_val_converter(mins, secs)

            results = [mins + ':' + secs,
            converter.split_to_kmh(),
            converter.split_to_mph(),
            converter.split_to_msplit()
            ]

        elif unit == 'min/mile':
            converter = multiple_val_converter(mins, secs)

            results = [converter.msplit_to_split(),
            converter.msplit_to_kmh(),
            converter.msplit_to_mph(),
            mins + ':' + secs
            ]

        html_output = home_page.render(results = results)
        self.write(html_output)

def make_app():
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}

    return tornado.web.Application([
        (r"/home", home),
    ],debug=single_process, **settings)

if __name__ == "__main__":
    if single_process==False: 
        app = make_app()
        server=tornado.httpserver.HTTPServer(app) 
        server.bind(8765)
        server.start(0) 
        try: 
            tornado.ioloop.IOLoop.current().start()
        except KeyboardInterrupt: 
            tornado.ioloop.IOLoop.instance().stop() 

    else: 
        app = make_app()
        app.listen(8765)
        tornado.ioloop.IOLoop.current().start()
