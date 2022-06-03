providers = [
    "pe_bbva_netcash",
    "bancolombia_corp_co",
    "telecredito",
    "telebanking_corp_pe",
    "bancolombia",
    "bcp",
    "bci_corp_cl",
    "santander_pers_cl",
    "scotia_pers_cl",
    "interbank_corp_pe",
    "davivienda",
    "scotia_pe_corp",
    "bancogeneral_pers_pa",
    "bbva_pers_co",
    "bcp_pers_pe",
    "bogota_corp_co",
    "santander",
]

header = "Summary, Assignee, Reporter, Issue Type, Description, Priority, Story Points, Epic Link"
body_template = """
"[Banking] - Migrar codigos de error data - PROVIDER", , vscafati@prometeoapi.com, Task, "
Como usuario de prometeo, quiero recibir errores mas descriptivos a la hora de interacturar la API. Por lo que se desarrollo una mejora sobre los errores retornados para que cumplan dicho proposito.

*Acceptance Criteria:*
* Migrar códigos de error de los endpoints de datos para el provider {{PROVIDER}}. Los cuales comprenden:
** {{/login}}, inicio de sesión.
** {{/account}}, cuentas.
** {{/account/\{account-id\}}}, movimientos de cuentas.
** {{/info}}, información personal.
** {{/credit-cards}}, tarjetas de credito
** {{/credit-cards/\{credit-card-id\}}}, movimientos de tarjeta de credito.
", , 2, DEV-966"""
lines = [header]
for prov in providers:
    lines.append(body_template.replace("PROVIDER", prov))

with open("file.csv", "w") as fp:
    fp.writelines(lines)
