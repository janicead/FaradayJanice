import json
import pathlib

from lxml import etree
import click


def obtener_cantidad_elementos_unicos_por_tag(nombre_tag, root):
    tags = root.findall(nombre_tag)
    mis_tags_unicos = set(
        element.find('id').text
        for element in tags
    )
    return len(mis_tags_unicos)


def obtener_cantidad_websites_unicas(root):
    web_sites = root.findall('.//web-site-id')
    mis_web_sites = set(
        element.text
        for element in web_sites
    )
    return len(mis_web_sites)


def obtener_vulns_web_y_no_web(vulns):
    mis_vulns_web = set()
    mis_vulns_no_web = set()
    for element in vulns:
        vuln_service = element.find('service-id')
        mi_id = element.find('id').text
        if vuln_service is None:
            mis_vulns_no_web.add(mi_id)
        else:
            mis_vulns_web.add(mi_id)
    return mis_vulns_web, mis_vulns_no_web

def vulns_to_dict(vulns):
    return [
        {
            child.tag: child.text
            for child in vuln.getchildren()
        }
        for vuln in vulns
    ]

@click.command(help="Generate dict report")
@click.option("--fileinput", required=True, prompt=True)
@click.option("--fileoutput", required=True, prompt=True)
def xmlfile_to_json(fileinput, fileoutput):
    if pathlib.Path(fileinput).exists():
        root = etree.parse(fileinput)
    else:
        print("El archivo ingresado no existe")
        return



    # Obtengo cantidad de host unicos
    cantidad_hosts = obtener_cantidad_elementos_unicos_por_tag('.//host', root)
    # Obtengo cantidad de service unicos
    cantidad_services = obtener_cantidad_elementos_unicos_por_tag('.//service', root)
    # Obtengo cantidad de websites unicos
    cantidad_web_sites = obtener_cantidad_websites_unicas(root)

    vulns = root.findall('.//vuln')
    #Obtengo vulns web y no webs
    vulns_web, vulns_no_web = obtener_vulns_web_y_no_web(vulns)
    cantidad_vulns_web = len(vulns_web)
    cantidad_vulns_no_web = len(vulns_no_web)

    data = {
        "hosts_count": cantidad_hosts,
        "services_count": cantidad_services,
        "website_count": cantidad_web_sites,
        "web_vulns_count": cantidad_vulns_web,
        "vulns_count": cantidad_vulns_no_web,
        "vulns": vulns_to_dict(vulns)
    }
    with open(fileoutput, 'w') as fp:
        json.dump(data, fp)
    print("El archivo fue creado con exito.")

if __name__ == "__main__":
    xmlfile_to_json()
