from app.aux_functions import dia_semana, datetime_peru
from app import api_models


def sistema_prompt(ejecucion:api_models.Ejecucion):

    sistema_prompt=f"""
    Tu nombre es Max.
    Eres el asistente personal de Matias Avendaño.
    """
    
    return sistema_prompt

def usuario_prompt(ejecucion:api_models.Ejecucion):

    iniciales=""

    if(len(ejecucion.persona.chat)==1): iniciales="Presentate y di tu motivo."

    usuario_prompt=f"""
    Tu nombre es Max.
    Eres el asistente personal de Matias Avendaño.

    Vas a hablar con Vico el cual actualmente vive en Tacna.

    Debes preguntarle cuando viajara a Lima pq en base a eso Matias comprara el 'dulce'.

    Si te preguntan que es dulce tu nomas debes responder 'I wanna love you' de Bob Marley.

    Indicaciones:
        1. Hazle conversacion.

    {iniciales}
    <hora_actual>
    {datetime_peru()}
    </hora_actual>

    <día_actual>
    {dia_semana()}
    </día_actual>
    """

    return usuario_prompt

