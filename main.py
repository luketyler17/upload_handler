import tornado.web
import tornado
import subprocess
import json
import yaml
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class UploadHandler(tornado.web.RequestHandler):
    async def post(self):
        # create the files for subprocess
        body = json.loads(self.request.files['file'][0].body)
        yaml_body = yaml.safe_load(self.request.files['yaml'][0].body.decode())
        cwd = os.getcwd()

        # for py_filter specifically
        with open(f"{cwd}/json_file.json", "w+") as out_file:
            json.dump(body, out_file, indent=6)
            out_file.close()
        with open(f"{cwd}/config.yaml", "w+") as out_file:
            yaml.dump(yaml_body, out_file)
            out_file.close()

        # subprocess call to py_filter with args and directory
        # change path to local path of py_filter
        path = "/home/luke/Desktop/py_filter/py_filter.py"
        sub_args = ["python", path, "-i", f"{cwd}/json_file.json", "-y",
                    f"{cwd}/config.yaml", "-d", f"{cwd}/py_output"]
        subprocess.call(sub_args)

        await send_back(self)
        # for py_filter specifically
        os.remove(f"{cwd}/json_file.json")
        os.remove(f"{cwd}/config.yaml")
        await self.finish()


async def send_back(self):
    cwd = os.getcwd()
    with open(f"{cwd}/py_output/py_filter_found.json", "rb") as out_file:
        while True:
            chunk = out_file.read((1024 * 1024))
            if not chunk:
                break
            try:
                self.write(chunk)
                await self.flush()
            except tornado.web.iostream.StreamClosedError:
                break
            finally:
                del chunk


settings = {
    'template_path': 'templates',
    'static_path': 'static',
    "srf_cookies": False
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadHandler),
], debug=True, **settings)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    application.listen(8888)
    print("Listening of port 8888")
    tornado.ioloop.IOLoop.instance().start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
