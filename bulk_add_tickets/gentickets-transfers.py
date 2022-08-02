providers = [
    "bcp_pers_pe",
    "scotia_pers_pe",
    "brou_pers_uy",
]

header = "Summary, Assignee, Reporter, Issue Type, Description, Priority, Story Points, Epic Link"
body_template = """
"[Banking] - Migrar codigos de error transfer - PROVIDER", , vscafati@prometeoapi.com, Task, "
Como usuario de prometeo, quiero recibir errores mas descriptivos a la hora de interacturar la API. Por lo que se desarrollo una mejora sobre los errores retornados para que cumplan dicho proposito.

*Acceptance Criteria:*
* Migrar códigos de error de los endpoints de datos para el provider {{PROVIDER}}. Los cuales comprenden:
** {{/transfer/preprocess}}, Preprocesamiento de una transferencia.
** {{/transfer/confirm}}, Confirmación de una transferencia. (Solo en algunos providers)
** {{transfer/detail}}, Obtiene los detalles de una transferencia.
", , 2, DEV-966"""
lines = [header]
for prov in providers:
    lines.append(body_template.replace("PROVIDER", prov))

with open("file.csv", "w") as fp:
    fp.writelines(lines)
