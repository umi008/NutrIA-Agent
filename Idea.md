
# Agente de Nutrición con IA 

Un agente conversacional que interactúa con el usuario para recopilar datos, realizar cálculos y generar un plan de bienestar integral (nutrición y ejercicio).

---

## 1. Definición del Agente

El agente es un **`ConversationalAgent`** que interactúa con el usuario para recopilar información y, posteriormente, utiliza un conjunto de herramientas especializadas para realizar cálculos y generar un plan de bienestar integral que incluye nutrición y ejercicio.

---

## 2. Recopilación de Información (Inputs)

La primera fase del agente se centra en la interacción con el usuario para obtener los datos necesarios. Se utiliza un **`PromptTemplate`** inicial para guiar al usuario. La clave es asegurar que el agente entienda y valide cada entrada.

### Prompt Inicial

Una cadena de `PromptTemplates` o una única `ChatPromptTemplate` que recopile de forma estructurada los siguientes datos:

* **Edad**
* **Peso** (kg o lbs)
* **Altura** (cm o pulgadas)
* **Nivel de actividad física**: Crucial incluir una breve explicación para que el usuario elija correctamente. (ej. "Sedentario: poco o ningún ejercicio", "Ligero: ejercicio ligero 1-3 días/semana", etc.).
* **Objetivos**: Bajar de peso, subir de peso, mantener, ganar masa muscular, etc.
* **Preferencias alimentarias**: Lista de comidas que no come (`dislikes`) y comidas que le gustan (`likes`).
* **Preferencias de ejercicio**: Dónde (`home`, `gym`, `mixto`) y con qué frecuencia (número de días).
* **Tipo de rutina de ejercicio**: `U/L` (Upper/Lower), `R` (Full Body), etc.

---

## 3. Herramientas y Cálculos (Tools)

El agente necesita **herramientas personalizadas (`Custom Tools`)** para realizar cálculos matemáticos precisos, ya que los LLM por sí solos pueden cometer errores.

### `Tool calculate_bmi`
* **Descripción**: Calcula el Índice de Masa Corporal (IMC) basado en el peso y la altura.
* **Input**: `peso`, `altura`.
* **Output**: `valor_imc`, `clasificación_imc` (ej. "Normal", "Sobrepeso").
* **Fórmula**: $IMC = \frac{peso(kg)}{altura(m)^2}$

### `Tool calculate_bmr`
* **Descripción**: Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor.
* **Input**: `edad`, `peso`, `altura`, `género`.
* **Output**: `valor_tmb`.
* **Fórmula (Mifflin-St Jeor)**:
    * **Hombres**: $TMB = (10 \times peso(kg)) + (6.25 \times altura(cm)) - (5 \times edad(años)) + 5$
    * **Mujeres**: $TMB = (10 \times peso(kg)) + (6.25 \times altura(cm)) - (5 \times edad(años)) - 161$

### `Tool calculate_macros`
* **Descripción**: Calcula la cantidad de macronutrientes (proteínas, carbohidratos, grasas) basándose en la TMB, el nivel de actividad y los objetivos.
* **Input**: `tmb`, `nivel_actividad`, `objetivo`.
* **Output**: `macros_totales` (ej. 200g proteínas, 250g carbohidratos, 60g grasas).

---

## 4. Generación del Plan Integral

Una vez que el agente tiene todos los datos, pasa a la fase de generación del plan. El LLM usa los resultados de las herramientas y las preferencias del usuario para crear los outputs. Para optimizar el tiempo de respuesta, la generación del **Plan Nutricional**, la **Lista de Compras** y la **Rutina de Ejercicio** se pueden ejecutar en **procesos paralelos**.

### Plan Nutricional y Dieta
* **Prompting**: Se le dará al LLM un prompt con el contexto completo (datos del usuario, IMC, TMB, macros) y se le pedirá que genere un plan nutricional semanal.
* **Instrucciones clave en el prompt**:
    * Generar comidas específicas que cumplan con los macros calculados.
    * Integrar las preferencias (`likes`, `dislikes`).
    * Proporcionar opciones de sustituciones y flexibilidad (ej. "si no tienes pollo, puedes usar tofu o pescado").

### Lista de Compras Inteligente
* **Prompting**: Se le pedirá al LLM que analice la dieta generada y extraiga una lista de ingredientes agrupados por categorías (ej. "Proteínas", "Vegetales", "Lácteos").
* **Instrucciones clave en el prompt**:
    * La lista debe ser un `output_parser` para un formato consistente.
    * Debe ser fácil de leer y usar.

### Rutina de Ejercicio y Recomendaciones Adicionales
* **Prompting**: Se le proporcionará al LLM el contexto de las preferencias de ejercicio del usuario (`home`/`gym`/`mixto`, días, tipo de rutina).
* **Instrucciones clave en el prompt**:
    * Generar la rutina en un **formato de tabla Markdown** con las columnas: Ejercicio, Sets, Repeticiones, Descanso (minutos), Grupo muscular.
    * Añadir recomendaciones adicionales, como la importancia del descanso, la hidratación o la progresión gradual.

---

## 5. Arquitectura del Agente (Diagrama de Flujo)

* **Paso 1**: **Input del Usuario**: El agente interactúa y recopila datos.
* **Paso 2**: **Activación de Herramientas**: El agente llama a las herramientas `calculate_bmi`, `calculate_bmr`, y `calculate_macros` en secuencia.
* **Paso 3**: **Razonamiento del LLM**: El LLM recibe los datos del usuario y los resultados de las herramientas.
* **Paso 4**: **Generación de Outputs (en paralelo)**: El LLM genera el plan nutricional, la lista de compras y la rutina de ejercicios de manera simultánea para una respuesta más rápida.
* **Paso 5**: **Presentación**: El agente presenta los resultados al usuario en un formato claro y estructurado.