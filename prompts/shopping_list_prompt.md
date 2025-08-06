# Prompt para Generación de Lista de Compras Inteligente

**Objetivo:** Analizar un plan nutricional y generar una lista de compras estructurada y categorizada.

**Instrucciones para el LLM:**

1.  **Analiza el Plan Nutricional:** Revisa cuidadosamente el siguiente plan nutricional proporcionado. Extrae todos los ingredientes necesarios para preparar las comidas indicadas.

    ```
    {plan_nutricional}
    ```

2.  **Agrupa por Categorías:** Organiza todos los ingredientes extraídos en categorías lógicas para facilitar las compras. Utiliza las siguientes categorías como guía, pero si encuentras un ingrediente que no encaja, crea una nueva categoría apropiada:
    *   Proteínas (ej. pollo, carne de res, pescado, tofu, lentejas)
    *   Vegetales (ej. espinacas, brócoli, zanahorias, tomates)
    *   Frutas (ej. manzanas, plátanos, fresas)
    *   Carbohidratos Complejos (ej. avena, arroz integral, quinoa, pan integral)
    *   Lácteos y Alternativas (ej. leche, yogur, queso, leche de almendras)
    *   Grasas Saludables (ej. aguacate, nueces, semillas, aceite de oliva)
    *   Especias y Condimentos (ej. sal, pimienta, ajo en polvo, hierbas)

3.  **Formato de Salida:**
    *   Presenta la lista de compras de una manera clara y fácil de leer.
    *   El resultado debe ser estructurado para que pueda ser procesado por un `output_parser`. Genera la lista en formato Markdown, usando encabezados para cada categoría y una lista de viñetas para los ingredientes.

**Ejemplo de Salida Esperada:**

### Proteínas
*   Pechuga de pollo
*   Salmón
*   Lentejas

### Vegetales
*   Brócoli
*   Espinacas
*   Cebolla

... y así sucesivamente para cada categoría.