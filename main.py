# Generando código con la ayuda de la IA
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "utiliza el código siguiente como base y genera código incremental sobre el mismo que contenga la funcionalidad indicada por el usuario. En la respuesta, cuando vayas a escribir el código en python precede éste con <python>  y utiliza