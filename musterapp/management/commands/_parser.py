import re
import urllib
import os
import xml.etree.ElementTree as ET

class MusterParser: 
    
    _ns = {'lido': 'http://www.lido-schema.org',
           'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    _recpattern = re.compile("HA\.II\.(\d+)(?:\.(\d+))?")
    
    _img_url_tpl ="Htw-berlin-stoffmuster-ha02-{:02d}-{:03d}.jpg"
    _commonsapi_url_tpl = "http://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image={}"
    
    _valid_volumes = ['HA.II.02', 'HA.II.03', 'HA.II.29', 'HA.II.30', 'HA.II.31', 'HA.II.33', 
                     'HA.II.34', 'HA.II.25', 'HA.II.50', 'HA.II.26', 'HA.II.07', 'HA.II.08', 
                     'HA.II.09', 'HA.II.10', 'HA.II.12', 'HA.II.13', 'HA.II.14', 'HA.II.15', 
                     'HA.II.16', 'HA.II.20', 'HA.II.22', 'HA.II.27', 'HA.II.28', 'HA.II.49']

    def __init__(self, cachedir=None, verbose=False):
        self._valid_volumes_ids = sorted([ int(s[6:]) for s in self._valid_volumes ])
        self._cachedir = cachedir
        self._download = cachedir is not None
        self._verbose = verbose
        
    
    def parse(self, tree):
        ns = self._ns
        
        if not isinstance(tree, ET.ElementTree):
            tree = ET.parse(tree)
        
        volumes = {}
        queue = []
        
        it = tree.iterfind("lido:lido", ns)
        queue = list(it)

        while queue:
            lido = queue.pop(0)
            recid = lido.find("lido:lidoRecID", ns).text
            if recid is None:
                print("Error: no recid at")
                continue

            match = self._recpattern.match(recid)
            if match is None:
                print("Error: no recpattern match on " + recid)
                continue

            volid = int(match.group(1))
            if volid not in self._valid_volumes_ids:
                if self._verbose:
                    print("volume id not in valid list " + recid)
                continue

            pageid = match.group(2) 
            if pageid is None:
                if volid in volumes:
                    print("Error: volume already exists " + recid)
                    break    
                volumes[volid] = self._vol_info(lido, recid)

            else:
                if volid not in volumes:
                    print("Warning: volume not parsed yet " + recid)
                    queue.append(lido)
                    continue


                pageid = int(pageid)
                volume = volumes[volid]


                if pageid in volume:
                    if pageid == 0:
                        print("Warning: page 0 already exists : " + recid)
                    else:
                        print("Error: page already exists " + str(pageid) + " : " + recid)
                    continue

                page = self._page_info(lido, recid)

                page["colors"] =  page["types"] = []
                match = re.match("^.*\((.+)\)[ .]*$", page["general_desc"])
                if match is not None:
                    tags = match.group(1).strip().split(";")
                    page["colors"] = list(filter(None, re.split("[, ]", tags[0])))
                    if len(tags) > 1:
                        page["types"] = list(filter(None, re.split("[, ]", tags[1])))

                img_name = self._img_url_tpl.format(volid, pageid)
                page["img_name"] = img_name

                page["img_path"] = page["img_meta_path"] = ""
                if self._download:
                    page["img_path"], page["img_meta_path"] = \
                        self._download_img(volume["record_id"], recid, img_name)


                volume["pages"][pageid] = page
                
        return volumes
            
            
        
    def _common_info(self, lido):
        ns = self._ns

        object_name = lido.find(".//lido:objectWorkType/lido:conceptID[@lido:type='object name']/../lido:term", ns).text
        object_category = lido.find(".//lido:classification[@lido:type='object category']/lido:term", ns).text

        general_desc = lido.find(".//lido:objectDescriptionWrap"
                                    "/lido:objectDescriptionSet[@lido:type='general description']"
                                    "/lido:descriptiveNoteValue", ns)
        general_desc = general_desc.text if general_desc is not None else ""

        physical_desc = lido.find(".//lido:objectDescriptionWrap"
                                    "/lido:objectDescriptionSet[@lido:type='physical description']"
                                    "/lido:descriptiveNoteValue", ns)
        physical_desc = physical_desc.text if physical_desc is not None else ""


        dims = lido.findall(".//lido:objectMeasurements"
                            "/lido:measurementsSet", ns)
        height = width = ""
        pagecount = -1
        for dim in dims:
            type = dim.find("lido:measurementType",ns).text
            value = dim.find("lido:measurementValue",ns).text
            unit = dim.find("lido:measurementUnit",ns).text   
            if type == "Breite":
                width = float(value)
            elif type == "Höhe":
                height = float(value)
            elif type == "Umfang":
                pagecount = int(float(value))

        return {"object_name": object_name,
                "object_category": object_category,
                "general_desc": general_desc,
                "physical_desc": physical_desc,
                "page_width": width, 
                "page_height": height,
                "page_count": pagecount}
    
    
    
    def _vol_info(self, lido, recid):
        ns = self._ns

        titles = lido.findall(".//lido:titleWrap/lido:titleSet/lido:appellationValue", ns)
        titles = [ t.text for t in titles if t.text ]
        title = "|".join(titles)

        #production = lido.find(".//lido:event/lido:eventType/)
        producer_name = producer_role = location = ""
        for event in lido.findall(".//lido:event", ns):
            type = event.find("./lido:eventType/lido:term", ns)
            if type is None or type.text != "Production":
                continue

            producer_name = event.find("./lido:eventActor//lido:nameActorSet/lido:appellationValue",ns)
            producer_name = producer_name.text if producer_name is not None else ""
            producer_role = event.find("./lido:eventActor//lido:roleActor/lido:term", ns)
            producer_role = producer_role.text if producer_role is not None else ""
            location = event.find("./lido:eventPlace//lido:namePlaceSet//lido:appellationValue", ns)
            location = location.text if location is not None else ""


        # TODO: eventMaterialsTech

        result = self._common_info(lido)

        result.update({
                "record_id": recid,
                "title": title, 
                "producer_name": producer_name,
                "producer_role": producer_role,
                "producer_location": location,
                "pages": {}
            })

        return result
    
    
    def _page_info(self, lido, recid):

        result = self._common_info(lido)
        del result["page_count"]

        result.update({
                "record_id": recid
            })
        return result

    
    def _download_img(self, volrecid, imgrecid, img_name):
        img_path_rel = "pages/" + volrecid + "/" + imgrecid + "/" + img_name
        img_meta_path_rel = "pages/" + volrecid + "/" + imgrecid + "/" + img_name + ".xml"

        path = os.path.join(self._cachedir, "pages", volrecid, imgrecid)
        if not os.path.exists(path):
            os.makedirs(path)

        commonsmeta_path = os.path.join(self._cachedir, img_meta_path_rel)
        if not os.path.exists(commonsmeta_path):
            img_url_api = self._commonsapi_url_tpl.format(img_name)
            urllib.request.urlretrieve(img_url_api, commonsmeta_path)
        
        img_path = os.path.join(self._cachedir, img_path_rel)
        if not os.path.exists(img_path):
            tree = ET.parse(commonsmeta_path)
            commonsurl = tree.find("./file/urls/file")
            if commonsurl is None:
                return "", ""

            urllib.request.urlretrieve(commonsurl.text, img_path)

        return img_path_rel, img_meta_path_rel
