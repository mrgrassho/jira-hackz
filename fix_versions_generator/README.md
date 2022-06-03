# Fix Version Generator

Generador de fix versions utilizando la API de Jira. La logica actualmente implementada es la siguiente:

Dado un PROJ en JIRA, un rango de fechas y la primer fix version de comienzo. Esta tool generará:

- **Major releases**, Los lunes de cada semana.
- **Minor releases**, Los jueves de cada semana.