from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL, Email


# Form to add a Cafe to the DATABASE
# TODO: Make available only for admin (when authentication is set up)
class CafeFormDataBase(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(message="Required")])
    location = StringField('Location', validators=[DataRequired(message="Required"), URL(message="Enter valid URL")])
    open_time = StringField('Open', validators=[DataRequired(message="Required")])
    close_time = StringField('Close', validators=[DataRequired(message="Required")])
    coffee_rating = SelectField("Coffee rating",
                                choices=["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"],
                                validators=[DataRequired(message="Required")])
    wifi_rating = SelectField("Wifi rating",
                              choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired(message="Required")])
    p_sockets = SelectField("Power sockets availability ",
                            choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                            validators=[DataRequired(message="Required")])
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Required Field.")],
                       render_kw={"placeholder": "Full Name"})
    email = StringField("Email", validators=[DataRequired("Required Field."), Email("Not a valid email.")],
                        render_kw={"placeholder": "Valid Email"})
    phone = StringField("Phone Number", validators=[DataRequired("Required Field.")],
                        render_kw={"placeholder": "Starting with country code"})
    message = TextAreaField(label="Message", validators=[DataRequired("Required Field.")],
                            render_kw={"placeholder": "What do you want to tell me?"})
    submit = SubmitField("Send Message")


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(message="Required")])
    location = StringField('Location', validators=[DataRequired(message="Required"), URL(message="Enter valid URL")])
    description = TextAreaField('Why Add?', validators=[DataRequired(message="Required")],
                                render_kw={"placeholder": "Tell us why do you think we should add this Cafe."})
    submit = SubmitField('Suggest Cafe')
