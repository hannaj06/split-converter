from split_converter import *
from split_converter.single_val_converter import single_val_converter
from split_converter.multiple_val_converter import multiple_val_converter
from split_converter.db_controller import db_controller
from multiprocessing import Process
from split_converter.converterError import converterError

templateLoader = FileSystemLoader( searchpath = 'templates')
templateEnv = Environment(loader = templateLoader)
home_page = templateEnv.get_template('home.html')

single_process=False 




class home(tornado.web.RequestHandler):
    def save_record(self, results):
        db = db_controller()
        db.insert_record([results])
        db.close()

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

        try:
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

            #html is displayed while results are saved to db
            results_process = Process(target=self.save_record, args = ({'timestamp': datetime.datetime.now().strftime("%d-%m-%y - %H:%M.%S"), 'results': results},))
            results_process.start()
            db = db_controller()
            history = db.fetch_r()

            his = []
            for i in history:
                i = i[0].replace('[', '').replace(']', '')
                his.append(i.split(','))

            db.close()
            html_output = home_page.render(his = his, results = results)
            self.write(html_output)
            results_process.join()
            
        except converterError as e:
            html_output = home_page.render(message = str(e)) 
            self.write(html_output)

class export(tornado.web.RequestHandler):
    def get(self):
        db = db_controller()
        history = db.fetch()
        db.close()
        export_file = open('static/split_converter.txt', 'w')
        export_file.write('split converter historcal data\n\n')
        export_file.write('mm-dd-yy - hh:mm.ss | [min/500m, kmh, mph, min/mile]\n')
        export_file.write('------------------------------------------------------------\n')
        for record in history:
            export_file.write(str(record[0]) + '  |  ' + str(record[1]) + '\n')       
        export_file.close()
        self.redirect('/static/split_converter.txt')

class clear_db(tornado.web.RequestHandler):
    def get(self):
        db = db_controller()
        db.clear_db()
        db.close()
        self.redirect('/home')


def make_app():
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}

    return tornado.web.Application([
        (r"/home", home),
        (r"/export", export),
        (r"/clear_db", clear_db),
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
