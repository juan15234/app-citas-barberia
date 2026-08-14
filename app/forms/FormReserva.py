from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp

class FormReserva(FlaskForm):
    nombre = StringField("Nombre", validators=[ DataRequired() ], render_kw={ "placeholder":"" })
    correo = StringField("Correo", validators=[ DataRequired(), Email(), ], render_kw={ "placeholder":"" })
    numero = StringField("Número", validators=[ DataRequired(), Length(min=10,max=10), Regexp(r'^[0-9]+$', message="El número solo puede contener números") ])
    boton_reservar = SubmitField("Reservar")