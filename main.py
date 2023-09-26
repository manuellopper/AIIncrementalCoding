<python>
    # Generando código con la ayuda de la IA
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "utiliza el código siguiente como base y genera código incremental sobre el mismo que contenga la funcionalidad indicada por el usuario. En la respuesta, cuando vayas a escribir el código en python precede éste con <python>  y utiliza </python> para terminar el bloque de código. "},
            {"role": "user", "content": file_content},
            {"role": "user", "content": prompt}
        ],
      temperature=0
    )
    response_content = response['choices'][0]['message']['content'].strip()

    # Separando el código Python de la respuesta no perteneciente al código
    code_pattern = re.compile(r'<python>(.*?)</python>', re.DOTALL)
    code_matches = code_pattern.findall(response_content)
    non_code = code_pattern.sub('', response_content)

    # El código Python se encuentra en la lista 'code_matches'
    # La respuesta no perteneciente al código Python se encuentra en la variable 'non_code'
</python>