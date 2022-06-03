# Fix Version Generator

Generador de fix versions utilizando la API de Jira. La logica actualmente implementada es la siguiente:

Dado un PROJ en JIRA, un rango de fechas y la primer fix version de comienzo. Esta tool generará:

- **Major releases**, Los major de cada semana.
- **Minor releases**, Los minor de cada semana.

## Usage

```sh
usage: fix_version_gen.py [-h] [-f {WEEKLY,EVERY_TWO_WEEKS,MONTHLY}] [-ma {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}]
                          [-mi {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}]
                          jira_project start_date end_date version

positional arguments:
  jira_project          Specify Jira project name
  start_date            Specify fix version start date. Format YYYYMMDD
  end_date              Specify fix version end date. Format YYYYMMDD
  version               Specify fix version number. Following this format: 'Feature.Mayor.Minor'. Example: 1.1.0

optional arguments:
  -h, --help            show this help message and exit
  -f {WEEKLY,EVERY_TWO_WEEKS,MONTHLY}, --freq {WEEKLY,EVERY_TWO_WEEKS,MONTHLY}
                        Specify the frequency of release. (default: WEEKLY)
  -ma {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}, --major {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}
                        Specify the weekday of major release. (default: MONDAY)
  -mi {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}, --minor {MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY}
                        Specify the weekday of minor release. (default: THURSDAY)
```