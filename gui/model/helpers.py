import jinja2


class TextModel:
    
    def __init__(self) -> None:
        self.template_path = None

    def text_model(self) -> str:
        ret_val = ""
        try:
            templateLoader = jinja2.FileSystemLoader(searchpath="./")
            templateEnv = jinja2.Environment(loader=templateLoader)
            t = templateEnv.get_template(self.template_path)
            ret_val = t.render(model=self)
        except Exception as ex:
            print(ex)

        return ret_val