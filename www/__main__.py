import scrumboard
from scrumboard.board import Board
from flask import *
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

#from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import Form as InsecureForm
from wtforms import FileField, SelectField, TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.form import WebobInputWrapper
from wtforms.validators import Required
from werkzeug.datastructures import MultiDict
import glob
import os, time
import ConfigParser
import cv2.cv as cv
from PIL import Image as pil

class SelectForm(InsecureForm):
    _files = glob.glob('/Users/thobra/Dropbox/Photos/*.jpg')
    files = [(f, os.path.basename(f)) for f in _files]
    files_field = SelectField('Select image', choices=files)

class SettingsForm(Form):
    #select_image = FormField(SelectForm)
    select_image = FileField('Select image', [validators.required()])
    binarize_threshold = IntegerField('Threshold', [validators.NumberRange(min=10, max=250, message="Wrong!")])

    # _files = glob.glob('/Users/thobra/Dropbox/Photos/*.jpg')
    # files = [(f, os.path.basename(f)) for f in _files]
    # radio_field = SelectField('This is a radio field',
    #                                 choices=files)
    # checkbox_field = BooleanField('This is a checkbox',
    #                               description='Checkboxes can be tricky.')

    # subforms
    #mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    #office_phone = FormField(TelephoneForm, label='Your office phone')

    submit_button = SubmitField('Save')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


def create_app(config=None):
    app = Flask(__name__)
    toolbar = DebugToolbarExtension(app)
    app.debug = True
    # app.register_blueprint(Blueprint('images', \
    #     __name__, \
    #     static_folder=scrumboard.config.get('config', 'static_file_path')))
    Bootstrap(app)
    # in a real app, these should be configured through Flask-Appconfig
    app.config['UPLOAD_FOLDER'] = '/tmp'
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
         '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    def loadImg(fn):
        """
        Copying from class Image the part of loading an image from the filesystem
        Does not work when running through Image(path)
        """
        _pil = pil.open(fn).convert("RGB")
        _bitmap = cv.CreateImageHeader(_pil.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(_bitmap, _pil.tostring())
        cv.CvtColor(_bitmap, _bitmap, cv.CV_RGB2BGR)
        return _bitmap

    @app.route('/')
    def index():
        return redirect(url_for('settings'))

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        default = config.as_dict()
        form = SettingsForm(**default['settings'])
        filename = None
        cards = None
        if request.method == 'POST' and form.validate():
            #fn = form.select_image.data
            fn = request.files['select_image']
            filename = fn.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], fn.filename)
            fn.save(filepath)
            for field in form.data:
                config.set('settings', field, form[field].data)
            write_config(config)
            board = Board()
            img = loadImg(filepath)
            board.image = img
            board.findCards()
            # Image.save does not return a status, we don't know whether it was successful
            board.draw(save=True)
            cards = board.list_cards
            flash('Image loaded successfully')
            print form

        return render_template('index.html', form=form, timestamp=time.time(), cards=cards)

    return app

class DictParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

if __name__ == '__main__':
    config_file = "scrumboard/settings.ini"
    def write_config(config_obj):
        global config_file
        with open(config_file, 'wb') as configfile:
            config_obj.write(configfile)

    config = DictParser()
    config.readfp(open(config_file))
    #config.read(["setting.ini"])


    create_app(config=config).run(debug=True)
