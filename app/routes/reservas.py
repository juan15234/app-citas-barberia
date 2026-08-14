from flask import Blueprint, render_template

from app.forms.FormReserva import FormReserva

reservas_bp = Blueprint("reservas_bp", __name__, url_prefix="/reservas")

@reservas_bp.route("/<tipo_servicio>", methods=['POST','GET'])
def reserva(tipo_servicio):
    
    form = FormReserva()
    
    if form.validate_on_submit():
        
        nombre_cliente = form.nombre.data
        email_cliente = form.email.data
        numero_cliente = form.email.data
        
        print(nombre_cliente, email_cliente, numero_cliente)
        
    else:
        print(form.errors)
        return render_template("reserva.html", form=form, error=form.errors)