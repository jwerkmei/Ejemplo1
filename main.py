from openai import OpenAI
client = OpenAI()

costo_token_entrada = (2.50*1)/1000000
costo_token_salida = (10*1)/1000000

data_contacto = input("Ingrese nombre completo, número de teléfono, correo electrónico: ")
data_academica = input("Títulos obtenidos, instituciones educativas, fecha de graduación: ")
data_laboral = input("Puestos anteriores, empresas, responsabilidades, fechas de empleo: ")
data = "Información de contacto: "+data_contacto+" ; Información académica: "+data_academica+" ; data_laboral: "+data_laboral

validacion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
          "role": "system",
          "content": [
              {
                  "type": "text",
                  "text": """
                  Debes verificar que se proporcionen todos los parámetros: nombre completo, número de teléfono, 
                  correo electrónico. 
                  Responde con "Sí" si todos los parámetros están presentes, o "No" si falta alguno de ellos.

                  La información que se proporcione debe incluir solo lo previamente especificado 
                  (nombre completo, número de teléfono, correo electrónico).
                  Indicame que datos faltan.
                  """
              }
          ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": data
                }
            ]
        },
    ],
    temperature=0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
)

print(50*'-')
print(validacion.choices[0].message.content)
print("Tokens: ", validacion.usage)

prompt_tokens_v = validacion.usage.prompt_tokens
completion_tokens_v = validacion.usage.completion_tokens
total_tokens_v = validacion.usage.total_tokens

print(f"Costo tokens de entrada: {prompt_tokens_v*costo_token_entrada:.10f} dólares")
print(f"Costo tokens de salida: {completion_tokens_v*costo_token_salida:.10f} dólares")
print(f"Costo total: {prompt_tokens_v*costo_token_entrada+completion_tokens_v*costo_token_salida:.10f} dólares")
print(50*'-')


if validacion.choices[0].message.content == "Sí." or validacion.choices[0].message.content =="Sí":
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Eres un asistente especialista en escribir curriculum vitae. Debes utilizar solo la información entregada y no inventar antecedentes.
                        La información a entregar sera: Nombre completo, número de teléfono, correo electrónico, Títulos obtenidos, instituciones educativas, fechas de
                        graduación, Puestos anteriores, empresas, responsabilidades, fechas de empleo.  Con esto tienes que generar un curriculum vitae. Agregar
                        campo con introducción con un resumen del perfil.  Sugerir, que otra información agregar.
                        """
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": data
                    }
                ]
            },
        ],
        temperature=1.0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )

    print(50*'-')
    print(response.choices[0].message.content)
    print("Tokens: ", response.usage)

    prompt_tokens_s = response.usage.prompt_tokens
    completion_tokens_s = response.usage.completion_tokens
    total_tokens_s = response.usage.total_tokens

    print(f"Costo tokens de entrada: {prompt_tokens_s*costo_token_entrada:.10f} dólares")
    print(f"Costo tokens de salida: {completion_tokens_s*costo_token_salida:.10f} dólares")
    print(f"Costo total: {prompt_tokens_s*costo_token_entrada+completion_tokens_s*costo_token_salida:.10f} dólares")
    print(50*'-')
    print(f"Costo total de las dos consultas, validación + respuesta: {(prompt_tokens_v*costo_token_entrada+completion_tokens_v*costo_token_salida)+(prompt_tokens_s*costo_token_entrada+completion_tokens_s*costo_token_salida):.10f} dólares")
else:
    print("Faltan datos")